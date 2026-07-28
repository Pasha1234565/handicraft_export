from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class ArtisanJobCard(Document):
	"""Artisan Job Card — subcontracting work order triggering Purchase Invoice on submit."""

	def on_submit(self):
		"""On submit, generate Purchase Invoice for received pieces."""
		if self.qty_received > 0:
			self._create_purchase_invoice()

	def before_cancel(self):
		"""On cancel, cancel the linked Purchase Invoice if it exists."""
		pi_name = frappe.db.get_value(
			"Purchase Invoice",
			{"custom_artisan_job_card": self.name, "docstatus": 1},
			"name",
		)
		if pi_name:
			pi_doc = frappe.get_doc("Purchase Invoice", pi_name)
			pi_doc.cancel()

	def _create_purchase_invoice(self):
		"""
		Create a standard Purchase Invoice for the artisan's linked supplier.
		The invoice amount = qty_received * piece_rate_inr.

		Sets the expense_account explicitly from the company defaults
		to avoid "Expense account is mandatory for item" validation errors.
		"""
		artisan = frappe.get_doc("Artisan", self.artisan)
		linked_supplier = artisan.linked_supplier

		if not linked_supplier:
			frappe.throw(
				f"Artisan {self.artisan} does not have a linked Supplier. "
				"Please set one before submitting the Job Card."
			)

		# Fetch default expense account from the company
		company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
		expense_account = None
		if company:
			expense_account = frappe.db.get_value(
				"Company", company, "default_expense_account"
			)

		# Fallback: try to find any Cost of Goods Sold account
		if not expense_account:
			expense_account = frappe.db.get_value(
				"Account",
				{"account_type": "Cost of Goods Sold", "is_group": 0},
				"name",
			)

		# If still no expense account, throw a clear error
		if not expense_account:
			frappe.throw(
				"Could not find a default expense account for this Purchase Invoice. "
				"Please set 'default_expense_account' on your Company record, "
				"or create a 'Cost of Goods Sold' type account."
			)

		item_row = {
			"item_name": f"Job Work - {self.name}",
			"description": (
				f"Artisan Job Card {self.name}\n"
				f"Ordered: {self.qty_ordered} | Received: {self.qty_received} | "
				f"Rejected: {self.qty_rejected}\n"
				f"Piece Rate: ₹{self.piece_rate_inr}"
			),
			"qty": self.qty_received,
			"rate": self.piece_rate_inr,
		}

		if expense_account:
			item_row["expense_account"] = expense_account

		pi = frappe.get_doc({
			"doctype": "Purchase Invoice",
			"supplier": linked_supplier,
			"posting_date": frappe.utils.today(),
			"custom_artisan_job_card": self.name,
			"items": [item_row],
		})

		# Set missing values (handles account defaults, tax templates, etc.)
		pi.set_missing_values()
		pi.insert()
		pi.submit()
		frappe.msgprint(f"Purchase Invoice {pi.name} created and submitted.")
