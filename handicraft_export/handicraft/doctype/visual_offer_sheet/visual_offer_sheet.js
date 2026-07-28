// Create Export Order from submitted Visual Offer Sheet
frappe.ui.form.on("Visual Offer Sheet", {
	refresh: function (frm) {
		if (frm.doc.docstatus === 1 && !frm.doc.__islocal) {
			frm.add_custom_button(__("Create Export Order"), function () {
				frappe.call({
					method: "handicraft_export.handicraft.api.create_export_order_from_offer_sheet",
					args: {
						offer_sheet: frm.doc.name,
					},
					callback: function (r) {
						if (r.message) {
							frappe.msgprint(__("Export Order {0} created.", [r.message]));
							frappe.set_route("Form", "Export Order", r.message);
						}
					},
				});
			});
		}
	},
});
