from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class VisualOfferSheet(Document):
	"""Visual Offer Sheet — pre-sales quotation with photo grid."""

	def before_save(self):
		self.calculate_totals()

	def before_submit(self):
		self.calculate_totals()

	def calculate_totals(self):
		"""Compute total amount from child table items."""
		total = 0.0
		for item in self.get("offer_sheet_items", []):
			if item.qty and item.quoted_price_usd:
				item.amount = item.qty * item.quoted_price_usd
				total += item.amount
		self.total_amount = total
