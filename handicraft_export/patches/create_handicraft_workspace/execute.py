from __future__ import unicode_literals

import json
import uuid
import frappe


def execute():
	"""Create or update Handicraft Export Desk workspace with full layout."""
	workspace_name = "Handicraft Export Desk"

	if frappe.db.exists("Workspace", workspace_name):
		print(f"  ℹ️  Workspace '{workspace_name}' already exists — updating")
		workspace = frappe.get_doc("Workspace", workspace_name)
	else:
		workspace = frappe.new_doc("Workspace")
		workspace.name = workspace_name
		workspace.title = workspace_name
		workspace.workspace_name = workspace_name
		workspace.label = workspace_name

	# These must be set on BOTH new and existing workspaces
	workspace.module = "Handicraft"
	workspace.public = 1
	workspace.icon = "package"
	workspace.sequence_id = 1.0

	# Clear previous dynamic children so we rebuild fresh
	workspace.set("shortcuts", [])
	workspace.set("number_cards", [])
	workspace.set("charts", [])
	workspace.set("links", [])
	workspace.set("custom_blocks", [])

	# Build content layout
	workspace.content = build_workspace_content()

	# Add shortcuts, number cards, charts, links
	add_shortcuts(workspace)
	add_number_cards(workspace)
	add_charts(workspace)
	add_links(workspace)

	try:
		workspace.flags.ignore_permissions = True
		workspace.flags.ignore_links = True
		workspace.save()
		frappe.db.commit()
		print(f"  ✅ Updated workspace: {workspace_name}")
	except Exception as e:
		frappe.db.rollback()
		print(f"  ❌ Failed to update workspace: {e}")
		raise


# ── Layout Content ─────────────────────────────────────

def _uid():
	"""Generate a short unique ID for content blocks."""
	return uuid.uuid4().hex[:12]

def build_workspace_content():
	"""Build workspace layout JSON content with proper block IDs."""
	content = [
		# Row 1: Quick Actions
		{"id": _uid(), "type": "header", "data": {"text": "Quick Actions", "level": 4, "col": 12}},
		{"id": _uid(), "type": "shortcut", "data": {"shortcut_name": "New Visual Offer", "col": 3}},
		{"id": _uid(), "type": "shortcut", "data": {"shortcut_name": "New Job Card", "col": 3}},
		{"id": _uid(), "type": "shortcut", "data": {"shortcut_name": "Log QC", "col": 3}},
		{"id": _uid(), "type": "shortcut", "data": {"shortcut_name": "New Export Order", "col": 3}},
		{"id": _uid(), "type": "spacer", "data": {"col": 12}},
		# Row 2: Key Metrics
		{"id": _uid(), "type": "header", "data": {"text": "Key Metrics", "level": 4, "col": 12}},
		{"id": _uid(), "type": "number_card", "data": {"number_card_name": "Total CBM Shipping This Week", "col": 3}},
		{"id": _uid(), "type": "number_card", "data": {"number_card_name": "Active Artisans (YTD)", "col": 3}},
		{"id": _uid(), "type": "number_card", "data": {"number_card_name": "Pending Job Cards", "col": 3}},
		{"id": _uid(), "type": "spacer", "data": {"col": 12}},
		# Row 3: Charts
		{"id": _uid(), "type": "header", "data": {"text": "Analytics", "level": 4, "col": 12}},
		{"id": _uid(), "type": "chart", "data": {"chart_name": "Artisan Yield", "col": 6}},
		{"id": _uid(), "type": "spacer", "data": {"col": 12}},
		# Row 4: Navigation Cards
		{"id": _uid(), "type": "header", "data": {"text": "Handicraft Export Operations", "level": 4, "col": 12}},
		{"id": _uid(), "type": "card", "data": {"card_name": "Pre-Sales", "col": 4}},
		{"id": _uid(), "type": "card", "data": {"card_name": "Order Management", "col": 4}},
		{"id": _uid(), "type": "card", "data": {"card_name": "Subcontracting & QC", "col": 4}},
	]
	return json.dumps(content)


# ── Shortcuts ──────────────────────────────────────────

def add_shortcuts(workspace):
	"""Add shortcut tiles to the workspace."""
	shortcuts = [
		{"label": "New Visual Offer", "type": "DocType", "link_to": "Visual Offer Sheet", "doc_view": "New", "icon": "file-text", "onboard": 1},
		{"label": "New Job Card", "type": "DocType", "link_to": "Artisan Job Card", "doc_view": "New", "icon": "task", "onboard": 1},
		{"label": "Log QC", "type": "DocType", "link_to": "Batch Quality Record", "doc_view": "New", "icon": "check-circle", "onboard": 1},
		{"label": "New Export Order", "type": "DocType", "link_to": "Export Order", "doc_view": "New", "icon": "truck", "onboard": 1},
	]
	for s in shortcuts:
		workspace.append("shortcuts", s)


# ── Number Cards ───────────────────────────────────────

def add_number_cards(workspace):
	"""Add number cards to the workspace."""
	cards = [
		{"number_card_name": "Total CBM Shipping This Week", "label": "Total CBM Shipping", "type": "Document Type", "document_type": "Export Order", "function": "Sum", "aggregate_function_based_on": "total_cbm", "filter_operator": "Timespan", "filter_field": "estimated_ship_date", "filter_value": "This Week", "color": "#e67e22", "show_trend": 1},
		{"number_card_name": "Active Artisans (YTD)", "label": "Active Artisans (YTD)", "type": "Document Type", "document_type": "Artisan", "function": "Count", "filter_operator": "Timespan", "filter_field": "creation", "filter_value": "This Year", "color": "#28a745", "show_trend": 1},
		{"number_card_name": "Pending Job Cards", "label": "Pending Job Cards", "type": "Document Type", "document_type": "Artisan Job Card", "function": "Count", "filter_operator": "=", "filter_field": "docstatus", "filter_value": "0", "color": "#dc3545", "show_trend": 1},
	]
	for c in cards:
		workspace.append("number_cards", c)


# ── Charts ─────────────────────────────────────────────

def add_charts(workspace):
	"""Add chart entries to the workspace."""
	charts = [
		{"chart_name": "Artisan Yield", "label": "Artisan Yield", "chart_type": "Dashboard Chart", "width": "Half"},
	]
	for c in charts:
		workspace.append("charts", c)


# ── Links (Sidebar Navigation) ─────────────────────────

def add_links(workspace):
	"""Add sidebar links organized by card break sections."""
	links = [
		# Pre-Sales
		{"type": "Card Break", "label": "Pre-Sales", "hidden": 0, "onboard": 1},
		{"label": "Visual Offer Sheet", "type": "Link", "link_type": "DocType", "link_to": "Visual Offer Sheet", "hidden": 0, "onboard": 1},
		{"label": "Artisan Product Catalog", "type": "Link", "link_type": "DocType", "link_to": "Artisan Product Catalog Entry", "hidden": 0, "onboard": 1},
		# Order Management
		{"type": "Card Break", "label": "Order Management", "hidden": 0, "onboard": 1},
		{"label": "Export Order", "type": "Link", "link_type": "DocType", "link_to": "Export Order", "hidden": 0, "onboard": 1},
		# Subcontracting & QC
		{"type": "Card Break", "label": "Subcontracting & QC", "hidden": 0, "onboard": 1},
		{"label": "Artisan Job Card", "type": "Link", "link_type": "DocType", "link_to": "Artisan Job Card", "hidden": 0, "onboard": 1},
		{"label": "Batch Quality Record", "type": "Link", "link_type": "DocType", "link_to": "Batch Quality Record", "hidden": 0, "onboard": 1},
		# Master Data
		{"type": "Card Break", "label": "Master Data", "hidden": 0, "onboard": 1},
		{"label": "Artisan Cluster", "type": "Link", "link_type": "DocType", "link_to": "Artisan Cluster", "hidden": 0, "onboard": 1},
		{"label": "Artisan", "type": "Link", "link_type": "DocType", "link_to": "Artisan", "hidden": 0, "onboard": 1},
		# Reports
		{"type": "Card Break", "label": "Reports", "hidden": 0, "onboard": 1},
		{"label": "Document Readiness Dashboard", "type": "Link", "link_type": "Report", "link_to": "Document Readiness Dashboard", "hidden": 0, "is_query_report": 1, "onboard": 1},
		{"label": "Cluster Output Capacity", "type": "Link", "link_type": "Report", "link_to": "Cluster Output Capacity", "hidden": 0, "is_query_report": 1, "onboard": 1},
		{"label": "Artisan Yield & Wastage", "type": "Link", "link_type": "Report", "link_to": "Artisan Yield & Wastage", "hidden": 0, "is_query_report": 1, "onboard": 1},
	]
	for link in links:
		workspace.append("links", link)
