from __future__ import unicode_literals

import frappe
from frappe.model.sync import sync_for


def execute():
	"""Force-sync all DocTypes, Reports, and Workspace from JSON files.

	Uses Frappe's built-in sync_for() which properly creates DocType records
	along with their database tables, fields, and schema. This handles the
	case where Frappe's automatic model sync during `bench migrate` does not
	create DocType records from the JSON files in the doctype/ directory.
	"""
	app_name = "handicraft_export"

	print("  🔄 Syncing DocTypes from JSON files...")
	try:
		sync_for(app_name, force=True)
		frappe.db.commit()
		print("  ✅ DocTypes synced successfully")
	except Exception as e:
		frappe.db.rollback()
		print(f"  ❌ Error syncing DocTypes: {e}")
		raise

	print("  ✅ Force-sync completed successfully")
