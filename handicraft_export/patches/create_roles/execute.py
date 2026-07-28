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
	# Uses direct SQL to avoid saving the DocType (which requires developer mode
	# for standard DocTypes like UOM).
	_grant_read_permission("UOM", ["Export Coordinator", "Artisan Liaison"])

	frappe.db.commit()
	frappe.clear_cache()
	print("  🧹 Permission cache cleared")


def _grant_read_permission(doctype, roles):
	"""Grant read permission on a standard DocType to specified roles.

	Uses direct SQL to insert/update DocPerm records, avoiding the need to
	save the DocType (which would fail in non-developer mode for standard DocTypes).
	"""
	if not frappe.db.exists("DocType", doctype):
		print(f"  ⚠️  DocType {doctype} not found — skipping permission setup")
		return

	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			continue

		# Check if this role already has a permission entry
		existing = frappe.db.get_value(
			"DocPerm",
			{"parent": doctype, "parentfield": "permissions", "role": role_name},
			"name",
		)
		if existing:
			# Update existing DocPerm to grant read + select access
			frappe.db.set_value("DocPerm", existing, "read", 1)
			frappe.db.set_value("DocPerm", existing, "select", 1)
			print(f"  🔑 Granted read+select permission on {doctype} for {role_name}")
		else:
			# Get next index for ordering
			max_idx = frappe.db.sql("""
				SELECT COALESCE(MAX(`idx`), 0) FROM `tabDocPerm`
				WHERE `parent` = %s AND `parentfield` = 'permissions'
			""", doctype)[0][0]

			# Insert new DocPerm record directly
			frappe.db.sql("""
				INSERT INTO `tabDocPerm`
				(`name`, `parent`, `parentfield`, `parenttype`,
				 `role`, `read`, `select`, `idx`,
				 `creation`, `modified`, `modified_by`, `owner`, `docstatus`)
				VALUES
				(%s, %s, 'permissions', 'DocType',
				 %s, 1, 1, %s,
				 NOW(), NOW(), 'Administrator', 'Administrator', 0)
			""", (
				frappe.generate_hash(length=10),
				doctype,
				role_name,
				max_idx + 1,
			))
			print(f"  🔑 Granted read+select permission on {doctype} for {role_name}")
