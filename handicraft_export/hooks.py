from __future__ import unicode_literals

app_name = "handicraft_export"
app_title = "Handicraft Export"
app_publisher = "Your Company"
app_description = "Export Readiness & Subcontracting for Handicrafts"
app_icon = "octicon octicon-package"
app_color = "orange"
app_email = "info@example.com"
app_license = "MIT"

# Required Apps (installed automatically on site install)
# ------------------------------
required_apps = ["erpnext"]

# Fixtures
# ------------------------------
fixtures = [
	{"dt": "Workspace", "filters": [["module", "=", "Handicraft"]]},
	{"dt": "DocType", "filters": [["module", "=", "Handicraft"]]},
	{"dt": "Report", "filters": [["module", "=", "Handicraft"]]},
	{"dt": "Role", "filters": [["name", "in", ["Export Coordinator", "Artisan Liaison"]]]},
	{"dt": "Notification", "filters": [["document_type", "in", ["Export Order", "Batch Quality Record"]]]},
]

# DocType Class Overrides
# ------------------------------
doctype_class = {
	"Artisan Cluster": "handicraft_export.handicraft.doctype.artisan_cluster.artisan_cluster.ArtisanCluster",
	"Artisan": "handicraft_export.handicraft.doctype.artisan.artisan.Artisan",
	"Catalog Image": "handicraft_export.handicraft.doctype.catalog_image.catalog_image.CatalogImage",
	"Artisan Product Catalog Entry": "handicraft_export.handicraft.doctype.artisan_product_catalog_entry.artisan_product_catalog_entry.ArtisanProductCatalogEntry",
	"Visual Offer Sheet": "handicraft_export.handicraft.doctype.visual_offer_sheet.visual_offer_sheet.VisualOfferSheet",
	"Offer Sheet Item": "handicraft_export.handicraft.doctype.offer_sheet_item.offer_sheet_item.OfferSheetItem",
	"Export Order": "handicraft_export.handicraft.doctype.export_order.export_order.ExportOrder",
	"Export Packing List": "handicraft_export.handicraft.doctype.export_packing_list.export_packing_list.ExportPackingList",
	"Artisan Job Card": "handicraft_export.handicraft.doctype.artisan_job_card.artisan_job_card.ArtisanJobCard",
	"Raw Material Issued": "handicraft_export.handicraft.doctype.raw_material_issued.raw_material_issued.RawMaterialIssued",
	"Batch Quality Record": "handicraft_export.handicraft.doctype.batch_quality_record.batch_quality_record.BatchQualityRecord",
}

# Document Events
# ------------------------------
doc_events = {}

# Scheduled Tasks
# ------------------------------
scheduler_events = {
	"daily": [
		"handicraft_export.handicraft.tasks.daily_check_document_readiness",
	],
	"cron": {
		"0 9 * * 1": [
			"handicraft_export.handicraft.tasks.weekly_update_cluster_analytics",
		],
	},
}

# Permissions
# ------------------------------
# permission_query_conditions = {}

# Website
# ------------------------------
# website_route_rules = []

# Jinja
# ------------------------------
# jinja = {}

# Boot
# ------------------------------
# boot_session = boot_session

# After Migrate
# ------------------------------
after_migrate = [
	"handicraft_export.patches.create_roles.execute",
	"handicraft_export.patches.create_custom_fields.execute",
	"handicraft_export.patches.setup_workspace.execute",
]

# After Install
# ------------------------------
after_install = [
	"handicraft_export.patches.create_roles.execute",
	"handicraft_export.patches.create_custom_fields.execute",
]
