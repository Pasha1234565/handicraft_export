from __future__ import unicode_literals

import frappe


def execute():
	"""Ensure the Handicraft module exists in the system and is registered.

	This patch both creates the Module Def in the database AND registers
	it in Frappe's runtime module_app dict, so that frappe.reload_doc()
	can find the module during the same session.
	"""
	module_name = "Handicraft"

	# Step 1: Create Module Def in database if missing
	if not frappe.db.exists("Module Def", module_name):
		module = frappe.get_doc({
			"doctype": "Module Def",
			"module_name": module_name,
			"app_name": "handicraft_export",
			"custom": 1,
		})
		module.insert(ignore_permissions=True)
		frappe.db.commit()

	# Step 2: Register in runtime module_app dict (needed by reload_doc)
	from frappe.modules.utils import scrub
	scrubbed = scrub(module_name)
	if scrubbed not in frappe.local.module_app:
		frappe.local.module_app[scrubbed] = "handicraft_export"
