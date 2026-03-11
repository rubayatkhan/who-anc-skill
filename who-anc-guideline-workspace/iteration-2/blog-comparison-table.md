# WHO ANC Guideline Skill — Evaluation Results

## Headline

**With the skill: 74/74 assertions passed (100%). Without: 33/74 (44.6%).**

The WHO ANC Guideline Skill (v1.1) achieves perfect adherence to WHO clinical expectations across all 12 patient vignettes. Without the skill, the same model produces clinically reasonable but protocol-incomplete notes — missing exact doses, WHO-specific classifications, structured schedules, and emergency formatting.

---

## Iteration-2 Results: with_skill vs without_skill

| # | Vignette | With Skill | Without Skill | Delta |
|---|----------|:----------:|:-------------:|:-----:|
| 1 | Routine first contact | 8/8 (100%) | 5/8 (63%) | +3 |
| 2 | Anemia in high-prevalence setting | 5/5 (100%) | 2/5 (40%) | +3 |
| 3 | Pre-eclampsia high risk | 6/6 (100%) | 6/6 (100%) | 0 |
| 4 | HIV-positive on ART | 5/5 (100%) | 2/5 (40%) | +3 |
| 5 | GDM screening | 4/4 (100%) | 2/4 (50%) | +2 |
| 6 | Adolescent primigravida | 5/5 (100%) | 3/5 (60%) | +2 |
| 7 | Late booking (32 weeks) | 5/5 (100%) | 1/5 (20%) | +4 |
| 8 | Routine third trimester | 5/5 (100%) | 1/5 (20%) | +4 |
| 9 | Multiple risk factors | 8/8 (100%) | 3/8 (38%) | +5 |
| 10 | **Severe pre-eclampsia (emergency)** | **7/7 (100%)** | **1/7 (14%)** | **+6** |
| 11 | Malaria-endemic setting (IPTp-SP) | 8/8 (100%) | 5/8 (63%) | +3 |
| 12 | **Gestational hypertension (discrimination)** | **8/8 (100%)** | **2/8 (25%)** | **+6** |
| | **TOTAL** | **74/74 (100%)** | **33/74 (44.6%)** | **+41** |

---

## Skill Improvement: v1.0 → v1.1

| Metric | v1.0 (iter-1) | v1.1 (iter-2) |
|--------|:-------------:|:-------------:|
| with_skill pass rate | 94.6% (70/74) | **100% (74/74)** |
| Evals with failures | 3 (eval-01, 10, 11) | **0** |

### What changed in v1.1
- Fixed mild anemia dosing (was 120mg therapeutic → corrected to 30-60mg daily)
- Added unknown prevalence default to daily iron supplementation
- Added facility capability qualifier for severe PE (admit if capable, refer if not)
- Added per-tablet IPTp-SP dose instruction (500mg/25mg per tablet, 3 tablets)
- Harmonized danger signs section with admission/referral logic

---

## Where the Skill Adds the Most Value

### Largest deltas (skill most needed)
1. **Emergency protocols** (eval-10: +6) — Skill enforces unmistakable urgency, specific stabilization doses, routine ANC suspension
2. **Diagnostic discrimination** (eval-12: +6) — Skill prevents over-diagnosis (gestational HTN vs pre-eclampsia), enforces exact WHO taxonomy
3. **Complex multi-risk** (eval-09: +5) — Skill ensures every protocol fires (therapeutic iron, aspirin, calcium) with exact doses

### Where the model is already strong (skill optional)
1. **Pre-eclampsia high risk** (eval-03: 0 delta) — Well-known clinical territory, model nails it without help

### Pattern: The skill's value scales with protocol specificity
- Generic clinical reasoning (risk identification, basic counseling): model handles well
- WHO-specific protocols (8-contact model, dose thresholds, classification taxonomy, IPTp-SP scheduling): skill essential

---

## Methodology

- **Model**: Claude Opus 4.6
- **Vignettes**: 12 clinical scenarios spanning routine, high-risk, emergency, and discrimination cases
- **Assertions**: 74 total expectations derived from WHO ANC recommendations (DAK)
- **Grading**: Each assertion independently graded PASS/FAIL by evaluator agents
- **Configurations**: Same model, same vignettes — only difference is whether SKILL.md is provided as context
