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
		The custom_artisan_job_card field is created by a patch on first migrate.
		"""
		artisan = frappe.get_doc("Artisan", self.artisan)
		linked_supplier = artisan.linked_supplier

		if not linked_supplier:
			frappe.throw(
				f"Artisan {self.artisan} does not have a linked Supplier. "
				"Please set one before submitting the Job Card."
			)

		pi = frappe.get_doc({
			"doctype": "Purchase Invoice",
			"supplier": linked_supplier,
			"posting_date": frappe.utils.today(),
			"custom_artisan_job_card": self.name,
			"items": [
				{
					"item_name": f"Job Work - {self.name}",
					"description": f"Artisan Job Card {self.name} — {self.qty_received} pcs @ ₹{self.piece_rate_inr}",
					"qty": self.qty_received,
					"rate": self.piece_rate_inr,
				}
			],
		})

		pi.insert()
		pi.submit()
		frappe.msgprint(f"Purchase Invoice {pi.name} created and submitted.")
