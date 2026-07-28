from __future__ import unicode_literals

import frappe


def execute():
	"""Ensure the Handicraft Export module exists in the system."""
	if not frappe.db.exists("Module Def", "Handicraft Export"):
		module = frappe.get_doc({
			"doctype": "Module Def",
			"module_name": "Handicraft Export",
			"app_name": "handicraft_export",
			"custom": 1,
		})
		module.insert(ignore_permissions=True)
		frappe.db.commit()
