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
	_ensure_doctype_permission("UOM", ["Export Coordinator", "Artisan Liaison"], ptype=0)

	frappe.db.commit()


def _ensure_doctype_permission(doctype, roles, ptype=0):
	"""Ensure a role has a specific permission type on a DocType.

	Args:
		doctype: Name of the DocType (e.g. "UOM")
		roles: List of role names
		ptype: Permission type bitmask:
			0 = read, 1 = write, 2 = create, 3 = delete,
			4 = submit, 5 = amend, 6 = cancel
	"""
	perm_labels = {0: "read", 1: "write", 2: "create", 3: "delete",
				   4: "submit", 5: "amend", 6: "cancel"}
	perm_field = perm_labels.get(ptype, "read")

	if not frappe.db.exists("DocType", doctype):
		print(f"  ⚠️  DocType {doctype} not found — skipping permission setup")
		return

	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			continue

		# Check if permission already exists
		existing = frappe.db.get_value(
			"DocPerm",
			{"parent": doctype, "role": role_name},
			"name",
		)
		if existing:
			# Update existing to add the permission
			frappe.db.set_value("DocPerm", existing, perm_field, 1)
		else:
			# Create new permission record
			perm = frappe.get_doc({
				"doctype": "DocPerm",
				"parent": doctype,
				"parentfield": "permissions",
				"parenttype": "DocType",
				"role": role_name,
				perm_field: 1,
			})
			perm.insert(ignore_permissions=True)

		print(f"  🔑 Set {perm_field} permission on {doctype} for {role_name}")
