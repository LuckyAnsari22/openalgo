# OpenAlgo Contribution Strategy — Getting PRs Merged

## Background & Lessons Learned

Your previous PRs (#1107, #1088, #1026) were rejected because they were **too large** (3,400+ additions across 29 files), had **merge conflicts** with `main`, and lacked **prior discussion** with maintainers. Meanwhile, your **PR #1077** (Google-style docstrings for utils module) **was successfully merged** — proving that small, focused, well-scoped PRs work.

The maintainers explicitly said:
> *"Start with a single, small test file for one service... smaller, incremental PRs would be much easier to review and merge!"*

---

## Golden Rules for Every PR

1. **Sync your fork** before creating any branch (`git fetch upstream && git rebase upstream/main`)
2. **One PR = one concern** — never mix features, fixes, and docs
3. **Link to an existing issue** with `Closes #NNN` or open an issue first for new ideas
4. **Use Conventional Commits**: `fix:`, `feat:`, `docs:`, `test:`, `refactor:`
5. **Keep PRs under ~200 lines changed** and touching ≤3 files
6. **Test locally** and ensure no lint/build errors

---

## Phased Contribution Roadmap

### 🟢 Phase 1: Quick Wins (Days 1-3) — Resume the Streak

These are **maintainer-created `good first issue` tasks** that are explicitly designed to be merged. Each is a standalone, 1-file PR.

#### PR 1: Fix bare `except:` in `_safe_timestamp()` (Your own Issue #1039)

> [!TIP]
> This is your **own issue** — perfect credibility since you found the bug yourself.

- **File**: `database/historify_db.py`
- **Change**: Replace `except:` with `except (TypeError, ValueError) as e:` + add `logger.warning()`
- **Branch**: `fix/bare-except-safe-timestamp`
- **Commit**: `fix: replace bare except with specific exception in _safe_timestamp()`
- **Size**: ~5 lines changed in 1 file

---

#### PR 2: Add `aria-label` attributes to icon-only buttons — **ONE page only** (Issue #1005)

> [!IMPORTANT]
> The issue lists 4 files. Do **NOT** PR all 4 at once. Pick **one page** (e.g., `Holdings.tsx`) and PR it. The maintainer will see the pattern works and likely ask you to do the rest.

- **File**: `frontend/src/pages/Holdings.tsx`
- **Change**: Add `aria-label="Refresh holdings"`, `aria-label="Export to CSV"` etc. to icon-only `<Button>` elements
- **Branch**: `a11y/aria-labels-holdings`
- **Commit**: `fix(a11y): add aria-labels to icon-only buttons on Holdings page`
- **Reference**: `Closes #1005 (partial — Holdings page)`
- **Size**: ~10 lines changed in 1 file

---

#### PR 3: Add tooltips to icon-only buttons — **ONE page only** (Issue #1011)

- **File**: `frontend/src/pages/OrderBook.tsx`  
- **Change**: Wrap the filter button with `<TooltipProvider>` / `<Tooltip>` from existing shadcn/ui components
- **Branch**: `feat/tooltips-orderbook`
- **Commit**: `feat(ui): add tooltip to filter button on OrderBook page`
- **Reference**: `Closes #1011 (partial — OrderBook page)`
- **Size**: ~15 lines changed in 1 file

---

### 🟡 Phase 2: Frontend UX Improvements (Days 4-7)

#### PR 4: Improve empty state UI on MarketTimings page (Issue #889)

- **File**: `frontend/src/pages/admin/MarketTimings.tsx`
- **Change**: Replace plain text "Markets are closed today" with icon + heading + description pattern matching `StrategyIndex.tsx`
- **Branch**: `feat/empty-state-market-timings`
- **Commit**: `feat(ui): improve empty state on MarketTimings page`
- **Size**: ~20 lines in 1 file

#### PR 5: Improve empty state UI on Search page (Issue #889)

- **File**: `frontend/src/pages/Search.tsx`
- **Branch**: `feat/empty-state-search`
- **Commit**: `feat(ui): improve empty state on Search page`
- **Size**: ~20 lines in 1 file

#### PR 6-8: Continue `aria-label` and tooltip PRs for remaining pages

- One PR per page: `OrderBook.tsx`, `Positions.tsx`, `TradeBook.tsx`

---

### 🔵 Phase 3: Backend Quality (Days 8-14)

#### PR 9: Docstrings for one more module (follow your #1077 pattern)

- Pick **one small module** (e.g., `database/auth_db.py` or a single broker's `api/data.py`)
- Add Google-style docstrings + type hints
- **This is your proven formula** — #1077 was merged for exactly this

#### PR 10: A single, small test file (with prior issue discussion)

> [!WARNING]
> Before writing ANY test PR: **open an issue first** asking the maintainer which service they'd like tested, and propose your testing approach + mocking strategy. Get approval before writing code.

- Open issue: *"test: propose unit test for [service_name] — seeking feedback on approach"*
- Wait for maintainer response
- Write ONE test file for ONE service, max ~100 lines, no broker credentials needed
- Use `unittest.mock` patterns consistent with existing `test/` files

---

## Contribution Calendar (Streak Maintenance)

| Day | Action | Type |
|-----|--------|------|
| Day 1 (Today) | Sync fork + PR 1 (bare except fix) | `fix:` |
| Day 2 | PR 2 (aria-labels on Holdings) | `a11y:` |
| Day 3 | PR 3 (tooltip on OrderBook) | `feat:` |
| Day 4 | PR 4 (empty state MarketTimings) | `feat:` |
| Day 5 | PR 5 (empty state Search) | `feat:` |
| Day 6 | PR 6 (aria-labels OrderBook) | `a11y:` |
| Day 7 | PR 7 (aria-labels Positions) | `a11y:` |
| Day 8 | Open discussion issue for test approach | `issue` |
| Day 9 | PR 8 (docstrings for one module) | `docs:` |
| Day 10-14 | Continue based on maintainer feedback | varies |
| **March 20 (URGENT)** | **FOSS Hack Final Push: Docstrings, Tests, & Contributor Journey** | `docs`, `test` |

> [!NOTE]
> Even if a PR isn't merged the same day, the **commit to your fork** counts for the GitHub streak. So always push to your fork daily.

---

## PR Template to Use

```markdown
## What does this PR do?
[One-sentence summary]

## Related Issue
Closes #NNN (or "Partial fix for #NNN — covers [page name] only")

## Changes
- [bullet list of specific changes]

## How to Test
- [exact steps to verify]

## Screenshots (if UI change)
[before/after screenshots]
```

---

## Verification Plan

Since these are contributions to an external open-source repo, verification is:

### Before Each PR
1. **Sync fork**: `git fetch upstream && git rebase upstream/main` — zero merge conflicts
2. **Build check**: `npm run build` in `frontend/` passes with no errors
3. **Lint check**: No new lint warnings introduced
4. **Local test**: For frontend changes, verify the component renders correctly in browser
5. **For backend changes**: Run existing `pytest` tests to ensure nothing is broken

### After PR is Opened
- Monitor for maintainer feedback within 24-48 hours
- Be responsive to requested changes
- If no response in 3 days, leave a polite comment asking for review

---

## Immediate Next Steps

1. **Clone/sync your fork** of `marketcalls/openalgo`
2. **Start with PR 1** (the bare `except:` fix from your own issue #1039) — smallest possible change, high-value, your own bug report
3. **Then PR 2** (aria-labels on one page) — maintainer-created good-first-issue

---

## 🚀 FOSS Hack 2026: The Winning Stretch (Final Phase)

To win FOSS Hack 2026, we need to transition from "fixing bugs" to "improving the project's soul." Execute these on **March 20th** as priority:

### 1. Finalize Documentation (Type Hints & Docstrings)
- **Action**: Complete the `docs/add-docstrings-utils` branch.
- **Why**: Proves you care about the long-term maintainability of the project—a core value for FOSS Hack judges.
- **File**: `utils/auth_utils.py`, `utils/config.py`, or similar small untyped modules.

### 2. Verify PRs with Tests 🧪
- **Action**: For your `fix/logger-exception` PRs, ensure you can point to a passing local test run or CI/CD badge.
- **Why**: Shows your code is "merge-ready" and safe, which builds immense trust with the maintainer.

### 3. The "Contributor Journey" PR 🗺️
- **Action**: Identify a file that was hard for you to understand (e.g., `services/place_smart_order_service.py` or a complex database module) and add clarifying comments or a small README in that directory.
- **Why**: Helps future contributors get started faster. Highlighting this in your PR description as "Improving the Contributor Experience" is a major "win" signal for open-source contests.
