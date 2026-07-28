# README

## Handicraft Export — Export Readiness & Subcontracting for Handicrafts

**App Name:** Handicraft Export (`handicraft_export`)
**Module:** Handicraft
**Domain:** Handicrafts / Export Readiness & Artisan Subcontracting
**Required Apps:** Frappe v15, ERPNext v15 (Selling, Buying, and Stock modules)
**Repository:** https://github.com/Pasha1234565/handicraft_export.git

---

## TABLE OF CONTENTS

1. [Application Overview](#1-application-overview)
2. [System Architecture](#2-system-architecture)
3. [Getting Started](#3-getting-started)
4. [The Day-to-Day Workflow, Step by Step](#4-the-day-to-day-workflow-step-by-step)
5. [Visual Offer Sheet & CBM Calculator](#5-visual-offer-sheet--cbm-calculator)
6. [Active Document Generation](#6-active-document-generation)
7. [Subcontracting & Piece-Rate Billing](#7-subcontracting--piece-rate-billing)
8. [Quality Control & Notifications](#8-quality-control--notifications)
9. [Reports](#9-reports)
10. [Workspace Navigation](#10-workspace-navigation)
11. [Scheduled Tasks & Automation](#11-scheduled-tasks--automation)
12. [Setup & Configuration (Fixtures)](#12-setup--configuration-fixtures)
13. [Demo Data](#13-demo-data)
14. [Troubleshooting](#14-troubleshooting)
15. [Appendix](#15-appendix)

---

## 1. APPLICATION OVERVIEW

### 1.1 Purpose

**Handicraft Export** is a Frappe/ERPNext v15 application built for handicraft exporters who need to manage the full export lifecycle — from creating photo-rich visual offer sheets for international buyers, through container planning with CBM calculations, to managing artisan subcontracting with piece-rate billing. It layers on top of standard ERPNext's Selling & Buying modules.

The app covers:

- **Pre-Sales Visual Quotations** — Create professional photo-grid offer sheets showcasing handicraft products with images, dimensions, and pricing
- **Export Order Management** — Track international orders with packing lists, certificate of origin, and incoterms
- **CBM Calculator & Container Planning** — Automatically compute cubic meter volumes and estimate container requirements (LCL / 20ft FCL / 40ft FCL)
- **Artisan Subcontracting** — Issue job cards to artisans with piece rates, track received/rejected quantities, and generate automated Purchase Invoices
- **Quality Control** — Batch inspection records with quantity tracking, defect analysis
- **Active Document Generation** — Print-ready Commercial Invoice and Packing List templates linked to Export Orders
- **Document Readiness Alerts** — Automated notifications when shipping documents are missing near shipment dates

### 1.2 Key Features

- **11 DocTypes** — 7 document/master DocTypes, 4 child tables
- **3 Submittable DocTypes** — Visual Offer Sheet, Export Order, Artisan Job Card
- **2 Custom Roles** — Export Coordinator, Artisan Liaison
- **3 Jinja Print Formats** — Visual Offer Sheet (photo grid), Commercial Invoice - Export, Packing List
- **3 Reports** — Document Readiness Dashboard, Cluster Output Capacity, Artisan Yield & Wastage
- **3 Automated Notifications** — Document Missing Near Shipment, QC Failed/Rework Needed, Container Threshold Alert
- **2 Scheduled Tasks** — Daily document readiness checks, weekly cluster analytics
- **2 API Endpoints** — `generate_artisan_invoice` (auto Purchase Invoice on Job Card submit), `create_export_order_from_offer_sheet`
- **Automatic Purchase Invoice Generation** — Submitting an Artisan Job Card with received quantities automatically creates and submits a Purchase Invoice
- **CBM Auto-Calculation** — Product dimensions automatically compute CBM on save
- **Container Estimation** — Total CBM determines LCL, 20ft FCL, or 40ft FCL container requirements

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Technology Stack
- **Framework:** Frappe v15 / ERPNext v15
- **Database:** MariaDB
- **Automated Tasks:** Frappe Scheduler (daily + weekly cron)
- **Dependencies:** ERPNext (required — installs automatically)

### 2.2 DocType Structure

| # | DocType Name | Type | Card Section | Submittable |
|---|--------------|------|--------------|:-----------:|
| 1 | Artisan Cluster | Document | Master Data | ❌ |
| 2 | Artisan | Document | Master Data | ❌ |
| 3 | Artisan Product Catalog Entry | Document | Pre-Sales | ❌ |
| 4 | Catalog Image | Child Table | — | ❌ |
| 5 | Visual Offer Sheet | Document | Pre-Sales | ✅ |
| 6 | Offer Sheet Item | Child Table | — | ❌ |
| 7 | Export Order | Document | Export | ✅ |
| 8 | Export Packing List | Child Table | — | ❌ |
| 9 | Artisan Job Card | Document | Subcontracting | ✅ |
| 10 | Raw Material Issued | Child Table | — | ❌ |
| 11 | Batch Quality Record | Document | Quality Control | ❌ |

### 2.3 Naming Series Convention

| DocType | Prefix | Format |
|---------|--------|--------|
| Artisan Cluster | — | By fieldname (`cluster_name`) |
| Artisan | ART | `ART-{artisan_name}-{#####}` |
| Artisan Product Catalog Entry | PC | `PC-{product_name}-{#####}` |
| Visual Offer Sheet | VOS | `VOS-{buyer}-{YYYY}-{#####}` |
| Export Order | EXPORD | `EXPORD-{YYYY}-{#####}` |
| Artisan Job Card | AJC | `AJC-{YYYY}-{#####}` |
| Batch Quality Record | QC | `QC-{YYYY}-{#####}` |

### 2.4 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                        WORKFLOW OVERVIEW                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  🎨 MASTER DATA SETUP                                                  │
│  ┌──────────────┐   ┌──────────┐   ┌──────────────────┐              │
│  │ Artisan      │──▶│  Artisan │──▶│ Artisan Product  │              │
│  │ Cluster      │   │          │   │ Catalog Entry    │              │
│  └──────────────┘   └────┬─────┘   │ (with CBM +     │              │
│                          │         │  images)         │              │
│                          ▼         └────────┬─────────┘              │
│                   ┌────────────┐            │                        │
│                   │  Supplier  │            │                        │
│                   │ (standard  │            │                        │
│                   │  ERPNext)  │            │                        │
│                   └────────────┘            │                        │
│                                             ▼                        │
│  📄 PRE-SALES                                                         │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              Visual Offer Sheet (Submittable)                 │    │
│  │  ┌──────────────────────────────────────────────┐            │    │
│  │  │ Offer Sheet Items × N                        │            │    │
│  │  │ (Product Catalog Entry, Qty, Price)          │            │    │
│  │  └──────────────────────────────────────────────┘            │    │
│  │  ├─ Jinja Print Format: Photo Grid (2-3 columns)             │    │
│  │  └─ Action: "Create Export Order" button                     │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                             │                                        │
│                             ▼                                        │
│  🚢 EXPORT                                                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              Export Order (Submittable)                       │    │
│  │  ┌──────────────────────────────────────────────┐            │    │
│  │  │ Export Packing List × N                      │            │    │
│  │  │ (Carton#, Item, Qty, Net/Gross Wt, CBM)     │            │    │
│  │  └──────────────────────────────────────────────┘            │    │
│  │  ├─ CBM Calculator (before_save)                             │    │
│  │  │  Sum → total_cbm → container_estimate (LCL/20ft/40ft)    │    │
│  │  └─ Active Docs: Commercial Invoice, Packing List (Jinja)   │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                             │                                        │
│                             ▼                                        │
│  🛠️ SUBCONTRACTING                                                  │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │           Artisan Job Card (Submittable)                      │    │
│  │  ┌──────────────────────────────────────────────┐            │    │
│  │  │ Raw Materials Issued × N                     │            │    │
│  │  │ (Item, Qty, UOM)                             │            │    │
│  │  └──────────────────────────────────────────────┘            │    │
│  │  ├─ Qty: Ordered / Received / Rejected                       │    │
│  │  └─ on submit → API → Purchase Invoice (standard ERPNext)    │    │
│  └────────────────────────┬─────────────────────────────────────┘    │
│                           │                                          │
│                           ▼                                          │
│  🔍 QUALITY CONTROL                                                  │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │          Batch Quality Record                                 │    │
│  │  Qty: Checked / Passed / Rework / Failed                     │    │
│  │  Status: Pass / Rework / Fail                                │    │
│  │  on "Fail" or "Rework" → System Notification                 │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  📊 REPORTS                                                           │
│  ┌──────────────┐  ┌──────────────────┐  ┌───────────────────────┐   │
│  │ Document     │  │ Cluster Output   │  │ Artisan Yield &       │   │
│  │ Readiness    │  │ Capacity         │  │ Wastage               │   │
│  │ Dashboard    │  │ Report           │  │ Script Report         │   │
│  └──────────────┘  └──────────────────┘  └───────────────────────┘   │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. GETTING STARTED

### 3.1 Installation

```bash
# From the bench directory
bench get-app https://github.com/Pasha1234565/handicraft_export.git
bench --site your-site.com install-app handicraft_export
bench --site your-site.com migrate
```

> **Note:** ERPNext is automatically installed as a dependency when you `install-app` on a new site. No separate installation step is needed.

### 3.2 Role Setup

Two roles are created automatically on `install-app` (via the `create_roles` patch):

1. **Export Coordinator** — Full access to Export Orders, Visual Offer Sheets, and the standard ERPNext sales flow. Can view but not edit Artisan Job Cards (to prevent altering piece-rates).
2. **Artisan Liaison** — Full access to Artisans, Clusters, Product Catalog, Job Cards, and Batch Quality Records. No access to Export Orders or Visual Offer Sheets (to shield international pricing from the cluster operations layer).

**To assign roles to a user:**
1. Go to **System Manager → User → [your user] → Roles**
2. Add **"Export Coordinator"** and/or **"Artisan Liaison"**
3. Save, then log out and log back in for permissions to take effect

### 3.3 Initial Configuration

Before using the app day-to-day, set up the following:

1. **Company** — Go to **Accounting → Company → New** and create your company (required for Purchase Invoice generation from Job Cards)
2. **Default Company** — Set it in **Settings → Global Defaults → Default Company**
3. **Artisan Clusters** — Create the regional clusters your artisans belong to
4. **Artisans** — Each artisan needs a **linked Supplier** (standard ERPNext) for payment processing
5. **Products** — Create standard ERPNext **Items** for your handicraft products, then add them to the **Artisan Product Catalog Entry** with CBM dimensions

### 3.4 Post-Installation Checks

After `install-app` and `migrate`, verify everything is working:

1. Check the **Handicraft Export Desk** workspace appears in the desk menu
2. Open a **Visual Offer Sheet** → ensure the **Submit** button is visible
3. Open an **Export Order** → ensure the **Submit** button is visible
4. Open an **Artisan Job Card** → ensure the **Submit** button is visible

If submit buttons are missing, the user may need to log out and log back in, or the Administrator should verify the role assignment in **User → Permissions**.

---

## 4. THE DAY-TO-DAY WORKFLOW, STEP BY STEP

This is the sequence you'll follow for a typical handicraft export cycle — from setting up an artisan cluster to shipping an order and paying the artisans.

### Step 1 — Create an Artisan Cluster

Before adding individual artisans, group them into clusters by region.

1. Go to **Handicraft Export Desk → Artisan Cluster**.
2. Click **+ Add Artisan Cluster**.
3. Enter the **Cluster Name** (e.g., "Sahariya Wood Carvers"), **Nodal Agency/NGO** (e.g., "SEWA Bharat"), **Region** (e.g., "Rajasthan"), and **UDYAM Registration Status** (Pending / Registered / Exempt).
4. Click **Save**.

### Step 2 — Create an Artisan

Each artisan must be registered in the system with a linked Supplier for payment processing.

1. Go to **Handicraft Export Desk → Artisan**.
2. Click **+ Add Artisan**.
3. Enter the **Artisan Name**, select their **Artisan Cluster** and **Primary Craft** (Item Group).
4. **Crucially**, select a **Linked Supplier** — this is the standard ERPNext Supplier entity used for accounting and Purchase Invoicing.
5. Add optional contact details (Email, Phone, Address).
6. Click **Save**.

### Step 3 — Create Products & Catalog Entries

First, ensure the handicraft products exist as standard ERPNext Items:

1. Go to **Item → + Add Item**.
2. Create items with codes, names, and item groups (e.g., HDC-WD-001 "Rosewood Elephant Sculpture" in "Wood Carving" group).

Then, create the Artisan Product Catalog Entry:

1. Go to **Artisan Product Catalog Entry → + Add**.
2. Enter the **Product Name**, select the **Item Code** (from standard Items), and the **Artisan**.
3. Fill in **Production Time (Days)** and **Min Order Qty**.
4. In the **CBM Data** section, enter **Length, Width, Height (cm)**, **Weight per Unit (kg)**, and **Units per Carton**.
5. The **Calculated CBM** is auto-computed on save: `(L × W × H) / 1,000,000`.
6. Add product photos in the **Catalog Images** child table (mark one as primary).
7. Click **Save**.

### Step 4 — Create a Visual Offer Sheet

This is the pre-sales quotation document with a photo-rich print format.

1. Click the **New Visual Offer** shortcut on the dashboard.
2. Enter the **Buyer** name, **Buyer Email**, **Incoterm** (EXW / FOB / CIF / DAP / DDP), and **Valid Until** date.
3. In the **Offer Sheet Items** table, add rows selecting **Product Catalog Entry**, **Quantity**, and **Quoted Price (USD)**. Product name and artisan are fetched automatically.
4. The **Total Amount (USD)** is computed from line totals.
5. Click **Save**, then **Submit** to finalize the offer.
6. **Print** the document to see the photo-grid format — products are displayed in a 2-3 column CSS grid with images, names, dimensions, MOQ, and quoted prices.

### Step 5 — Create an Export Order

From a submitted Visual Offer Sheet, or directly:

1. Click **Export Order → + Add**.
2. Enter the **Buyer Country**, **Incoterm**, **Port of Discharge**, and **Estimated Ship Date**.
3. Track the **Certificate of Origin Status** (Not Started → Applied → Issued).
4. In the **Export Packing List** table, add rows for each carton with **Carton Number**, **Item**, **Qty Inside**, **Net Weight**, **Gross Weight**, and **CBM**.
5. On save, the **Total CBM** is auto-calculated from the packing list.
6. The **Container Estimate** is automatically determined:
   - **< 15 CBM** → **LCL** (Less than Container Load)
   - **15 to < 33 CBM** → **20ft FCL** (Full Container Load)
   - **≥ 33 CBM** → **40ft FCL**
7. Click **Save**, then **Submit**.

### Step 6 — Issue Artisan Job Cards

When an export order is placed, issue job cards to the artisans who will produce the goods.

1. Click the **New Job Card** shortcut on the dashboard.
2. Link the **Export Order** and select the **Artisan**.
3. Enter the **Piece Rate (INR)** — the per-piece payment rate.
4. Set **Qty Ordered**, **Qty Received** (initially 0), and **Qty Rejected** (initially 0).
5. In the **Raw Materials Issued** table, log any materials given to the artisan (Item, Qty, UOM).
6. Click **Save**. When the artisan delivers the finished goods, update **Qty Received** and **Qty Rejected**, then **Submit**.

**Behind the scenes:** On submission, the system calls `generate_artisan_invoice()` which:
- Fetches the artisan's linked Supplier
- Creates a standard ERPNext **Purchase Invoice** for `qty_received × piece_rate_inr`
- Inserts and submits the Purchase Invoice
- This avoids duplicating standard accounting math while automating artisan payments

### Step 7 — Log Quality Control

After receiving goods from an artisan, inspect them and record the results.

1. Click the **Log QC** shortcut on the dashboard.
2. Select the **Job Card** — the **Artisan**, **Export Order**, and **QC Date** are fetched/auto-filled.
3. Enter **Qty Checked**, **Qty Passed**, **Qty Rework**, and **Qty Failed**.
4. Set the **QC Status**: **Pass**, **Rework**, or **Fail**.
5. Describe any **Defect Type / Description**.
6. Attach **QC Photos** (optional) and add **Inspector Notes**.
7. Click **Save**.

**Notifications:**
- If QC Status is **Fail** or **Rework**, the Artisan Liaison receives a **System Notification** immediately.
- If the **Container Estimate** changes on an Export Order (e.g., from LCL to 20ft FCL), the Logistics desk gets a **Container Threshold Alert** system notification.

---

## 5. VISUAL OFFER SHEET & CBM CALCULATOR

### 5.1 Photo-Grid Print Format

The **Visual Offer Sheet** includes a custom Jinja Print Format that renders products as a visual photo grid:

- **2-column or 3-column CSS Grid** layout
- Each cell displays: **Product Image** (primary), **Product Name**, **Dimensions**, **MOQ**, and **Quoted Price (USD)**
- The print format iterates over `Offer Sheet Item` child table rows and fetches the primary image from the linked `Artisan Product Catalog Entry`

This is critical for handicraft exports — buyers purchase based on photos, not SKU text.

### 5.2 CBM Calculation

The **CBM Calculator** works at two levels:

**Per Product (catalog level):**
- Fields: `length_cm`, `width_cm`, `height_cm`
- Auto-computed: `calculated_cbm = (length × width × height) / 1,000,000`
- Formula runs on `before_save` via the `ArtisanProductCatalogEntry` controller

**Per Export Order (aggregate level):**
- Sums all CBM values from the `Export Packing List` child table into `total_cbm`
- Applies container estimate logic:
  - `total_cbm < 15` → **LCL**
  - `15 <= total_cbm < 33` → **20ft FCL**
  - `total_cbm >= 33` → **40ft FCL**
- Runs on `before_save` via the `ExportOrder` controller
- When the container estimate changes, the **Container Threshold Alert** notification fires

### 5.3 Create Export Order from Offer Sheet

A whitelisted API function `create_export_order_from_offer_sheet()` enables pulling items from a submitted Visual Offer Sheet into a new Export Order. This can be wired to a custom button on the Offer Sheet form.

---

## 6. ACTIVE DOCUMENT GENERATION

The app includes three Jinja Print Formats for generating export-ready documents:

### 6.1 Visual Offer Sheet (Print Format)

- **DocType:** Visual Offer Sheet
- **Type:** Jinja
- **Output:** Photo-grid layout with product images, dimensions, and pricing

### 6.2 Commercial Invoice - Export (Print Format)

- **DocType:** Export Order
- **Type:** Jinja
- **Output:** Professional commercial invoice with:
  - Buyer country, incoterm, port of discharge
  - HS Codes (from the linked standard Item master)
  - Export Packing List items with quantities and values
  - Total CBM and container estimate

### 6.3 Packing List (Print Format)

- **DocType:** Export Order
- **Type:** Jinja
- **Output:** Detailed packing list with:
  - Carton-by-carton breakdown (carton number, item, quantity)
  - Grouped totals for Net Weight, Gross Weight, and CBM
  - Container estimate reference

---

## 7. SUBCONTRACTING & PIECE-RATE BILLING

### 7.1 Artisan Job Card Workflow

```
Draft ──(Receive goods + submit)──▶ Submitted
```

The lifecycle of an Artisan Job Card:

1. **Create** — Link to an Export Order, select Artisan, set piece rate and ordered quantity
2. **Issue Raw Materials** — Log materials given to the artisan via the child table
3. **Receive Goods** — Update qty_received and qty_rejected as the artisan delivers
4. **Submit** — This triggers the automated invoice generation

### 7.2 Automated Purchase Invoice Generation

On submission of an Artisan Job Card with `qty_received > 0`, the system:

1. Fetches the artisan's **linked Supplier** (standard ERPNext Supplier)
2. Checks if a Purchase Invoice already exists for this Job Card (prevents duplicates)
3. Creates a standard **Purchase Invoice** with:
   - **Supplier:** Artisan's linked Supplier
   - **Item:** "Job Work - {Job Card Name}"
   - **Quantity:** qty_received
   - **Rate:** piece_rate_inr
   - **Description:** Full details of the job card, ordered/received/rejected quantities
4. **Inserts and submits** the Purchase Invoice
5. The Purchase Invoice is linked back to the Job Card via a custom field (`custom_artisan_job_card`)

This routes artisan wages through the standard Purchase Invoice doctype without duplicating accounting logic.

### 7.3 Raw Material Tracking

The **Raw Materials Issued** child table on the Artisan Job Card tracks materials given to artisans:

- **Material Item** (Link → Item)
- **Qty Issued** (Float)
- **UOM** (Link → UOM)

This provides a record of what materials were consumed for each job, useful for cost analysis and inventory reconciliation.

---

## 8. QUALITY CONTROL & NOTIFICATIONS

### 8.1 Batch Quality Record

The Batch Quality Record captures detailed inspection data:

| Field | Type | Purpose |
|-------|------|---------|
| Job Card | Link | Links to the Artisan Job Card being inspected |
| Artisan | Link (fetched) | Auto-filled from Job Card |
| Export Order | Link (fetched) | Auto-filled from Job Card |
| QC Date | Date | Defaults to today |
| Inspector | Link → User | Who performed the inspection |
| Qty Checked | Int | Total pieces inspected |
| Qty Passed | Int | Pieces meeting quality standards |
| Qty Rework | Int | Pieces needing rework |
| Qty Failed | Int | Pieces that failed inspection |
| QC Status | Select | Pass / Rework / Fail |
| Defect Type | Small Text | Description of defects found |
| QC Photos | Attach Image | Evidence photos |
| Inspector Notes | Text | Detailed inspection notes |

### 8.2 Notifications

The app includes three automated notifications:

| Notification | Event | Channel | Condition | Recipients |
|--------------|-------|---------|-----------|------------|
| **Document Missing Near Shipment** | Days Before (3 days) | Email | Certificate of Origin Status ≠ "Issued" | Export Coordinator |
| **QC Failed / Rework Needed** | After Save | System Notification | qc_status in ["Fail", "Rework"] | Artisan Liaison |
| **Container Threshold Alert** | Value Change | System Notification | container_estimate changes | Export Coordinator / Logistics |

---

## 9. REPORTS

| Report | Type | Based On | Purpose |
|--------|------|----------|---------|
| **Document Readiness Dashboard** | Query Report | Export Order | Flags Export Orders where Commercial Invoice or COO is missing 3 days before estimated shipment |
| **Cluster Output Capacity** | Query Report | Artisan / Artisan Cluster | Groups active Artisans by Artisan Cluster and aggregates their production_time_days to show NGO/Gov buyers total capacity |
| **Artisan Yield & Wastage** | Script Report | Artisan Job Card | Compares qty_ordered vs qty_received vs qty_rejected across Artisan Job Cards to analyze yield and wastage |

---

## 10. WORKSPACE NAVIGATION

**Workspace:** Handicraft Export Desk

**Shortcuts (top row):**
- 📄 **New Visual Offer** — Opens a new Visual Offer Sheet form
- 📝 **New Job Card** — Opens a new Artisan Job Card form
- 🔍 **Log QC** — Opens a new Batch Quality Record form

**Number Cards:**
- **Total CBM Shipping This Week** — Aggregated CBM from Export Orders shipping this week
- **Active Artisans (YTD)** — Count of artisans with job cards this year
- **Pending Job Cards** — Count of unsubmitted or partially fulfilled job cards

**Chart:**
- **Artisan Yield** — Bar chart comparing ordered vs received values, sourced from the Artisan Yield & Wastage report data

**Card Sections:**
- **Master Data** — Artisan Cluster, Artisan
- **Pre-Sales** — Visual Offer Sheet, Artisan Product Catalog Entry
- **Export** — Export Order
- **Subcontracting** — Artisan Job Card
- **Quality Control** — Batch Quality Record
- **Reports** — Document Readiness Dashboard, Cluster Output Capacity, Artisan Yield & Wastage

---

## 11. SCHEDULED TASKS & AUTOMATION

| Task | Frequency | What it does |
|------|-----------|--------------|
| `daily_check_document_readiness` | Daily | Scans Export Orders shipping in 3 days, flags missing Certificate of Origin, and emails Export Coordinator |
| `weekly_update_cluster_analytics` | Weekly (Mon 9 AM) | Updates each Artisan Cluster's active artisan count for reporting |

> Ensure the scheduler is enabled on your site: `bench --site your-site.com scheduler enable`

---

## 12. SETUP & CONFIGURATION (FIXTURES)

The following are set up automatically via hooks and patches:

### On `install-app` (via `after_install`):
- **Roles** — Export Coordinator, Artisan Liaison (created with `create_roles.execute`)
- **Custom Fields** — On standard DocTypes (Sales Order, Purchase Invoice) with `create_custom_fields.execute`

### On `migrate` (via `after_migrate`):
- **Module Def** — "Handicraft" module registered against the app (`create_handicraft_export_module`)
- **DocType Sync** — Force-syncs all DocTypes from JSON files (`force_sync_doctypes`)
- **Workspace** — Handicraft Export Desk workspace (`create_handicraft_workspace`)
- **Dashboard Charts** — Artisan Yield chart linked to workspace (`create_dashboard_charts`)
- **Roles** — Ensure roles exist and UOM permissions are set (`create_roles`)
- **DocType Permissions** — Set DocPerm records for all custom DocTypes (bypasses developer-mode restriction) (`set_doctype_permissions`)
- **Custom Fields** — Additional custom fields on standard DocTypes (`create_custom_fields`)

### Pre-model-sync patches:
- **Module Registration** — `create_handicraft_export_module.execute` (ensures Frappe's model sync can find our module)

### Fixtures (exported for redeployment):
- Workspace (filtered by module "Handicraft")
- DocType (filtered by module "Handicraft")
- Report (filtered by module "Handicraft")
- Role (Export Coordinator, Artisan Liaison)
- Notification (Document Missing Near Shipment, QC Failed/Rework Needed, Container Threshold Alert)

---

## 13. DEMO DATA

Demo data can be seeded via the bench console command:

```bash
bench --site your-site.com execute handicraft_export.handicraft.demo_data.execute
```

This creates sample data across all modules:

| Category | Count | Details |
|----------|-------|---------|
| 🏘️ **Artisan Clusters** | 5 | Sahariya Wood Carvers, Madhubani Art Village, Kutch Embroidery Circle, Channapatna Toy Makers, Bidri Art Metal Workers |
| 👨‍🎨 **Artisans** | 8 | Artisans from Rajasthan, Bihar, Gujarat, Karnataka, Telangana with realistic names and contact info |
| 📦 **Products (Items)** | 10 | Wood carvings, textiles, metal crafts, pottery, jewelry across different item groups |
| 🪵 **Raw Materials** | 11 | Wood blocks, brass sheets, clay, silk fabric, glaze, embroidery thread, etc. |
| 🏢 **Suppliers** | 5 | Cooperative societies and trusts for artisan accounting entities |
| 📋 **Catalog Entries** | 8 | Products linked to artisans with CBM dimensions and production data |
| 📄 **Visual Offer Sheets** | 3 | Offers to buyers in USA ($7,800+), Germany, and UK |
| 🚢 **Export Orders** | 2 | FOB USA (Newark) with 11 cartons and CIF Germany (Hamburg) with 8 cartons |
| 📝 **Job Cards** | 6 | 3 for USA order, 3 for Germany order with varying quantities and piece rates |
| 🔍 **QC Records** | 6 | Mix of Pass and Rework statuses with inspector notes |

The script is **idempotent** — it checks existence before creating records, so it's safe to run multiple times.

---

## 14. TROUBLESHOOTING

| Issue | Cause | Solution |
|-------|-------|----------|
| App not found during install | App not in `apps.txt` | `echo "handicraft_export" >> sites/apps.txt` |
| Module "Handicraft" not found | Module Def not created | `bench --site your-site.com migrate` (handled by `create_handicraft_export_module` patch) |
| Submit button missing on Visual Offer Sheet / Export Order | DocPerm records not created or user lacks role | Ensure user has **Export Coordinator** role assigned, then log out and log back in. Or run `bench --site your-site.com migrate` to re-run `set_doctype_permissions` |
| "User does not have doctype access via role permission for document UOM" | Custom roles lack UOM read permission | Run `bench --site your-site.com migrate` (handled by `create_roles` patch). Or manually run `bench --site your-site.com execute handicraft_export.patches.create_roles.execute` |
| "Expense account is mandatory for item" when submitting Job Card | No default expense account set on Company | Go to **Accounting → Company → [Your Company]** and set **Default Expense Account**, or ensure a COGS account exists |
| "Please select a Company" on Job Card submission | No company set for the site | Set **Company** in **Settings → Global Defaults → Default Company** |
| Purchase Invoice not created on Job Card submit | Artisan has no linked Supplier | Edit the Artisan record and set the **Linked Supplier** field |
| Handicraft Export Desk workspace missing | Workspace creation failed | `bench --site your-site.com execute handicraft_export.patches.create_handicraft_workspace.execute` |
| Dashboard chart missing from workspace | Chart creation failed | `bench --site your-site.com execute handicraft_export.patches.create_dashboard_charts.execute` |
| Scheduled tasks not running | Scheduler disabled | `bench --site your-site.com scheduler enable` |
| Demo data creation fails halfway | Pre-existing data conflicts | The script is idempotent; run it again and it will skip existing records |
| DocType changes not reflected after migrate | Schema not synced | Set `developer_mode: 1` in `site_config.json` and run `bench --site your-site.com migrate` |
| Notifications not firing | Scheduler disabled or notification disabled | Check the Notification document is enabled and the scheduler is running |

---

## 15. APPENDIX

### A. Role Permissions

| Role | Artisan Cluster | Artisan | Product Catalog | Visual Offer Sheet | Export Order | Artisan Job Card | Batch QC | Submit/Amend |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Export Coordinator** | Read | Read | Read | Full Access | Full Access | Read | Read | ✅ (VOS, EO) |
| **Artisan Liaison** | Full Access | Full Access | Full Access | — | — | Full Access | Full Access | ✅ (AJC, BQR) |
| **System Manager** | Read | Read | Read | Read | Read | Full Access | Full Access | ✅ (All) |

### B. Key DocType Field Reference

#### Artisan Cluster
| Field | Type | Notes |
|-------|------|-------|
| Cluster Name | Data | Unique, document name |
| Nodal Agency / NGO | Data | Partner organization |
| Region | Data | Geographic region |
| UDYAM Registration Status | Select | Pending / Registered / Exempt |

#### Artisan
| Field | Type | Notes |
|-------|------|-------|
| Artisan Name | Data | Required |
| Artisan Cluster | Link → Artisan Cluster | Required |
| Primary Craft | Link → Item Group | Their main craft category |
| Linked Supplier | Link → Supplier | Standard ERPNext Supplier for payments |
| Contact Email / Phone / Address | Data / Small Text | Contact details |

#### Artisan Product Catalog Entry
| Field | Type | Notes |
|-------|------|-------|
| Product Name | Data | Required |
| Item Code | Link → Item | Standard ERPNext Item |
| Artisan | Link → Artisan | Required |
| Product Images | Table → Catalog Image | Multiple images, one primary |
| Production Time Days / Min Order Qty | Int | Production lead time |
| Length/Width/Height cm | Float | Product dimensions |
| Weight per Unit kg | Float | Shipping weight |
| Units per Carton | Int | How many fit in a carton |
| Calculated CBM | Float (read-only) | Auto-computed: (L×W×H)/1,000,000 |

#### Visual Offer Sheet (Submittable)
| Field | Type | Notes |
|-------|------|-------|
| Buyer | Data | Required |
| Buyer Email | Data | Email contact |
| Incoterm | Select | EXW / FOB / CIF / DAP / DDP |
| Valid Until | Date | Offer validity |
| Offer Sheet Items | Table → Offer Sheet Item | Product, qty, price |
| Total Amount (USD) | Currency | Read-only, computed sum |

#### Export Order (Submittable)
| Field | Type | Notes |
|-------|------|-------|
| Linked Sales Order | Link → Sales Order | Optional standard SO reference |
| Buyer Country | Data | Required |
| Incoterm | Select | EXW / FOB / CIF / DAP / DDP |
| Port of Discharge | Data | Destination port |
| Certificate of Origin Status | Select | Not Started / Applied / Issued |
| Estimated Ship Date | Date | For readiness alerts |
| Export Packing List | Table → Export Packing List | Carton-level details |
| Total CBM | Float (read-only) | Auto-summed from packing list |
| Container Estimate | Data (read-only) | LCL / 20ft FCL / 40ft FCL |

#### Artisan Job Card (Submittable)
| Field | Type | Notes |
|-------|------|-------|
| Export Order | Link → Export Order | Required |
| Artisan | Link → Artisan | Required |
| Piece Rate (INR) | Currency | Per-piece payment rate |
| Qty Ordered | Int | Required |
| Qty Received | Int | Updated on delivery |
| Qty Rejected | Int | Defective pieces |
| Raw Materials Issued | Table → Raw Material Issued | Materials given to artisan |

#### Batch Quality Record
| Field | Type | Notes |
|-------|------|-------|
| Job Card | Link → Artisan Job Card | Required |
| Artisan | Link (fetched) | From Job Card |
| Export Order | Link (fetched) | From Job Card |
| QC Date | Date | Defaults to today |
| Inspector | Link → User | Who inspected |
| Qty Checked / Passed / Rework / Failed | Int | Quantity breakdown |
| QC Status | Select | Pass / Rework / Fail |
| Defect Type | Small Text | Description of defects |
| QC Photos | Attach Image | Evidence |
| Inspector Notes | Text | Notes and observations |

### C. API Reference

#### `generate_artisan_invoice(job_card_name)`
- **Method:** `@frappe.whitelist()`
- **Called from:** Client-side on Job Card submission (via `doc_events` or custom button)
- **Purpose:** Creates and submits a standard Purchase Invoice for the artisan's received work
- **Returns:** Purchase Invoice name, or `None` if no received qty
- **Error handling:** Throws if Job Card not submitted, no linked Supplier, or no expense account configured

#### `create_export_order_from_offer_sheet(offer_sheet)`
- **Method:** `@frappe.whitelist()`
- **Purpose:** Creates a draft Export Order from a submitted Visual Offer Sheet
- **Returns:** Export Order name
- **Error handling:** Throws if Offer Sheet is not submitted

### D. Related Documents
- Frappe Framework Documentation: https://frappeframework.com/docs
- ERPNext Selling Module: https://docs.erpnext.com/docs/user/manual/en/selling
- ERPNext Buying Module: https://docs.erpnext.com/docs/user/manual/en/buying
- ERPNext Stock Module: https://docs.erpnext.com/docs/user/manual/en/stock

### E. Known Limitations

- **No ICEGATE/DGFT integration** — This app generates printable paperwork (Commercial Invoice, Packing List) but does not electronically file customs declarations
- **No freight cost calculation** — The CBM calculator informs container selection but does not calculate freight costs (rates are volatile)
- **No advanced inventory integration** — Raw material issuance is recorded but not automatically deducted from stock; this requires standard ERPNext Stock Entry workflows
- **No artisan portal** — Artisans cannot log in to view their job cards or payment status (future enhancement)

### F. Repository

- **Repository:** https://github.com/Pasha1234565/handicraft_export.git

---

*End of README*
