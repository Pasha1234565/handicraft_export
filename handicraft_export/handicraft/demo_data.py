from __future__ import unicode_literals

import frappe
from frappe.utils import nowdate, add_days, add_years
from frappe.utils.data import flt


def execute():
	"""Seed demo data for the Handicraft Export app.

	Usage:
		bench --site yoursite.local execute handicraft_export.handicraft.demo_data.execute
	"""
	print("=" * 60)
	print("🌍  HANDICRAFT EXPORT — Demo Data Seeder")
	print("=" * 60)

	# ── 1. Item Groups (for crafts) ──
	craft_groups = ensure_craft_item_groups()

	# ── 2. Standard ERPNext Items (handicraft products) ──
	items = ensure_items(craft_groups)

	# ── 3. Suppliers (artisan accounting entities) ──
	suppliers = ensure_suppliers()

	# ── 4. Artisan Clusters ──
	clusters = ensure_artisan_clusters()

	# ── 5. Artisans ──
	artisans = ensure_artisans(clusters, suppliers, craft_groups)

	# ── 6. Artisan Product Catalog Entries ──
	catalog_entries = ensure_catalog_entries(artisans, items)

	# ── 7. Visual Offer Sheets ──
	offer_sheets = ensure_visual_offer_sheets(catalog_entries)

	# ── 8. Export Orders ──
	export_orders = ensure_export_orders(catalog_entries)

	# ── 9. Artisan Job Cards ──
	job_cards = ensure_job_cards(export_orders, artisans)

	# ── 10. Batch Quality Records ──
	ensure_batch_qc(job_cards)

	print()
	print("=" * 60)
	print("✅  Demo data seeded successfully!")
	print("=" * 60)


# ═══════════════════════════════════════════════════════
#  1. Item Groups
# ═══════════════════════════════════════════════════════

def ensure_craft_item_groups():
	"""Ensure Item Groups for handicraft categories exist."""
	groups = {
		"Wood Carving": {},
		"Textile & Embroidery": {},
		"Metal Craft": {},
		"Pottery & Ceramics": {},
		"Jewelry & Beadwork": {},
		"Paintings & Wall Art": {},
		"Handicraft Raw Materials": {},
	}

	created = {}
	for group_name in groups:
		if not frappe.db.exists("Item Group", group_name):
			doc = frappe.get_doc({
				"doctype": "Item Group",
				"item_group_name": group_name,
				"parent_item_group": "All Item Groups",
				"is_group": 0,
			})
			doc.insert(ignore_permissions=True)
			print(f"  📂 Created Item Group: {group_name}")
		else:
			print(f"  📂 Item Group already exists: {group_name}")
		created[group_name] = group_name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  2. ERPNext Items (Handicraft Products)
# ═══════════════════════════════════════════════════════

def ensure_items(craft_groups):
	"""Ensure standard Items for handicraft products exist."""
	default_uom = frappe.db.get_single_value("Stock Settings", "stock_uom") or "Nos"

	items_data = [
		# Wood Carving
		{"item_code": "HDC-WD-001", "item_name": "Rosewood Elephant Sculpture", "item_group": "Wood Carving", "description": "Hand-carved rosewood elephant sculpture, 12 inches", "stock_uom": default_uom, "weight_per_unit": 2.5, "weight_uom": "Kg"},
		{"item_code": "HDC-WD-002", "item_name": "Sandalwood Jewelry Box", "item_group": "Wood Carving", "description": "Intricately carved sandalwood jewelry box with floral motif", "stock_uom": default_uom, "weight_per_unit": 1.2, "weight_uom": "Kg"},
		{"item_code": "HDC-WD-003", "item_name": "Teak Wood Wall Panel", "item_group": "Wood Carving", "description": "Teak wood wall panel with traditional dancers, 24x36 inches", "stock_uom": default_uom, "weight_per_unit": 5.0, "weight_uom": "Kg"},
		# Textile & Embroidery
		{"item_code": "HDC-TX-001", "item_name": "Silk Embroidered Saree", "item_group": "Textile & Embroidery", "description": "Hand-embroidered pure silk saree with zari work", "stock_uom": default_uom, "weight_per_unit": 0.8, "weight_uom": "Kg"},
		{"item_code": "HDC-TX-002", "item_name": "Cotton Block Print Tablecloth", "item_group": "Textile & Embroidery", "description": "Hand block-printed cotton tablecloth, 60x90 inches", "stock_uom": default_uom, "weight_per_unit": 0.5, "weight_uom": "Kg"},
		# Metal Craft
		{"item_code": "HDC-MT-001", "item_name": "Brass Dancing Lady Statue", "item_group": "Metal Craft", "description": "Brass statue of dancing lady, lost wax process, 18 inches", "stock_uom": default_uom, "weight_per_unit": 3.0, "weight_uom": "Kg"},
		{"item_code": "HDC-MT-002", "item_name": "Copper Decorative Vase", "item_group": "Metal Craft", "description": "Hand-hammered copper vase with floral engravings", "stock_uom": default_uom, "weight_per_unit": 1.8, "weight_uom": "Kg"},
		# Pottery & Ceramics
		{"item_code": "HDC-PT-001", "item_name": "Blue Pottery Serving Bowl", "item_group": "Pottery & Ceramics", "description": "Hand-painted blue pottery serving bowl, 10 inch diameter", "stock_uom": default_uom, "weight_per_unit": 0.6, "weight_uom": "Kg"},
		{"item_code": "HDC-PT-002", "item_name": "Terracotta Tea Set", "item_group": "Pottery & Ceramics", "description": "6-piece terracotta tea set with tribal motifs", "stock_uom": default_uom, "weight_per_unit": 2.0, "weight_uom": "Kg"},
		# Jewelry
		{"item_code": "HDC-JW-001", "item_name": "Silver Tribal Necklace", "item_group": "Jewelry & Beadwork", "description": "Handcrafted silver necklace with tribal beadwork", "stock_uom": default_uom, "weight_per_unit": 0.3, "weight_uom": "Kg"},
	]

	created = {}
	for item_data in items_data:
		if not frappe.db.exists("Item", item_data["item_code"]):
			doc = frappe.get_doc({
				"doctype": "Item",
				**item_data,
			})
			doc.insert(ignore_permissions=True)
			print(f"  📦 Created Item: {item_data['item_code']} - {item_data['item_name']}")
		else:
			print(f"  📦 Item already exists: {item_data['item_code']}")
		created[item_data["item_name"]] = item_data["item_code"]

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  3. Suppliers
# ═══════════════════════════════════════════════════════

def ensure_suppliers():
	"""Ensure Suppliers for artisans exist."""
	suppliers_data = [
		{"supplier_name": "Mumbai Handicrafts Cooperative", "supplier_group": "Distributor", "supplier_type": "Company", "email": "info@mumbaihandicrafts.in", "mobile_no": "+91-9876543210"},
		{"supplier_name": "Rajasthan Rural Artisans Collective", "supplier_group": "Distributor", "supplier_type": "Company", "email": "info@rajasthanartisans.in", "mobile_no": "+91-9876543211"},
		{"supplier_name": "Kerala Woodcraft Society", "supplier_group": "Distributor", "supplier_type": "Company", "email": "info@keralawoodcraft.in", "mobile_no": "+91-9876543212"},
		{"supplier_name": "Varanasi Silk Weavers Association", "supplier_group": "Distributor", "supplier_type": "Company", "email": "info@varanasisilk.in", "mobile_no": "+91-9876543213"},
		{"supplier_name": "Jaipur Blue Pottery Trust", "supplier_group": "Distributor", "supplier_type": "Company", "email": "info@jaipurpottery.in", "mobile_no": "+91-9876543214"},
	]

	created = {}
	for s_data in suppliers_data:
		name = s_data["supplier_name"]
		if not frappe.db.exists("Supplier", name):
			doc = frappe.get_doc({
				"doctype": "Supplier",
				**s_data,
			})
			doc.insert(ignore_permissions=True)
			print(f"  🏢 Created Supplier: {name}")
		else:
			print(f"  🏢 Supplier already exists: {name}")
		created[name] = name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  4. Artisan Clusters
# ═══════════════════════════════════════════════════════

def ensure_artisan_clusters():
	"""Ensure Artisan Clusters exist."""
	clusters_data = [
		{"cluster_name": "Sahariya Wood Carvers", "nodal_agency_or_ngo": "SEWA Bharat", "region": "Rajasthan", "udyam_registration_status": "Registered"},
		{"cluster_name": "Madhubani Art Village", "nodal_agency_or_ngo": "Mithila Art Foundation", "region": "Bihar", "udyam_registration_status": "Registered"},
		{"cluster_name": "Kutch Embroidery Circle", "nodal_agency_or_ngo": "Kutch Mahila Vikas Sangathan", "region": "Gujarat", "udyam_registration_status": "Registered"},
		{"cluster_name": "Channapatna Toy Makers", "nodal_agency_or_ngo": "Karnataka Handicrafts Dev Corp", "region": "Karnataka", "udyam_registration_status": "Registered"},
		{"cluster_name": "Bidri Art Metal Workers", "nodal_agency_or_ngo": "Telangana Handicrafts Department", "region": "Telangana", "udyam_registration_status": "Registered"},
	]

	created = {}
	for c_data in clusters_data:
		name = c_data["cluster_name"]
		if not frappe.db.exists("Artisan Cluster", name):
			doc = frappe.get_doc({
				"doctype": "Artisan Cluster",
				**c_data,
			})
			doc.insert(ignore_permissions=True)
			print(f"  🏘️  Created Artisan Cluster: {name}")
		else:
			print(f"  🏘️  Artisan Cluster already exists: {name}")
		created[name] = name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  5. Artisans
# ═══════════════════════════════════════════════════════

def ensure_artisans(clusters, suppliers, craft_groups):
	"""Ensure Artisans exist."""
	artisans_data = [
		{"artisan_name": "Ram Vilas Sharma", "cluster": "Sahariya Wood Carvers", "supplier": "Rajasthan Rural Artisans Collective", "craft": "Wood Carving", "email": "ram.sharma@email.in", "phone": "+91-9876500001", "address": "Village Padampura, Sawai Madhopur, Rajasthan"},
		{"artisan_name": "Sita Devi", "cluster": "Madhubani Art Village", "supplier": "Mumbai Handicrafts Cooperative", "craft": "Paintings & Wall Art", "email": "sita.devi@email.in", "phone": "+91-9876500002", "address": "Madhubani, Bihar"},
		{"artisan_name": "Johan Rabari", "cluster": "Kutch Embroidery Circle", "supplier": "Mumbai Handicrafts Cooperative", "craft": "Textile & Embroidery", "email": "johan.rabari@email.in", "phone": "+91-9876500003", "address": "Bhuj, Kutch, Gujarat"},
		{"artisan_name": "Mohan Rao", "cluster": "Channapatna Toy Makers", "supplier": "Kerala Woodcraft Society", "craft": "Wood Carving", "email": "mohan.rao@email.in", "phone": "+91-9876500004", "address": "Channapatna, Karnataka"},
		{"artisan_name": "Ghulam Ali", "cluster": "Bidri Art Metal Workers", "supplier": "Rajasthan Rural Artisans Collective", "craft": "Metal Craft", "email": "ghulam.ali@email.in", "phone": "+91-9876500005", "address": "Bidar, Telangana"},
		{"artisan_name": "Lakshmi Bai", "cluster": "Madhubani Art Village", "supplier": "Mumbai Handicrafts Cooperative", "craft": "Paintings & Wall Art", "email": "lakshmi.bai@email.in", "phone": "+91-9876500006", "address": "Madhubani, Bihar"},
		{"artisan_name": "Rajesh Kumar Suthar", "cluster": "Sahariya Wood Carvers", "supplier": "Rajasthan Rural Artisans Collective", "craft": "Wood Carving", "email": "rajesh.suthar@email.in", "phone": "+91-9876500007", "address": "Sawai Madhopur, Rajasthan"},
		{"artisan_name": "Aisha Ben", "cluster": "Kutch Embroidery Circle", "supplier": "Mumbai Handicrafts Cooperative", "craft": "Textile & Embroidery", "email": "aisha.ben@email.in", "phone": "+91-9876500008", "address": "Anjar, Kutch, Gujarat"},
	]

	created = {}
	for a_data in artisans_data:
		name = a_data["artisan_name"]
		if frappe.db.exists("Artisan", {"artisan_name": name}):
			print(f"  👨‍🎨 Artisan already exists: {name}")
			existing = frappe.get_value("Artisan", {"artisan_name": name}, "name")
			created[name] = existing
			continue

		doc = frappe.get_doc({
			"doctype": "Artisan",
			"artisan_name": name,
			"artisan_cluster": a_data["cluster"],
			"primary_craft": a_data["craft"],
			"linked_supplier": a_data["supplier"],
			"contact_email": a_data["email"],
			"contact_phone": a_data["phone"],
			"address": a_data["address"],
		})
		doc.insert(ignore_permissions=True)
		print(f"  👨‍🎨 Created Artisan: {name} ({doc.name})")
		created[name] = doc.name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  6. Artisan Product Catalog Entries
# ═══════════════════════════════════════════════════════

def ensure_catalog_entries(artisans, items):
	"""Ensure Artisan Product Catalog Entries exist."""
	entries_data = [
		{"product_name": "Rosewood Elephant Sculpture - Ram Vilas", "item": items.get("Rosewood Elephant Sculpture", "HDC-WD-001"), "artisan": artisans["Ram Vilas Sharma"], "production_days": 10, "min_qty": 5, "length": 30, "width": 12, "height": 15, "weight": 2.5, "units_per_carton": 6},
		{"product_name": "Sandalwood Jewelry Box - Rajesh", "item": items.get("Sandalwood Jewelry Box", "HDC-WD-002"), "artisan": artisans["Rajesh Kumar Suthar"], "production_days": 7, "min_qty": 10, "length": 20, "width": 15, "height": 10, "weight": 1.2, "units_per_carton": 12},
		{"product_name": "Madhubani Wall Panel - Sita Devi", "item": items.get("Teak Wood Wall Panel", "HDC-WD-003"), "artisan": artisans["Sita Devi"], "production_days": 15, "min_qty": 3, "length": 90, "width": 60, "height": 5, "weight": 5.0, "units_per_carton": 4},
		{"product_name": "Embroidered Silk Saree - Aisha", "item": items.get("Silk Embroidered Saree", "HDC-TX-001"), "artisan": artisans["Aisha Ben"], "production_days": 20, "min_qty": 5, "length": 30, "width": 20, "height": 5, "weight": 0.8, "units_per_carton": 20},
		{"product_name": "Block Print Tablecloth - Johan", "item": items.get("Cotton Block Print Tablecloth", "HDC-TX-002"), "artisan": artisans["Johan Rabari"], "production_days": 5, "min_qty": 20, "length": 15, "width": 15, "height": 10, "weight": 0.5, "units_per_carton": 30},
		{"product_name": "Brass Dancing Lady - Ghulam", "item": items.get("Brass Dancing Lady Statue", "HDC-MT-001"), "artisan": artisans["Ghulam Ali"], "production_days": 14, "min_qty": 4, "length": 25, "width": 15, "height": 45, "weight": 3.0, "units_per_carton": 6},
		{"product_name": "Blue Pottery Bowl Set - Lakshmi", "item": items.get("Blue Pottery Serving Bowl", "HDC-PT-001"), "artisan": artisans["Lakshmi Bai"], "production_days": 8, "min_qty": 12, "length": 30, "width": 30, "height": 15, "weight": 0.6, "units_per_carton": 12},
		{"product_name": "Terracotta Tea Set - Mohan", "item": items.get("Terracotta Tea Set", "HDC-PT-002"), "artisan": artisans["Mohan Rao"], "production_days": 6, "min_qty": 10, "length": 25, "width": 20, "height": 20, "weight": 2.0, "units_per_carton": 8},
	]

	created = {}
	for e_data in entries_data:
		product_name = e_data["product_name"]
		if frappe.db.exists("Artisan Product Catalog Entry", {"product_name": product_name}):
			print(f"  📋 Catalog Entry already exists: {product_name}")
			existing = frappe.get_value("Artisan Product Catalog Entry", {"product_name": product_name}, "name")
			created[product_name] = existing
			continue

		# Calculate CBM
		cbm = (e_data["length"] * e_data["width"] * e_data["height"]) / 1000000.0

		doc = frappe.get_doc({
			"doctype": "Artisan Product Catalog Entry",
			"product_name": product_name,
			"item_code": e_data["item"],
			"artisan": e_data["artisan"],
			"production_time_days": e_data["production_days"],
			"min_order_qty": e_data["min_qty"],
			"length_cm": e_data["length"],
			"width_cm": e_data["width"],
			"height_cm": e_data["height"],
			"weight_per_unit_kg": e_data["weight"],
			"units_per_carton": e_data["units_per_carton"],
			"calculated_cbm": flt(cbm, 6),
		})
		doc.insert(ignore_permissions=True)
		print(f"  📋 Created Catalog Entry: {product_name} (CBM: {cbm:.6f})")
		created[product_name] = doc.name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  7. Visual Offer Sheets
# ═══════════════════════════════════════════════════════

def ensure_visual_offer_sheets(catalog_entries):
	"""Ensure Visual Offer Sheets exist."""
	today = nowdate()
	buyers = [
		{
			"buyer": "Artisan Global Imports, USA",
			"email": "buyer@artisanglobal.com",
			"incoterm": "FOB",
			"valid_until": add_days(today, 30),
			"items": [
				("Rosewood Elephant Sculpture - Ram Vilas", 50, 45.00),
				("Brass Dancing Lady - Ghulam", 30, 120.00),
				("Blue Pottery Bowl Set - Lakshmi", 100, 18.50),
			],
		},
		{
			"buyer": "Handicraft Haus, Germany",
			"email": "orders@handicrafthaus.de",
			"incoterm": "CIF",
			"valid_until": add_days(today, 45),
			"items": [
				("Embroidered Silk Saree - Aisha", 25, 85.00),
				("Sandalwood Jewelry Box - Rajesh", 60, 32.00),
				("Terracotta Tea Set - Mohan", 40, 28.00),
			],
		},
		{
			"buyer": "East West Traders, UK",
			"email": "info@eastwesttraders.co.uk",
			"incoterm": "FOB",
			"valid_until": add_days(today, 60),
			"items": [
				("Madhubani Wall Panel - Sita Devi", 15, 250.00),
				("Block Print Tablecloth - Johan", 200, 12.00),
				("Sandalwood Jewelry Box - Rajesh", 80, 32.00),
			],
		},
	]

	created = {}
	for b in buyers:
		buyer_name = b["buyer"]
		if frappe.db.exists("Visual Offer Sheet", {"buyer": buyer_name}):
			print(f"  📄 Offer Sheet already exists for: {buyer_name}")
			existing = frappe.get_value("Visual Offer Sheet", {"buyer": buyer_name}, "name")
			created[buyer_name] = existing
			continue

		total_amount = 0
		offer_items = []
		for product_name, qty, price in b["items"]:
			catalog_name = catalog_entries.get(product_name)
			if not catalog_name:
				print(f"  ⚠️  Catalog entry not found: {product_name}")
				continue
			amount = qty * price
			total_amount += amount
			offer_items.append({
				"product_catalog_entry": catalog_name,
				"qty": qty,
				"quoted_price_usd": price,
				"amount": amount,
			})

		if not offer_items:
			continue

		doc = frappe.get_doc({
			"doctype": "Visual Offer Sheet",
			"buyer": buyer_name,
			"buyer_email": b["email"],
			"incoterm": b["incoterm"],
			"valid_until": b["valid_until"],
			"offer_sheet_items": offer_items,
			"total_amount": total_amount,
		})
		doc.insert(ignore_permissions=True)
		print(f"  📄 Created Offer Sheet for {buyer_name} — ${total_amount:,.2f}")
		created[buyer_name] = doc.name

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  8. Export Orders
# ═══════════════════════════════════════════════════════

def ensure_export_orders(catalog_entries):
	"""Ensure Export Orders exist."""
	today = nowdate()

	orders_data = [
		{
			"buyer_country": "USA",
			"incoterm": "FOB",
			"port_of_discharge": "Newark, NJ",
			"coo_status": "Applied",
			"ship_date": add_days(today, 20),
			"packing": [
				{"carton": "CTN-001", "item": "Rosewood Elephant", "qty": 12, "net_wt": 28.0, "gross_wt": 30.5, "cbm": 0.054},
				{"carton": "CTN-002", "item": "Rosewood Elephant", "qty": 12, "net_wt": 28.0, "gross_wt": 30.5, "cbm": 0.054},
				{"carton": "CTN-003", "item": "Rosewood Elephant", "qty": 12, "net_wt": 28.0, "gross_wt": 30.5, "cbm": 0.054},
				{"carton": "CTN-004", "item": "Rosewood Elephant", "qty": 14, "net_wt": 32.0, "gross_wt": 35.0, "cbm": 0.063},
				{"carton": "CTN-005", "item": "Brass Dancing Lady", "qty": 6, "net_wt": 16.0, "gross_wt": 18.0, "cbm": 0.084},
				{"carton": "CTN-006", "item": "Brass Dancing Lady", "qty": 6, "net_wt": 16.0, "gross_wt": 18.0, "cbm": 0.084},
				{"carton": "CTN-007", "item": "Brass Dancing Lady", "qty": 6, "net_wt": 16.0, "gross_wt": 18.0, "cbm": 0.084},
				{"carton": "CTN-008", "item": "Brass Dancing Lady", "qty": 6, "net_wt": 16.0, "gross_wt": 18.0, "cbm": 0.084},
				{"carton": "CTN-009", "item": "Brass Dancing Lady", "qty": 6, "net_wt": 16.0, "gross_wt": 18.0, "cbm": 0.084},
				{"carton": "CTN-010", "item": "Blue Pottery Bowl", "qty": 50, "net_wt": 30.0, "gross_wt": 35.0, "cbm": 0.135},
				{"carton": "CTN-011", "item": "Blue Pottery Bowl", "qty": 50, "net_wt": 30.0, "gross_wt": 35.0, "cbm": 0.135},
			],
		},
		{
			"buyer_country": "Germany",
			"incoterm": "CIF",
			"port_of_discharge": "Hamburg",
			"coo_status": "Not Started",
			"ship_date": add_days(today, 35),
			"packing": [
				{"carton": "CTN-G1", "item": "Silk Saree", "qty": 10, "net_wt": 7.0, "gross_wt": 8.5, "cbm": 0.003},
				{"carton": "CTN-G2", "item": "Silk Saree", "qty": 10, "net_wt": 7.0, "gross_wt": 8.5, "cbm": 0.003},
				{"carton": "CTN-G3", "item": "Silk Saree", "qty": 5, "net_wt": 3.5, "gross_wt": 4.5, "cbm": 0.0015},
				{"carton": "CTN-G4", "item": "Sandalwood Box", "qty": 20, "net_wt": 22.0, "gross_wt": 24.0, "cbm": 0.030},
				{"carton": "CTN-G5", "item": "Sandalwood Box", "qty": 20, "net_wt": 22.0, "gross_wt": 24.0, "cbm": 0.030},
				{"carton": "CTN-G6", "item": "Sandalwood Box", "qty": 20, "net_wt": 22.0, "gross_wt": 24.0, "cbm": 0.030},
				{"carton": "CTN-G7", "item": "Terracotta Tea Set", "qty": 20, "net_wt": 35.0, "gross_wt": 40.0, "cbm": 0.080},
				{"carton": "CTN-G8", "item": "Terracotta Tea Set", "qty": 20, "net_wt": 35.0, "gross_wt": 40.0, "cbm": 0.080},
			],
		},
	]

	created = []
	for o_data in orders_data:
		total_cbm = sum(p["cbm"] for p in o_data["packing"])

		# Determine container estimate
		if total_cbm < 15:
			container = "LCL"
		elif total_cbm < 33:
			container = "20ft FCL"
		else:
			container = "40ft FCL"

		packing_list = []
		for p in o_data["packing"]:
			packing_list.append({
				"carton_number": p["carton"],
				"qty_inside": p["qty"],
				"net_weight": p["net_wt"],
				"gross_weight": p["gross_wt"],
				"cbm": p["cbm"],
			})

		doc = frappe.get_doc({
			"doctype": "Export Order",
			"buyer_country": o_data["buyer_country"],
			"incoterm": o_data["incoterm"],
			"port_of_discharge": o_data["port_of_discharge"],
			"certificate_of_origin_status": o_data["coo_status"],
			"estimated_ship_date": o_data["ship_date"],
			"export_packing_list": packing_list,
			"total_cbm": flt(total_cbm, 4),
			"container_estimate": container,
		})
		doc.insert(ignore_permissions=True)
		print(f"  🚢 Created Export Order to {o_data['buyer_country']} ({container}, {total_cbm:.2f} CBM)")
		created.append(doc.name)

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  9. Artisan Job Cards
# ═══════════════════════════════════════════════════════

def ensure_job_cards(export_orders, artisans):
	"""Ensure Artisan Job Cards exist."""
	if not export_orders:
		return []

	job_cards_data = [
		{"export_order": export_orders[0], "artisan": "Ram Vilas Sharma", "piece_rate": 450.00, "ordered": 50, "received": 50, "rejected": 2, "materials": [("Wood Block - Teak", 2.5, "Kg"), ("Carving Tools Kit", 1, "Nos")]},
		{"export_order": export_orders[0], "artisan": "Ghulam Ali", "piece_rate": 850.00, "ordered": 30, "received": 28, "rejected": 1, "materials": [("Brass Sheet", 3.0, "Kg"), ("Polishing Compound", 0.5, "Kg")]},
		{"export_order": export_orders[0], "artisan": "Lakshmi Bai", "piece_rate": 280.00, "ordered": 100, "received": 95, "rejected": 5, "materials": [("Clay Block", 10.0, "Kg"), ("Ceramic Glaze", 2.0, "Ltr")]},
		{"export_order": export_orders[1], "artisan": "Aisha Ben", "piece_rate": 1200.00, "ordered": 25, "received": 22, "rejected": 0, "materials": [("Silk Fabric", 15.0, "Mtr"), ("Embroidery Thread", 5.0, "Pkt")]},
		{"export_order": export_orders[1], "artisan": "Rajesh Kumar Suthar", "piece_rate": 500.00, "ordered": 60, "received": 55, "rejected": 3, "materials": [("Sandalwood Block", 8.0, "Kg"), ("Varnish", 1.0, "Ltr")]},
		{"export_order": export_orders[1], "artisan": "Mohan Rao", "piece_rate": 350.00, "ordered": 40, "received": 38, "rejected": 2, "materials": [("Terracotta Clay", 12.0, "Kg"), ("Natural Paint Set", 2.0, "Nos")]},
	]

	created = []
	for jc_data in job_cards_data:
		artisan_name = jc_data["artisan"]
		artisan_docname = artisans.get(artisan_name)
		if not artisan_docname:
			print(f"  ⚠️  Artisan not found: {artisan_name}")
			continue

		# Check if job card already exists for this artisan+order
		existing = frappe.db.exists("Artisan Job Card", {
			"export_order": jc_data["export_order"],
			"artisan": artisan_docname,
		})
		if existing:
			print(f"  📝 Job Card already exists for {artisan_name}")
			created.append(existing)
			continue

		materials = []
		if jc_data.get("materials"):
			for mat_item, mat_qty, mat_uom in jc_data["materials"]:
				materials.append({
					"material_item": mat_item,
					"qty_issued": mat_qty,
					"uom": mat_uom,
				})

		doc = frappe.get_doc({
			"doctype": "Artisan Job Card",
			"export_order": jc_data["export_order"],
			"artisan": artisan_docname,
			"piece_rate_inr": jc_data["piece_rate"],
			"qty_ordered": jc_data["ordered"],
			"qty_received": jc_data["received"],
			"qty_rejected": jc_data["rejected"],
			"raw_materials_issued": materials,
		})
		doc.insert(ignore_permissions=True)
		print(f"  📝 Created Job Card for {artisan_name} ({jc_data['received']}/{jc_data['ordered']} pcs)")
		created.append(doc.name)

	frappe.db.commit()
	return created


# ═══════════════════════════════════════════════════════
#  10. Batch Quality Records
# ═══════════════════════════════════════════════════════

def ensure_batch_qc(job_cards):
	"""Ensure Batch Quality Records exist."""
	if not job_cards:
		return

	qc_data = [
		{"job_card_idx": 0, "status": "Pass", "notes": "Excellent craftsmanship. All pieces meet export quality standards."},
		{"job_card_idx": 1, "status": "Rework", "notes": "One piece has minor surface scratches. Returned for polishing."},
		{"job_card_idx": 2, "status": "Pass", "notes": "Good glaze consistency. Color uniformity is satisfactory."},
		{"job_card_idx": 3, "status": "Pass", "notes": "Embroidery work is outstanding. No defects found."},
		{"job_card_idx": 4, "status": "Rework", "notes": "Three boxes have uneven varnish. Sent back for refinishing."},
		{"job_card_idx": 5, "status": "Pass", "notes": "All tea set pieces are well-formed. Packaging is sturdy."},
	]

	for qc in qc_data:
		idx = qc["job_card_idx"]
		if idx >= len(job_cards):
			continue

		job_card = job_cards[idx]

		# Skip if QC record already exists for this job card
		if frappe.db.exists("Batch Quality Record", {"job_card": job_card}):
			print(f"  🔍 QC Record already exists for Job Card {job_card}")
			continue

		# Fetch artisan from job card
		jc_doc = frappe.get_doc("Artisan Job Card", job_card)

		doc = frappe.get_doc({
			"doctype": "Batch Quality Record",
			"job_card": job_card,
			"qc_status": qc["status"],
			"inspector_notes": qc["notes"],
		})
		doc.insert(ignore_permissions=True)
		print(f"  🔍 Created QC Record: {qc['status']} — {doc.name}")
