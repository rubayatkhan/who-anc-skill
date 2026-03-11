# ANC Contact Schedule — WHO 8-Contact Model

## Overview

The WHO 2016 ANC model recommends a minimum of **8 contacts** during pregnancy, replacing the previous 4-visit "focused ANC" model. Evidence shows that 8+ contacts reduce perinatal mortality by up to 8 per 1,000 births compared to the 4-visit model.

## Contact Schedule

| Contact | GA (weeks) | Trimester | Key Focus |
|---------|-----------|-----------|-----------|
| 1 | Up to 12 | T1 | Booking, baseline labs, risk assessment, supplementation initiation |
| 2 | 20 | T2 | Review results, fetal growth, ongoing risk assessment |
| 3 | 26 | T2 | GDM screening (24-28w), anemia recheck, IPTp-SP dose 2 |
| 4 | 30 | T3 | Growth monitoring, pre-eclampsia screening, IPTp-SP dose 3 |
| 5 | 34 | T3 | Growth, presentation check, birth preparedness |
| 6 | 36 | T3 | Presentation confirmation, birth plan review, IPTp-SP dose 4 |
| 7 | 38 | T3 | Growth, cervical assessment, delivery planning |
| 8 | 40 | T3 | Post-dates assessment, delivery planning |

## Required Assessments Per Contact

| Assessment | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|-----------|----|----|----|----|----|----|----|----|
| Blood pressure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Weight | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fundal height (SFH) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fetal heart rate | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fetal presentation | — | — | — | — | ✓ | ✓ | ✓ | ✓ |
| Hemoglobin | ✓ | — | ✓ | — | — | ✓ | — | — |
| Blood type & Rh | ✓ | — | — | — | — | — | — | — |
| HIV test | ✓ | — | — | — | — | — | — | — |
| HIV retest (high-prev) | — | — | ✓ | — | — | — | — | — |
| Syphilis test | ✓ | — | — | — | — | — | — | — |
| Urine dipstick (protein) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Urine culture | ✓ | — | — | — | — | — | — | — |
| GDM screening (OGTT) | — | — | ✓* | — | — | — | — | — |
| Ultrasound | ✓** | — | — | — | — | — | — | — |

*\* GDM screening recommended at 24-28 weeks (Contact 3 window)*
*\*\* Early ultrasound before 24 weeks for GA dating, viability, multiple pregnancy*

## Supplementation Schedule

| Supplement | Start | Dose | Duration |
|-----------|-------|------|----------|
| Iron (non-anemic) | Contact 1 | 30-60mg elemental iron daily | Throughout pregnancy |
| Iron (anemic) | At diagnosis | 120mg elemental iron daily | Until Hb normalizes, then prophylactic |
| Folic acid | Contact 1 | 400mcg daily | Throughout pregnancy |
| Calcium (low-intake populations) | Contact 1 | 1.5-2g daily, divided doses | Throughout pregnancy |
| Aspirin (high PE risk) | Before 20 weeks, ideally 12w | 75mg daily | Until 36 weeks |

## Late Booking Logic

When a woman presents for her **first ANC visit** after 12 weeks:

1. **Determine current GA** and identify which contact window she falls into
2. **Perform ALL Contact 1 baseline assessments** regardless of current GA:
   - Full lab panel (blood type, Rh, Hb, HIV, syphilis, urine)
   - Complete history and risk assessment
   - Initiate all supplementation
3. **Add catch-up assessments** from missed contacts:
   - If GA > 24w and no GDM screening: recommend OGTT
   - If GA > 20w and no ultrasound: recommend ultrasound (even if beyond ideal window)
   - If malaria-endemic and GA > 13w: initiate IPTp-SP immediately
4. **Schedule remaining contacts** in compressed format:
   - Minimum 2-week intervals between contacts
   - Prioritize contacts closest to delivery
   - Always include contacts at 36w and 38w minimum

## Contact Mapping Rules

Given a gestational age (GA), map to the appropriate contact:

```
IF first visit ever → Contact 1 (regardless of GA)
ELSE:
  GA ≤ 12w → Contact 1
  GA 13-19w → Between Contact 1 and 2
  GA 20-25w → Contact 2
  GA 26-29w → Contact 3
  GA 30-33w → Contact 4
  GA 34-35w → Contact 5
  GA 36-37w → Contact 6
  GA 38-39w → Contact 7
  GA ≥ 40w → Contact 8
```

## LMIC Implementation Notes

- Where ultrasound is unavailable, use LMP and fundal height for GA estimation
- Where lab capacity is limited, prioritize: Hb, HIV, syphilis, urine protein
- Community health workers can perform: BP, weight, SFH, dipstick urine, and danger sign screening
- Referral criteria should be clearly defined for each facility level
