from __future__ import unicode_literals

import frappe


def execute():
	"""Create custom roles and set required permissions for Handicraft Export."""
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
		role_name = role_data["role_name"]
		if not frappe.db.exists("Role", role_name):
			role = frappe.get_doc({"doctype": "Role", **role_data})
			role.insert(ignore_permissions=True)
			print(f"  🔐 Created Role: {role_name}")

	# Grant read access to standard doctypes needed by the app.
	# The Artisan Job Card child table (Raw Material Issued) has a Link
	# to UOM, so all roles that submit Job Cards need UOM read permission.
	_grant_read_permission("UOM", ["Export Coordinator", "Artisan Liaison"])

	frappe.db.commit()
	frappe.clear_cache()
	print("  🧹 Permission cache cleared")


def _grant_read_permission(doctype, roles):
	"""Grant read permission on a DocType to specified roles.

	Uses the proper frappe.get_doc().append().save() pattern to ensure
	the child table relationship is correctly established.
	"""
	if not frappe.db.exists("DocType", doctype):
		print(f"  ⚠️  DocType {doctype} not found — skipping permission setup")
		return

	doc_type = frappe.get_doc("DocType", doctype)

	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			continue

		# Check if this role already has a permission entry
		existing = False
		for perm in doc_type.permissions:
			if perm.role == role_name:
				if not perm.read:
					perm.read = 1
					print(f"  🔑 Updated read permission on {doctype} for {role_name}")
				else:
					print(f"  ℹ️  Read permission already exists on {doctype} for {role_name}")
				existing = True
				break

		if not existing:
			doc_type.append("permissions", {
				"role": role_name,
				"read": 1,
			})
			print(f"  🔑 Granted read permission on {doctype} for {role_name}")

	doc_type.save(ignore_permissions=True)
