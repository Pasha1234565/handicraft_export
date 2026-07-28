from __future__ import unicode_literals

import frappe
from frappe.desk.doctype.workspace.workspace import Workspace


def execute():
	"""Create the Handicraft Export Desk workspace.

	This patch is resilient — if linked entities (Module Def, DocTypes, Reports)

don't exist yet at migration time, it logs a warning and skips rather than
	crashing the entire migrate.
	"""
	workspace_name = "Handicraft Export Desk"

	if frappe.db.exists("Workspace", workspace_name):
		return

	workspace = frappe.get_doc({
		"doctype": "Workspace",
		"workspace_name": workspace_name,
		"icon": "package",
		"label": workspace_name,
		"module": "Handicraft",
		"is_standard": 1,
		"charts": [
			{
				"label": "Artisan Yield",
				"chart_name": "Artisan Yield",
				"type": "Bar",
			}
		],
		"links": [
			{
				"label": "Pre-Sales",
				"type": "Section Break",
				"hidden": 0,
			},
			{
				"label": "Visual Offer Sheet",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Visual Offer Sheet",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Artisan Product Catalog",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Artisan Product Catalog Entry",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Order Management",
				"type": "Section Break",
				"hidden": 0,
			},
			{
				"label": "Export Order",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Export Order",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Subcontracting",
				"type": "Section Break",
				"hidden": 0,
			},
			{
				"label": "Artisan Job Card",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Artisan Job Card",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Batch Quality Record",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Batch Quality Record",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Master Data",
				"type": "Section Break",
				"hidden": 0,
			},
			{
				"label": "Artisan Cluster",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Artisan Cluster",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Artisan",
				"type": "DocType",
				"link_type": "DocType",
				"link_to": "Artisan",
				"onboard": 1,
				"hidden": 0,
			},
			{
				"label": "Reports",
				"type": "Section Break",
				"hidden": 0,
			},
			{
				"label": "Document Readiness Dashboard",
				"type": "Report",
				"link_type": "Report",
				"link_to": "Document Readiness Dashboard",
				"hidden": 0,
			},
			{
				"label": "Cluster Output Capacity",
				"type": "Report",
				"link_type": "Report",
				"link_to": "Cluster Output Capacity",
				"hidden": 0,
			},
			{
				"label": "Artisan Yield & Wastage",
				"type": "Report",
				"link_type": "Report",
				"link_to": "Artisan Yield & Wastage",
				"hidden": 0,
			},
		],
		"number_cards": [
			{
				"label": "Total CBM Shipping This Week",
				"type": "DocType",
				"doc_type": "Export Order",
				"function": "Sum",
				"aggregate_function": "SUM",
				"aggregate_field": "total_cbm",
				"filters_json": '{"estimated_ship_date": ["Timespan", "this week"], "docstatus": 1}',
			},
			{
				"label": "Active Artisans (YTD)",
				"type": "DocType",
				"doc_type": "Artisan",
				"function": "Count",
				"filters_json": '{"creation": ["Timespan", "this year"]}',
			},
			{
				"label": "Pending Job Cards",
				"type": "DocType",
				"doc_type": "Artisan Job Card",
				"function": "Count",
				"filters_json": '{"docstatus": 0}',
			},
		],
	})

	try:
		workspace.insert(ignore_permissions=True)
		frappe.db.commit()
	except frappe.LinkValidationError as e:
		frappe.log_error(
			message=f"Workspace '{workspace_name}' could not be created: {e}",
			title="Workspace Creation Skipped",
		)
		frappe.db.rollback()
		frappe.msgprint(
			f"Workspace '{workspace_name}' will be created after all DocTypes/Reports are synced. "
			"Run migration again after installing all apps."
		)
