from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class ArtisanProductCatalogEntry(Document):
	"""Artisan Product Catalog Entry — product listing with CBM calculation."""

	def before_save(self):
		self.calculate_cbm()

	def calculate_cbm(self):
		"""Auto-calculate CBM from dimensions: (L * W * H) / 1,000,000."""
		if self.length_cm and self.width_cm and self.height_cm:
			self.calculated_cbm = (self.length_cm * self.width_cm * self.height_cm) / 1000000.0
		else:
			self.calculated_cbm = 0.0
