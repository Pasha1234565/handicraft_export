from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class ExportOrder(Document):
	"""Export Order — extends Sales Order for export-specific fields and CBM planning."""

	def before_save(self):
		self.calculate_cbm_and_container()

	def before_submit(self):
		self.calculate_cbm_and_container()

	def calculate_cbm_and_container(self):
		"""
		Sum CBM from Export Packing List child table into total_cbm,
		then estimate container type:
		- < 15 CBM  → LCL
		- 15–33 CBM → 20ft FCL
		- >= 33 CBM → 40ft FCL
		"""
		total = 0.0
		for row in self.get("export_packing_list", []):
			if row.cbm:
				total += row.cbm

		old_container = self.container_estimate
		self.total_cbm = total

		if total <= 0:
			self.container_estimate = ""
		elif total < 15:
			self.container_estimate = "LCL"
		elif total < 33:
			self.container_estimate = "20ft FCL"
		else:
			self.container_estimate = "40ft FCL"

		# Notify if container estimate changed
		if old_container and old_container != self.container_estimate:
			self._notify_container_change(old_container)

	def _notify_container_change(self, old_estimate):
		"""Create a system notification when container estimate changes."""
		try:
			frappe.publish_realtime(
				"container_threshold_alert",
				{
					"doc_name": self.name,
					"old_estimate": old_estimate,
					"new_estimate": self.container_estimate,
				},
				after_commit=True,
			)
		except Exception:
			pass
