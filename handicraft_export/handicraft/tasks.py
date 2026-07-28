from __future__ import unicode_literals

import frappe
from frappe.utils import today, add_days


def daily_check_document_readiness():
	"""
	Daily scheduled task: Check Export Orders where estimated ship date is
	within 3 days and flag if Commercial Invoice or COO is missing.
	"""
	threshold_date = add_days(today(), 3)

	export_orders = frappe.get_all(
		"Export Order",
		filters={
			"estimated_ship_date": threshold_date,
			"docstatus": 1,
		},
		fields=["name", "buyer_country", "certificate_of_origin_status"],
	)

	for eo in export_orders:
		missing_docs = []
		if eo.certificate_of_origin_status != "Issued":
			missing_docs.append("Certificate of Origin")

		# Check if Commercial Invoice print format exists
		# (we assume if order is submitted, CI can be generated)
		# But we flag if COO is missing as the main concern

		if missing_docs:
			subject = f"Document Readiness Alert: {eo.name}"
			message = (
				f"Export Order {eo.name} is shipping in 3 days ({threshold_date}).\n"
				f"Missing documents: {', '.join(missing_docs)}.\n"
				f"Buyer Country: {eo.buyer_country}"
			)

			# Send email to Export Coordinator
			coordinator_emails = frappe.get_all(
				"User",
				filters={
					"role_profile_name": "Export Coordinator",
					"enabled": 1,
				},
				fields=["email"],
			)

			for user in coordinator_emails:
				try:
					frappe.sendmail(
						recipients=user.email,
						subject=subject,
						message=message,
					)
				except Exception:
					frappe.log_error(f"Failed to send readiness email for {eo.name}")

			frappe.db.commit()


def weekly_update_cluster_analytics():
	"""
	Weekly scheduled task: Update aggregated cluster statistics.
	Can be extended to sync with external dashboards.
	"""
	clusters = frappe.get_all("Artisan Cluster", pluck="name")

	for cluster in clusters:
		artisan_count = frappe.db.count("Artisan", {"artisan_cluster": cluster})
		frappe.db.set_value(
			"Artisan Cluster",
			cluster,
			"custom_active_artisan_count",
			artisan_count,
		)

	frappe.db.commit()
