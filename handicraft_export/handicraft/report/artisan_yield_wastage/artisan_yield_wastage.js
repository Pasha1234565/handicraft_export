// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["Artisan Yield & Wastage"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "artisan",
			"label": __("Artisan"),
			"fieldtype": "Link",
			"options": "Artisan",
		},
		{
			"fieldname": "artisan_cluster",
			"label": __("Artisan Cluster"),
			"fieldtype": "Link",
			"options": "Artisan Cluster",
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "yield_pct" && data && data.yield_pct !== undefined) {
			if (data.yield_pct < 80) {
				value = `<span style="color:red;font-weight:bold;">${value}</span>`;
			} else if (data.yield_pct < 95) {
				value = `<span style="color:orange;font-weight:bold;">${value}</span>`;
			} else {
				value = `<span style="color:green;font-weight:bold;">${value}</span>`;
			}
		}
		return value;
	},
};
