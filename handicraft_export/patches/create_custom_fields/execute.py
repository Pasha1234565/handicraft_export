from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	"""Create custom fields for Handicraft Export on standard DocTypes."""
	custom_fields = {
		"Purchase Invoice": [
			{
				"fieldname": "custom_artisan_job_card",
				"fieldtype": "Data",
				"label": "Artisan Job Card",
				"insert_after": "supplier",
				"read_only": 1,
				"translatable": 0,
			},
		],
		"Sales Order": [
			{
				"fieldname": "custom_handicraft_export_order",
				"fieldtype": "Link",
				"label": "Handicraft Export Order",
				"options": "Export Order",
				"insert_after": "transaction_date",
				"read_only": 0,
			},
		],
	}

	try:
		create_custom_fields(custom_fields, ignore_validate=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Failed to create custom fields: {e}")
