// Document Readiness Dashboard
frappe.query_reports["Document Readiness Dashboard"] = {
	"filters": [
		{
			"fieldname": "buyer_country",
			"label": __("Buyer Country"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "readiness_flag",
			"label": __("Readiness Flag"),
			"fieldtype": "Select",
			"options": ["", "OK", "⚠ Missing Documents"],
		},
	],
};
