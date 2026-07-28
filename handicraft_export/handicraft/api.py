from __future__ import unicode_literals

import frappe


@frappe.whitelist()
def generate_artisan_invoice(job_card_name):
	"""
	Creates a standard Purchase Invoice for the artisan linked to the Job Card.
	Called upon submission of Artisan Job Card.

	Args:
		job_card_name (str): Name of the Artisan Job Card document.

	Returns:
		str: Name of the created Purchase Invoice, or None if qty_received is 0.
	"""
	# Fetch job card
	job_card = frappe.get_doc("Artisan Job Card", job_card_name)

	if job_card.docstatus != 1:
		frappe.throw(f"Job Card {job_card_name} must be submitted first.")

	if job_card.qty_received <= 0:
		frappe.msgprint(f"No received qty for {job_card_name}. Skipping invoice.")
		return

	# Fetch linked artisan & supplier
	artisan = frappe.get_doc("Artisan", job_card.artisan)
	linked_supplier = artisan.linked_supplier

	if not linked_supplier:
		frappe.throw(
			f"Artisan {job_card.artisan} does not have a linked Supplier. "
			"Please set one before generating the invoice."
		)

	# Check if invoice already exists for this job card
	existing = frappe.db.get_value(
		"Purchase Invoice",
		{"custom_artisan_job_card": job_card_name, "docstatus": ["!=", 2]},
		"name",
	)
	if existing:
		frappe.msgprint(f"Purchase Invoice {existing} already exists for {job_card_name}.")
		return existing

	# Create Purchase Invoice
	pi = frappe.get_doc({
		"doctype": "Purchase Invoice",
		"supplier": linked_supplier,
		"posting_date": frappe.utils.today(),
		"custom_artisan_job_card": job_card_name,
		"items": [
			{
				"item_name": f"Job Work - {job_card_name}",
				"description": (
					f"Artisan Job Card {job_card_name}\n"
					f"Ordered: {job_card.qty_ordered} | Received: {job_card.qty_received} | "
					f"Rejected: {job_card.qty_rejected}\n"
					f"Piece Rate: ₹{job_card.piece_rate_inr}"
				),
				"qty": job_card.qty_received,
				"rate": job_card.piece_rate_inr,
			}
		],
	})

	pi.insert()
	pi.submit()
	frappe.msgprint(f"Purchase Invoice {pi.name} created and submitted successfully.")
	return pi.name


@frappe.whitelist()
def create_export_order_from_offer_sheet(offer_sheet):
	"""
	Create an Export Order from a submitted Visual Offer Sheet.
	Copies buyer info and creates a draft Export Order.

	Args:
		offer_sheet (str): Name of the submitted Visual Offer Sheet.

	Returns:
		str: Name of the created Export Order.
	"""
	vos = frappe.get_doc("Visual Offer Sheet", offer_sheet)

	if vos.docstatus != 1:
		frappe.throw("Visual Offer Sheet must be submitted first.")

	exp = frappe.get_doc({
		"doctype": "Export Order",
		"buyer_country": vos.buyer,  # buyer name as reference; country can be edited
		"incoterm": vos.incoterm,
	})

	# Optionally create a Sales Order first
	# (skipped for now — user can link manually)

	exp.insert(ignore_permissions=True)
	frappe.msgprint(f"Export Order {exp.name} created from {offer_sheet}.")
	return exp.name
