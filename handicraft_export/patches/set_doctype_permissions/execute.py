from __future__ import unicode_literals

import frappe


def execute():
	"""Set DocPerm records for all custom DocTypes so submit/amend/cancel work.

	Because the site is not in developer mode, the permission blocks in DocType
	JSON files are NOT applied during sync. This patch directly inserts the
	correct DocPerm records using SQL, bypassing DocType.validate().
	"""
	# Define all custom DocTypes and their required permissions
	doctype_permissions = {
		"Visual Offer Sheet": {
			"Export Coordinator": _perm("create", "write", "submit", "amend", "cancel", "read", "delete", "print", "email", "share", "report", "export"),
			"System Manager": _perm("read", "print", "email", "share", "report", "export"),
		},
		"Export Order": {
			"Export Coordinator": _perm("create", "write", "submit", "amend", "cancel", "read", "delete", "print", "email", "share", "report", "export"),
			"System Manager": _perm("read", "print", "email", "share", "report", "export"),
		},
		"Artisan Job Card": {
			"Artisan Liaison": _perm("create", "write", "submit", "amend", "cancel", "read", "delete", "print", "email", "share", "report", "export"),
			"Export Coordinator": _perm("read", "print", "email", "share", "report", "export"),
			"System Manager": _perm("create", "write", "submit", "amend", "cancel", "read", "delete", "print", "email", "share", "report", "export"),
		},
		"Batch Quality Record": {
			"Artisan Liaison": _perm("create", "write", "read", "delete", "print", "email", "share", "report", "export"),
			"Export Coordinator": _perm("read", "print", "email", "share", "report", "export"),
			"System Manager": _perm("create", "write", "read", "delete", "print", "email", "share", "report", "export"),
		},
		"Artisan Cluster": {
			"Artisan Liaison": _perm("create", "write", "read", "delete", "print", "email", "share", "report", "export"),
			"Export Coordinator": _perm("read", "print", "email", "share", "report", "export"),
			"System Manager": _perm("read", "print", "email", "share", "report", "export"),
		},
		"Artisan": {
			"Artisan Liaison": _perm("create", "write", "read", "delete", "print", "email", "share", "report", "export"),
			"Export Coordinator": _perm("read", "print", "email", "share", "report", "export"),
			"System Manager": _perm("read", "print", "email", "share", "report", "export"),
		},
		"Artisan Product Catalog Entry": {
			"Artisan Liaison": _perm("create", "write", "read", "delete", "print", "email", "share", "report", "export"),
			"Export Coordinator": _perm("read", "print", "email", "share", "report", "export"),
			"System Manager": _perm("read", "print", "email", "share", "report", "export"),
		},
	}

	for doctype, roles in doctype_permissions.items():
		if not frappe.db.exists("DocType", doctype):
			print(f"  ⚠️  DocType {doctype} not found — skipping")
			continue

		for role_name, perm_flags in roles.items():
			if not frappe.db.exists("Role", role_name):
				continue

			_upsert_docperm(doctype, role_name, perm_flags)

	frappe.db.commit()
	frappe.clear_cache()
	print("  🧹 Cache cleared — permissions should now be active")
	print("  ✅ All custom DocType permissions set successfully")
	print()
	print("  ℹ️  Users must log out and log back in for new permissions to take effect")


def _perm(*args):
	"""Build a dict of permission flags from string names.

	Usage: _perm('read', 'write', 'submit', 'amend', 'cancel')
	"""
	all_perms = ["read", "write", "create", "delete", "submit", "cancel",
				 "amend", "print", "email", "report", "import", "export",
				 "share"]
	return {p: 1 for p in args if p in all_perms}


def _upsert_docperm(doctype, role_name, perm_flags):
	"""Insert or update a DocPerm record for a given DocType + Role.

	Uses direct SQL to avoid needing developer mode.
	"""
	existing = frappe.db.get_value(
		"DocPerm",
		{"parent": doctype, "parentfield": "permissions", "role": role_name},
		"name",
	)

	if existing:
		# Update existing record
		for field, value in perm_flags.items():
			if value:
				frappe.db.set_value("DocPerm", existing, field, 1)
		print(f"  🔄 Updated {doctype} permission for {role_name}")
	else:
		# Get next idx
		max_idx = frappe.db.sql("""
			SELECT COALESCE(MAX(`idx`), 0) FROM `tabDocPerm`
			WHERE `parent` = %s AND `parentfield` = 'permissions'
		""", doctype)[0][0]

		# Build INSERT with all fields
		fields = ["name", "parent", "parentfield", "parenttype", "role", "idx",
				  "creation", "modified", "modified_by", "owner", "docstatus"]
		placeholders = ["%s", "%s", "'permissions'", "'DocType'", "%s", "%s",
						"NOW()", "NOW()", "'Administrator'", "'Administrator'", "0"]
		values = [frappe.generate_hash(length=10), doctype, role_name, max_idx + 1]

		for perm_field in ["read", "write", "create", "delete", "submit",
						   "cancel", "amend", "print", "email", "report",
						   "import", "export", "share"]:
			if perm_field in perm_flags:
				fields.append(f"`{perm_field}`")
				placeholders.append("%s")
				values.append(1)

		query = f"""
			INSERT INTO `tabDocPerm`
			({', '.join(fields)})
			VALUES ({', '.join(placeholders)})
		"""
		frappe.db.sql(query, values)
		print(f"  ✅ Created {doctype} permission for {role_name} ({', '.join(perm_flags.keys())})")
