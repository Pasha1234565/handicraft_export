from __future__ import unicode_literals

import frappe


def execute():
	"""Create custom roles for Handicraft Export."""
	roles = [
		{
			"role_name": "Export Coordinator",
			"desk_access": 1,
		},
		{
			"role_name": "Artisan Liaison",
			"desk_access": 1,
		},
	]

	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.get_doc({"doctype": "Role", **role_data})
			role.insert(ignore_permissions=True)

	# Set Homepage for each role on their workspace
	frappe.db.commit()
