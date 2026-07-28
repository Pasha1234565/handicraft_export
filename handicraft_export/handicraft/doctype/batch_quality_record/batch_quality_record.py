from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class BatchQualityRecord(Document):
	"""Batch Quality Record — QC inspection result for Job Card output."""

	def after_insert(self):
		"""Send system notification if QC fails or requires rework."""
		if self.qc_status in ("Fail", "Rework"):
			self._notify_qc_issue()

	def _notify_qc_issue(self):
		"""Notify Artisan Liaison about failed/rework QC."""
		try:
			frappe.publish_realtime(
				"qc_failed_rework_needed",
				{
					"doc_name": self.name,
					"job_card": self.job_card,
					"artisan": self.artisan,
					"qc_status": self.qc_status,
				},
				after_commit=True,
			)
		except Exception:
			pass
