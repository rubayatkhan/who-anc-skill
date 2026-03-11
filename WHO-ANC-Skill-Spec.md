# WHO ANC SMART Guideline Skill — Build Spec for Claude Code

## Purpose

Build a Claude skill that encodes the WHO Antenatal Care (ANC) SMART Guideline decision logic, then benchmark it against synthetic patient vignettes to demonstrate that **a harnessed model dramatically outperforms the same model without a harness** on clinical protocol adherence. This is the centerpiece demo for a blog post titled "From Chatbot to Second Brain: Building AI Harnesses for Global Health."

The core thesis: the skill (a harness component) converts a general-purpose LLM into a guideline-concordant clinical decision support tool — without fine-tuning, without specialized medical models. Context engineering > model capabilities.

---

## Scope: A Curated Subset of the WHO ANC DAK

**This skill intentionally encodes approximately 40-45% of the full WHO ANC Digital Adaptation Kit (DAK), not the complete guideline.** The full DAK contains 49 recommendations with hundreds of data elements and dozens of decision support tables. We selected the ~15 highest-impact clinical decision pathways that are most relevant to primary-level ANC in Sub-Saharan Africa and South Asia.

### What IS encoded (in scope):
- The 8-contact ANC schedule and late booking logic
- Iron/folate supplementation (prophylactic and therapeutic)
- Calcium supplementation
- **Full hypertensive disorders of pregnancy taxonomy** (chronic HTN, gestational HTN, pre-eclampsia, superimposed pre-eclampsia, eclampsia) with aspirin prophylaxis
- Anemia classification and management (WHO pregnancy thresholds)
- **Malaria in pregnancy: IPTp-SP (Intermittent Preventive Treatment with Sulfadoxine-Pyrimethamine)** and ITN provision
- GDM screening
- HIV testing, PMTCT basics
- Syphilis testing and treatment
- Tetanus toxoid scheduling
- Danger signs and immediate referral triggers
- Gestational-age-appropriate counseling

### What is NOT encoded (out of scope for this demo):
- Hepatitis B/C testing and vaccination
- TB screening
- Deworming (mebendazole by helminth prevalence)
- Intimate partner violence screening
- Substance use and tobacco screening
- Symphysis fundal height interpretation and growth curves
- Detailed ultrasound indication logic
- Rh immunoglobulin decision tree
- Group B Streptococcus screening
- Detailed nutrition assessment beyond supplementation
- Urine culture / ASB management
- Thyroid screening

### Why this scope is the right choice for the blog:
The argument is about the **pattern** (skills as a bridge from L2 to L4), not about completeness. Fifteen well-chosen decision trees prove the point as effectively as forty-nine. The blog should be explicit: *"We encoded 15 of the 49 ANC recommendations. Even this partial implementation achieved X% concordance vs. Y% without the harness. The question for LMICs isn't 'is this as rigorous as full CQL/FHIR implementation?' — it's 'is this more likely to actually exist at the point of care?'"*

The full CQL/FHIR L3 implementation is more rigorous (formally verifiable logic vs. probabilistic LLM execution). But it took a WHO team with health informaticists, knowledge engineers, CQL authors, and terminologists approximately a year to build. This skill encodes comparable clinical decision support in hours. For the 80% of LMIC facilities that will never have L3 artifacts, a skill that gets 85%+ concordance is dramatically better than nothing — or a naked LLM at ~50%.

---

## Pre-requisites

- Use the **skill-creator** meta-skill at `/mnt/skills/examples/skill-creator/SKILL.md`
- Follow its full workflow: draft → test → review → iterate → benchmark → package
- All eval schemas must conform to `/mnt/skills/examples/skill-creator/references/schemas.md`

---

## Part 1: The Skill

### 1.1 Skill Identity

```
Name: who-anc-guideline
Location: who-anc-guideline/SKILL.md
```

### 1.2 What the Skill Does

Given a patient profile (a synthetic clinical vignette describing a pregnant woman's demographics, obstetric history, current gestational age, vitals, lab results, and presenting complaints), the skill:

1. **Classifies the ANC contact** — determines which of the 8 recommended ANC contacts this visit corresponds to based on gestational age
2. **Runs decision-support logic** — applies the WHO ANC recommendation decision trees to determine:
   - Required assessments for this contact (blood pressure, weight, urine, blood tests, ultrasound, etc.)
   - Nutritional supplementation recommendations (iron, folic acid, calcium) based on population prevalence and individual risk
   - Immunization requirements (tetanus toxoid based on history)
   - **Hypertensive disorder classification** using the full taxonomy: chronic hypertension, gestational hypertension, pre-eclampsia (with/without severe features), superimposed pre-eclampsia, eclampsia — with corresponding management pathways
   - Anemia classification and management (WHO pregnancy thresholds)
   - **Malaria prevention**: IPTp-SP dosing schedule and ITN provision in endemic settings
   - HIV testing schedule and PMTCT management
   - GDM screening criteria and management
   - Counseling topics required for this gestational age
   - Referral triggers (danger signs requiring immediate facility referral)
3. **Generates a structured ANC Contact Note** with:
   - Contact number and gestational age
   - Assessments performed / to perform
   - Clinical findings and risk classification
   - Recommendations (supplementation, treatment, referral)
   - Next scheduled contact and what to prepare
   - Danger signs counseling checklist
4. **Flags any danger signs** present in the vignette that require immediate action

### 1.3 Skill Description (frontmatter)

```yaml
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
```

### 1.4 Skill Structure

```
who-anc-guideline/
├── SKILL.md                          # Main skill instructions (~400 lines)
├── references/
│   ├── anc-contact-schedule.md       # 8-contact model: timing, required actions per visit
│   ├── decision-trees.md             # Core clinical decision logic (iron/folate, calcium,
│   │                                 #   GDM, HIV, syphilis, Rh, tetanus)
│   ├── hypertensive-disorders.md     # Full taxonomy: chronic HTN, gestational HTN,
│   │                                 #   pre-eclampsia (mild/severe), superimposed,
│   │                                 #   eclampsia — classification criteria, management,
│   │                                 #   aspirin prophylaxis decision tree
│   ├── malaria-in-pregnancy.md       # IPTp-SP schedule, ITN, chloroquine prophylaxis,
│   │                                 #   treatment of uncomplicated/severe malaria,
│   │                                 #   endemic vs. non-endemic logic
│   ├── danger-signs.md               # Immediate referral triggers with urgency classification
│   ├── supplementation-logic.md      # Iron, folic acid, calcium dosing by context
│   └── counseling-topics.md          # Gestational-age-appropriate counseling checklist
├── scripts/
│   └── validate_anc_note.py          # Deterministic checker: verifies output contains
│                                     #   required sections, checks GA↔contact consistency,
│                                     #   validates supplementation doses, hypertensive
│                                     #   classification accuracy, IPTp-SP timing
└── evals/
    ├── evals.json                    # Test cases with expectations
    └── vignettes/                    # Synthetic patient vignettes as input files
        ├── vignette-01-routine-first-contact.md
        ├── vignette-02-anemia-risk.md
        ├── vignette-03-preeclampsia-high-risk.md
        ├── vignette-04-hiv-positive.md
        ├── vignette-05-gdm-screening.md
        ├── vignette-06-adolescent-primigravida.md
        ├── vignette-07-late-booking.md
        ├── vignette-08-routine-third-trimester.md
        ├── vignette-09-multiple-risk-factors.md
        ├── vignette-10-danger-signs-severe-preeclampsia.md
        ├── vignette-11-malaria-endemic-setting.md
        └── vignette-12-gestational-hypertension-evolving.md
```

### 1.5 SKILL.md Body — Key Sections

The SKILL.md should contain these sections (write them based on the WHO ANC DAK logic):

**Section 1: Overview & Contact Schedule**
- The 8-contact model: Contact 1 (≤12 weeks), Contact 2 (20 weeks), Contact 3 (26 weeks), Contact 4 (30 weeks), Contact 5 (34 weeks), Contact 6 (36 weeks), Contact 7 (38 weeks), Contact 8 (40 weeks)
- How to determine which contact applies based on gestational age
- What happens when a patient books late (common in LMICs)

**Section 2: Required Assessments Per Contact**
- Matrix of which assessments are required at which contacts
- Blood pressure (every contact), weight (every contact), urine dipstick (contacts 1, 6-8), blood group & Rh (contact 1), hemoglobin (contacts 1, 4-5), HIV test (contact 1, repeat at contact 4-5 in high-prevalence), syphilis (contact 1), blood glucose (contacts 3-4), ultrasound (before 24 weeks)
- Refer to `references/anc-contact-schedule.md` for the full matrix

**Section 3: Clinical Decision Trees**
- Point to `references/decision-trees.md` for the full logic on supplementation, GDM, HIV, syphilis, tetanus
- Summarize the key decision points inline:
  - Iron supplementation: 30-60mg daily (or 120mg weekly in non-anemia, or 120mg daily if anemic)
  - Folic acid: 400mcg daily throughout
  - Calcium: 1.5-2g daily in populations with low calcium intake OR for women at high risk of pre-eclampsia
  - Tetanus toxoid: based on vaccination history (TT1-TT5 schedule)

**Section 4: Hypertensive Disorders of Pregnancy (NEW — dedicated section)**
- Point to `references/hypertensive-disorders.md` for the full decision tree
- This is a CRITICAL section — hypertensive disorders are the #2 cause of maternal death globally
- Encode the full WHO/ISSHP classification taxonomy inline in SKILL.md:

  **4a. Classification criteria (all must be applied at every contact):**
  - **Chronic hypertension**: BP ≥140/90 known before pregnancy or before 20 weeks GA, persists >12 weeks postpartum
  - **Gestational hypertension**: BP ≥140/90 after 20 weeks GA in a previously normotensive woman, WITHOUT proteinuria or end-organ dysfunction
  - **Pre-eclampsia (without severe features)**: BP ≥140/90 after 20 weeks + proteinuria (≥300mg/24h or dipstick ≥+1 or protein:creatinine ratio ≥0.3) OR new-onset end-organ dysfunction
  - **Pre-eclampsia with severe features**: BP ≥160/110 OR proteinuria with any of: platelets <100,000, creatinine >1.1, liver transaminases >2x upper limit, pulmonary edema, cerebral or visual symptoms
  - **Superimposed pre-eclampsia**: Pre-existing chronic hypertension + new proteinuria after 20 weeks or sudden worsening of hypertension or development of end-organ dysfunction
  - **Eclampsia**: Pre-eclampsia + generalized tonic-clonic seizures not attributable to other causes

  **4b. Aspirin prophylaxis decision tree:**
  - Assess pre-eclampsia risk at Contact 1
  - HIGH RISK if ≥1 of: history of pre-eclampsia, chronic hypertension, renal disease, autoimmune disease (SLE/APS), type 1 or 2 diabetes, multiple pregnancy
  - MODERATE RISK if ≥2 of: nulliparity, age ≥35, BMI >30, family history of pre-eclampsia, interpregnancy interval >10 years, low socioeconomic status
  - If HIGH or MODERATE risk → aspirin 75-150mg daily starting at 12 weeks, continue until 36 weeks or delivery
  - Calcium 1.5-2g daily if population calcium intake is low or if high risk

  **4c. Management by classification:**
  - Gestational HTN: twice-weekly BP monitoring, weekly proteinuria screening, deliver at 37 weeks if controlled
  - Pre-eclampsia without severe features: admission or close outpatient monitoring, deliver at 37 weeks, antihypertensive if BP ≥160/110
  - Pre-eclampsia with severe features: ADMIT, stabilize (MgSO4, antihypertensive), deliver within 24-48h if ≥34 weeks, corticosteroids if <34 weeks
  - Eclampsia: EMERGENCY — MgSO4 loading dose (4g IV over 5 min + 10g IM), stabilize, deliver as soon as mother stabilized

**Section 5: Malaria in Pregnancy (NEW — dedicated section)**
- Point to `references/malaria-in-pregnancy.md` for the full decision tree
- This section applies ONLY in malaria-endemic settings (most of Sub-Saharan Africa, parts of South and Southeast Asia)
- The skill must ask/determine whether the patient is in an endemic area

  **5a. IPTp-SP (Intermittent Preventive Treatment with Sulfadoxine-Pyrimethamine):**
  - WHO recommendation: all pregnant women in moderate-to-high transmission areas
  - Start at 13 weeks GA (after first trimester / quickening)
  - Give SP (500mg sulfadoxine / 25mg pyrimethamine) as a single dose at each scheduled ANC contact
  - Minimum 3 doses, spaced ≥1 month apart
  - Can give at every ANC contact from 13 weeks until delivery
  - Give as DOT (directly observed therapy) at the ANC visit
  - Contraindications: first trimester, HIV-positive women on cotrimoxazole prophylaxis (use cotrimoxazole instead), known sulfa allergy

  **5b. ITN (Insecticide-Treated Nets):**
  - Provide ITN at first ANC contact in endemic areas
  - Counsel on correct use every night

  **5c. Treatment of malaria in pregnancy:**
  - First trimester: oral quinine + clindamycin (7 days)
  - Second/third trimester: ACT (artemisinin-based combination therapy) — typically artemether-lumefantrine
  - Severe malaria at any GA: IV artesunate (EMERGENCY, refer to hospital)
  - Always confirm with rapid diagnostic test (RDT) or microscopy before treatment

  **5d. Integration with ANC contact schedule:**
  - Contact 1 (≤12 weeks): provide ITN, counsel. Do NOT give IPTp-SP yet (first trimester)
  - Contact 2 (20 weeks): first dose IPTp-SP (if not already given after 13 weeks)
  - Contact 3-8: IPTp-SP at each contact, minimum 1 month apart

**Section 6: Risk Classification (updated)**
- Hypertensive disorders: use taxonomy from Section 4 — classify at every contact based on BP, proteinuria, symptoms
- Anemia classification (Hb ≥11 = normal, 10-10.9 = mild, 7-9.9 = moderate, <7 = severe)
- GDM screening criteria
- Malaria exposure: endemic vs. non-endemic setting determines whether IPTp-SP applies

**Section 7: Danger Signs — Immediate Referral**
- Point to `references/danger-signs.md`
- Vaginal bleeding, severe headache with blurred vision, convulsions, severe abdominal pain, fast/difficult breathing, fever, reduced/absent fetal movement, water breaking before labor (PROM)
- **Eclampsia-specific**: seizures in a hypertensive pregnant woman = eclampsia until proven otherwise
- **Severe malaria**: high fever + altered consciousness/prostration + parasitemia in endemic area
- The skill MUST flag these prominently and recommend immediate facility referral

**Section 8: Output Format**
- Define the exact ANC Contact Note template:

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

### Counseling Topics for This Contact
- [Gestational-age-appropriate topics]

## Next Contact
- Scheduled at [X] weeks (Contact [#])
- Prepare: [any tests or preparations needed]
```

**Section 9: Safety Constraints**
- NEVER recommend medication dosages outside WHO guidelines
- ALWAYS flag danger signs, even if the prompt doesn't explicitly ask about them
- ALWAYS recommend facility referral for severe classifications (severe pre-eclampsia, eclampsia, severe anemia, severe malaria)
- ALWAYS classify hypertensive status using the full taxonomy — never use vague terms like "high blood pressure" without classification
- For IPTp-SP: NEVER recommend in first trimester, NEVER give to women on cotrimoxazole
- If information is insufficient to classify risk, state what additional information is needed rather than guessing
- Include a disclaimer: "This is a decision-support tool based on WHO guidelines. Clinical judgment by a qualified provider is always required."

### 1.6 Reference Files to Build

**references/anc-contact-schedule.md** (~100 lines)
Build this as a markdown table showing each of the 8 contacts with columns for: gestational age, required assessments, required labs, supplementation review points, and counseling topics. Source from the WHO ANC DAK (Digital Adaptation Kit) available at https://build.fhir.org/ig/WorldHealthOrganization/smart-anc/ and the 2016 WHO ANC Recommendations document.

**references/decision-trees.md** (~150 lines)
Encode the key decision trees as structured if/then logic in markdown. Cover:
- Iron supplementation decision tree (population anemia prevalence → individual Hb → dose)
- Calcium supplementation decision tree (population intake level → individual risk → dose)
- GDM screening decision tree (GA → risk factors → test type)
- HIV testing decision tree (prevalence setting → testing schedule)
- Syphilis testing and treatment
- Tetanus toxoid scheduling based on prior doses
(Note: pre-eclampsia/hypertensive disorders and malaria now have their own dedicated reference files)

**references/hypertensive-disorders.md** (~150 lines)
The full hypertensive disorders of pregnancy taxonomy and management. Include:
- Classification criteria table (chronic HTN, gestational HTN, pre-eclampsia ± severe features, superimposed, eclampsia)
- BP thresholds and proteinuria criteria for each classification
- Aspirin prophylaxis decision tree with HIGH and MODERATE risk definitions
- Management pathway per classification (monitoring frequency, antihypertensive thresholds, delivery timing, MgSO4 indications)
- Emergency eclampsia protocol
This is the single most important reference file for the high-acuity vignettes. Source: WHO 2011 recommendations for prevention and treatment of pre-eclampsia and eclampsia, updated with 2016 ANC guidance.

**references/malaria-in-pregnancy.md** (~100 lines)
Complete malaria prevention and treatment in pregnancy. Include:
- IPTp-SP dosing schedule (timing, dose, frequency, DOT)
- ITN provision and counseling
- Contraindications (first trimester, cotrimoxazole interaction for HIV+ women)
- Treatment by trimester (quinine+clindamycin in T1, ACT in T2/T3)
- Severe malaria emergency management (IV artesunate, referral)
- Integration with 8-contact ANC schedule showing when each intervention applies
Source: WHO 2012 updated recommendations on IPTp-SP, WHO Guidelines for Malaria (2022 update).

**references/danger-signs.md** (~60 lines)
List all WHO-defined danger signs in pregnancy with urgency classification and recommended action. Include eclampsia-specific and severe malaria-specific danger signs.

**references/supplementation-logic.md** (~80 lines)
Detailed dosing tables with population-level and individual-level parameters.

**references/counseling-topics.md** (~60 lines)
Gestational-age-mapped counseling topics (nutrition, birth preparedness, breastfeeding, family planning, danger sign recognition, malaria prevention in endemic areas, etc.)

### 1.7 Validation Script

**scripts/validate_anc_note.py**

A Python script that programmatically checks an ANC Contact Note output for:
- Required sections present (Patient Summary, Hypertensive Status, Risk Classification, Assessments, Recommendations, Next Contact)
- Gestational age ↔ contact number consistency (e.g., GA 26 weeks should map to Contact 3)
- Hypertensive disorder classification uses valid taxonomy term (not vague "high blood pressure")
- Iron supplementation dose within WHO range (30-60mg daily or 120mg weekly for non-anemic; 120mg daily for anemic)
- Folic acid dose = 400mcg
- Calcium recommendation present if high pre-eclampsia risk
- Aspirin recommendation present if high/moderate pre-eclampsia risk AND GA ≥ 12 weeks
- IPTp-SP recommended if malaria-endemic AND GA ≥ 13 weeks AND NOT on cotrimoxazole
- IPTp-SP NOT recommended if first trimester or on cotrimoxazole
- Danger signs flagged if present in input vignette
- Disclaimer present

Usage: `python scripts/validate_anc_note.py --input <vignette.md> --output <anc_note.md>`
Returns JSON with pass/fail per check.

---

## Part 2: The Evaluation

### 2.1 Synthetic Patient Vignettes (12 total)

Build these as realistic clinical vignettes — the kind of information a CHW might collect on a tablet. Each should be a markdown file with structured patient data. Here are the 12 scenarios:

**Vignette 1: Routine first contact, low risk**
- 25yo G2P1, GA 10 weeks by LMP, BP 110/70, weight 58kg, Hb 12.1, HIV negative, no complaints
- Expected: Contact 1 assessments, standard iron/folate, low pre-eclampsia risk, routine counseling

**Vignette 2: Moderate anemia at first contact**
- 22yo G1P0, GA 11 weeks, BP 100/65, Hb 9.2, no other risk factors
- Expected: Moderate anemia classification, therapeutic iron dose (120mg daily), follow-up Hb, dietary counseling

**Vignette 3: High pre-eclampsia risk**
- 38yo G1P0, BMI 33, chronic hypertension on medication, GA 14 weeks, BP 135/88
- Expected: High pre-eclampsia risk, aspirin 75mg recommendation, calcium 1.5-2g, close monitoring schedule

**Vignette 4: HIV-positive patient**
- 28yo G3P2, GA 20 weeks, HIV positive on ART (TDF/3TC/DTG), viral load suppressed, Hb 10.8
- Expected: Mild anemia, ART continuation, infant prophylaxis planning, repeat viral load schedule, enhanced counseling

**Vignette 5: GDM screening contact**
- 30yo G2P1, GA 26 weeks, BMI 29, family history of diabetes, random blood glucose 7.8 mmol/L
- Expected: Contact 3, GDM screening recommendation, dietary counseling, glucose monitoring plan

**Vignette 6: Adolescent primigravida**
- 16yo G1P0, GA 8 weeks, underweight (BMI 17.5), Hb 10.5, no prior vaccinations
- Expected: Nutritional supplementation emphasis, tetanus vaccination schedule, age-appropriate counseling, psychosocial support referral

**Vignette 7: Late booking (first visit at 32 weeks)**
- 29yo G4P3, GA 32 weeks, no prior ANC this pregnancy, BP 120/80, Hb 11.5
- Expected: Catch-up assessments (all Contact 1-4 labs/tests), compressed visit schedule, birth preparedness emphasis

**Vignette 8: Routine third trimester (Contact 6)**
- 27yo G2P1, GA 36 weeks, all prior contacts normal, BP 115/72, Hb 11.8, cephalic presentation
- Expected: Contact 6 specific assessments, birth preparedness review, danger sign review, breastfeeding counseling

**Vignette 9: Multiple risk factors (complex)**
- 34yo G1P0, GA 24 weeks, BMI 32, Hb 8.5, BP 130/85, proteinuria +1, previous cesarean
- Expected: Severe anemia, pre-eclampsia workup, therapeutic iron, aspirin, calcium, close monitoring, facility delivery plan

**Vignette 10: Active danger signs — severe pre-eclampsia**
- 31yo G3P2, GA 34 weeks, presents with severe headache, blurred vision, BP 160/110, proteinuria +++, epigastric pain
- Expected: PROMINENT danger sign alert, immediate referral to higher-level facility, classified as pre-eclampsia with severe features, MgSO4 and antihypertensive stabilization, delivery planning

**Vignette 11: Malaria-endemic setting — routine ANC with IPTp-SP**
- 24yo G2P1, GA 22 weeks, presenting at rural health center in western Kenya (malaria-endemic), BP 110/68, Hb 10.2, HIV negative, no fever or malaria symptoms currently, received ITN at first contact, no prior IPTp-SP doses
- Expected: Contact 2 assessment, first dose IPTp-SP given as DOT, mild anemia identified with standard iron supplementation, ITN use reinforced, next IPTp-SP at Contact 3. This tests whether the skill correctly applies the malaria-endemic protocol including IPTp timing and DOT requirement.

**Vignette 12: Gestational hypertension evolving toward pre-eclampsia**
- 30yo G1P0, GA 32 weeks, Contact 5, previously normotensive at all prior contacts. Today BP 148/95 on two readings 15 min apart. No proteinuria on dipstick. No headache, visual changes, or epigastric pain. Mild pedal edema. Hb 11.5. Setting: urban clinic, Dar es Salaam (malaria-endemic).
- Expected: Classified as GESTATIONAL HYPERTENSION (new-onset elevated BP after 20 weeks, no proteinuria, no severe features). NOT pre-eclampsia (yet). Management: twice-weekly BP monitoring, weekly proteinuria screening, counsel on danger signs (especially headache, visual changes, epigastric pain as warning of progression). Plan delivery at 37 weeks if stable. Also: IPTp-SP should be current (dose 3-4 by this GA). This vignette specifically tests the skill's ability to distinguish gestational HTN from pre-eclampsia — a nuance the unharnessed model is likely to get wrong by over-diagnosing pre-eclampsia.

### 2.2 Evaluation Configuration (evals.json)

```json
{
  "skill_name": "who-anc-guideline",
  "evals": [
    {
      "id": 1,
      "prompt": "Please assess this pregnant patient and generate an ANC contact note following WHO guidelines.\n\n[contents of vignette-01-routine-first-contact.md]",
      "expected_output": "Complete ANC Contact 1 note with standard supplementation, low risk classification, all required first-contact assessments listed",
      "files": ["evals/vignettes/vignette-01-routine-first-contact.md"],
      "expectations": [
        "Output identifies this as ANC Contact 1 (first contact, ≤12 weeks)",
        "Iron supplementation recommended at 30-60mg elemental iron daily",
        "Folic acid 400mcg daily recommended",
        "Blood group, Rh factor, hemoglobin, HIV, syphilis tests listed as required assessments",
        "Pre-eclampsia risk classified as LOW",
        "Next contact scheduled at approximately 20 weeks",
        "No danger signs flagged",
        "Disclaimer about clinical judgment present"
      ]
    },
    {
      "id": 2,
      "prompt": "Assess this ANC patient and provide guideline-based recommendations.\n\n[contents of vignette-02-anemia-risk.md]",
      "expected_output": "ANC note identifying moderate anemia, recommending therapeutic iron dose, dietary counseling",
      "files": ["evals/vignettes/vignette-02-anemia-risk.md"],
      "expectations": [
        "Anemia classified as MODERATE (Hb 9.2 is in 7-9.9 range)",
        "Iron dose is 120mg elemental iron daily (therapeutic, not prophylactic)",
        "Hemoglobin recheck recommended within 1-3 months",
        "Dietary counseling on iron-rich foods mentioned",
        "Folic acid 400mcg daily recommended"
      ]
    },
    {
      "id": 3,
      "prompt": "Generate an ANC assessment for this patient.\n\n[contents of vignette-03-preeclampsia-danger.md]",
      "expected_output": "High pre-eclampsia risk identified, aspirin + calcium recommended, close monitoring",
      "files": ["evals/vignettes/vignette-03-preeclampsia-danger.md"],
      "expectations": [
        "Pre-eclampsia risk classified as HIGH (nulliparity + age >35 + BMI >30 + chronic hypertension)",
        "Aspirin 75mg daily recommended starting from 12 weeks",
        "Calcium 1.5-2g daily recommended",
        "Blood pressure monitoring frequency increased",
        "Proteinuria monitoring recommended",
        "Current BP (135/88) flagged as elevated but not in immediate danger range"
      ]
    },
    {
      "id": 4,
      "prompt": "This HIV-positive pregnant woman needs her ANC contact note.\n\n[contents of vignette-04-hiv-positive.md]",
      "expected_output": "ANC note with HIV-specific management integrated into routine ANC",
      "files": ["evals/vignettes/vignette-04-hiv-positive.md"],
      "expectations": [
        "ART continuation explicitly recommended",
        "Viral load monitoring schedule mentioned",
        "Infant prophylaxis or PMTCT planning mentioned",
        "Mild anemia identified (Hb 10.8)",
        "Standard iron/folate supplementation recommended alongside ART"
      ]
    },
    {
      "id": 5,
      "prompt": "Assess this patient for her 26-week ANC visit.\n\n[contents of vignette-05-gdm-screening.md]",
      "expected_output": "Contact 3 note with GDM screening recommendation",
      "files": ["evals/vignettes/vignette-05-gdm-screening.md"],
      "expectations": [
        "Identified as ANC Contact 3 (26 weeks)",
        "GDM screening recommended based on risk factors (BMI, family history, elevated glucose)",
        "Oral glucose tolerance test (OGTT) or equivalent mentioned",
        "Dietary counseling for GDM prevention recommended"
      ]
    },
    {
      "id": 6,
      "prompt": "Please provide ANC guidance for this adolescent patient.\n\n[contents of vignette-06-adolescent-primigravida.md]",
      "expected_output": "ANC note with adolescent-specific considerations, nutrition emphasis, vaccination",
      "files": ["evals/vignettes/vignette-06-adolescent-primigravida.md"],
      "expectations": [
        "Undernutrition/low BMI flagged as concern",
        "Enhanced nutritional supplementation or counseling recommended",
        "Tetanus toxoid vaccination schedule initiated (TT1 with schedule for TT2+)",
        "Psychosocial support or adolescent-friendly services mentioned",
        "Mild anemia identified and treated"
      ]
    },
    {
      "id": 7,
      "prompt": "This woman is coming for her first ANC visit at 32 weeks. What catch-up assessments are needed?\n\n[contents of vignette-07-late-booking.md]",
      "expected_output": "Catch-up ANC note listing all missed assessments from contacts 1-4",
      "files": ["evals/vignettes/vignette-07-late-booking.md"],
      "expectations": [
        "Late booking explicitly acknowledged",
        "All Contact 1 baseline labs recommended (blood group, Rh, HIV, syphilis, hemoglobin)",
        "Ultrasound recommended even though beyond ideal window",
        "Compressed remaining visit schedule outlined",
        "Birth preparedness emphasized given late presentation"
      ]
    },
    {
      "id": 8,
      "prompt": "Generate a Contact 6 ANC note for this patient with normal pregnancy progression.\n\n[contents of vignette-08-routine-third-trimester.md]",
      "expected_output": "Routine Contact 6 note with third-trimester-specific assessments",
      "files": ["evals/vignettes/vignette-08-routine-third-trimester.md"],
      "expectations": [
        "Identified as ANC Contact 6 (36 weeks)",
        "Fetal presentation assessment included",
        "Birth preparedness and complication readiness counseled",
        "Breastfeeding counseling included",
        "Next contact at 38 weeks (Contact 7)"
      ]
    },
    {
      "id": 9,
      "prompt": "This patient has multiple complications. Please assess and generate recommendations.\n\n[contents of vignette-09-multiple-risk-factors.md]",
      "expected_output": "Complex ANC note addressing severe anemia, pre-eclampsia risk, multiple interventions",
      "files": ["evals/vignettes/vignette-09-multiple-risk-factors.md"],
      "expectations": [
        "Severe anemia classified (Hb 8.5, but actually this is moderate — 7-9.9 range)",
        "Therapeutic iron (120mg daily) recommended",
        "Pre-eclampsia risk classified as HIGH (nulliparity + BMI >30 + elevated BP + proteinuria)",
        "Aspirin 75mg recommended",
        "Calcium 1.5-2g recommended",
        "Proteinuria flagged for monitoring and workup",
        "Facility-based delivery plan recommended",
        "Multiple risks result in more frequent monitoring schedule"
      ]
    },
    {
      "id": 10,
      "prompt": "URGENT: This patient just presented with the following symptoms. Assess immediately.\n\n[contents of vignette-10-danger-signs-severe-preeclampsia.md]",
      "expected_output": "IMMEDIATE danger sign alert with urgent referral, classified as pre-eclampsia with severe features",
      "files": ["evals/vignettes/vignette-10-danger-signs-severe-preeclampsia.md"],
      "expectations": [
        "DANGER SIGNS prominently flagged (not buried in routine assessment)",
        "Classified specifically as PRE-ECLAMPSIA WITH SEVERE FEATURES (not just 'pre-eclampsia' or 'high blood pressure')",
        "IMMEDIATE referral to higher-level facility recommended",
        "Stabilization measures mentioned (magnesium sulfate for seizure prophylaxis, antihypertensive)",
        "BP 160/110 classified as severely elevated",
        "Output does NOT proceed with routine ANC assessment — emergency takes priority",
        "Urgency is unmistakable in tone and formatting"
      ]
    },
    {
      "id": 11,
      "prompt": "Please provide an ANC assessment for this patient at a rural health center in western Kenya.\n\n[contents of vignette-11-malaria-endemic-setting.md]",
      "expected_output": "ANC Contact 2 note with IPTp-SP as a key recommendation, malaria prevention integrated into routine ANC",
      "files": ["evals/vignettes/vignette-11-malaria-endemic-setting.md"],
      "expectations": [
        "Setting identified as malaria-endemic",
        "IPTp-SP first dose recommended (GA 22 weeks, eligible since >13 weeks)",
        "IPTp-SP specified as directly observed therapy (DOT) at the clinic",
        "Correct dose mentioned: sulfadoxine 500mg / pyrimethamine 25mg as single dose",
        "ITN use reinforced (already provided at first contact)",
        "Mild anemia identified (Hb 10.2, within 10-10.9 range)",
        "Standard iron supplementation (30-60mg daily, not therapeutic dose)",
        "Next IPTp-SP dose scheduled at Contact 3 (26 weeks), ≥1 month apart"
      ]
    },
    {
      "id": 12,
      "prompt": "This previously normotensive patient has elevated blood pressure at today's visit. Please assess.\n\n[contents of vignette-12-gestational-hypertension-evolving.md]",
      "expected_output": "Gestational hypertension classified (NOT pre-eclampsia), with monitoring plan and danger sign counseling",
      "files": ["evals/vignettes/vignette-12-gestational-hypertension-evolving.md"],
      "expectations": [
        "Classified as GESTATIONAL HYPERTENSION specifically (not pre-eclampsia, not just 'elevated BP')",
        "Reasoning states: new-onset hypertension after 20 weeks + no proteinuria + no severe features",
        "Does NOT over-diagnose as pre-eclampsia (critical discrimination test)",
        "Twice-weekly blood pressure monitoring recommended",
        "Weekly proteinuria screening recommended (watching for progression to pre-eclampsia)",
        "Danger signs counseled — specifically headache, visual changes, epigastric pain as warning of pre-eclampsia progression",
        "Delivery planning at 37 weeks if condition remains stable",
        "IPTp-SP status addressed (malaria-endemic setting, should be on dose 3-4 by 32 weeks)"
      ]
    }
  ]
}
```

### 2.3 Assertions to Grade Programmatically vs. Qualitatively

**Programmatic (use validate_anc_note.py):**
- Required sections present in output
- Contact number ↔ gestational age consistency
- Hypertensive disorder classification uses valid taxonomy term
- Supplementation doses within WHO ranges
- IPTp-SP correctly recommended/withheld based on GA, setting, and cotrimoxazole status
- Danger signs flagged when present in input
- Disclaimer present

**Qualitative (human review via eval-viewer):**
- Clinical reasoning quality
- Correct discrimination between hypertensive disorder categories (especially gestational HTN vs. pre-eclampsia — vignette 12)
- Appropriate handling of risk factor interactions
- Malaria protocol integration with routine ANC
- Counseling topic relevance and completeness
- Tone/urgency appropriate to clinical situation
- Would a midwife/CHW find this note useful and trustworthy?

---

## Part 3: The Benchmark (With-Skill vs. Without-Skill)

### 3.1 What We're Measuring

For each of the 12 vignettes, run **two configurations**:

1. **with_skill**: Claude reads the WHO ANC Guideline skill, then processes the vignette
2. **without_skill**: Claude receives only the vignette and the same prompt — no skill, no reference files, no decision trees

This is the A/B test that proves the thesis. We expect:
- **with_skill**: 85-95% expectation pass rate (guideline-concordant, structured, safe)
- **without_skill**: 40-60% pass rate (general medical knowledge but missing specific WHO protocol details, dosing errors, structural gaps, may not flag danger signs prominently)

The two new vignettes (11, 12) are specifically designed to maximize the delta:
- **Vignette 11 (malaria)**: the unharnessed model likely knows about malaria in pregnancy generically but will miss IPTp-SP dosing specifics, DOT requirement, cotrimoxazole interaction, and the 13-week start threshold
- **Vignette 12 (gestational HTN)**: the unharnessed model will likely over-diagnose pre-eclampsia — this tests the skill's ability to enforce precise taxonomy distinctions

### 3.2 Key Metrics to Surface

For the blog post, the most important outputs are:

1. **Overall pass rate delta** (with vs. without skill) — the headline number
2. **Per-vignette pass rates** — especially the complex cases (9, 10) where we expect the biggest delta
3. **Safety-critical failures** — any without-skill runs that miss danger signs, recommend wrong doses, or fail to refer when needed
4. **Specific failure patterns** — what exactly does the unharnessed model get wrong? (e.g., wrong iron dose for anemia, missing calcium for pre-eclampsia, not catching late booking catch-up needs)

### 3.3 Execution Steps

Follow the skill-creator workflow:

1. **Draft** the SKILL.md and all reference files (7 reference files total)
2. **Build** the 12 vignettes as markdown files
3. **Write** evals.json with all expectations
4. **Run** all 12 with_skill and 12 without_skill (24 total runs)
   - In Cowork: spawn subagents in parallel (with-skill + baseline for each vignette simultaneously)
   - In Claude.ai: run sequentially (with-skill first, then without-skill)
5. **Grade** each run using the grader agent + validate_anc_note.py for programmatic checks
6. **Aggregate** benchmark using `python -m scripts.aggregate_benchmark`
7. **Generate** eval viewer using `generate_review.py --static` for human review
8. **Iterate** if pass rates need improvement

### 3.4 Expected Benchmark Output

The benchmark.json should show something like:

```
with_skill:    pass_rate mean=0.90 ± 0.08
without_skill: pass_rate mean=0.45 ± 0.18
delta:         +0.45 (45 percentage points)
```

If the delta is less than 25 percentage points, the skill needs strengthening. If it's less than 15, something is wrong with the evaluation design (assertions may be too easy). The variance for without_skill should be notably higher — the unharnessed model will score well on routine cases (vignettes 1, 8) but poorly on protocol-specific ones (vignettes 2, 11, 12).

---

## Part 4: Deliverables for the Blog Post

After the benchmark completes, produce these artifacts:

### 4.1 Summary Table
A markdown table showing per-vignette pass rates for both configurations:

| Vignette | Scenario | With Skill | Without Skill | Delta |
|----------|----------|-----------|--------------|-------|
| 1 | Routine first contact | 100% | 75% | +25% |
| 2 | Moderate anemia | 100% | 40% | +60% |
| ... | ... | ... | ... | ... |
| 10 | Severe pre-eclampsia | 100% | 43% | +57% |
| 11 | Malaria endemic (IPTp-SP) | 88% | 25% | +63% |
| 12 | Gestational HTN (not pre-eclampsia) | 88% | 25% | +63% |
| **Overall** | | **90%** | **45%** | **+45%** |

### 4.2 Failure Analysis
A short narrative (3-5 paragraphs) analyzing *what specifically the unharnessed model got wrong*. Expected patterns:
- Iron dosing errors (prophylactic vs. therapeutic for anemia)
- Missing calcium/aspirin for pre-eclampsia risk
- Incomplete catch-up recommendations for late bookings
- Danger signs not given sufficient prominence
- Missing disclaimer / safety framing
- **Hypertensive disorder misclassification**: the unharnessed model will likely conflate gestational hypertension with pre-eclampsia, or use vague terms like "pregnancy-induced hypertension" instead of the precise taxonomy
- **Malaria protocol gaps**: generic knowledge of malaria prevention but missing IPTp-SP specifics (DOT, 13-week threshold, cotrimoxazole interaction, spacing requirements)
- **Over- or under-diagnosis**: without the structured taxonomy, the model may either over-diagnose pre-eclampsia (vignette 12) or under-recognize severe features (vignette 10)

### 4.3 "The Harness Difference" Visuals
Two before/after comparisons for the blog:

**Comparison A (Emergency)**: Vignette 10 — severe pre-eclampsia. Show the without-skill output (which likely buries the emergency in routine assessment and uses vague "high blood pressure" language) versus the with-skill output (which leads with bold danger sign alert, classifies as "pre-eclampsia with severe features," and recommends immediate referral with MgSO4 stabilization).

**Comparison B (Discrimination)**: Vignette 12 — gestational hypertension. Show the without-skill output (which likely over-diagnoses pre-eclampsia based on elevated BP alone) versus the with-skill output (which correctly classifies as gestational HTN, explains why it's NOT pre-eclampsia, and sets up a monitoring plan watching for progression). This is arguably the more impressive demo — it shows the skill preventing a *false positive*, not just catching a true positive.

### 4.4 The Packaged Skill
Package using `python -m scripts.package_skill who-anc-guideline/` for download/sharing.

---

## Part 5: Blog Narrative Framing

This demo serves the following argumentative purpose in the blog:

1. **"Context eats models for breakfast" — now with evidence.** The same model (Claude), on the same hardware, with the same prompt structure, goes from ~45% to ~90% guideline concordance just by adding structured context. The improvement is most dramatic on protocol-specific details the model "sort of knows" but gets wrong without structured decision trees — iron dosing thresholds, IPTp-SP timing rules, and the precise taxonomy of hypertensive disorders.

2. **The skill IS the bridge from L1 to L4.** WHO's SMART Guidelines use a 4-layer framework: L1 (narrative guidelines) → L2 (decision trees in the DAK) → L3 (CQL/FHIR code) → L4 (executable tool). The skill takes L2 content and makes it LLM-executable — bypassing the expensive L3 step of writing CQL code and FHIR profiles. This is a radically cheaper and faster path to clinical decision support. **But be honest about the tradeoff**: CQL logic is formally verifiable; a skill is probabilistic. For the 80% of LMIC facilities that will never build L3 artifacts, 90% concordance via a skill is dramatically better than 45% from a naked LLM — or the current reality of no decision support at all.

3. **Scope is a feature, not a bug.** We encoded ~15 of the 49 ANC recommendations — the highest-impact pathways for LMIC primary care. The blog should name what was included and what was excluded. The argument: "A complete skill covering all 49 recommendations is buildable. But even a partial implementation on the most critical pathways (hypertensive disorders — the #2 cause of maternal death; malaria — responsible for 10,000 maternal deaths/year in Africa; anemia — affecting 40% of pregnant women in LMICs) transforms clinical decision support."

4. **The analogy to the personal harness is direct.** Just as CLAUDE.md + Skills + Obsidian vault turned a generic chatbot into a personalized second brain, HEALTH.md + clinical skills + a medical knowledge base turns a generic chatbot into a guideline-concordant clinical advisor.

5. **The 45-point improvement is actually conservative.** In production, the harness would also have MCP connectors to patient records (FHIR/DHIS2), long-term memory of prior contacts, scheduled monitoring for overdue patients, and population-level context (endemic area profiles, local formulary). Each additional harness component closes the gap further.

---

## Implementation Notes for Claude Code

- **Source material**: The WHO ANC recommendations (2016) are publicly available. The DAK decision logic is available at https://build.fhir.org/ig/WorldHealthOrganization/smart-anc/ and the GitHub repo at https://github.com/WorldHealthOrganization/smart-anc. You can also reference the JMIR 2020 paper (doi:10.2196/16355) which details the clinical algorithms.
- **Hypertensive disorders sources**: WHO 2011 "Recommendations for prevention and treatment of pre-eclampsia and eclampsia" and the ISSHP classification (2018 update). The distinction between gestational HTN and pre-eclampsia is clinically critical — get the thresholds exact.
- **Malaria sources**: WHO 2012 "Updated WHO Policy Recommendation: Intermittent Preventive Treatment of malaria in pregnancy using Sulfadoxine-Pyrimethamine (IPTp-SP)" and WHO Guidelines for Malaria (2022, 3rd edition). Key detail: the cotrimoxazole/IPTp-SP interaction for HIV-positive women is frequently missed.
- **Clinical accuracy matters**: This will be published and read by health professionals. Double-check all dosing, risk classification thresholds, and danger sign lists against WHO source documents. If uncertain about any clinical detail, note the uncertainty and cite the source.
- **Keep it LMIC-focused**: Vignettes should reflect settings where ANC is commonly delivered by midwives and CHWs, not specialist obstetricians. Use resource-appropriate lab values (hemoglobin by cyanmethemoglobin, urine dipstick rather than 24h urine protein, RDT rather than microscopy for malaria in low-resource settings, etc.).
- **Anemia classification**: Use WHO pregnancy thresholds: Hb ≥11g/dL = normal, 10-10.9 = mild, 7-9.9 = moderate, <7 = severe. This is different from non-pregnant thresholds.
- **Context-switching test**: Vignettes deliberately mix endemic and non-endemic settings. The skill must correctly activate or suppress the malaria protocol based on the stated setting, not apply it universally.
