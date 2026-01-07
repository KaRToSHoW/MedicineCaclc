"""
Extended database seeding script with comprehensive medical calculators
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Calculator


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_calculators():
    """Seed database with comprehensive calculator data"""
    calculators_data = [
        # General Health
        {
            "name": "BMI Calculator",
            "description": "Calculate Body Mass Index",
            "category": "General Health",
            "formula": "{weight} / (({height} / 100) ** 2)",
            "input_fields": [
                {"name": "weight", "label": "Weight (kg)", "type": "number", "required": True, "min_value": 20, "max_value": 300},
                {"name": "height", "label": "Height (cm)", "type": "number", "required": True, "min_value": 100, "max_value": 250}
            ],
            "interpretation_rules": [
                {"condition": "< 18.5", "interpretation": "Underweight"},
                {"condition": ">= 18.5 and < 25", "interpretation": "Normal weight"},
                {"condition": ">= 25 and < 30", "interpretation": "Overweight"},
                {"condition": ">= 30", "interpretation": "Obese"}
            ]
        },
        {
            "name": "Basal Metabolic Rate",
            "description": "Calculate daily calorie needs (Harris-Benedict)",
            "category": "Nutrition",
            "formula": "88.362 + (13.397 * {weight}) + (4.799 * {height}) - (5.677 * {age})",
            "input_fields": [
                {"name": "weight", "label": "Weight (kg)", "type": "number", "required": True, "min_value": 20, "max_value": 300},
                {"name": "height", "label": "Height (cm)", "type": "number", "required": True, "min_value": 100, "max_value": 250},
                {"name": "age", "label": "Age (years)", "type": "number", "required": True, "min_value": 1, "max_value": 120}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Daily calorie needs calculated"}
            ]
        },
        {
            "name": "Body Surface Area (BSA)",
            "description": "Calculate BSA using Mosteller formula",
            "category": "General Health",
            "formula": "(({height} * {weight}) / 3600) ** 0.5",
            "input_fields": [
                {"name": "height", "label": "Height (cm)", "type": "number", "required": True, "min_value": 100, "max_value": 250},
                {"name": "weight", "label": "Weight (kg)", "type": "number", "required": True, "min_value": 20, "max_value": 300}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Body surface area in m²"}
            ]
        },
        {
            "name": "Ideal Body Weight",
            "description": "Calculate IBW using Devine formula (males)",
            "category": "General Health",
            "formula": "50 + 2.3 * (({height} / 2.54) - 60)",
            "input_fields": [
                {"name": "height", "label": "Height (cm)", "type": "number", "required": True, "min_value": 100, "max_value": 250}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Ideal body weight in kg"}
            ]
        },
        
        # Cardiology
        {
            "name": "HEART Score",
            "description": "Assess chest pain risk",
            "category": "Cardiology",
            "formula": "{history} + {ecg} + {age} + {risk_factors} + {troponin}",
            "input_fields": [
                {
                    "name": "history", "label": "History", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "Slightly suspicious"},
                        {"value": 1, "label": "Moderately suspicious"},
                        {"value": 2, "label": "Highly suspicious"}
                    ]
                },
                {
                    "name": "ecg", "label": "ECG", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "Normal"},
                        {"value": 1, "label": "Non-specific changes"},
                        {"value": 2, "label": "Significant changes"}
                    ]
                },
                {
                    "name": "age", "label": "Age", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "< 45 years"},
                        {"value": 1, "label": "45-64 years"},
                        {"value": 2, "label": "≥ 65 years"}
                    ]
                },
                {
                    "name": "risk_factors", "label": "Risk Factors", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "None"},
                        {"value": 1, "label": "1-2 factors"},
                        {"value": 2, "label": "≥ 3 factors"}
                    ]
                },
                {
                    "name": "troponin", "label": "Troponin", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "Normal"},
                        {"value": 1, "label": "1-3x normal"},
                        {"value": 2, "label": "> 3x normal"}
                    ]
                }
            ],
            "interpretation_rules": [
                {"condition": "<= 3", "interpretation": "Low risk (0.9-1.7% MACE)"},
                {"condition": ">= 4 and < 7", "interpretation": "Moderate risk (12-16.6% MACE)"},
                {"condition": ">= 7", "interpretation": "High risk (50-65% MACE)"}
            ]
        },
        {
            "name": "Mean Arterial Pressure",
            "description": "Calculate MAP from blood pressure",
            "category": "Cardiology",
            "formula": "{diastolic} + ({systolic} - {diastolic}) / 3",
            "input_fields": [
                {"name": "systolic", "label": "Systolic BP (mmHg)", "type": "number", "required": True, "min_value": 60, "max_value": 250},
                {"name": "diastolic", "label": "Diastolic BP (mmHg)", "type": "number", "required": True, "min_value": 40, "max_value": 150}
            ],
            "interpretation_rules": [
                {"condition": "< 70", "interpretation": "Low MAP - risk of inadequate perfusion"},
                {"condition": ">= 70 and <= 100", "interpretation": "Normal MAP"},
                {"condition": "> 100", "interpretation": "High MAP - hypertensive"}
            ]
        },
        {
            "name": "QTc Interval (Bazett)",
            "description": "Calculate corrected QT interval",
            "category": "Cardiology",
            "formula": "{qt} / ({rr} ** 0.5)",
            "input_fields": [
                {"name": "qt", "label": "QT interval (ms)", "type": "number", "required": True, "min_value": 200, "max_value": 700},
                {"name": "rr", "label": "RR interval (s)", "type": "number", "required": True, "min_value": 0.4, "max_value": 2.0}
            ],
            "interpretation_rules": [
                {"condition": "< 440", "interpretation": "Normal QTc (males: <440ms, females: <460ms)"},
                {"condition": ">= 440 and < 500", "interpretation": "Borderline prolonged QTc"},
                {"condition": ">= 500", "interpretation": "Prolonged QTc - increased risk of arrhythmia"}
            ]
        },
        {
            "name": "CHA2DS2-VASc Score",
            "description": "Stroke risk in atrial fibrillation",
            "category": "Cardiology",
            "formula": "{chf} + {hypertension} + {age} + {diabetes} + {stroke} + {vascular} + {sex}",
            "input_fields": [
                {"name": "chf", "label": "CHF/LV dysfunction", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "hypertension", "label": "Hypertension", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "age", "label": "Age", "type": "select", "required": True, "options": [{"value": 0, "label": "<65"}, {"value": 1, "label": "65-74"}, {"value": 2, "label": "≥75"}]},
                {"name": "diabetes", "label": "Diabetes", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "stroke", "label": "Prior stroke/TIA", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 2, "label": "Yes"}]},
                {"name": "vascular", "label": "Vascular disease", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "sex", "label": "Sex", "type": "select", "required": True, "options": [{"value": 0, "label": "Male"}, {"value": 1, "label": "Female"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "0% annual stroke risk"},
                {"condition": "== 1", "interpretation": "1.3% annual stroke risk"},
                {"condition": "== 2", "interpretation": "2.2% annual stroke risk"},
                {"condition": ">= 3", "interpretation": "≥3.2% annual stroke risk - anticoagulation recommended"}
            ]
        },
        
        # Nephrology
        {
            "name": "Creatinine Clearance",
            "description": "Calculate kidney function (Cockcroft-Gault)",
            "category": "Nephrology",
            "formula": "((140 - {age}) * {weight}) / (72 * {creatinine})",
            "input_fields": [
                {"name": "age", "label": "Age (years)", "type": "number", "required": True, "min_value": 1, "max_value": 120},
                {"name": "weight", "label": "Weight (kg)", "type": "number", "required": True, "min_value": 20, "max_value": 300},
                {"name": "creatinine", "label": "Serum Creatinine (mg/dL)", "type": "number", "required": True, "min_value": 0.1, "max_value": 20}
            ],
            "interpretation_rules": [
                {"condition": "< 30", "interpretation": "Stage 4-5 CKD: Severe kidney disease"},
                {"condition": ">= 30 and < 60", "interpretation": "Stage 3 CKD: Moderate kidney disease"},
                {"condition": ">= 60 and < 90", "interpretation": "Stage 2 CKD: Mild kidney disease"},
                {"condition": ">= 90", "interpretation": "Stage 1: Normal kidney function"}
            ]
        },
        {
            "name": "eGFR (MDRD)",
            "description": "Estimated glomerular filtration rate",
            "category": "Nephrology",
            "formula": "175 * ({creatinine} ** -1.154) * ({age} ** -0.203)",
            "input_fields": [
                {"name": "creatinine", "label": "Serum Creatinine (mg/dL)", "type": "number", "required": True, "min_value": 0.1, "max_value": 20},
                {"name": "age", "label": "Age (years)", "type": "number", "required": True, "min_value": 18, "max_value": 120}
            ],
            "interpretation_rules": [
                {"condition": "< 15", "interpretation": "Stage 5 CKD: Kidney failure"},
                {"condition": ">= 15 and < 30", "interpretation": "Stage 4 CKD: Severe reduction"},
                {"condition": ">= 30 and < 60", "interpretation": "Stage 3 CKD: Moderate reduction"},
                {"condition": ">= 60 and < 90", "interpretation": "Stage 2 CKD: Mild reduction"},
                {"condition": ">= 90", "interpretation": "Stage 1: Normal or high"}
            ]
        },
        {
            "name": "Fractional Excretion of Sodium",
            "description": "Differentiate types of acute kidney injury",
            "category": "Nephrology",
            "formula": "({urine_sodium} * {plasma_creatinine} / ({plasma_sodium} * {urine_creatinine})) * 100",
            "input_fields": [
                {"name": "urine_sodium", "label": "Urine Sodium (mEq/L)", "type": "number", "required": True, "min_value": 1, "max_value": 300},
                {"name": "plasma_sodium", "label": "Plasma Sodium (mEq/L)", "type": "number", "required": True, "min_value": 100, "max_value": 200},
                {"name": "urine_creatinine", "label": "Urine Creatinine (mg/dL)", "type": "number", "required": True, "min_value": 1, "max_value": 500},
                {"name": "plasma_creatinine", "label": "Plasma Creatinine (mg/dL)", "type": "number", "required": True, "min_value": 0.1, "max_value": 20}
            ],
            "interpretation_rules": [
                {"condition": "< 1", "interpretation": "Pre-renal AKI (volume depletion)"},
                {"condition": ">= 1 and < 2", "interpretation": "Indeterminate"},
                {"condition": ">= 2", "interpretation": "Intrinsic renal AKI"}
            ]
        },
        
        # Neurology
        {
            "name": "Glasgow Coma Scale",
            "description": "Assess level of consciousness",
            "category": "Neurology",
            "formula": "{eye_opening} + {verbal_response} + {motor_response}",
            "input_fields": [
                {
                    "name": "eye_opening", "label": "Eye Opening", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "No response"},
                        {"value": 2, "label": "To pain"},
                        {"value": 3, "label": "To speech"},
                        {"value": 4, "label": "Spontaneous"}
                    ]
                },
                {
                    "name": "verbal_response", "label": "Verbal Response", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "No response"},
                        {"value": 2, "label": "Incomprehensible sounds"},
                        {"value": 3, "label": "Inappropriate words"},
                        {"value": 4, "label": "Confused"},
                        {"value": 5, "label": "Oriented"}
                    ]
                },
                {
                    "name": "motor_response", "label": "Motor Response", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "No response"},
                        {"value": 2, "label": "Decerebrate posture"},
                        {"value": 3, "label": "Decorticate posture"},
                        {"value": 4, "label": "Withdraws from pain"},
                        {"value": 5, "label": "Localizes pain"},
                        {"value": 6, "label": "Obeys commands"}
                    ]
                }
            ],
            "interpretation_rules": [
                {"condition": "== 3", "interpretation": "GCS 3: Deep coma or death"},
                {"condition": "> 3 and <= 8", "interpretation": "GCS 4-8: Severe (Coma)"},
                {"condition": "> 8 and <= 12", "interpretation": "GCS 9-12: Moderate"},
                {"condition": "> 12 and < 15", "interpretation": "GCS 13-14: Mild"},
                {"condition": "== 15", "interpretation": "GCS 15: Normal"}
            ]
        },
        {
            "name": "NIH Stroke Scale (simplified)",
            "description": "Assess stroke severity (simplified version)",
            "category": "Neurology",
            "formula": "{consciousness} + {gaze} + {visual} + {facial} + {motor_arm} + {motor_leg} + {ataxia} + {sensory} + {language} + {dysarthria} + {extinction}",
            "input_fields": [
                {"name": "consciousness", "label": "Level of Consciousness", "type": "select", "required": True, "options": [{"value": 0, "label": "Alert"}, {"value": 1, "label": "Drowsy"}, {"value": 2, "label": "Stuporous"}, {"value": 3, "label": "Coma"}]},
                {"name": "gaze", "label": "Gaze", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Partial palsy"}, {"value": 2, "label": "Forced deviation"}]},
                {"name": "visual", "label": "Visual", "type": "select", "required": True, "options": [{"value": 0, "label": "No loss"}, {"value": 1, "label": "Partial"}, {"value": 2, "label": "Complete"}, {"value": 3, "label": "Bilateral"}]},
                {"name": "facial", "label": "Facial Palsy", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Minor"}, {"value": 2, "label": "Partial"}, {"value": 3, "label": "Complete"}]},
                {"name": "motor_arm", "label": "Motor Arm", "type": "select", "required": True, "options": [{"value": 0, "label": "No drift"}, {"value": 1, "label": "Drift"}, {"value": 2, "label": "Some effort"}, {"value": 3, "label": "No effort"}, {"value": 4, "label": "No movement"}]},
                {"name": "motor_leg", "label": "Motor Leg", "type": "select", "required": True, "options": [{"value": 0, "label": "No drift"}, {"value": 1, "label": "Drift"}, {"value": 2, "label": "Some effort"}, {"value": 3, "label": "No effort"}, {"value": 4, "label": "No movement"}]},
                {"name": "ataxia", "label": "Ataxia", "type": "select", "required": True, "options": [{"value": 0, "label": "Absent"}, {"value": 1, "label": "Present one limb"}, {"value": 2, "label": "Present two limbs"}]},
                {"name": "sensory", "label": "Sensory", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Mild loss"}, {"value": 2, "label": "Severe loss"}]},
                {"name": "language", "label": "Language", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Mild aphasia"}, {"value": 2, "label": "Severe aphasia"}, {"value": 3, "label": "Mute"}]},
                {"name": "dysarthria", "label": "Dysarthria", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Mild"}, {"value": 2, "label": "Severe"}]},
                {"name": "extinction", "label": "Extinction/Inattention", "type": "select", "required": True, "options": [{"value": 0, "label": "Normal"}, {"value": 1, "label": "Mild"}, {"value": 2, "label": "Severe"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "No stroke symptoms"},
                {"condition": "> 0 and <= 4", "interpretation": "Minor stroke"},
                {"condition": "> 4 and <= 15", "interpretation": "Moderate stroke"},
                {"condition": "> 15 and <= 20", "interpretation": "Moderate to severe stroke"},
                {"condition": "> 20", "interpretation": "Severe stroke"}
            ]
        },
        
        # Pediatrics
        {
            "name": "Pediatric Weight Estimation",
            "description": "Estimate child weight by age (Broselow)",
            "category": "Pediatrics",
            "formula": "(2 * {age}) + 8",
            "input_fields": [
                {"name": "age", "label": "Age (years)", "type": "number", "required": True, "min_value": 1, "max_value": 10}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Estimated weight in kg"}
            ]
        },
        {
            "name": "Apgar Score",
            "description": "Assess newborn health at 1 and 5 minutes",
            "category": "Pediatrics",
            "formula": "{appearance} + {pulse} + {grimace} + {activity} + {respiration}",
            "input_fields": [
                {"name": "appearance", "label": "Appearance (color)", "type": "select", "required": True, "options": [{"value": 0, "label": "Blue/pale"}, {"value": 1, "label": "Body pink, extremities blue"}, {"value": 2, "label": "Completely pink"}]},
                {"name": "pulse", "label": "Pulse (heart rate)", "type": "select", "required": True, "options": [{"value": 0, "label": "Absent"}, {"value": 1, "label": "<100 bpm"}, {"value": 2, "label": ">100 bpm"}]},
                {"name": "grimace", "label": "Grimace (reflex)", "type": "select", "required": True, "options": [{"value": 0, "label": "No response"}, {"value": 1, "label": "Grimace"}, {"value": 2, "label": "Cry/cough"}]},
                {"name": "activity", "label": "Activity (muscle tone)", "type": "select", "required": True, "options": [{"value": 0, "label": "Limp"}, {"value": 1, "label": "Some flexion"}, {"value": 2, "label": "Active motion"}]},
                {"name": "respiration", "label": "Respiration", "type": "select", "required": True, "options": [{"value": 0, "label": "Absent"}, {"value": 1, "label": "Weak/irregular"}, {"value": 2, "label": "Strong cry"}]}
            ],
            "interpretation_rules": [
                {"condition": "<= 3", "interpretation": "Critical - immediate intervention needed"},
                {"condition": "> 3 and <= 6", "interpretation": "Fairly low - may need intervention"},
                {"condition": "> 6", "interpretation": "Normal - good condition"}
            ]
        },
        
        # Pulmonology
        {
            "name": "CURB-65 Score",
            "description": "Pneumonia severity assessment",
            "category": "Pulmonology",
            "formula": "{confusion} + {urea} + {respiratory_rate} + {blood_pressure} + {age}",
            "input_fields": [
                {"name": "confusion", "label": "Confusion", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "urea", "label": "BUN > 19 mg/dL", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "respiratory_rate", "label": "RR ≥ 30/min", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "blood_pressure", "label": "SBP <90 or DBP ≤60", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "age", "label": "Age ≥ 65", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Low risk - outpatient treatment"},
                {"condition": "== 1", "interpretation": "Low risk - consider outpatient"},
                {"condition": "== 2", "interpretation": "Moderate risk - hospital admission"},
                {"condition": ">= 3", "interpretation": "High risk - ICU consideration"}
            ]
        },
        {
            "name": "Wells' Criteria for PE",
            "description": "Assess pulmonary embolism probability",
            "category": "Pulmonology",
            "formula": "{clinical_signs} + {pe_likely} + {heart_rate} + {immobilization} + {previous_pe} + {hemoptysis} + {malignancy}",
            "input_fields": [
                {"name": "clinical_signs", "label": "Clinical signs of DVT", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes"}]},
                {"name": "pe_likely", "label": "PE most likely diagnosis", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes"}]},
                {"name": "heart_rate", "label": "Heart rate > 100", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "immobilization", "label": "Immobilization/surgery", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "previous_pe", "label": "Previous PE/DVT", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "hemoptysis", "label": "Hemoptysis", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "malignancy", "label": "Malignancy", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "< 2", "interpretation": "Low probability (3.6%)"},
                {"condition": ">= 2 and < 6", "interpretation": "Moderate probability (20.5%)"},
                {"condition": ">= 6", "interpretation": "High probability (66.7%)"}
            ]
        },
        
        # Hematology
        {
            "name": "Absolute Neutrophil Count",
            "description": "Calculate ANC from WBC differential",
            "category": "Hematology",
            "formula": "{wbc} * ({neutrophils} + {bands}) / 100",
            "input_fields": [
                {"name": "wbc", "label": "WBC count (cells/μL)", "type": "number", "required": True, "min_value": 100, "max_value": 100000},
                {"name": "neutrophils", "label": "Neutrophils (%)", "type": "number", "required": True, "min_value": 0, "max_value": 100},
                {"name": "bands", "label": "Bands (%)", "type": "number", "required": True, "min_value": 0, "max_value": 100}
            ],
            "interpretation_rules": [
                {"condition": "< 500", "interpretation": "Severe neutropenia - high infection risk"},
                {"condition": ">= 500 and < 1000", "interpretation": "Moderate neutropenia"},
                {"condition": ">= 1000 and < 1500", "interpretation": "Mild neutropenia"},
                {"condition": ">= 1500", "interpretation": "Normal ANC"}
            ]
        },
        {
            "name": "Corrected Calcium",
            "description": "Adjust calcium for albumin level",
            "category": "Hematology",
            "formula": "{calcium} + 0.8 * (4 - {albumin})",
            "input_fields": [
                {"name": "calcium", "label": "Serum Calcium (mg/dL)", "type": "number", "required": True, "min_value": 1, "max_value": 20},
                {"name": "albumin", "label": "Serum Albumin (g/dL)", "type": "number", "required": True, "min_value": 1, "max_value": 6}
            ],
            "interpretation_rules": [
                {"condition": "< 8.5", "interpretation": "Hypocalcemia"},
                {"condition": ">= 8.5 and <= 10.5", "interpretation": "Normal calcium"},
                {"condition": "> 10.5", "interpretation": "Hypercalcemia"}
            ]
        },
        
        # Emergency Medicine
        {
            "name": "Revised Trauma Score",
            "description": "Assess trauma severity",
            "category": "Emergency",
            "formula": "0.9368 * {gcs} + 0.7326 * {sbp} + 0.2908 * {rr}",
            "input_fields": [
                {"name": "gcs", "label": "Glasgow Coma Scale", "type": "select", "required": True, "options": [{"value": 0, "label": "3"}, {"value": 1, "label": "4-5"}, {"value": 2, "label": "6-8"}, {"value": 3, "label": "9-12"}, {"value": 4, "label": "13-15"}]},
                {"name": "sbp", "label": "Systolic BP", "type": "select", "required": True, "options": [{"value": 0, "label": "0"}, {"value": 1, "label": "1-49"}, {"value": 2, "label": "50-75"}, {"value": 3, "label": "76-89"}, {"value": 4, "label": ">89"}]},
                {"name": "rr", "label": "Respiratory Rate", "type": "select", "required": True, "options": [{"value": 0, "label": "0"}, {"value": 1, "label": "1-5"}, {"value": 2, "label": "6-9"}, {"value": 3, "label": ">29"}, {"value": 4, "label": "10-29"}]}
            ],
            "interpretation_rules": [
                {"condition": "< 4", "interpretation": "Severe trauma - critical"},
                {"condition": ">= 4 and < 7", "interpretation": "Moderate trauma"},
                {"condition": ">= 7", "interpretation": "Minor trauma"}
            ]
        },
        {
            "name": "Anion Gap",
            "description": "Calculate serum anion gap",
            "category": "Emergency",
            "formula": "{sodium} - ({chloride} + {bicarbonate})",
            "input_fields": [
                {"name": "sodium", "label": "Sodium (mEq/L)", "type": "number", "required": True, "min_value": 100, "max_value": 200},
                {"name": "chloride", "label": "Chloride (mEq/L)", "type": "number", "required": True, "min_value": 50, "max_value": 150},
                {"name": "bicarbonate", "label": "Bicarbonate (mEq/L)", "type": "number", "required": True, "min_value": 5, "max_value": 50}
            ],
            "interpretation_rules": [
                {"condition": "< 3", "interpretation": "Low anion gap"},
                {"condition": ">= 3 and <= 11", "interpretation": "Normal anion gap"},
                {"condition": "> 11 and <= 16", "interpretation": "Borderline high"},
                {"condition": "> 16", "interpretation": "High anion gap metabolic acidosis"}
            ]
        },
        
        # Obstetrics
        {
            "name": "Bishop Score",
            "description": "Assess cervical favorability for induction",
            "category": "Obstetrics",
            "formula": "{dilation} + {effacement} + {station} + {consistency} + {position}",
            "input_fields": [
                {"name": "dilation", "label": "Cervical Dilation", "type": "select", "required": True, "options": [{"value": 0, "label": "Closed"}, {"value": 1, "label": "1-2 cm"}, {"value": 2, "label": "3-4 cm"}, {"value": 3, "label": "≥5 cm"}]},
                {"name": "effacement", "label": "Effacement", "type": "select", "required": True, "options": [{"value": 0, "label": "0-30%"}, {"value": 1, "label": "40-50%"}, {"value": 2, "label": "60-70%"}, {"value": 3, "label": "≥80%"}]},
                {"name": "station", "label": "Station", "type": "select", "required": True, "options": [{"value": 0, "label": "-3"}, {"value": 1, "label": "-2"}, {"value": 2, "label": "-1, 0"}, {"value": 3, "label": "+1, +2"}]},
                {"name": "consistency", "label": "Cervical Consistency", "type": "select", "required": True, "options": [{"value": 0, "label": "Firm"}, {"value": 1, "label": "Medium"}, {"value": 2, "label": "Soft"}]},
                {"name": "position", "label": "Cervical Position", "type": "select", "required": True, "options": [{"value": 0, "label": "Posterior"}, {"value": 1, "label": "Mid"}, {"value": 2, "label": "Anterior"}]}
            ],
            "interpretation_rules": [
                {"condition": "<= 5", "interpretation": "Unfavorable - induction may fail"},
                {"condition": "> 5 and <= 8", "interpretation": "Moderately favorable"},
                {"condition": "> 8", "interpretation": "Favorable - high success rate"}
            ]
        },
        
        # Endocrinology
        {
            "name": "Corrected Sodium",
            "description": "Adjust sodium for hyperglycemia",
            "category": "Endocrinology",
            "formula": "{sodium} + 0.024 * ({glucose} - 100)",
            "input_fields": [
                {"name": "sodium", "label": "Measured Sodium (mEq/L)", "type": "number", "required": True, "min_value": 100, "max_value": 200},
                {"name": "glucose", "label": "Glucose (mg/dL)", "type": "number", "required": True, "min_value": 50, "max_value": 1000}
            ],
            "interpretation_rules": [
                {"condition": "< 135", "interpretation": "Hyponatremia"},
                {"condition": ">= 135 and <= 145", "interpretation": "Normal sodium"},
                {"condition": "> 145", "interpretation": "Hypernatremia"}
            ]
        },
        {
            "name": "HbA1c to Average Glucose",
            "description": "Convert HbA1c to estimated average glucose",
            "category": "Endocrinology",
            "formula": "28.7 * {hba1c} - 46.7",
            "input_fields": [
                {"name": "hba1c", "label": "HbA1c (%)", "type": "number", "required": True, "min_value": 4, "max_value": 15}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Estimated average glucose in mg/dL"}
            ]
        },
        
        # Hepatology
        {
            "name": "Child-Pugh Score",
            "description": "Assess cirrhosis severity",
            "category": "Hepatology",
            "formula": "{bilirubin} + {albumin} + {inr} + {ascites} + {encephalopathy}",
            "input_fields": [
                {"name": "bilirubin", "label": "Bilirubin", "type": "select", "required": True, "options": [{"value": 1, "label": "<2 mg/dL"}, {"value": 2, "label": "2-3 mg/dL"}, {"value": 3, "label": ">3 mg/dL"}]},
                {"name": "albumin", "label": "Albumin", "type": "select", "required": True, "options": [{"value": 1, "label": ">3.5 g/dL"}, {"value": 2, "label": "2.8-3.5 g/dL"}, {"value": 3, "label": "<2.8 g/dL"}]},
                {"name": "inr", "label": "INR", "type": "select", "required": True, "options": [{"value": 1, "label": "<1.7"}, {"value": 2, "label": "1.7-2.3"}, {"value": 3, "label": ">2.3"}]},
                {"name": "ascites", "label": "Ascites", "type": "select", "required": True, "options": [{"value": 1, "label": "None"}, {"value": 2, "label": "Slight"}, {"value": 3, "label": "Moderate"}]},
                {"name": "encephalopathy", "label": "Encephalopathy", "type": "select", "required": True, "options": [{"value": 1, "label": "None"}, {"value": 2, "label": "Grade 1-2"}, {"value": 3, "label": "Grade 3-4"}]}
            ],
            "interpretation_rules": [
                {"condition": "<= 6", "interpretation": "Class A - good prognosis (1-year survival 100%, 2-year 85%)"},
                {"condition": "> 6 and <= 9", "interpretation": "Class B - moderate prognosis (1-year survival 80%, 2-year 60%)"},
                {"condition": "> 9", "interpretation": "Class C - poor prognosis (1-year survival 45%, 2-year 35%)"}
            ]
        },
        {
            "name": "MELD Score",
            "description": "Model for End-Stage Liver Disease",
            "category": "Hepatology",
            "formula": "9.57 * {ln_creatinine} + 3.78 * {ln_bilirubin} + 11.2 * {ln_inr} + 6.43",
            "input_fields": [
                {"name": "ln_creatinine", "label": "Ln(Creatinine mg/dL)", "type": "number", "required": True, "min_value": -2, "max_value": 3},
                {"name": "ln_bilirubin", "label": "Ln(Bilirubin mg/dL)", "type": "number", "required": True, "min_value": -2, "max_value": 5},
                {"name": "ln_inr", "label": "Ln(INR)", "type": "number", "required": True, "min_value": -2, "max_value": 3}
            ],
            "interpretation_rules": [
                {"condition": "< 10", "interpretation": "Low risk - 1.9% 3-month mortality"},
                {"condition": ">= 10 and < 20", "interpretation": "Moderate risk - 6% 3-month mortality"},
                {"condition": ">= 20 and < 30", "interpretation": "High risk - 19.6% 3-month mortality"},
                {"condition": ">= 30 and < 40", "interpretation": "Very high risk - 52.6% 3-month mortality"},
                {"condition": ">= 40", "interpretation": "Critical - 71.3% 3-month mortality"}
            ]
        },
        
        # Infectious Disease
        {
            "name": "Centor Score",
            "description": "Assess streptococcal pharyngitis probability",
            "category": "Infectious Disease",
            "formula": "{tonsillar_exudate} + {tender_nodes} + {fever} + {no_cough}",
            "input_fields": [
                {"name": "tonsillar_exudate", "label": "Tonsillar exudate", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "tender_nodes", "label": "Tender anterior cervical nodes", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "fever", "label": "Fever >38°C", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "no_cough", "label": "Absence of cough", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "2.5% probability - no testing/treatment"},
                {"condition": "== 1", "interpretation": "6.5% probability - no testing/treatment"},
                {"condition": "== 2", "interpretation": "15% probability - rapid strep test"},
                {"condition": "== 3", "interpretation": "32% probability - rapid strep test"},
                {"condition": "== 4", "interpretation": "56% probability - empiric antibiotics"}
            ]
        }
    ]
    
    async with AsyncSessionLocal() as session:
        # Delete existing calculators
        await session.execute(delete(Calculator))
        await session.commit()
        print("Cleared existing calculators")
        
        # Add new calculators
        valid_fields = {'name', 'description', 'category', 'formula', 'input_fields', 'interpretation_rules'}
        
        for calc_data in calculators_data:
            filtered_data = {k: v for k, v in calc_data.items() if k in valid_fields}
            calculator = Calculator(**filtered_data)
            session.add(calculator)
        
        await session.commit()
        print(f"Successfully seeded {len(calculators_data)} calculators")


async def main():
    """Main function"""
    print("Creating database tables...")
    await create_tables()
    print("Tables created successfully!")
    
    print("\nSeeding calculators...")
    await seed_calculators()
    print("Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(main())
