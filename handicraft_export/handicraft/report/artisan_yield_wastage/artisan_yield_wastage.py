# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "artisan_name",
			"label": _("Artisan"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "artisan_cluster",
			"label": _("Cluster"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "job_card",
			"label": _("Job Card"),
			"fieldtype": "Link",
			"options": "Artisan Job Card",
			"width": 140,
		},
		{
			"fieldname": "export_order",
			"label": _("Export Order"),
			"fieldtype": "Link",
			"options": "Export Order",
			"width": 140,
		},
		{
			"fieldname": "qty_ordered",
			"label": _("Qty Ordered"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "qty_received",
			"label": _("Qty Received"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "qty_rejected",
			"label": _("Qty Rejected"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "qty_wastage",
			"label": _("Wastage"),
			"fieldtype": "Int",
			"width": 80,
		},
		{
			"fieldname": "yield_pct",
			"label": _("Yield %"),
			"fieldtype": "Percent",
			"width": 90,
		},
	]


def get_data(filters):
	conditions = []
	values = {}

	if filters.get("from_date"):
		conditions.append("jc.modified >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("jc.modified <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	if filters.get("artisan"):
		conditions.append("jc.artisan = %(artisan)s")
		values["artisan"] = filters["artisan"]

	if filters.get("artisan_cluster"):
		conditions.append("a.artisan_cluster = %(artisan_cluster)s")
		values["artisan_cluster"] = filters["artisan_cluster"]

	where_clause = " AND ".join(conditions) if conditions else "1=1"

	query = f"""
		SELECT
			a.artisan_name,
			ac.cluster_name AS artisan_cluster,
			jc.name AS job_card,
			jc.export_order,
			jc.qty_ordered,
			jc.qty_received,
			jc.qty_rejected,
			(jc.qty_ordered - jc.qty_received) AS qty_wastage,
			CASE
				WHEN jc.qty_ordered > 0
				THEN ROUND((jc.qty_received / jc.qty_ordered) * 100, 2)
				ELSE 0
			END AS yield_pct
		FROM `tabArtisan Job Card` jc
		INNER JOIN `tabArtisan` a ON a.name = jc.artisan
		LEFT JOIN `tabArtisan Cluster` ac ON ac.name = a.artisan_cluster
		WHERE jc.docstatus = 1 AND {where_clause}
		ORDER BY yield_pct ASC
	"""

	return frappe.db.sql(query, values, as_dict=True)
