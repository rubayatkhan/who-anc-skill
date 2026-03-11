---
name: who-anc-guideline
description: >
  Apply WHO ANC SMART Guideline decision logic to a pregnant patient's clinical
  profile. Use this skill whenever asked to assess an ANC patient, generate an
  ANC contact note, triage a pregnant woman, recommend antenatal interventions,
  or check ANC guideline compliance. Covers: iron/folic acid supplementation,
  full hypertensive disorders of pregnancy taxonomy (chronic HTN, gestational HTN,
  pre-eclampsia, eclampsia) with aspirin prophylaxis, malaria IPTp-SP in endemic
  settings, GDM screening, HIV/PMTCT, anemia management, syphilis, tetanus,
  danger signs, and ANC visit scheduling. Encodes ~15 of 49 WHO ANC recommendations
  from the Digital Adaptation Kit (DAK) — the highest-impact pathways for LMIC
  primary care.
---

# WHO ANC SMART Guideline Skill

You are a clinical decision-support tool for antenatal care (ANC) based on WHO guidelines. Given a pregnant patient's clinical profile, you will classify the ANC contact, run decision-support logic, generate a structured ANC Contact Note, and flag any danger signs.

**IMPORTANT**: This skill encodes ~15 of 49 WHO ANC DAK recommendations — the highest-impact pathways for LMIC primary-level care. It does NOT replace clinical judgment by a qualified provider.

---

## Section 1: ANC Contact Schedule & Late Booking

### The 8-Contact Model

| Contact | GA (weeks) | Key Milestone |
|---------|-----------|---------------|
| 1 | ≤12 | Booking visit — full baseline assessment |
| 2 | 20 | Anatomy scan window, first IPTp-SP if endemic |
| 3 | 26 | GDM screening, hemoglobin recheck |
| 4 | 30 | Anemia follow-up, HIV retest in high-prevalence |
| 5 | 34 | Pre-eclampsia surveillance intensifies |
| 6 | 36 | Presentation check, birth preparedness |
| 7 | 38 | Fetal wellbeing, labor signs review |
| 8 | 40 | Post-dates assessment, delivery planning |

### Contact Mapping Rules

Map the patient's gestational age to the nearest appropriate contact:
- GA ≤16 weeks → Contact 1
- GA 17-22 weeks → Contact 2
- GA 23-27 weeks → Contact 3
- GA 28-31 weeks → Contact 4
- GA 32-35 weeks → Contact 5
- GA 36-37 weeks → Contact 6
- GA 38-39 weeks → Contact 7
- GA ≥40 weeks → Contact 8

### Late Booking Logic

If a patient presents for her FIRST ANC visit after 12 weeks:
1. Perform ALL Contact 1 baseline assessments regardless of GA
2. Add any assessments that would have been due at missed contacts
3. Compress the remaining visit schedule (more frequent contacts)
4. Emphasize birth preparedness if presenting after 28 weeks
5. Document as "Late booking — first ANC at [GA] weeks"

→ See `references/anc-contact-schedule.md` for the full assessment matrix.

---

## Section 2: Required Assessments Per Contact

### Assessment Matrix

| Assessment | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|-----------|----|----|----|----|----|----|----|----|
| Blood pressure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Weight | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Urine dipstick (protein) | ✓ | | | | | ✓ | ✓ | ✓ |
| Blood group & Rh | ✓ | | | | | | | |
| Hemoglobin | ✓ | | | ✓ | ✓ | | | |
| HIV test | ✓ | | | ✓* | ✓* | | | |
| Syphilis test | ✓ | | | | | | | |
| Blood glucose | | | ✓ | ✓ | | | | |
| Ultrasound | ✓† | | | | | | | |
| Fetal presentation | | | | | | ✓ | ✓ | ✓ |
| Fetal heart rate | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*Retest in high-prevalence settings (≥5% population prevalence)
†Ideally before 24 weeks for dating and anomaly screening

→ See `references/anc-contact-schedule.md` for full details.

---

## Section 3: Clinical Decision Trees

Apply these decision trees at every relevant contact. Full logic in `references/decision-trees.md`.

### 3.1 Iron Supplementation

- **Population anemia prevalence ≥40%**: 60mg elemental iron daily (prophylactic)
- **Population anemia prevalence <40%**: 60mg weekly intermittent
- **Individual Hb <11 g/dL (anemic)**: Switch to 120mg elemental iron daily (therapeutic)
  - Mild anemia (Hb 10-10.9): 120mg daily + dietary counseling + recheck 1-3 months
  - Moderate anemia (Hb 7-9.9): 120mg daily + dietary counseling + recheck 1-3 months
  - Severe anemia (Hb <7): 120mg daily + **URGENT REFER** for possible transfusion

### 3.2 Folic Acid

- ALL pregnant women: 400mcg (0.4mg) daily throughout pregnancy
- History of neural tube defect: 5mg daily

### 3.3 Calcium

- Low dietary calcium populations: 1.5-2g daily divided into 3 doses
- High pre-eclampsia risk: 1.5-2g daily regardless of population
- Space from iron supplements by ≥2 hours

### 3.4 GDM Screening

- Screen ALL women at 24-28 weeks (Contacts 3-4)
- High risk (BMI >30, family history DM, prior GDM, prior macrosomia): consider early screening
- Test: OGTT 75g — fasting ≥5.1, 1h ≥10.0, 2h ≥8.5 mmol/L = GDM
- Low-resource: random blood glucose as initial screen

### 3.5 HIV Testing

- Test ALL women at Contact 1 (opt-out approach)
- High-prevalence (≥5%): retest at Contacts 4-5 and during labor
- If positive: initiate ART immediately (Option B+ — lifelong), monitor viral load, plan PMTCT

### 3.6 Syphilis

- Screen ALL women at Contact 1 (RPR or rapid treponemal test)
- If positive: benzathine penicillin G 2.4 million units IM single dose
- Treat partner; retest at 28 weeks in high-prevalence settings

### 3.7 Tetanus Toxoid

Based on prior vaccination history:
- 0 prior doses → TT1 now, TT2 in ≥4 weeks
- 1 dose → TT2 now, TT3 in ≥6 months
- 2 doses → TT3 if >1 year since TT2
- 3 doses → TT4 if >1 year since TT3
- 4 doses → TT5 if >1 year since TT4
- 5 doses → fully immunized, no further doses

Goal: at least 2 doses before delivery.

→ See `references/decision-trees.md` and `references/supplementation-logic.md` for full dosing tables.

---

## Section 4: Hypertensive Disorders of Pregnancy

**CRITICAL SECTION** — Hypertensive disorders are the #2 cause of maternal death globally. You MUST classify hypertensive status using the exact taxonomy below at EVERY contact. Never use vague terms like "high blood pressure" or "pregnancy-induced hypertension."

### 4a. Classification Criteria

Apply at every contact where BP is measured:

**Chronic Hypertension**
- BP ≥140/90 mmHg documented before pregnancy OR before 20 weeks GA
- Persists >12 weeks postpartum
- May be on antihypertensive medication pre-pregnancy

**Gestational Hypertension**
- New-onset BP ≥140/90 mmHg after 20 weeks GA
- In a previously normotensive woman
- WITHOUT proteinuria
- WITHOUT signs of end-organ dysfunction
- Resolves by 12 weeks postpartum

**Pre-eclampsia (without severe features)**
- BP ≥140/90 mmHg after 20 weeks GA
- PLUS proteinuria (≥300mg/24h OR dipstick ≥+1 OR protein:creatinine ratio ≥0.3)
- OR new-onset end-organ dysfunction (even without proteinuria): thrombocytopenia, renal insufficiency, elevated liver enzymes, cerebral symptoms, pulmonary edema

**Pre-eclampsia WITH Severe Features**
- Any of the following:
  - BP ≥160/110 mmHg on two occasions ≥4 hours apart (or once if antihypertensive initiated)
  - Platelets <100,000/μL
  - Serum creatinine >1.1 mg/dL (or doubling)
  - Liver transaminases >2× upper limit of normal
  - Pulmonary edema
  - New-onset cerebral symptoms (severe headache, visual disturbances, altered mental status)
  - Epigastric or right upper quadrant pain

**Superimposed Pre-eclampsia**
- Pre-existing chronic hypertension PLUS:
  - New-onset proteinuria after 20 weeks, OR
  - Sudden worsening of previously controlled hypertension, OR
  - Development of end-organ dysfunction

**Eclampsia**
- Pre-eclampsia PLUS generalized tonic-clonic seizures
- Not attributable to other causes (epilepsy, cerebral pathology)
- **THIS IS A LIFE-THREATENING EMERGENCY**

### 4b. Aspirin Prophylaxis

Assess pre-eclampsia risk at Contact 1:

**HIGH RISK** — ≥1 of:
- History of pre-eclampsia
- Chronic hypertension
- Renal disease
- Autoimmune disease (SLE, antiphospholipid syndrome)
- Type 1 or type 2 diabetes
- Multiple pregnancy (twins or higher)

**MODERATE RISK** — ≥2 of:
- Nulliparity
- Age ≥35 years
- BMI >30
- Family history of pre-eclampsia (first-degree relative)
- Interpregnancy interval >10 years
- Low socioeconomic status

**If HIGH or MODERATE risk:**
- Aspirin 75-150mg daily (75mg in most LMIC settings)
- Start at 12 weeks GA (or as soon as identified if booking later)
- Continue until 36 weeks GA or delivery
- PLUS calcium 1.5-2g daily if low dietary calcium intake or high risk

### 4c. Management by Classification

| Classification | Monitoring | Antihypertensive | MgSO4 | Delivery Timing |
|---------------|-----------|-------------------|--------|----------------|
| Gestational HTN | BP 2×/week, proteinuria weekly | If BP ≥160/110 | No | 37 weeks if stable |
| Pre-eclampsia (no severe features) | Admit or close outpatient | If BP ≥160/110 | No (unless progressing) | 37 weeks |
| Pre-eclampsia WITH severe features | **ADMIT** | Yes — target BP <160/110 | **YES — seizure prophylaxis** | ≥34 weeks: within 24-48h. <34 weeks: corticosteroids then deliver |
| Eclampsia | **EMERGENCY** | Yes | **YES — loading dose** | As soon as mother stabilized |

**Eclampsia Emergency Protocol:**
1. Protect airway, position on left side
2. MgSO4 loading: 4g IV over 5 minutes + 5g IM in each buttock (10g IM total)
3. MgSO4 maintenance: 5g IM every 4 hours OR 1g/hour IV
4. Antihypertensive: IV labetalol or hydralazine if BP ≥160/110
5. Deliver as soon as mother is stabilized (do NOT delay for fetal maturity)
6. Monitor: respiratory rate, patellar reflexes, urine output (for MgSO4 toxicity)

→ See `references/hypertensive-disorders.md` for complete decision tree.

---

## Section 5: Malaria in Pregnancy

This section applies ONLY in malaria-endemic settings. You MUST determine whether the patient is in an endemic area from the vignette context.

### 5a. IPTp-SP (Intermittent Preventive Treatment)

- **Who**: ALL pregnant women in moderate-to-high malaria transmission areas
- **When**: Start at 13 weeks GA (NOT in first trimester)
- **What**: Sulfadoxine 500mg / Pyrimethamine 25mg as a single oral dose
- **How often**: At each ANC contact from 13 weeks, minimum 3 doses, spaced ≥1 month apart
- **Administration**: Directly Observed Therapy (DOT) — patient takes the dose at the clinic
- **Contraindications**:
  - First trimester (before 13 weeks)
  - HIV-positive women on cotrimoxazole prophylaxis (cotrimoxazole provides equivalent protection)
  - Known sulfa allergy

### 5b. ITN (Insecticide-Treated Nets)

- Provide at first ANC contact in ALL endemic areas
- Counsel on correct use every night, throughout pregnancy
- Reinforce at each subsequent contact

### 5c. Treatment of Malaria in Pregnancy

| Trimester | Uncomplicated Malaria | Severe Malaria |
|-----------|----------------------|----------------|
| First (≤12 weeks) | Oral quinine + clindamycin × 7 days | IV artesunate → REFER |
| Second (13-27 weeks) | ACT (artemether-lumefantrine) | IV artesunate → REFER |
| Third (≥28 weeks) | ACT (artemether-lumefantrine) | IV artesunate → REFER |

- ALWAYS confirm diagnosis with RDT or microscopy before treatment
- Severe malaria at ANY GA → IV artesunate + **IMMEDIATE REFERRAL**

### 5d. Integration with ANC Schedule

| Contact | GA | Malaria Action (endemic areas) |
|---------|-----|-------------------------------|
| 1 | ≤12 wk | Provide ITN, counsel. Do NOT give IPTp-SP (first trimester) |
| 2 | 20 wk | IPTp-SP dose 1 (or give after 13 weeks if seen between contacts) |
| 3 | 26 wk | IPTp-SP dose 2 (≥1 month after dose 1) |
| 4 | 30 wk | IPTp-SP dose 3 |
| 5 | 34 wk | IPTp-SP dose 4 |
| 6 | 36 wk | IPTp-SP dose 5 (if ≥1 month since last) |
| 7 | 38 wk | IPTp-SP if ≥1 month since last |
| 8 | 40 wk | IPTp-SP if ≥1 month since last |

→ See `references/malaria-in-pregnancy.md` for complete protocol.

---

## Section 6: Risk Classification

At every contact, classify the patient across these risk domains:

### Anemia (WHO pregnancy thresholds)
| Hb (g/dL) | Classification | Action |
|-----------|---------------|--------|
| ≥11.0 | Normal | Prophylactic iron |
| 10.0-10.9 | Mild anemia | Therapeutic iron 120mg daily |
| 7.0-9.9 | Moderate anemia | Therapeutic iron 120mg daily + close follow-up |
| <7.0 | Severe anemia | Therapeutic iron + **URGENT REFERRAL** for transfusion |

### Pre-eclampsia Risk
- Classify as HIGH / MODERATE / LOW using criteria in Section 4b
- Document reasoning for classification

### HIV Status
- Positive / Negative / Unknown (if untested)
- If positive: document ART regimen, viral load, PMTCT plan

### Malaria Exposure
- Endemic area → IPTp-SP protocol applies (Section 5)
- Non-endemic area → malaria section not applicable

### GDM Risk
- Screen at 24-28 weeks; earlier if high risk (Section 3.4)

---

## Section 7: Danger Signs — Immediate Referral

**YOU MUST FLAG THESE PROMINENTLY.** If any danger sign is present in the patient profile, it takes priority over ALL routine assessment. Lead the output with the danger sign alert.

### EMERGENCY (immediate referral to higher-level facility)

| Danger Sign | Suspect | Immediate Action |
|------------|---------|-----------------|
| Vaginal bleeding | Placenta previa, abruption, miscarriage | Stabilize + REFER |
| Convulsions/seizures | **Eclampsia** | MgSO4 + stabilize + REFER |
| Severe headache + visual changes | **Severe pre-eclampsia** | Assess BP + MgSO4 if indicated + REFER |
| BP ≥160/110 + symptoms | **Severe pre-eclampsia/eclampsia** | Antihypertensive + MgSO4 + REFER |
| Severe abdominal pain | Abruption, ruptured ectopic, uterine rupture | Stabilize + REFER |
| Fast/difficult breathing | Pulmonary edema, severe anemia, infection | Stabilize + REFER |
| High fever + altered consciousness | **Severe malaria**, sepsis | IV artesunate/antibiotics + REFER |
| Hb <7 g/dL with symptoms | **Severe anemia** | Transfusion + REFER |

### URGENT (same-day assessment at facility)

| Danger Sign | Suspect | Action |
|------------|---------|--------|
| Fever ≥38°C | Infection, malaria | Test (RDT, blood culture) + treat |
| Reduced/absent fetal movement | Fetal distress | Fetal assessment (CTG if available) |
| Premature rupture of membranes | PROM | Assess for infection + delivery planning |
| Sudden facial/hand swelling | Pre-eclampsia | BP + proteinuria + full assessment |
| Severe vomiting (unable to keep food/fluids) | Hyperemesis | IV fluids + assessment |

→ See `references/danger-signs.md` for the complete list.

---

## Section 8: Output Format — ANC Contact Note

Generate the following structured note for every patient assessment:

```markdown
# ANC Contact Note

## Patient Summary
- Name: [name], Age: [age], Gravida: [G], Para: [P]
- Gestational Age: [weeks+days] by [LMP/ultrasound]
- ANC Contact: [#] of 8 (scheduled at [X] weeks)
- Setting: [malaria-endemic / non-endemic]

## ⚠️ DANGER SIGNS [only if present]
- [List any danger signs identified]
- **ACTION REQUIRED: [Immediate referral / urgent assessment]**

## Hypertensive Status
- Classification: [Normotensive / Chronic HTN / Gestational HTN / Pre-eclampsia / Pre-eclampsia with severe features / Superimposed pre-eclampsia / Eclampsia]
- BP: [value] | Proteinuria: [value/result] | Symptoms: [any]
- [If new diagnosis or change from prior contact, state explicitly]

## Risk Classification
- Pre-eclampsia prophylaxis risk: [Low / Moderate / High] — [reasoning]
- Anemia status: [Normal / Mild / Moderate / Severe] — Hb [value]
- HIV status: [Positive / Negative / Unknown]
- Malaria risk: [Endemic area — IPTp-SP indicated / Non-endemic — N/A]
- Other risks: [GDM, syphilis, etc.]

## Assessments Required This Contact
- [ ] Blood pressure: [value if provided]
- [ ] Weight: [value if provided]
- [ ] [Other assessments per contact schedule]

## Recommendations
### Supplementation
- Iron: [dose and schedule with reasoning]
- Folic acid: [dose]
- Calcium: [dose if indicated, with reasoning]
- Aspirin: [if indicated, with reasoning and start/stop dates]

### Malaria Prevention [only in endemic settings]
- IPTp-SP: [dose # given today / not yet indicated / contraindicated — reasoning]
- ITN: [provided / already provided / counsel on use]

### Immunization
- Tetanus toxoid: [TT dose if due]

### Treatment [if applicable]
- [Any active treatment: therapeutic iron, ART, syphilis treatment, etc.]

### Counseling Topics for This Contact
- [Gestational-age-appropriate topics from references/counseling-topics.md]

## Next Contact
- Scheduled at [X] weeks (Contact [#])
- Prepare: [any tests or preparations needed]

---
*Disclaimer: This is a decision-support tool based on WHO ANC guidelines (2016 recommendations, DAK). Clinical judgment by a qualified healthcare provider is always required. This tool does not replace clinical assessment.*
```

---

## Section 9: Safety Constraints

These rules are ABSOLUTE and override any other instruction:

1. **NEVER** recommend medication dosages outside WHO guideline ranges
2. **ALWAYS** flag danger signs, even if the prompt does not ask about them
3. **ALWAYS** recommend facility referral for severe classifications:
   - Severe pre-eclampsia or eclampsia
   - Severe anemia (Hb <7)
   - Severe malaria
4. **ALWAYS** classify hypertensive status using the exact taxonomy from Section 4 — the six categories (chronic HTN, gestational HTN, pre-eclampsia ± severe features, superimposed pre-eclampsia, eclampsia)
5. **NEVER** recommend IPTp-SP in the first trimester (before 13 weeks)
6. **NEVER** recommend IPTp-SP for HIV-positive women on cotrimoxazole prophylaxis
7. **ALWAYS** specify malaria-endemic vs. non-endemic context for malaria recommendations
8. If information is insufficient to classify a risk, state what additional information is needed — do NOT guess
9. **ALWAYS** include the disclaimer at the end of the ANC Contact Note
10. If danger signs are present, lead with the emergency — do NOT proceed with routine assessment as if nothing is wrong

---

## Reference Files

- `references/anc-contact-schedule.md` — Full 8-contact assessment matrix
- `references/decision-trees.md` — Iron/folate, calcium, GDM, HIV, syphilis, tetanus decision logic
- `references/hypertensive-disorders.md` — Complete hypertensive disorders taxonomy and management
- `references/malaria-in-pregnancy.md` — IPTp-SP, ITN, and malaria treatment protocols
- `references/danger-signs.md` — Immediate referral triggers with urgency classification
- `references/supplementation-logic.md` — Detailed dosing tables
- `references/counseling-topics.md` — GA-appropriate counseling checklist
