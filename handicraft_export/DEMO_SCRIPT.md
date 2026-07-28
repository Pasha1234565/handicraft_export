# Handicraft Export — Demo Video Script

**Duration:** ~12 minutes
**App Version:** 1.0.0
**Target Audience:** Handicraft export managers, artisan coordinators, ERPNext implementers
**Style:** Walkthrough with screen recordings, annotated callouts, and on-screen text overlays

---

## 🎬 INTRO (0:00 – 0:45)

### Scene: Title Card + Overview

| Element | Detail |
|---------|--------|
| **Visual** | Animated title screen: "Handicraft Export — From Cluster to Shipment" with orange (#e67e22) branding. Subtitle: "Frappe/ERPNext v15 App for Export Readiness & Artisan Subcontracting" |
| **Overlay** | GitHub repo URL: `github.com/Pasha1234565/handicraft_export` |

**Narration:**
> "Welcome to Handicraft Export — a Frappe ERPNext app designed for handicraft exporters who need to manage the full export lifecycle. From registering artisan clusters in rural India, to creating photo-rich visual offer sheets for international buyers, to automating artisan payments with piece-rate billing — this app handles it all. Let's walk through the complete workflow end to end."

**Transition:** Fade to ERPNext desk login screen.

---

### Scene: Login & Workspace Overview

| Element | Detail |
|---------|--------|
| **Visual** | User logs into ERPNext site as "Export Coordinator". Desk loads showing the **Handicraft Export Desk** workspace in the module navigation. |
| **Screenshot Callout** 🖼️ | **Callout A:** Handicraft Export Desk workspace card in the Awesome Bar dropdown |
| **Timestamp** | 0:25 |

**Narration:**
> "We start at the Handicraft Export Desk — the central workspace for this app. You'll find shortcuts to create new Visual Offers, Job Cards, and QC Logs. Number cards show your weekly shipping volume, active artisans, and pending job cards at a glance."

**On-Screen Text:** `3 Shortcuts · 3 Number Cards · 1 Chart`

**Transition:** Click on "Artisan Cluster" from the workspace links section.

---

## 🏘️ PHASE 1: MASTER DATA SETUP (0:45 – 3:00)

### 1A — Artisan Cluster (0:45 – 1:30)

| Element | Detail |
|--------|--------|
| **Visual** | Click **Handicraft Export Desk → Artisan Cluster → + Add Artisan Cluster** |
| **Screenshot Callout** 🖼️ | **Callout B:** The + Add button in the list view toolbar |
| **Timestamp** | 0:50 |

**On-Screen Text:** `Starting with the multitenancy layer — Artisan Clusters`

**Narration:**
> "We begin with the master data layer. First, we create an Artisan Cluster — a group of artisans organized by region or NGO affiliation. This is the multitenancy layer that lets us manage different artisan communities."

**Visual:** Fills in the form:
- **Cluster Name:** `Sahariya Wood Carvers`
- **Nodal Agency / NGO:** `SEWA Bharat`
- **Region:** `Rajasthan`
- **UDYAM Registration Status:** `Registered`

**Narration:**
> "We enter the cluster name — Sahariya Wood Carvers, based in Rajasthan, registered under the UDYAM scheme. The Nodal Agency field tracks the supporting NGO."

**Screenshot Callout** 🖼️ | **Callout C:** The completed Artisan Cluster form — note all 4 fields filled with the UDYAM dropdown open showing Pending / Registered / Exempt options

**Visual:** Clicks **Save**. Doc reloads clean.

**Transition:** Click on the "Artisan" link in the navigation.

---

### 1B — Create an Artisan (1:30 – 2:15)

| Element | Detail |
|--------|--------|
| **Visual** | Opens **Artisan → + Add Artisan** |
| **Screenshot Callout** 🖼️ | **Callout D:** Artisan form showing the Linked Supplier field — this is critical |
| **Timestamp** | 1:35 |

**On-Screen Text:** `Each artisan needs a linked Supplier for payment processing`

**Narration:**
> "Now we register a specific artisan within this cluster. Let's add Ram Vilas Sharma, a wood carver. We select his cluster, choose his primary craft category, and crucially — we link him to a standard ERPNext Supplier."

**Visual:** Fills in the form:
- **Artisan Name:** `Ram Vilas Sharma`
- **Artisan Cluster:** `Sahariya Wood Carvers`
- **Primary Craft:** `Wood Carving`
- **Linked Supplier:** `Rajasthan Rural Artisans Collective`
- **Contact Email:** `ram.sharma@email.in`
- **Contact Phone:** `+91-9876500001`
- **Address:** `Village Padampura, Sawai Madhopur, Rajasthan`

**Narration:**
> "This linked supplier is how the system will route automated payments. When we submit a Job Card later, a standard Purchase Invoice is generated against this supplier — no double-entry needed."

**Visual:** Clicks **Save**.

**Transition:** Navigate to Artisan Product Catalog Entry.

---

### 1C — Product Catalog with CBM (2:15 – 3:00)

| Element | Detail |
|--------|--------|
| **Visual** | Opens **Artisan Product Catalog Entry → + Add** |
| **Timestamp** | 2:20 |

**On-Screen Text:** `CBM = (L × W × H) / 1,000,000 — auto-calculated on save`

**Narration:**
> "Next, we create a Product Catalog Entry — this links a physical product to an artisan and captures its shipping dimensions for CBM calculation. CBM stands for Cubic Meter, and it's essential for container planning."

**Visual:** Fills in the form:
- **Product Name:** `Rosewood Elephant Sculpture - Ram Vilas`
- **Item Code:** Select `HDC-WD-001 (Rosewood Elephant Sculpture)` from standard Items
- **Artisan:** Select `Ram Vilas Sharma`
- **Production Time (Days):** `10`
- **Min Order Qty:** `5`
- **Length (cm):** `30`
- **Width (cm):** `12`
- **Height (cm):** `15`
- **Weight per Unit (kg):** `2.5`
- **Units per Carton:** `6`

**Screenshot Callout** 🖼️ | **Callout E:** The CBM Data section — all 5 dimension fields visible, highlight the read-only "Calculated CBM" field

**Visual:** Clicks **Save**. The **Calculated CBM** field auto-populates to `0.005400`.

**Narration:**
> "Notice the Calculated CBM field — `30 × 12 × 15 divided by 1 million` gives us `0.0054` CBM per unit. This will feed into our container planning later. Let's save."

**Screenshot Callout** 🖼️ | **Callout F:** Saved form with CBM value `0.005400` visible in read-only field (orange highlight)

**Transition:** Fade to the workspace shortcut for "New Visual Offer".

---

## 📄 PHASE 2: PRE-SALES — VISUAL OFFER SHEET (3:00 – 5:00)

### 2A — Creating an Offer (3:00 – 4:00)

| Element | Detail |
|--------|--------|
| **Visual** | Click **New Visual Offer** shortcut on the workspace → opens **Visual Offer Sheet** form |
| **Screenshot Callout** 🖼️ | **Callout G:** The "New Visual Offer" shortcut button on the Handicraft Export Desk workspace (icon: file-text) |
| **Timestamp** | 3:05 |

**On-Screen Text:** `Submittable DocType — Create quotes with photo-grid print format`

**Narration:**
> "Now we move to pre-sales. We click 'New Visual Offer' from the workspace shortcut — this opens a Visual Offer Sheet. This is a submittable document designed for international buyers who purchase based on photos, not just SKU codes."

**Visual:** Fills in the form:
- **Buyer:** `Artisan Global Imports, USA`
- **Buyer Email:** `buyer@artisanglobal.com`
- **Incoterm:** `FOB`
- **Valid Until:** (selects date 30 days from now)

**Narration:**
> "We set the buyer details and incoterm. FOB — Free on Board — means the buyer takes responsibility once goods are on the vessel."

**Visual:** Adds 3 rows in the **Offer Sheet Items** child table:
1. Product: `Rosewood Elephant Sculpture - Ram Vilas` → Qty: `50`, Price: `$45.00` → Amount auto-calculates to `$2,250.00`
2. Product: `Brass Dancing Lady - Ghulam` → Qty: `30`, Price: `$120.00` → Amount: `$3,600.00`
3. Product: `Blue Pottery Bowl Set - Lakshmi` → Qty: `100`, Price: `$18.50` → Amount: `$1,850.00`

**Screenshot Callout** 🖼️ | **Callout H:** The Offer Sheet Items child table with 3 rows — note the auto-fetched Product Name and Artisan fields from the catalog entry

**Narration:**
> "We add products from our catalog. Each row links to a catalog entry — the product name and artisan are fetched automatically. The total amount updates to $7,700."

**Visual:** Clicks **Save**, then **Submit**.

---

### 2B — Visual Offer Print Format (4:00 – 4:40)

| Element | Detail |
|--------|--------|
| **Visual** | After submission, clicks **Print → Visual Offer Sheet** |
| **Screenshot Callout** 🖼️ | **Callout I:** The print format selector dropdown with "Visual Offer Sheet" selected |
| **Timestamp** | 4:05 |

**Narration:**
> "After submission, we can print the offer. The Visual Offer Sheet has a custom Jinja print format — let's look at it."

**Visual:** PDF preview opens showing the photo-grid layout (landscape A4):
- Orange header: "Visual Offer Sheet" with offer name, date, valid until
- Buyer meta bar showing: Buyer name, Email, Incoterm, Total Amount
- 3-column grid of product cards, each with: Image area, product name, dimensions, MOQ, qty, unit price, subtotal

**Screenshot Callout** 🖼️ | **Callout J:** Full-page screenshot of the printed Visual Offer Sheet — highlight the 3-column grid layout, the orange #e67e22 branding, the image placeholders, and the meta bar

**Narration:**
> "This is the photo-grid print format — products displayed in a three-column CSS grid. Each card shows the product image, dimensions, minimum order quantity, and quoted price. This is the key feature for handicraft exports — buyers see the product, not just a SKU number."

**On-Screen Text:** `3-column photo grid · A4 landscape · Custom Jinja template`

**Transition:** Back to the submitted Offer Sheet form.

---

### 2C — Create Export Order Button (4:40 – 5:00)

| Element | Detail |
|--------|--------|
| **Visual** | On the submitted Offer Sheet, hovers over **Create Export Order** button in the toolbar |
| **Screenshot Callout** 🖼️ | **Callout K:** The "Create Export Order" custom button in the form toolbar (visible only when docstatus = 1) |
| **Timestamp** | 4:45 |

**Narration:**
> "On a submitted offer, there's a 'Create Export Order' button. This calls a backend API that creates a draft Export Order, pulling the buyer info forward."

**Visual:** Clicks **Create Export Order** → Frappe loads the new Export Order form with buyer country and incoterm pre-filled.

**Narration:**
> "The new Export Order opens with the buyer details carried over. Now let's complete the export order with shipping details."

**Transition:** Zooms into the Export Order form.

---

## 🚢 PHASE 3: EXPORT ORDER & CBM PLANNING (5:00 – 7:30)

### 3A — Export Order Details (5:00 – 5:45)

| Element | Detail |
|--------|--------|
| **Visual** | Opens a pre-existing Export Order (or the newly created one) — form visible |
| **Screenshot Callout** 🖼️ | **Callout L:** Export Order form header showing all key fields — Buyer Country, Incoterm, Port, COO Status |
| **Timestamp** | 5:05 |

**On-Screen Text:** `Submittable · Auto-calculates Total CBM and Container Estimate`

**Narration:**
> "The Export Order is the core shipping document. Let's fill in the details for our USA order."

**Visual:** Fills in / shows:
- **Linked Sales Order:** (optional — can link to standard ERPNext Sales Order)
- **Buyer Country:** `USA`
- **Incoterm:** `FOB`
- **Port of Discharge:** `Newark, NJ`
- **Certificate of Origin Status:** `Applied`
- **Estimated Ship Date:** (20 days from now)

**Narration:**
> "We set the destination, incoterm, and document status. The Certificate of Origin tracks whether we've applied or received it — critical for customs clearance."

**Transition:** Scroll down to the Export Packing List child table.

---

### 3B — Packing List & CBM Calculation (5:45 – 7:00)

| Element | Detail |
|--------|--------|
| **Visual** | Scrolls to **Export Packing List** section, opens as a grid |
| **Screenshot Callout** 🖼️ | **Callout M:** The Export Packing List child table with multiple carton rows visible — highlight the CBM column, the Total CBM read-only field below, and the Container Estimate field |
| **Timestamp** | 5:50 |

**On-Screen Text:** `Sum of carton CBM → Container Estimate: LCL / 20ft FCL / 40ft FCL`

**Narration:**
> "Here's where the CBM magic happens. We add carton-level packing details — each row is a carton with its item, quantity, weights, and CBM. Let's add our shipments."

**Visual:** Adds 11 rows to the Export Packing List table (use existing demo data or add quickly):

| Carton # | Item | Qty | Net Wt | Gross Wt | CBM |
|----------|------|:---:|:------:|:--------:|:---:|
| CTN-001 | HDC-WD-001 | 12 | 28.0 | 30.5 | 0.054 |
| CTN-002 | HDC-WD-001 | 12 | 28.0 | 30.5 | 0.054 |
| CTN-003 | HDC-WD-001 | 12 | 28.0 | 30.5 | 0.054 |
| CTN-004 | HDC-WD-001 | 14 | 32.0 | 35.0 | 0.063 |
| CTN-005 | HDC-MT-001 | 6 | 16.0 | 18.0 | 0.084 |
| CTN-006-009 | HDC-MT-001 | (4 more cartons × 6 pcs, same weights) |
| CTN-010-011 | HDC-PT-001 | (2 cartons × 50 pcs, each 0.135 CBM) |

**Screenshot Callout** 🖼️ | **Callout N:** Mouse hover on the `total_cbm` field showing `0.9450` — callout text: "Auto-calculated on save via before_save hook"

**Visual:** Clicks **Save**. Two fields update:
- **Total CBM:** `0.9450` (sum of all carton CBM values)
- **Container Estimate:** `LCL`

**Narration:**
> "On save, the system runs a before_save hook that sums all carton CBM values into Total CBM — here, 0.945 CBM. Then it applies the container logic: under 15 CBM means LCL — Less than Container Load. If this were between 15 and 33 CBM, it would suggest a 20-foot full container. Over 33, a 40-footer."

**On-Screen Text:** `CBM < 15 → LCL | 15-33 → 20ft FCL | ≥ 33 → 40ft FCL`

**Transition:** Click **Submit** on the Export Order.

---

### 3C — Print Commercial Invoice & Packing List (7:00 – 7:30)

| Element | Detail |
|--------|--------|
| **Visual** | Export Order submitted → Clicks **Print → Commercial Invoice - Export** |
| **Timestamp** | 7:05 |

**Narration:**
> "Once submitted, we can generate the active documents. Let's look at the Commercial Invoice."

**Screenshot Callout** 🖼️ | **Printout O:** The Commercial Invoice - Export print format — show the header with COO status badge, the table with HS Code column populated from Item master, and the totals at bottom

**Narration:**
> "The Commercial Invoice pulls HS Codes from the Item master, shows the COO status with color-coded badges, and summarizes the packing list with totals."

**Visual:** Clicks **Print → Packing List**.

**Screenshot Callout** 🖼️ | **Printout P:** The Packing List print format — show the grouped totals for Net Weight, Gross Weight, and CBM at the bottom of the table

**Narration:**
> "The Packing List gives a clean, professional carton-by-carton breakdown with totals — perfect for customs documentation."

**Transition:** Back to workspace, click "New Job Card" shortcut.

---

## 🛠️ PHASE 4: SUBCONTRACTING & JOB CARDS (7:30 – 9:30)

### 4A — Create Artisan Job Card (7:30 – 8:30)

| Element | Detail |
|--------|--------|
| **Visual** | Click **New Job Card** shortcut → opens **Artisan Job Card** form |
| **Screenshot Callout** 🖼️ | **Callout Q:** The new Job Card form — all key fields visible |
| **Timestamp** | 7:35 |

**On-Screen Text:** `Submittable · On submit: auto-generates Purchase Invoice for piece-rate payment`

**Narration:**
> "Now we move to subcontracting. We create an Artisan Job Card — this is the document that tracks work assigned to an artisan, the raw materials they receive, and ultimately triggers their payment."

**Visual:** Fills in:
- **Export Order:** Select `EXPORD-2026-00001` (USA order)
- **Artisan:** Select `Ram Vilas Sharma`
- **Piece Rate (INR):** `450.00`
- **Qty Ordered:** `50`
- **Qty Received:** (leave at 0 for now)
- **Qty Rejected:** (leave at 0)

**Narration:**
> "We link this job card to our USA export order, select Ram Vilas at a piece rate of 450 rupees per piece. We've ordered 50 pieces but haven't received them yet."

**Visual:** Scrolls to **Raw Materials Issued** child table → adds rows:
1. **Material Item:** `RM-WD-001 (Wood Block - Teak)`, **Qty:** `2.5`, **UOM:** `Kg`
2. **Material Item:** `RM-WD-003 (Varnish)`, **Qty:** `1.0`, **UOM:** `Ltr`

**Screenshot Callout** 🖼️ | **Callout R:** The Raw Materials Issued child table with 2 material rows — callout text: "Track materials given to artisan for cost analysis"

**Narration:**
> "We can also log raw materials issued — 2.5 kg of teak wood blocks and 1 liter of varnish. This helps with cost tracking per job."

**Visual:** Clicks **Save** (draft).

**Transition:** Job card form remains open.

---

### 4B — Receive Goods & Submit (8:30 – 9:00)

| Element | Detail |
|--------|--------|
| **Visual** | Edits the saved Job Card — updates **Qty Received** to `50`, **Qty Rejected** to `2` |
| **Timestamp** | 8:35 |

**Narration:**
> "A week later, the artisan delivers the finished pieces. We update the quantities — 50 received, 2 rejected due to minor surface imperfections."

**Visual:** Clicks **Submit**.

**Screenshot Callout** 🖼️ | **Callout S:** The submit confirmation — system message: "Purchase Invoice PI-2026-00001 created and submitted."

**Narration:**
> "When we submit, two things happen. First, the system validates that qty_received is greater than 0. Then it calls the `generate_artisan_invoice` API, which creates and submits a standard ERPNext Purchase Invoice."

**On-Screen Text:** `48 approved pieces × ₹450 = ₹21,600 Purchase Invoice created automatically`

**Visual:** Opens the created Purchase Invoice via the message link → shows:
- **Supplier:** `Rajasthan Rural Artisans Collective`
- **Item:** `Job Work - AJC-2026-00001`
- **Qty:** `48` (50 received − 2 rejected)
- **Rate:** `₹450.00`
- **Amount:** `₹21,600.00`

**Screenshot Callout** 🖼️ | **Callout T:** The generated Purchase Invoice — highlight the item row showing 48 × ₹450 = ₹21,600, and the custom field linking back to the Job Card

**Narration:**
> "Notice: the system correctly uses 48 pieces — 50 received minus 2 rejected — at 450 rupees each, totaling 21,600 rupees. This is a standard Purchase Invoice, so all your existing accounting workflows, tax configurations, and payment entries work seamlessly."

**Transition:** Navigate to Batch Quality Record.

---

### 4C — Cancel a Job Card (9:00 – 9:30)

| Element | Detail |
|--------|--------|
| **Visual** | Opens the submitted Job Card → clicks **Cancel** |
| **Timestamp** | 9:05 |

**Narration:**
> "If needed, canceling the Job Card automatically cancels the linked Purchase Invoice — the system finds it and cancels it too."

**Visual:** Shows the Purchase Invoice now showing "Cancelled" status.

**Narration:**
> "This ensures your financial records stay consistent. Let's move on to Quality Control."

**Transition:** Fade to Batch Quality Record form.

---

## 🔍 PHASE 5: QUALITY CONTROL (9:30 – 10:30)

### Scene: Batch Quality Record

| Element | Detail |
|--------|--------|
| **Visual** | Click **Log QC** shortcut → opens **Batch Quality Record** |
| **Screenshot Callout** 🖼️ | **Callout U:** The Batch Quality Record form — full form with all quantity fields visible |
| **Timestamp** | 9:35 |

**On-Screen Text:** `Auto-fetches Artisan and Export Order from the selected Job Card`

**Narration:**
> "Now we log quality control. We click the 'Log QC' shortcut. The form fetches the artisan and export order automatically from the selected job card."

**Visual:** Fills in:
- **Job Card:** Select submitted Job Card
  - **Artisan:** Auto-fetched to `Ram Vilas Sharma`
  - **Export Order:** Auto-fetched to export order
- **QC Date:** Today (default)
- **Inspector:** Select current user
- **Qty Checked:** `50`
- **Qty Passed:** `48`
- **Qty Rework:** `0`
- **Qty Failed:** `2`
- **QC Status:** `Pass`
- **Defect Type:** `Minor surface scratches on 2 pieces`
- **Inspector Notes:** `Overall quality is excellent. 48 pieces approved for shipment.`

**Screenshot Callout** 🖼️ | **Callout V:** The Quantity Inspection section with all 4 qty fields — qty_passed + qty_rework + qty_failed should equal qty_checked

**Narration:**
> "We log 50 pieces checked, 48 passed, 2 failed — the status is 'Pass' since failures are within tolerance. The 'Rework' and 'Fail' statuses trigger system notifications to the Artisan Liaison."

**Visual:** Clicks **Save**. No notification trigger since status is "Pass".

**Transition:** Navigate to the Reports section.

---

## 📊 PHASE 6: REPORTS & WORKSPACE (10:30 – 11:30)

### 6A — Document Readiness Dashboard (10:30 – 10:55)

| Element | Detail |
|--------|--------|
| **Visual** | Opens **Document Readiness Dashboard** from workspace links |
| **Screenshot Callout** 🖼️ | **Callout W:** The Document Readiness Dashboard report showing export orders with readiness flags |
| **Timestamp** | 10:35 |

**Narration:**
> "Let's look at our reports. The Document Readiness Dashboard flags export orders where the Certificate of Origin hasn't been issued within 3 days of the estimated ship date."

**Visual:** Report shows columns: Export Order, Buyer Country, Estimated Ship Date, COO Status, Readiness Flag (⚠ Missing Documents or OK), Total CBM, Container Estimate.

**Screenshot Callout** 🖼️ | **Callout X:** A row flagged with "⚠ Missing Documents" — callout text: "Automatic email alert sent to Export Coordinator"

**Narration:**
> "If an order is shipping in 3 days and the COO isn't issued, the readiness flag turns red and the daily scheduled task sends an alert email to the Export Coordinator."

---

### 6B — Cluster Output Capacity (10:55 – 11:10)

| Element | Detail |
|--------|--------|
| **Visual** | Opens **Cluster Output Capacity** report |
| **Screenshot Callout** 🖼️ | **Callout Y:** The Cluster Output Capacity report grouped by cluster |
| **Timestamp** | 11:00 |

**Narration:**
> "The Cluster Output Capacity report groups active artisans by cluster and aggregates their production capacity — useful for NGO buyers or government tenders assessing cluster capability."

---

### 6C — Artisan Yield & Wastage (11:10 – 11:30)

| Element | Detail |
|--------|--------|
| **Visual** | Opens **Artisan Yield & Wastage** script report |
| **Screenshot Callout** 🖼️ | **Callout Z:** The Yield & Wastage report comparing ordered vs received vs rejected across job cards |
| **Timestamp** | 11:15 |

**Narration:**
> "Finally, the Artisan Yield & Wastage report compares ordered versus received versus rejected quantities across all Job Cards — helping identify which artisans consistently deliver quality work, and where wastage is high."

**Transition:** Fade to the workspace dashboard.

---

## 🏁 OUTRO (11:30 – 12:00)

### Scene: Full Workspace Recap

| Element | Detail |
|--------|--------|
| **Visual** | Returns to **Handicraft Export Desk** workspace |
| **Timestamp** | 11:35 |

**Screenshot Callout** 🖼️ | **Final Callout:** Full-page screenshot of the complete workspace with callout labels:
1️⃣ "Shortcuts: New Visual Offer, New Job Card, Log QC"
2️⃣ "Number Cards: Total CBM, Active Artisans, Pending Jobs"
3️⃣ "Chart: Artisan Yield bar chart"
4️⃣ "Card Links: Master Data, Pre-Sales, Export, Subcontracting, QC, Reports"

**Narration:**
> "That's the full cycle — from creating an artisan cluster in rural India, to a photo-rich offer sheet for a US buyer, to container planning with CBM calculations, to artisan job cards that automatically generate Purchase Invoices on submission, to quality control and readiness reporting."

**On-Screen Text (animating in):**
```
🏘️ Clusters → 👨‍🎨 Artisans → 📦 Catalog → 📄 Offer Sheet
→ 🚢 Export Order → 🛠️ Job Card → 💳 Auto Invoice → 🔍 QC
```

**Narration:**
> "The Handicraft Export app layers on top of standard ERPNext — it doesn't replace your accounting or inventory modules. It extends them with export-specific workflows while keeping everything integrated."

**Closing Screen:**
- **GitHub:** `github.com/Pasha1234565/handicraft_export.git`
- **Install:** `bench get-app https://github.com/Pasha1234565/handicraft_export.git`
- **Contact:** info@example.com
- **License:** MIT
- Logo/icon: 🎨 (orange, `octicon octicon-package`)

**Narration:**
> "Thank you for watching. The app is open source under MIT license — install it on your ERPNext site and start streamlining your handicraft export operations today."

*End of Script*

---

## APPENDIX: Screenshot Callout Index

| Callout | Screen | Key Focus | Timestamp |
|---------|--------|-----------|-----------|
| A | Workspace nav | Handicraft Export Desk in Awesome Bar | 0:25 |
| B | Artisan Cluster list | + Add button | 0:50 |
| C | Artisan Cluster form | All 4 fields + UDYAM dropdown | 1:10 |
| D | Artisan form | Linked Supplier field highlight | 1:35 |
| E | Catalog Entry form | CBM Data section with dimension fields | 2:30 |
| F | Catalog Entry saved | Calculated CBM read-only value | 2:50 |
| G | Workspace | "New Visual Offer" shortcut button | 3:05 |
| H | Offer Sheet Items child table | 3 rows with auto-fetched fields | 3:40 |
| I | Print dropdown | "Visual Offer Sheet" print format selected | 4:05 |
| J | Printed PDF | Full photo-grid layout, 3 columns | 4:15 |
| K | Submit toolbar | "Create Export Order" custom button | 4:45 |
| L | Export Order form | Header fields — country, incoterm, port, COO | 5:05 |
| M | Packing List table | Multiple carton rows, Total CBM field | 5:50 |
| N | Total CBM field | Mouse hover showing value 0.9450 | 6:30 |
| O | Commercial Invoice print | HS Codes, COO badge, packing summary | 7:05 |
| P | Packing List print | Grouped totals for Net/Gross/CBM | 7:20 |
| Q | Job Card form | All fields visible | 7:35 |
| R | Raw Materials Issued table | 2 material rows with Items + Qty + UOM | 8:10 |
| S | Submit confirmation | "Purchase Invoice created" message | 8:50 |
| T | Purchase Invoice form | Item row: 48 qty × ₹450 rate = ₹21,600 | 9:00 |
| U | Batch QC form | Full form with all quantity fields | 9:35 |
| V | Quantity Inspection section | qty_passed + qty_rework + qty_failed | 10:00 |
| W | Document Readiness Dashboard | Report with readiness flags | 10:35 |
| X | Flagged row | "⚠ Missing Documents" in red | 10:45 |
| Y | Cluster Output Capacity | Grouped by cluster with aggregated days | 11:00 |
| Z | Artisan Yield & Wastage | Ordered vs Received vs Rejected bars | 11:15 |
| Final | Workspace full page | Annotated with 4 callout bubbles | 11:35 |

---

## Equipment & Production Notes

| Item | Recommendation |
|------|---------------|
| **Screen Recorder** | OBS Studio or ScreenFlow — 1920×1080 at 30fps |
| **Annotations** | Use callout circles with zoom transitions (1.2x scale) when highlighting fields |
| **Mouse Cursor** | Use a highlighted cursor plugin (e.g., MouseFocus for OBS) |
| **Audio** | Lavalier mic for narration. Keep pace at ~150 words/min |
| **Transitions** | Use smooth fades (0.3s) between scenes. Use zoom (1.3x) when entering form fields |
| **Duration Target** | 10-12 minutes total. Each phase should be 1-2 minutes |
| **Music** | Low-volume ambient background (royalty-free) — fade out during narration |
| **Closed Captions** | Burn in English subtitles for accessibility |
| **Thumbnail** | Workspace screenshot with title overlay: "Handicraft Export — Full Walkthrough" |
