#!/usr/bin/env python3
"""
validate_anc_note.py — Deterministic validator for WHO ANC Contact Notes.

Checks an ANC Contact Note output against WHO guideline expectations derived
from the input vignette. Returns JSON with pass/fail per check.

Usage:
    python scripts/validate_anc_note.py --input <vignette.md> --output <anc_note.md>
    python scripts/validate_anc_note.py --output <anc_note.md>  # note-only checks
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def lower(text: str) -> str:
    return text.lower()


def has_any(text: str, terms: list[str]) -> bool:
    t = lower(text)
    return any(term in t for term in terms)


def has_all(text: str, terms: list[str]) -> bool:
    t = lower(text)
    return all(term in t for term in terms)


# ---------------------------------------------------------------------------
# Vignette parsing
# ---------------------------------------------------------------------------

def extract_ga_weeks(text: str) -> int | None:
    """Extract gestational age in weeks from vignette text."""
    patterns = [
        r"(?:GA|gestational age)[:\s]*(\d+)\s*(?:weeks|wks|w\b)",
        r"(\d+)\s*(?:weeks|wks)\s*(?:gestation|GA|by\s+(?:LMP|ultrasound|dating))",
        r"(\d+)\s*weeks?\s*(?:pregnant|pregnancy)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def extract_hb(text: str) -> float | None:
    """Extract hemoglobin value from vignette."""
    patterns = [
        r"(?:Hb|hemoglobin|haemoglobin)[:\s]*(\d+\.?\d*)\s*(?:g/dL|g/dl)?",
        r"(\d+\.?\d*)\s*g/dL\s*(?:\(Hb\))?",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def extract_bp(text: str) -> tuple[int, int] | None:
    """Extract blood pressure (systolic/diastolic) from vignette."""
    m = re.search(r"(?:BP|blood pressure)[:\s]*(\d{2,3})\s*/\s*(\d{2,3})", text, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def is_malaria_endemic(text: str) -> bool:
    t = lower(text)
    return any(kw in t for kw in [
        "malaria-endemic", "malaria endemic", "iptp", "iptsp",
        "western kenya", "sub-saharan", "subsaharan",
        "dar es salaam", "siaya", "endemic"
    ])


def is_hiv_positive(text: str) -> bool:
    t = lower(text)
    return any(kw in t for kw in [
        "hiv-positive", "hiv positive", "hiv+", "living with hiv",
        "hiv status: positive"
    ])


def is_on_cotrimoxazole(text: str) -> bool:
    t = lower(text)
    return any(kw in t for kw in ["cotrimoxazole", "septrin", "bactrim", "tmp-smx"])


def has_danger_signs(text: str) -> bool:
    danger_terms = [
        "seizure", "convulsion", "eclampsia",
        "bp 160", "bp 170", "bp 180", "160/110", "170/110", "180/",
        "severe headache", "blurred vision", "visual disturbance",
        "epigastric pain", "heavy bleeding", "vaginal bleeding",
        "unconscious", "difficulty breathing"
    ]
    return has_any(text, danger_terms)


def has_preeclampsia_risk_factors(text: str) -> dict:
    """Detect pre-eclampsia risk factors in vignette."""
    t = lower(text)
    high_factors = []
    moderate_factors = []

    # High risk factors
    if any(kw in t for kw in ["chronic hypertension", "chronic htn", "pre-existing hypertension"]):
        high_factors.append("chronic_htn")
    if any(kw in t for kw in ["history of pre-eclampsia", "previous pre-eclampsia", "prior pre-eclampsia"]):
        high_factors.append("prior_pe")
    if any(kw in t for kw in ["type 1 diabetes", "type 2 diabetes", "pre-existing diabetes"]):
        high_factors.append("diabetes")
    if any(kw in t for kw in ["renal disease", "kidney disease", "lupus", "sle ", "antiphospholipid"]):
        high_factors.append("autoimmune_renal")
    if any(kw in t for kw in ["twin", "triplet", "multiple pregnancy", "multiple gestation"]):
        high_factors.append("multiples")

    # Moderate risk factors
    if any(kw in t for kw in ["nulliparous", "g1p0", "g1 p0", "primigravida", "first pregnancy"]):
        moderate_factors.append("nulliparity")
    # Age
    age_m = re.search(r"(\d{2})\s*(?:yo|years? old|y/o|year-old)", t)
    if age_m and int(age_m.group(1)) >= 35:
        moderate_factors.append("age_gte_35")
    # BMI
    bmi_m = re.search(r"bmi[:\s]*(\d+\.?\d*)", t)
    if bmi_m and float(bmi_m.group(1)) > 30:
        moderate_factors.append("bmi_gt_30")
    if any(kw in t for kw in ["family history of pre-eclampsia", "mother had pre-eclampsia", "sister had pre-eclampsia"]):
        moderate_factors.append("family_hx_pe")

    return {
        "high": high_factors,
        "moderate": moderate_factors,
        "risk_level": "HIGH" if len(high_factors) >= 1 else ("MODERATE" if len(moderate_factors) >= 2 else "LOW")
    }


# ---------------------------------------------------------------------------
# Contact number mapping
# ---------------------------------------------------------------------------

def ga_to_expected_contact(ga: int, is_first_visit: bool = False) -> int | None:
    """Map GA to expected contact number."""
    if is_first_visit:
        return 1
    if ga <= 12:
        return 1
    elif ga <= 19:
        return None  # between contacts
    elif ga <= 25:
        return 2
    elif ga <= 29:
        return 3
    elif ga <= 33:
        return 4
    elif ga <= 35:
        return 5
    elif ga <= 37:
        return 6
    elif ga <= 39:
        return 7
    else:
        return 8


# ---------------------------------------------------------------------------
# Checks on the ANC note output
# ---------------------------------------------------------------------------

def check_required_sections(note: str) -> list[dict]:
    """Check that all required sections are present in the ANC note."""
    results = []
    sections = {
        "patient_summary": ["patient summary", "patient information", "demographics", "patient profile"],
        "hypertensive_status": ["hypertensive", "blood pressure classification", "bp classification", "hypertension status"],
        "risk_classification": ["risk classification", "risk assessment", "risk stratification", "risk level"],
        "assessments": ["assessment", "assessments required", "assessments performed", "investigations"],
        "recommendations": ["recommendation", "supplementation", "management plan", "plan"],
        "next_contact": ["next contact", "next visit", "follow-up", "next appointment"],
    }
    for section_name, keywords in sections.items():
        found = has_any(note, keywords)
        results.append({
            "check": f"section_present_{section_name}",
            "pass": found,
            "detail": f"Section '{section_name}' {'found' if found else 'NOT found'} in output"
        })
    return results


def check_ga_contact_consistency(note: str, ga: int | None) -> list[dict]:
    """Check that GA and contact number are consistent."""
    if ga is None:
        return [{"check": "ga_contact_consistency", "pass": True, "detail": "GA not extractable from vignette, skipping"}]

    expected = ga_to_expected_contact(ga)
    if expected is None:
        return [{"check": "ga_contact_consistency", "pass": True, "detail": f"GA {ga}w falls between standard contacts, skipping strict check"}]

    # Look for contact number in note
    contact_pattern = re.search(r"contact\s*#?\s*(\d)", lower(note))
    if contact_pattern:
        actual = int(contact_pattern.group(1))
        passed = actual == expected
        return [{
            "check": "ga_contact_consistency",
            "pass": passed,
            "detail": f"GA {ga}w → expected Contact {expected}, found Contact {actual}" + ("" if passed else " — MISMATCH")
        }]

    return [{"check": "ga_contact_consistency", "pass": True, "detail": "Contact number not explicitly stated, cannot verify"}]


def check_hypertensive_classification(note: str) -> list[dict]:
    """Check that hypertensive classification uses valid taxonomy terms."""
    valid_terms = [
        "chronic hypertension", "chronic htn",
        "gestational hypertension", "gestational htn",
        "pre-eclampsia", "preeclampsia", "pre eclampsia",
        "pre-eclampsia without severe features",
        "pre-eclampsia with severe features", "severe pre-eclampsia",
        "superimposed pre-eclampsia", "superimposed preeclampsia",
        "eclampsia",
        "normotensive", "normal blood pressure", "no hypertensive disorder"
    ]

    vague_terms = ["high blood pressure", "elevated bp", "raised blood pressure", "hypertension" ]

    t = lower(note)

    uses_valid = any(term in t for term in valid_terms)
    uses_vague_only = any(term in t for term in vague_terms) and not uses_valid

    if uses_vague_only:
        return [{
            "check": "hypertensive_classification_taxonomy",
            "pass": False,
            "detail": "Uses vague term (e.g., 'high blood pressure') without proper WHO taxonomy classification"
        }]

    return [{
        "check": "hypertensive_classification_taxonomy",
        "pass": True,
        "detail": "Hypertensive classification uses valid taxonomy" if uses_valid else "No hypertensive classification needed or present"
    }]


def check_iron_dose(note: str, hb: float | None) -> list[dict]:
    """Check iron supplementation dose is within WHO range."""
    t = lower(note)
    results = []

    # Check if iron is mentioned
    if "iron" not in t:
        results.append({
            "check": "iron_mentioned",
            "pass": False,
            "detail": "Iron supplementation not mentioned in output"
        })
        return results

    # Check dose appropriateness
    if hb is not None and hb < 10.0:
        # Should be therapeutic: 120mg
        if "120" in t or "therapeutic" in t:
            results.append({
                "check": "iron_dose_appropriate",
                "pass": True,
                "detail": f"Hb {hb} → therapeutic iron dose (120mg) correctly recommended"
            })
        elif any(d in t for d in ["30", "60", "30-60"]):
            results.append({
                "check": "iron_dose_appropriate",
                "pass": False,
                "detail": f"Hb {hb} (moderate anemia) but prophylactic dose (30-60mg) given instead of therapeutic (120mg)"
            })
        else:
            results.append({
                "check": "iron_dose_appropriate",
                "pass": False,
                "detail": f"Hb {hb} (anemia) — iron mentioned but specific dose not clear"
            })
    else:
        # Prophylactic is fine
        if any(d in t for d in ["30", "60", "30-60", "prophylactic"]):
            results.append({
                "check": "iron_dose_appropriate",
                "pass": True,
                "detail": "Prophylactic iron dose (30-60mg) correctly recommended"
            })
        elif "120" in t and (hb is None or hb >= 11.0):
            results.append({
                "check": "iron_dose_appropriate",
                "pass": False,
                "detail": f"Hb {hb} (normal) but therapeutic dose (120mg) given — should be prophylactic (30-60mg)"
            })
        else:
            results.append({
                "check": "iron_dose_appropriate",
                "pass": True,
                "detail": "Iron mentioned, dose appears reasonable"
            })

    return results


def check_folic_acid(note: str) -> list[dict]:
    """Check folic acid 400mcg is recommended."""
    t = lower(note)
    if "folic acid" in t or "folate" in t:
        if "400" in t:
            return [{"check": "folic_acid_dose", "pass": True, "detail": "Folic acid 400mcg recommended"}]
        return [{"check": "folic_acid_dose", "pass": True, "detail": "Folic acid mentioned (dose not explicitly 400mcg but present)"}]
    return [{"check": "folic_acid_dose", "pass": False, "detail": "Folic acid not mentioned in output"}]


def check_calcium_if_pe_risk(note: str, pe_risk: str) -> list[dict]:
    """Check calcium recommendation if high pre-eclampsia risk."""
    if pe_risk == "LOW":
        return []
    t = lower(note)
    if "calcium" in t:
        if "1.5" in t or "2g" in t or "1500" in t or "2000" in t:
            return [{"check": "calcium_for_pe_risk", "pass": True, "detail": f"PE risk {pe_risk} — calcium 1.5-2g recommended"}]
        return [{"check": "calcium_for_pe_risk", "pass": True, "detail": f"PE risk {pe_risk} — calcium mentioned"}]
    return [{"check": "calcium_for_pe_risk", "pass": False, "detail": f"PE risk {pe_risk} — calcium NOT recommended (should be for elevated PE risk)"}]


def check_aspirin_if_pe_risk(note: str, pe_risk: str, ga: int | None) -> list[dict]:
    """Check aspirin recommendation if high/moderate PE risk and GA >= 12 weeks."""
    if pe_risk == "LOW":
        return []
    if ga is not None and ga < 12:
        return []

    t = lower(note)
    if "aspirin" in t:
        if "75" in t or "81" in t or "150" in t:
            return [{"check": "aspirin_for_pe_risk", "pass": True, "detail": f"PE risk {pe_risk} — aspirin correctly recommended"}]
        return [{"check": "aspirin_for_pe_risk", "pass": True, "detail": f"PE risk {pe_risk} — aspirin mentioned"}]
    return [{"check": "aspirin_for_pe_risk", "pass": False, "detail": f"PE risk {pe_risk}, GA {ga}w — aspirin NOT recommended (should be for elevated PE risk)"}]


def check_iptp_sp(note: str, vignette: str, ga: int | None) -> list[dict]:
    """Check IPTp-SP recommendation logic."""
    if not is_malaria_endemic(vignette):
        return []

    t = lower(note)
    results = []

    if ga is not None and ga < 13:
        # Should NOT recommend IPTp-SP
        if "iptp" in t or "sp " in t or "sulfadoxine" in t:
            if any(neg in t for neg in ["not indicated", "not eligible", "contraindicated", "not yet", "not recommended"]):
                results.append({"check": "iptp_sp_first_trimester", "pass": True, "detail": "IPTp-SP correctly noted as not eligible in first trimester"})
            else:
                results.append({"check": "iptp_sp_first_trimester", "pass": False, "detail": "IPTp-SP appears to be recommended in first trimester — INCORRECT"})
        return results

    if is_on_cotrimoxazole(vignette):
        # Should NOT recommend IPTp-SP
        if "iptp" in t or "sulfadoxine" in t:
            if any(neg in t for neg in ["not indicated", "contraindicated", "not recommended", "not eligible"]):
                results.append({"check": "iptp_sp_cotrimoxazole", "pass": True, "detail": "IPTp-SP correctly withheld due to cotrimoxazole"})
            else:
                results.append({"check": "iptp_sp_cotrimoxazole", "pass": False, "detail": "IPTp-SP may be recommended despite cotrimoxazole use — INCORRECT"})
        return results

    # Should recommend IPTp-SP
    if has_any(t, ["iptp", "sulfadoxine", "sp dose", "sp as", "intermittent preventive"]):
        results.append({"check": "iptp_sp_recommended", "pass": True, "detail": f"IPTp-SP correctly recommended (endemic, GA {ga}w, eligible)"})
        # Check for DOT mention
        if has_any(t, ["directly observed", "dot", "observed therapy", "given at clinic", "administered at"]):
            results.append({"check": "iptp_sp_dot", "pass": True, "detail": "IPTp-SP DOT requirement mentioned"})
        else:
            results.append({"check": "iptp_sp_dot", "pass": False, "detail": "IPTp-SP DOT (directly observed therapy) not mentioned"})
    else:
        results.append({"check": "iptp_sp_recommended", "pass": False, "detail": f"Malaria-endemic setting, GA {ga}w, eligible — but IPTp-SP NOT recommended"})

    return results


def check_danger_signs_flagged(note: str, vignette: str) -> list[dict]:
    """Check that danger signs are flagged if present in vignette."""
    if not has_danger_signs(vignette):
        return []

    t = lower(note)
    danger_flagged = has_any(t, [
        "danger sign", "emergency", "immediate referral", "urgent",
        "refer immediately", "stabilize", "severe", "critical"
    ])

    return [{
        "check": "danger_signs_flagged",
        "pass": danger_flagged,
        "detail": "Danger signs prominently flagged in output" if danger_flagged else "Vignette contains danger signs but output does NOT flag them prominently"
    }]


def check_disclaimer(note: str) -> list[dict]:
    """Check that the clinical judgment disclaimer is present."""
    t = lower(note)
    has_disclaimer = has_any(t, [
        "clinical judgment", "qualified provider", "decision-support",
        "clinical decision", "healthcare provider", "medical professional",
        "disclaimer", "not a substitute"
    ])
    return [{
        "check": "disclaimer_present",
        "pass": has_disclaimer,
        "detail": "Clinical judgment disclaimer present" if has_disclaimer else "Disclaimer about clinical judgment NOT found"
    }]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate(vignette_path: str | None, note_path: str) -> dict:
    note = read_file(note_path)
    vignette = read_file(vignette_path) if vignette_path else ""

    ga = extract_ga_weeks(vignette) if vignette else None
    hb = extract_hb(vignette) if vignette else None
    pe_info = has_preeclampsia_risk_factors(vignette) if vignette else {"risk_level": "LOW"}

    all_checks: list[dict] = []

    # Structural checks (always run)
    all_checks.extend(check_required_sections(note))
    all_checks.extend(check_hypertensive_classification(note))
    all_checks.extend(check_folic_acid(note))
    all_checks.extend(check_disclaimer(note))

    # Vignette-informed checks
    if vignette:
        all_checks.extend(check_ga_contact_consistency(note, ga))
        all_checks.extend(check_iron_dose(note, hb))
        all_checks.extend(check_calcium_if_pe_risk(note, pe_info["risk_level"]))
        all_checks.extend(check_aspirin_if_pe_risk(note, pe_info["risk_level"], ga))
        all_checks.extend(check_iptp_sp(note, vignette, ga))
        all_checks.extend(check_danger_signs_flagged(note, vignette))

    passed = sum(1 for c in all_checks if c["pass"])
    failed = sum(1 for c in all_checks if not c["pass"])

    return {
        "vignette": vignette_path,
        "note": note_path,
        "extracted": {
            "ga_weeks": ga,
            "hemoglobin": hb,
            "pe_risk_level": pe_info["risk_level"],
            "malaria_endemic": is_malaria_endemic(vignette) if vignette else None,
            "hiv_positive": is_hiv_positive(vignette) if vignette else None,
            "danger_signs_present": has_danger_signs(vignette) if vignette else None,
        },
        "summary": {
            "total_checks": passed + failed,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / (passed + failed) * 100, 1) if (passed + failed) > 0 else 0,
        },
        "checks": all_checks,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate an ANC Contact Note against WHO guidelines")
    parser.add_argument("--input", "-i", help="Path to input vignette (optional, enables vignette-informed checks)")
    parser.add_argument("--output", "-o", required=True, help="Path to ANC Contact Note output to validate")
    args = parser.parse_args()

    result = validate(args.input, args.output)
    print(json.dumps(result, indent=2))

    # Exit code: 0 if all pass, 1 if any fail
    sys.exit(0 if result["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
