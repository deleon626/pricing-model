# Product Requirements Document (PRD)

## Video‑Project Pricing Calculator

---

### 1. Purpose

Create a self‑service calculator that converts a client brief into a defensible cost estimate—both a range and a recommended price—for one‑day video shoots handled by Lapis Visuals (or any similar agency). The tool must:
1. Standardise quoting
2. Surface the variables that drive budget
3. Let producers tweak assumptions without breaking the underlying model

---

### 2. Key Outcomes & Success Metrics

| Goal                  | KPI                                   | Target @ 90 days         |
|-----------------------|---------------------------------------|--------------------------|
| Cut average quoting time | Time from brief → draft quote         | ≤ 15 min                 |
| Reduce price disputes | % quotes re‑negotiated > ±10 %        | < 10 %                   |
| Capture cost drivers  | % quotes completed with full questionnaire | ≥ 95 %               |
| Data for benchmarking | # projects auto‑logged to DB           | 100 %                    |

---

### 3. Primary Users & Jobs‑to‑Be‑Done

| User            | JTBD                                                                 |
|-----------------|----------------------------------------------------------------------|
| Account Manager | Produce a quick yet defensible ball‑park during the first call.      |
| Producer / PM   | Refine all line items, add bespoke extras, generate final PDF.       |
| Finance         | Check margin, adjust contingency, push to invoicing & bookkeeping.   |
| Client (optional) | Play with levers (e.g., change location) to see budget impact.     |

---

### 4. Input Model

#### A. Questionnaire (client‑facing)
- Final video length (mins)
- # of deliverables
- Distribution channel(s) ✔︎ IG/TikTok ✔︎ YouTube …
- Format / genre (commercial, docu, event, etc.)
- Special requirements (SFX, motion GFX, green screen)
- Concept summary (free text)
- Ideal shoot date & final delivery date
- Budget range (optional)

#### B. Internal Production Variables

| Variable            | Default         | Options / Range                                              |
|---------------------|----------------|--------------------------------------------------------------|
| Shooting days       | 1              | 0.5 increments                                               |
| Crew size           | auto from template | manual override                                         |
| Location type       | none           | Studio (1.5 M) • Styled Home (6 M) • Rooftop Café (4.5 M)    |
| Talent count & usage| 1 lead, social‑only | any integer; +10–30 % agency markup toggle           |
| Props & set design  | 2 M–5 M        | “basic / custom / elaborate” presets                         |
| Footage volume      | “standard”     | slider: affects Editing, Color, SFX multipliers              |
| Contingency %       | 10 %           | 0–20 %                                                       |

---

### 5. Calculation Logic (single‑day baseline)

```
Total =  Σ Pre‑Prod  +  Σ Production  +  Σ Post‑Prod
       + Admin/Overhead (toggle)      + Contingency
```

| Cost Block         | Driver                | Formula                        | Defaults         |
|--------------------|----------------------|--------------------------------|------------------|
| Scriptwriting      | concept complexity   | base × complexity_factor       | 1 M–3 M          |
| Storyboard         | deliverables         | base × #videos                 | 1 M–2 M          |
| Location scout & permits | location type  | fixed lookup                   | see §4B          |
| Crew roles         | crew size scaler     | rate_per_role × shooting_days  | table from doc   |
| Equipment          | camera tier          | daily_rate × shooting_days     | 5 M/10 M         |
| Post‑production    | minutes_of_final × complexity | multipliers for Editing, Color, SFX | from doc |
| Producer fee       | toggle               | subtotal × 5–10 %              | 3 M–6 M          |
| Contingency        | risk appetite        | subtotal × %                   | 10 % default     |

> Rates stored in a version‑controlled JSON so producers can update without code push.

---

### 6. Functional Requirements

1. Interactive Form—Guided flow using the questionnaire, auto‑saving as draft.
2. Real‑time Quote Panel—Shows Low, High, and Recommended (median + margin).
3. Preset Templates—Commercial, Social Snippet, Documentary, etc. (pre‑fills variables).
4. Manual Overrides—Any line item editable; change logs retained.
5. Currency Handling—Rupiah formatting with digit‑grouping (e.g., Rp 5.000.000).
6. Version Stamp—Every quote tagged with cost‑table version & user ID.
7. Export—Branded PDF and XLSX; push to project‑management and invoicing APIs.
8. Permissions—View‑only for Juniors; edit for Producers; finance can lock final.
9. Analytics Dashboard—Average project margin, cost outliers, win/loss vs. quote.

---

### 8. Edge Cases & Rules

- Multi‑day shoots multiply daily roles but keep one‑off pre‑prod fees.
- Multiple deliverables: storyboard & edit scale linearly; insurance/permits don’t.
- Projects < Rp 20 M auto‑hide Admin/Overhead block (per note).
- If client budget < Low estimate, tool suggests scope reductions (reduce crew, etc.).
- Tax handling left to Finance; not included in calculator beyond displaying a note.

---

### 9. Acceptance Criteria (sample)

| ID    | Scenario                              | Expected                                                        |
|-------|---------------------------------------|-----------------------------------------------------------------|
| AC‑1  | Complete questionnaire with defaults  | Quote shows Rp 58 M – Rp 118 M (matches doc baseline)           |
| AC‑2  | Change shooting days from 1→2         | All per‑day roles & equipment double; one‑off items unchanged   |
| AC‑3  | Toggle “Producer Fee” off             | Admin/Overhead block disappears; total recalculates instantly   |
| AC‑4  | Export PDF                            | File matches on‑screen numbers, includes agency branding & version id |

---

### 10. Milestones

| Phase      | Output                                 | ETA    |
|------------|----------------------------------------|--------|
| Discovery  | finalised variables, UI wireframes     | Day 7  |
| Alpha      | core engine + bare form                | Day 21 |
| Beta       | full UI, PDF export, role auth         | Day 35 |
| Launch     | production deploy + training deck      | Day 45 |

---

### 11. Open Questions

1. Confirm if overhead always excluded for projects < Rp 20 M.
2. Decide margin formula for “Recommended” (e.g., median + fixed 12 %).
3. Required integrations: Xero? internal PM? CRM?
4. Handling of multi‑currency projects for cross‑border shoots.

---

*Document owner: Product Lead (Pricing Tools)*  
*Last updated: 22 Apr 2025*