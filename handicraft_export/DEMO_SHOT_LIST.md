# Handicraft Export — Demo Video Shots List

**📋 For the video editor / screen recorder.** Each row = one shot/scene.
**Duration:** ~12 min total
**Tool:** OBS Studio (free) or any screen recorder at 1920×1080, 30fps

---

## How to Record

1. Open your ERPNext site as **Export Coordinator** user (with `Export Coordinator` + `Artisan Liaison` roles)
2. Run demo data first: `bench --site mysite.local3 execute handicraft_export.handicraft.demo_data.execute`
3. Record each shot below following the navigation instructions
4. Narration is provided for each shot

---

## SHOT LIST

### 🎬 INTRO (0:00 – 0:45)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 001 | 0:00 | — | **Title Card** — Animated: *"Handicraft Export — From Cluster to Shipment"* Orange #e67e22 branding. Subtitle: Frappe/ERPNext v15 | "Welcome to Handicraft Export — a Frappe ERPNext app designed for handicraft exporters..." |
| 002 | 0:15 | Login screen | **Login page** — URL bar visible: `mysite.local3:8000/login` | "From registering artisan clusters in rural India..." |
| 003 | 0:25 | Log in → Desk loads | **Workspace** — Handicraft Export Desk as selected module. Show shortcuts: New Visual Offer, New Job Card, Log QC. Show number cards: Total CBM, Active Artisans, Pending Job Cards | "...to creating photo-rich visual offer sheets for international buyers..." |

---

### 🏘️ PHASE 1: MASTER DATA (0:45 – 3:00)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 101 | 0:45 | **Desk → Artisan Cluster → + Add** | **Artisan Cluster form** — Fields: Cluster Name, Nodal Agency / NGO, Region, UDYAM Registration Status | "We begin with the master data layer. First, we create an Artisan Cluster..." |
| 102 | 1:00 | Fill cluster form | **Form filled:** Cluster Name: `Sahariya Wood Carvers`, Nodal Agency: `SEWA Bharat`, Region: `Rajasthan`, UDYAM: `Registered` | "Sahariya Wood Carvers, based in Rajasthan, registered under UDYAM..." |
| 103 | 1:10 | Click **Save** | **Saved cluster** — clean form view, cluster name now a link | *(pause)* |
| 104 | 1:20 | **Desk → Artisan → + Add** | **Artisan form** — Fields: Artisan Name, Artisan Cluster, Primary Craft, Linked Supplier, Contact Email/Phone, Address | "Now we register a specific artisan within this cluster..." |
| 105 | 1:35 | Fill artisan form | **Form filled:** Name: `Ram Vilas Sharma`, Cluster: `Sahariya Wood Carvers`, Craft: `Wood Carving`, Supplier: `Rajasthan Rural Artisans Collective` | "Crucially, we link him to a standard ERPNext Supplier..." |
| 106 | 1:55 | Click **Save** | **Saved artisan** — name shown as `ART-Ram Vilas Sharma-00001` | "This linked supplier is how the system will route automated payments..." |
| 107 | 2:15 | **Desk → Artisan Product Catalog Entry → + Add** | **Catalog Entry form** — Fields: Product Name, Item Code (Link), Artisan, Images child table, Production Time, MOQ, CBM Data section (L/W/H, Weight, Units/Carton), Calculated CBM (read-only) | "Next, we create a Product Catalog Entry — this links a physical product to an artisan..." |
| 108 | 2:30 | Fill catalog form | **Form filled:** Product: `Rosewood Elephant Sculpture - Ram Vilas`, Item: `HDC-WD-001`, Artisan: `Ram Vilas Sharma`, L: `30` cm, W: `12` cm, H: `15` cm, Weight: `2.5` kg, Units/Carton: `6` | "CBM stands for Cubic Meter — 30 × 12 × 15 divided by 1 million..." |
| 109 | 2:50 | Click **Save** | **Saved with Calculated CBM** = `0.005400` (read-only field auto-populated) | "...gives us 0.0054 CBM per unit. This feeds into container planning later." |

---

### 📄 PHASE 2: PRE-SALES — OFFER SHEET (3:00 – 5:00)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 201 | 3:00 | **Workspace → "New Visual Offer" shortcut** | **Visual Offer Sheet form** — Fields: Buyer, Buyer Email, Incoterm, Valid Until, Amended From, Offer Sheet Items child table, Total Amount (read-only) | "Now we move to pre-sales. Click 'New Visual Offer'..." |
| 202 | 3:15 | Fill header fields | **Header filled:** Buyer: `Artisan Global Imports, USA`, Email: `buyer@artisanglobal.com`, Incoterm: `FOB`, Valid Until: *(date 30 days out)* | "We set the buyer details and incoterm — FOB, Free on Board..." |
| 203 | 3:30 | Add **3 Offer Sheet Items** | **Child table filled:** Row 1: Rosewood Elephant Sculpture, 50 pcs × $45.00 = $2,250. Row 2: Brass Dancing Lady, 30 pcs × $120.00 = $3,600. Row 3: Blue Pottery Bowl Set, 100 pcs × $18.50 = $1,850 | "We add products — each row links to a catalog entry. Product name and artisan are fetched automatically." |
| 204 | 3:50 | Click **Save**, then **Submit** | **Submitted offer** — docstatus = 1, toolbar shows Submit/Cancel/Amend buttons grayed out, "Create Export Order" button appears | *(transition pause)* |
| 205 | 4:00 | **Print → Visual Offer Sheet** | **PDF preview** — Landscape A4. Orange header. 3-column grid of product cards. Each card: image area, product name, dimensions, MOQ, qty, unit price, subtotal | "This is the photo-grid print format — 3-column CSS grid..." |
| 206 | 4:30 | Scroll through PDF | **PDF continued** — all products visible in grid | "...buyers see the product, not just a SKU number." |
| 207 | 4:45 | Back to submitted offer → Click **"Create Export Order"** | **New Export Order opens** — buyer country + incoterm pre-filled from offer sheet. Message: "Export Order EXPORD-2026-00001 created." | "The 'Create Export Order' button calls a backend API that creates a draft Export Order..." |

---

### 🚢 PHASE 3: EXPORT ORDER & CBM (5:00 – 7:30)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 301 | 5:00 | **Export Order form** (pre-existing or newly created) | **Export Order header** — Fields: Linked Sales Order, Buyer Country, Incoterm, Port of Discharge, COO Status, Est. Ship Date, Amended From | "The Export Order is the core shipping document..." |
| 302 | 5:20 | Fill export details | **Form filled:** Country: `USA`, Incoterm: `FOB`, Port: `Newark, NJ`, COO: `Applied`, Ship Date: *(20 days from now)* | "We set the destination, incoterm, and document status..." |
| 303 | 5:45 | Scroll to **Export Packing List** child table | **Packing List table** — Columns: Carton #, Item, Qty Inside, Net Weight, Gross Weight, CBM | "Here's where the CBM magic happens..." |
| 304 | 6:00 | Add 11 carton rows | **Table filled with data** — 5 CTN of Rosewood Elephants, 5 CTN of Brass Ladies, 2 CTN of Blue Pottery | *(record as you add rows — or show pre-filled demo data)* |
| 305 | 6:25 | Click **Save** | **Auto-calculated fields update:** Total CBM = `0.9450`, Container Estimate = `LCL` | "On save, the before_save hook sums all carton CBM into Total CBM..." |
| 306 | 6:45 | Zoom on **Container Estimate** field | **Close-up of field** — value `LCL` visible | "Under 15 CBM → LCL. 15-33 → 20ft FCL. Over 33 → 40ft FCL." |
| 307 | 7:00 | Click **Submit** → **Print → Commercial Invoice - Export** | **PDF: Commercial Invoice** — Header with COO status badge (orange/ green). Table with HS Codes column, carton details, totals row at bottom | "The Commercial Invoice pulls HS Codes from the Item master..." |
| 308 | 7:15 | **Print → Packing List** | **PDF: Packing List** — Grouped totals for Net Weight, Gross Weight, CBM at table footer | "The Packing List gives a professional carton-by-carton breakdown..." |

---

### 🛠️ PHASE 4: SUBCONTRACTING & JOB CARDS (7:30 – 9:30)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 401 | 7:30 | **Workspace → "New Job Card" shortcut** | **Artisan Job Card form** — Fields: Export Order, Artisan, Piece Rate (INR), Amended From, Qty Ordered, Qty Received, Qty Rejected, Raw Materials Issued child table | "Now we move to subcontracting. We create an Artisan Job Card..." |
| 402 | 7:50 | Fill job card fields | **Form filled:** Export Order: `EXPORD-2026-00001`, Artisan: `Ram Vilas Sharma`, Piece Rate: `₹450.00`, Qty Ordered: `50`, Qty Received: `0`, Qty Rejected: `0` | "We link this to our USA export order at 450 rupees per piece..." |
| 403 | 8:05 | Add **2 Raw Materials** rows | **Child table:** Row 1: `RM-WD-001` Wood Block - Teak, 2.5 Kg. Row 2: `RM-WD-003` Varnish, 1.0 Ltr | "We can also log raw materials issued — helps with cost tracking." |
| 404 | 8:20 | Click **Save** | **Saved draft** doc — Submit button visible | *(pause)* |
| 405 | 8:30 | Update **Qty Received** = 50, **Qty Rejected** = 2 → Click **Submit** | **Submit confirmation** — System message: *"Purchase Invoice PI-2026-00001 created and submitted."* | "On submit, the system calls generate_artisan_invoice() which creates a standard Purchase Invoice..." |
| 406 | 8:50 | Click message link to open Purchase Invoice | **Purchase Invoice** — Supplier: `Rajasthan Rural Artisans Collective`. Item: `Job Work - AJC-2026-00001`. Qty: `48`. Rate: `₹450.00`. Amount: `₹21,600.00` | "48 pieces — 50 received minus 2 rejected — at 450 rupees each, totaling ₹21,600..." |
| 407 | 9:10 | Return to Job Card → Click **Cancel** | **Cancelled Job Card** — system also cancels linked Purchase Invoice | "Cancel the Job Card and the linked Purchase Invoice is cancelled too." |

---

### 🔍 PHASE 5: QUALITY CONTROL (9:30 – 10:30)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 501 | 9:30 | **Workspace → "Log QC" shortcut** | **Batch Quality Record form** — Fields: Job Card, Artisan (fetched), Export Order (fetched), QC Date, Inspector, Qty Checked/Passed/Rework/Failed, QC Status, Defect Type, QC Photos, Inspector Notes | "Now we log quality control..." |
| 502 | 9:50 | Select Job Card → auto-fetch artisan & export order | **Artisan field** auto-populates to `Ram Vilas Sharma`. **Export Order** auto-populates | "...the form fetches the artisan and export order automatically." |
| 503 | 10:05 | Fill QC fields | **Form filled:** Qty Checked: `50`, Qty Passed: `48`, Qty Rework: `0`, Qty Failed: `2`, QC Status: `Pass`, Inspector Notes: "Overall quality excellent. 48 pieces approved." | "48 passed, 2 failed — status 'Pass'. Rework and Fail statuses trigger system notifications." |
| 504 | 10:20 | Click **Save** | **Saved QC record** — no notification triggered (status = Pass) | *(pause)* |

---

### 📊 PHASE 6: REPORTS (10:30 – 11:30)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 601 | 10:30 | **Desk → Document Readiness Dashboard** | **Report** — Columns: Export Order, Buyer Country, Est. Ship Date, COO Status, Readiness Flag (⚠ or OK), Total CBM, Container Estimate | "The Document Readiness Dashboard flags export orders where COO isn't issued within 3 days of shipment..." |
| 602 | 10:50 | Hover on a flagged row | **⚠ Missing Documents** row — red indicator visible | "...the daily scheduled task sends an alert email to the Export Coordinator." |
| 603 | 11:00 | **Desk → Cluster Output Capacity** | **Report** — Grouped by cluster: Artisan Cluster, Region, Active Artisans, Avg Production Time, Total Capacity, Unique Products | "The Cluster Output Capacity report groups active artisans by cluster..." |
| 604 | 11:15 | **Desk → Artisan Yield & Wastage** | **Script Report** — Bar chart or table comparing ordered vs received vs rejected across job cards | "The Artisan Yield & Wastage report helps identify which artisans consistently deliver quality work..." |

---

### 🏁 OUTRO (11:30 – 12:00)

| Shot | Time | Action / Navigation | Screen to Capture | Narration Cue |
|------|------|--------------------|-------------------|---------------|
| 701 | 11:30 | Return to **Handicraft Export Desk** | **Full workspace** — Annotated with callout bubbles: ① Shortcuts ② Number Cards ③ Chart ④ Card Sections | "That's the full cycle — from creating an artisan cluster in rural India..." |
| 702 | 11:45 | — | **On-screen animation:** Flow diagram: 🏘️ Clusters → 👨‍🎨 Artisans → 📦 Catalog → 📄 Offer Sheet → 🚢 Export Order → 🛠️ Job Card → 💳 Auto Invoice → 🔍 QC | "The Handicraft Export app layers on top of standard ERPNext..." |
| 703 | 11:55 | — | **Closing screen:** GitHub URL, install command, email, MIT license, orange icon | "Thank you for watching. Install it on your ERPNext site today." |

---

## Recording Tips for Each Phase

| Phase | Difficulty | Tips |
|-------|-----------|------|
| **Intro** | ⭐ | Record after everything else. Title card can be edited in post. |
| **Master Data** | ⭐⭐ | Have demo data pre-loaded. Show creating just 1 of each (not all 5 clusters) to save time. |
| **Offer Sheet** | ⭐⭐ | Record at 1.5x speed during data entry, slow down for submit + print preview. |
| **Export Order** | ⭐⭐⭐ | Packing list has 11 rows — use demo data to show pre-filled table. Focus on save → CBM update moment. |
| **Job Card** | ⭐⭐⭐ | Critical shot: the submit → Purchase Invoice auto-creation. Record this twice. |
| **QC** | ⭐ | Quick form fill. No surprises. |
| **Reports** | ⭐ | Simple scrolling through report data. |
| **Outro** | ⭐ | Use workspace screenshot + overlay text in post-production. |

## Post-Production Checklist

- [ ] Add callout circles/zooms on key fields (CBM, Container Estimate, Purchase Invoice amount)
- [ ] Burn in English subtitles / closed captions
- [ ] Import title card animation
- [ ] Add flow diagram animation at outro (Shot 702)
- [ ] Add background music (low volume, fade during narration)
- [ ] Export at 1920×1080, 30fps, H.264
- [ ] Upload to YouTube as Unlisted first, review with team, then make Public

## YouTube Upload Settings

| Field | Value |
|-------|-------|
| **Title** | Handicraft Export ERPNext App — Full Walkthrough Demo |
| **Description** | Complete walkthrough of the Handicraft Export Frappe/ERPNext v15 app. From artisan clusters and photo-rich visual offer sheets to CBM container planning and automated artisan payments. Open source — get it at github.com/Pasha1234565/handicraft_export.git |
| **Tags** | ERPNext, Frappe, Handicraft Export, CBM Calculator, Artisan Management, Export Readiness |
| **Category** | Science & Technology |
| **Visibility** | Unlisted → Public after review |
