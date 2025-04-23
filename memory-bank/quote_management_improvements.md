# Quote Management Improvements & Inconsistencies Plan

This document outlines a step-by-step plan to address inconsistencies and potential improvements identified in the quote management and customer association features of the Lapis Visuals Pricing Calculator.

## 1. Save vs. Update Quote Inconsistency

### Problem
- The "Save Current Quote" button always creates a new quote, even if the user is editing an existing one. This can lead to duplicate quotes and confusion.

### Solution
1. **Track Loaded Quote:**
   - Store the `quote_id` of the currently loaded quote in `st.session_state` (e.g., `st.session_state.loaded_quote_id`).
2. **Conditional Button:**
   - If a quote is loaded, show an "Update Quote" button instead of "Save Current Quote" in the Quote Builder tab.
   - If no quote is loaded, show "Save Current Quote" as before.
3. **Update Logic:**
   - When "Update Quote" is clicked, call `update_quote` with the loaded quote's ID and the current form data.
   - After updating, show a success message and clear `loaded_quote_id`.
4. **Reset State:**
   - Add a "Clear Loaded Quote" button to allow users to start a new quote from scratch.

---

## 2. Navigation After Loading a Quote

### Problem
- After loading a quote from the Customer Management tab, the user remains on that tab and must manually switch to the Quote Builder tab to view/edit the loaded quote.

### Solution
1. **Automatic Tab Switch:**
   - After a quote is loaded, programmatically set `st.session_state.active_tab = "Quote Builder"` and call `st.rerun()`.
   - This ensures the user is taken directly to the quote editing interface.

---

## 3. Distinguishing Saved vs. Live Quote Amounts

### Problem
- When a quote is loaded, the sidebar summary recalculates the quote using current rates, which may differ from the originally saved amounts.

### Solution
1. **Display Saved Amounts:**
   - In the Quote Builder tab, if a quote is loaded, display the originally saved amounts (low, high, recommended) alongside the live recalculated values.
   - Add a note explaining the difference (e.g., "Saved quote amounts reflect rates at the time of saving. Current summary uses latest rates.").

---

## 4. Customer ID Generation Robustness

### Problem
- Customer IDs are generated using `time.time()` and a UUID slice, which is robust but could be improved for uniqueness.

### Solution
1. **Use Full UUID:**
   - Change customer ID generation to use `uuid.uuid4().hex` for maximum uniqueness (e.g., `CUST-{uuid.uuid4().hex[:12].upper()}`).

---

## 5. Error Handling for File Operations

### Problem
- File operations (saving/loading JSON) could fail due to permissions or IO errors, but user feedback is limited.

### Solution
1. **Add Try/Except Blocks:**
   - Wrap file write operations in try/except blocks.
   - Display a user-friendly error message if saving fails.

---

## 6. Concurrency and Data Consistency (Long-Term)

### Problem
- File-based storage is not safe for concurrent users; simultaneous writes can cause data loss.

### Solution
1. **Short-Term:**
   - Warn users if the app is being used by multiple people at once.
2. **Long-Term:**
   - Migrate to a database (e.g., SQLite, PostgreSQL, or a cloud DB) for robust multi-user support.

---

## 7. State Persistence and User Experience

### Problem
- Unsaved changes in the quote builder are lost if the user navigates away without saving.

### Solution
1. **Warn on Unsaved Changes:**
   - Track if the form has unsaved changes and warn the user before switching tabs or customers.
2. **Auto-Save Drafts (Optional):**
   - Implement auto-save for in-progress quotes as drafts.

---

## 8. Documentation and User Guidance

### Problem
- Users may not understand the difference between saving, updating, and loading quotes.

### Solution
1. **Add Help Text:**
   - Add tooltips or help sections explaining the quote workflow.
2. **Update Documentation:**
   - Ensure the README and in-app documentation reflect the improved workflow.

---

## Implementation Order (Recommended)
1. Save vs. Update Quote logic
2. Navigation after loading a quote
3. Displaying saved vs. live quote amounts
4. Customer ID generation improvement
5. Error handling for file operations
6. Documentation/user guidance
7. State persistence/unsaved changes warning
8. Concurrency (long-term) 