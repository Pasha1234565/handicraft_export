from __future__ import unicode_literals

import frappe
from frappe.utils import now


def execute():
	"""Create Dashboard Chart records for the Handicraft Export workspace.

	This patch uses direct SQL operations (like msme-logistics does) to
	create dashboard chart records and link them to the workspace.
	This bypasses the fixture system which can fail with validation errors.
	"""
	workspace_name = "Handicraft Export Desk"

	# Only create chart if the underlying DocType exists
	if not frappe.db.exists("DocType", "Artisan Job Card"):
		print("  ⚠️  DocType 'Artisan Job Card' not found — skipping Artisan Yield chart")
		return

	create_chart(
		chart_name="Artisan Yield",
		chart_type="Group By",
		visual_type="Bar",
		document_type="Artisan Job Card",
		group_by_based_on="artisan",
		group_by_type="Sum",
		aggregate_function_based_on="qty_received",
		number_of_groups=10,
		workspace_name=workspace_name,
	)

	frappe.db.commit()
	print("  📊 Dashboard charts setup complete!")


def create_chart(
	chart_name,
	chart_type,
	visual_type,
	document_type,
	group_by_based_on,
	group_by_type,
	aggregate_function_based_on=None,
	number_of_groups=0,
	workspace_name=None,
):
	"""Create or update a Dashboard Chart record and link it to a workspace."""
	# STEP 1: Create/fix the Dashboard Chart record
	try:
		frappe.db.sql(
			"DELETE FROM `tabDashboard Chart` WHERE `name` = %(name)s",
			{"name": chart_name},
		)
		frappe.db.commit()

		frappe.db.sql(
			"""INSERT INTO `tabDashboard Chart`
			(`name`, `chart_name`, `chart_type`, `type`,
			 `document_type`, `group_by_based_on`, `group_by_type`,
			 `aggregate_function_based_on`, `number_of_groups`,
			 `module`, `is_public`, `is_standard`,
			 `filters_json`, `timeseries`,
			 `timespan`, `time_interval`,
			 `creation`, `modified`, `modified_by`, `owner`, `docstatus`)
			VALUES
			(%(name)s, %(chart_name)s, %(chart_type)s, %(type)s,
			 %(document_type)s, %(group_by_based_on)s, %(group_by_type)s,
			 %(aggregate_function_based_on)s, %(number_of_groups)s,
			 %(module)s, %(is_public)s, %(is_standard)s,
			 %(filters_json)s, %(timeseries)s,
			 %(timespan)s, %(time_interval)s,
			 %(creation)s, %(modified)s, %(owner)s, %(owner)s, 0)""",
			{
				"name": chart_name,
				"chart_name": chart_name,
				"chart_type": chart_type,
				"type": visual_type,
				"document_type": document_type,
				"group_by_based_on": group_by_based_on,
				"group_by_type": group_by_type,
				"aggregate_function_based_on": aggregate_function_based_on or "",
				"number_of_groups": number_of_groups,
				"module": "Handicraft",
				"is_public": 1,
				"is_standard": 0,
				"filters_json": "{}",
				"timeseries": 0,
				"timespan": "Last Month",
				"time_interval": "Monthly",
				"creation": now(),
				"modified": now(),
				"owner": "Administrator",
			},
		)
		frappe.db.commit()
		print(f"  ✅ Dashboard Chart '{chart_name}' created/updated")
	except Exception as e:
		print(f"  ⚠️  Dashboard Chart error for '{chart_name}': {e}")
		return

	if not workspace_name:
		return

	# STEP 2: Update the workspace's charts child table
	chart_link_name = f"ws-chart-{chart_name.lower().replace(' ', '-')}"
	try:
		frappe.db.sql(
			"""DELETE FROM `tabWorkspace Chart`
			WHERE `parent` = %(workspace)s AND `parentfield` = 'charts'
			AND `chart_name` = %(chart_name)s""",
			{"workspace": workspace_name, "chart_name": chart_name},
		)
		frappe.db.commit()

		frappe.db.sql(
			"""INSERT INTO `tabWorkspace Chart`
			(`name`, `parent`, `parenttype`, `parentfield`,
			 `chart_name`, `label`, `idx`,
			 `creation`, `modified`, `modified_by`, `owner`, `docstatus`)
			VALUES
			(%(name)s, %(parent)s, 'Workspace', 'charts',
			 %(chart_name)s, %(label)s, %(idx)s,
			 %(creation)s, %(modified)s, %(owner)s, %(owner)s, 0)""",
			{
				"name": chart_link_name,
				"parent": workspace_name,
				"chart_name": chart_name,
				"label": chart_name,
				"idx": 1,
				"creation": now(),
				"modified": now(),
				"owner": "Administrator",
			},
		)
		frappe.db.commit()
		print(f"  ✅ Workspace '{workspace_name}' now has chart link to '{chart_name}'")
	except Exception as e:
		print(f"  ⚠️  Workspace chart link error for '{chart_name}': {e}")
