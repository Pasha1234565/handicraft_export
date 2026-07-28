// Cluster Output Capacity
frappe.query_reports["Cluster Output Capacity"] = {
	"filters": [
		{
			"fieldname": "region",
			"label": __("Region"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "artisan_cluster",
			"label": __("Artisan Cluster"),
			"fieldtype": "Link",
			"options": "Artisan Cluster",
		},
	],
};
