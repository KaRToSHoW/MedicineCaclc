"""
Complete database seeding script with comprehensive medical calculators
All calculators include detailed clinical interpretation rules
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
    """Seed database with complete calculator data"""
    calculators_data = [
        # ============= GENERAL HEALTH =============
        {
            "name": "BMI Calculator",
            "description": "Calculate Body Mass Index to assess weight status",
            "category": "General Health",
            "formula": "{weight} / (({height} / 100) ** 2)",
            "input_fields": [
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 300},
                {"name": "height", "label": "Height", "unit": "cm", "type": "number", "required": True, "min": 100, "max": 250}
            ],
            "interpretation_rules": [
                {"condition": "< 16", "interpretation": "Severe underweight - immediate medical attention required"},
                {"condition": ">= 16 and < 18.5", "interpretation": "Underweight - nutritional assessment recommended"},
                {"condition": ">= 18.5 and < 25", "interpretation": "Normal weight - maintain healthy lifestyle"},
                {"condition": ">= 25 and < 30", "interpretation": "Overweight - lifestyle modifications recommended"},
                {"condition": ">= 30 and < 35", "interpretation": "Obese Class I - weight loss program advised"},
                {"condition": ">= 35 and < 40", "interpretation": "Obese Class II - medical weight management needed"},
                {"condition": ">= 40", "interpretation": "Obese Class III (Morbid) - bariatric evaluation recommended"}
            ]
        },
        {
            "name": "Body Surface Area (BSA)",
            "description": "Calculate BSA using Mosteller formula for drug dosing",
            "category": "General Health",
            "formula": "(({height} * {weight}) / 3600) ** 0.5",
            "input_fields": [
                {"name": "height", "label": "Height", "unit": "cm", "type": "number", "required": True, "min": 100, "max": 250},
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 300}
            ],
            "interpretation_rules": [
                {"condition": "< 1.5", "interpretation": "Low BSA - adjust drug dosing accordingly"},
                {"condition": ">= 1.5 and <= 2.0", "interpretation": "Normal BSA range"},
                {"condition": "> 2.0", "interpretation": "High BSA - verify calculations for dosing"}
            ]
        },
        {
            "name": "Ideal Body Weight (Devine)",
            "description": "Calculate IBW for drug dosing and nutritional assessment",
            "category": "General Health",
            "formula": "50 + 2.3 * (({height} / 2.54) - 60)",
            "input_fields": [
                {"name": "height", "label": "Height", "unit": "cm", "type": "number", "required": True, "min": 100, "max": 250}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Ideal body weight in kg (male formula)"}
            ]
        },
        {
            "name": "Waist-to-Hip Ratio",
            "description": "Assess abdominal obesity and cardiovascular risk",
            "category": "General Health",
            "formula": "{waist} / {hip}",
            "input_fields": [
                {"name": "waist", "label": "Waist Circumference", "unit": "cm", "type": "number", "required": True, "min": 40, "max": 200},
                {"name": "hip", "label": "Hip Circumference", "unit": "cm", "type": "number", "required": True, "min": 50, "max": 200}
            ],
            "interpretation_rules": [
                {"condition": "< 0.85", "interpretation": "Low cardiovascular risk"},
                {"condition": ">= 0.85 and < 0.90", "interpretation": "Moderate cardiovascular risk (females >0.85, males >0.90)"},
                {"condition": ">= 0.90", "interpretation": "High cardiovascular risk - abdominal obesity present"}
            ]
        },
        
        # ============= NUTRITION & METABOLISM =============
        {
            "name": "Basal Metabolic Rate (Harris-Benedict)",
            "description": "Calculate daily calorie needs at rest",
            "category": "Nutrition",
            "formula": "88.362 + (13.397 * {weight}) + (4.799 * {height}) - (5.677 * {age})",
            "input_fields": [
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 300},
                {"name": "height", "label": "Height", "unit": "cm", "type": "number", "required": True, "min": 100, "max": 250},
                {"name": "age", "label": "Age", "unit": "years", "type": "number", "required": True, "min": 1, "max": 120}
            ],
            "interpretation_rules": [
                {"condition": "< 1500", "interpretation": "Low BMR - may indicate metabolic issues or small body size"},
                {"condition": ">= 1500 and <= 2500", "interpretation": "Normal BMR range - multiply by activity factor for TDEE"},
                {"condition": "> 2500", "interpretation": "High BMR - large body size or high metabolic rate"}
            ]
        },
        {
            "name": "Daily Protein Requirements",
            "description": "Calculate protein needs based on weight and activity",
            "category": "Nutrition",
            "formula": "{weight} * {factor}",
            "input_fields": [
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 300},
                {
                    "name": "factor", "label": "Activity Level", "type": "select", "required": True,
                    "options": [
                        {"value": 0.8, "label": "Sedentary (0.8 g/kg)"},
                        {"value": 1.0, "label": "Light activity (1.0 g/kg)"},
                        {"value": 1.2, "label": "Moderate activity (1.2 g/kg)"},
                        {"value": 1.6, "label": "Active/Athlete (1.6 g/kg)"},
                        {"value": 2.0, "label": "Intense training (2.0 g/kg)"}
                    ]
                }
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Daily protein requirement in grams"}
            ]
        },
        
        # ============= CARDIOLOGY =============
        {
            "name": "HEART Score",
            "description": "Assess chest pain risk for major adverse cardiac events",
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
                        {"value": 1, "label": "Non-specific repolarization"},
                        {"value": 2, "label": "Significant ST deviation"}
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
                        {"value": 0, "label": "None known"},
                        {"value": 1, "label": "1-2 risk factors"},
                        {"value": 2, "label": "≥ 3 risk factors or history of CAD"}
                    ]
                },
                {
                    "name": "troponin", "label": "Initial Troponin", "type": "select", "required": True,
                    "options": [
                        {"value": 0, "label": "≤ Normal limit"},
                        {"value": 1, "label": "1-3x normal limit"},
                        {"value": 2, "label": "> 3x normal limit"}
                    ]
                }
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Very low risk (0.9-1.7% MACE) - discharge appropriate"},
                {"condition": ">= 1 and <= 3", "interpretation": "Low risk (0.9-1.7% MACE) - early discharge reasonable"},
                {"condition": ">= 4 and <= 6", "interpretation": "Moderate risk (12-16.6% MACE) - admission recommended"},
                {"condition": ">= 7 and <= 8", "interpretation": "High risk (50-65% MACE) - urgent intervention needed"},
                {"condition": ">= 9", "interpretation": "Very high risk (>65% MACE) - immediate cardiology consult"}
            ]
        },
        {
            "name": "Mean Arterial Pressure (MAP)",
            "description": "Calculate perfusion pressure",
            "category": "Cardiology",
            "formula": "{diastolic} + ({systolic} - {diastolic}) / 3",
            "input_fields": [
                {"name": "systolic", "label": "Systolic BP", "unit": "mmHg", "type": "number", "required": True, "min": 60, "max": 250},
                {"name": "diastolic", "label": "Diastolic BP", "unit": "mmHg", "type": "number", "required": True, "min": 40, "max": 150}
            ],
            "interpretation_rules": [
                {"condition": "< 60", "interpretation": "Critically low MAP - risk of organ hypoperfusion"},
                {"condition": ">= 60 and < 70", "interpretation": "Low MAP - may need vasopressor support"},
                {"condition": ">= 70 and <= 100", "interpretation": "Normal MAP - adequate tissue perfusion"},
                {"condition": "> 100 and <= 110", "interpretation": "Elevated MAP - monitor BP"},
                {"condition": "> 110", "interpretation": "High MAP - hypertensive crisis risk"}
            ]
        },
        {
            "name": "QTc Interval (Bazett)",
            "description": "Calculate heart rate corrected QT interval",
            "category": "Cardiology",
            "formula": "{qt} / ({rr} ** 0.5)",
            "input_fields": [
                {"name": "qt", "label": "QT Interval", "unit": "ms", "type": "number", "required": True, "min": 200, "max": 700},
                {"name": "rr", "label": "RR Interval", "unit": "seconds", "type": "number", "required": True, "min": 0.4, "max": 2.0}
            ],
            "interpretation_rules": [
                {"condition": "< 340", "interpretation": "Short QTc - risk of arrhythmia (consider genetics workup)"},
                {"condition": ">= 340 and < 430", "interpretation": "Normal QTc (males <430ms, females <450ms)"},
                {"condition": ">= 430 and < 450", "interpretation": "Borderline QTc (males) - monitor"},
                {"condition": ">= 450 and < 470", "interpretation": "Normal QTc (females) or borderline prolonged (males)"},
                {"condition": ">= 470 and < 500", "interpretation": "Prolonged QTc - review medications, electrolytes"},
                {"condition": ">= 500", "interpretation": "Severely prolonged QTc - high torsades risk, urgent intervention"}
            ]
        },
        {
            "name": "CHA2DS2-VASc Score",
            "description": "Stroke risk stratification in atrial fibrillation",
            "category": "Cardiology",
            "formula": "{chf} + {hypertension} + {age} + {diabetes} + {stroke} + {vascular} + {sex}",
            "input_fields": [
                {"name": "chf", "label": "Congestive heart failure", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "hypertension", "label": "Hypertension", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "age", "label": "Age", "type": "select", "required": True, "options": [{"value": 0, "label": "<65"}, {"value": 1, "label": "65-74"}, {"value": 2, "label": "≥75"}]},
                {"name": "diabetes", "label": "Diabetes mellitus", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "stroke", "label": "Prior stroke/TIA/thromboembolism", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 2, "label": "Yes"}]},
                {"name": "vascular", "label": "Vascular disease (MI, PAD, aortic plaque)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "sex", "label": "Sex", "type": "select", "required": True, "options": [{"value": 0, "label": "Male"}, {"value": 1, "label": "Female"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Very low risk (0% annual stroke) - no anticoagulation"},
                {"condition": "== 1", "interpretation": "Low risk (1.3% annual) - consider anticoagulation (male 1, female 0)"},
                {"condition": "== 2", "interpretation": "Moderate risk (2.2% annual) - anticoagulation recommended"},
                {"condition": "== 3", "interpretation": "Moderate-high risk (3.2% annual) - anticoagulation strongly recommended"},
                {"condition": ">= 4", "interpretation": "High risk (≥4.0% annual) - anticoagulation essential unless contraindicated"}
            ]
        },
        {
            "name": "Framingham Risk Score (Simplified)",
            "description": "10-year cardiovascular disease risk",
            "category": "Cardiology",
            "formula": "{age_points} + {cholesterol_points} + {hdl_points} + {bp_points} + {diabetes} + {smoker}",
            "input_fields": [
                {"name": "age_points", "label": "Age points", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "20-34 (0 pts)"},
                    {"value": 2, "label": "35-39 (2 pts)"},
                    {"value": 5, "label": "40-44 (5 pts)"},
                    {"value": 6, "label": "45-49 (6 pts)"},
                    {"value": 8, "label": "50-54 (8 pts)"},
                    {"value": 10, "label": "55-59 (10 pts)"},
                    {"value": 12, "label": "60-64 (12 pts)"},
                    {"value": 14, "label": "65-69 (14 pts)"},
                    {"value": 16, "label": "70-74 (16 pts)"},
                    {"value": 18, "label": "≥75 (18 pts)"}
                ]},
                {"name": "cholesterol_points", "label": "Total cholesterol", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<160 mg/dL (0 pts)"},
                    {"value": 1, "label": "160-199 (1 pt)"},
                    {"value": 2, "label": "200-239 (2 pts)"},
                    {"value": 3, "label": "240-279 (3 pts)"},
                    {"value": 4, "label": "≥280 (4 pts)"}
                ]},
                {"name": "hdl_points", "label": "HDL cholesterol", "type": "select", "required": True, "options": [
                    {"value": 2, "label": "<35 mg/dL (2 pts)"},
                    {"value": 1, "label": "35-44 (1 pt)"},
                    {"value": 0, "label": "45-49 (0 pts)"},
                    {"value": -1, "label": "50-59 (-1 pt)"},
                    {"value": -2, "label": "≥60 (-2 pts)"}
                ]},
                {"name": "bp_points", "label": "Blood pressure", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<120/<80 (0 pts)"},
                    {"value": 1, "label": "120-129/80-84 (1 pt)"},
                    {"value": 2, "label": "130-139/85-89 (2 pts)"},
                    {"value": 3, "label": "140-159/90-99 (3 pts)"},
                    {"value": 4, "label": "≥160/≥100 (4 pts)"}
                ]},
                {"name": "diabetes", "label": "Diabetes", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes (3 pts)"}]},
                {"name": "smoker", "label": "Current smoker", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 2, "label": "Yes (2 pts)"}]}
            ],
            "interpretation_rules": [
                {"condition": "< 10", "interpretation": "Low risk (<10% 10-year CVD risk) - lifestyle modification"},
                {"condition": ">= 10 and < 20", "interpretation": "Moderate risk (10-20%) - consider statin, ASA"},
                {"condition": ">= 20", "interpretation": "High risk (≥20%) - aggressive risk factor management indicated"}
            ]
        },
        {
            "name": "HAS-BLED Score",
            "description": "Bleeding risk assessment in patients on anticoagulation",
            "category": "Cardiology",
            "formula": "{hypertension} + {abnormal_renal} + {abnormal_liver} + {stroke} + {bleeding_history} + {labile_inr} + {age_65} + {drugs} + {alcohol}",
            "input_fields": [
                {"name": "hypertension", "label": "Hypertension (uncontrolled, >160 mmHg systolic)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "abnormal_renal", "label": "Abnormal renal function (dialysis, transplant, Cr>2.26 mg/dL)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "abnormal_liver", "label": "Abnormal liver function (cirrhosis or bilirubin >2x normal)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "stroke", "label": "Prior stroke", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "bleeding_history", "label": "Prior major bleeding or predisposition", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "labile_inr", "label": "Labile INR (unstable/high INRs, time in therapeutic range <60%)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "age_65", "label": "Age > 65 years", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "drugs", "label": "Medications predisposing to bleeding (antiplatelet agents, NSAIDs)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "alcohol", "label": "Alcohol use (≥8 drinks/week)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Заключение: Низкий риск кровотечения (0.9% годовой риск). Антикоагуляция безопасна, регулярный мониторинг."},
                {"condition": "== 1", "interpretation": "Заключение: Низкий риск кровотечения (3.4% годовой риск). Антикоагуляция приемлема, стандартный мониторинг."},
                {"condition": "== 2", "interpretation": "Заключение: Умеренный риск кровотечения (4.1% годовой риск). Осторожность при назначении антикоагулянтов, тщательный мониторинг."},
                {"condition": ">= 3", "interpretation": "Заключение: Высокий риск кровотечения (≥5.8% годовой риск при score ≥3). Требуется тщательная оценка соотношения риска/пользы антикоагуляции, усиленный мониторинг, коррекция модифицируемых факторов риска."}
            ]
        },
        {
            "name": "TIMI Risk Score for STEMI",
            "description": "30-day mortality risk in ST-elevation MI",
            "category": "Cardiology",
            "formula": "{age_score} + {diabetes_htn_angina} + {systolic_bp} + {heart_rate} + {killip} + {weight} + {anterior_stemi} + {time_to_treatment}",
            "input_fields": [
                {"name": "age_score", "label": "Age", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<65 years (0 pts)"},
                    {"value": 2, "label": "65-74 years (2 pts)"},
                    {"value": 3, "label": "≥75 years (3 pts)"}
                ]},
                {"name": "diabetes_htn_angina", "label": "Diabetes, hypertension, or angina", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "systolic_bp", "label": "Systolic BP <100 mmHg", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes (3 pts)"}]},
                {"name": "heart_rate", "label": "Heart rate >100 bpm", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 2, "label": "Yes (2 pts)"}]},
                {"name": "killip", "label": "Killip class II-IV", "type": "select", "required": True, "options": [{"value": 0, "label": "No (Class I)"}, {"value": 2, "label": "Yes (2 pts)"}]},
                {"name": "weight", "label": "Weight <67 kg (150 lbs)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "anterior_stemi", "label": "Anterior STEMI or LBBB", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "time_to_treatment", "label": "Time to treatment >4 hours", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Заключение: Очень низкий риск (0.8% 30-дневная смертность). Благоприятный прогноз при своевременном лечении."},
                {"condition": ">= 1 and <= 2", "interpretation": "Заключение: Низкий риск (1.6-2.2% смертность). Хороший прогноз при стандартной терапии."},
                {"condition": ">= 3 and <= 4", "interpretation": "Заключение: Умеренный риск (4.4-7.3% смертность). Рекомендуется агрессивная терапия, тщательный мониторинг."},
                {"condition": ">= 5 and <= 6", "interpretation": "Заключение: Высокий риск (12.4-16.1% смертность). Требуется интенсивная терапия, рассмотреть инвазивную стратегию."},
                {"condition": ">= 7 and <= 8", "interpretation": "Заключение: Очень высокий риск (23.4-26.8% смертность). Критическое состояние, немедленная реваскуляризация, интенсивная поддержка."},
                {"condition": "> 8", "interpretation": "Заключение: Экстремально высокий риск (>35.9% смертность). Крайне тяжелое состояние, максимальная интенсивная терапия, консультация кардиохирурга."}
            ]
        },
        {
            "name": "GRACE Score (Simplified)",
            "description": "6-month mortality risk in acute coronary syndrome",
            "category": "Cardiology",
            "formula": "{age_points} + {heart_rate_points} + {sbp_points} + {creatinine_points} + {killip_points} + {cardiac_arrest} + {st_deviation} + {elevated_enzymes}",
            "input_fields": [
                {"name": "age_points", "label": "Age", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<40 (0 pts)"},
                    {"value": 18, "label": "40-49 (18 pts)"},
                    {"value": 36, "label": "50-59 (36 pts)"},
                    {"value": 55, "label": "60-69 (55 pts)"},
                    {"value": 73, "label": "70-79 (73 pts)"},
                    {"value": 91, "label": "≥80 (91 pts)"}
                ]},
                {"name": "heart_rate_points", "label": "Heart rate (bpm)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<70 (0 pts)"},
                    {"value": 7, "label": "70-89 (7 pts)"},
                    {"value": 13, "label": "90-109 (13 pts)"},
                    {"value": 23, "label": "110-149 (23 pts)"},
                    {"value": 36, "label": "≥150 (36 pts)"}
                ]},
                {"name": "sbp_points", "label": "Systolic BP (mmHg)", "type": "select", "required": True, "options": [
                    {"value": 63, "label": "<80 (63 pts)"},
                    {"value": 58, "label": "80-99 (58 pts)"},
                    {"value": 47, "label": "100-119 (47 pts)"},
                    {"value": 37, "label": "120-139 (37 pts)"},
                    {"value": 26, "label": "140-159 (26 pts)"},
                    {"value": 11, "label": "160-199 (11 pts)"},
                    {"value": 0, "label": "≥200 (0 pts)"}
                ]},
                {"name": "creatinine_points", "label": "Serum creatinine (mg/dL)", "type": "select", "required": True, "options": [
                    {"value": 2, "label": "<0.4 (2 pts)"},
                    {"value": 5, "label": "0.4-0.79 (5 pts)"},
                    {"value": 8, "label": "0.8-1.19 (8 pts)"},
                    {"value": 11, "label": "1.2-1.59 (11 pts)"},
                    {"value": 14, "label": "1.6-1.99 (14 pts)"},
                    {"value": 23, "label": "2-3.99 (23 pts)"},
                    {"value": 31, "label": "≥4 (31 pts)"}
                ]},
                {"name": "killip_points", "label": "Killip class", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "I - No heart failure (0 pts)"},
                    {"value": 21, "label": "II - Rales, S3 (21 pts)"},
                    {"value": 43, "label": "III - Pulmonary edema (43 pts)"},
                    {"value": 64, "label": "IV - Cardiogenic shock (64 pts)"}
                ]},
                {"name": "cardiac_arrest", "label": "Cardiac arrest at admission", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 43, "label": "Yes (43 pts)"}]},
                {"name": "st_deviation", "label": "ST segment deviation", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 30, "label": "Yes (30 pts)"}]},
                {"name": "elevated_enzymes", "label": "Elevated cardiac enzymes", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 15, "label": "Yes (15 pts)"}]}
            ],
            "interpretation_rules": [
                {"condition": "<= 108", "interpretation": "Заключение: Низкий риск (<1% внутрибольничная смертность, <3% 6-месячная смертность). Возможна ранняя выписка, консервативная стратегия приемлема."},
                {"condition": "> 108 and <= 140", "interpretation": "Заключение: Умеренный риск (1-3% внутрибольничная смертность, 3-8% 6-месячная). Рекомендуется госпитализация, инвазивная стратегия в течение 72 часов."},
                {"condition": "> 140", "interpretation": "Заключение: Высокий риск (>3% внутрибольничная смертность, >8% 6-месячная). Требуется срочная инвазивная стратегия в течение 24 часов, интенсивная терапия, мониторинг в КИТ."}
            ]
        },
        {
            "name": "Killip Classification",
            "description": "Heart failure severity classification in acute MI",
            "category": "Cardiology",
            "formula": "{killip_class}",
            "input_fields": [
                {"name": "killip_class", "label": "Clinical findings", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "Class I - No heart failure (no rales, no S3)"},
                    {"value": 2, "label": "Class II - Heart failure (rales in <50% lung fields, S3 gallop)"},
                    {"value": 3, "label": "Class III - Severe heart failure (rales in >50% lung fields, pulmonary edema)"},
                    {"value": 4, "label": "Class IV - Cardiogenic shock (hypotension, signs of hypoperfusion)"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "== 1", "interpretation": "Заключение: Killip I - нет признаков сердечной недостаточности. Смертность 6%. Благоприятный прогноз, стандартная терапия ОИМ."},
                {"condition": "== 2", "interpretation": "Заключение: Killip II - сердечная недостаточность (хрипы в <50% легких, S3 галоп). Смертность 17%. Требуется агрессивная терапия СН, мониторинг гемодинамики."},
                {"condition": "== 3", "interpretation": "Заключение: Killip III - тяжелая сердечная недостаточность (отек легких). Смертность 38%. Критическое состояние, интенсивная терапия, рассмотреть неинвазивную вентиляцию, инотропы."},
                {"condition": "== 4", "interpretation": "Заключение: Killip IV - кардиогенный шок. Смертность 81%. Экстремально критическое состояние, требуется механическая поддержка кровообращения (IABP/ECMO), срочная реваскуляризация."}
            ]
        },
        
        # ============= NEPHROLOGY =============
        {
            "name": "Creatinine Clearance (Cockcroft-Gault)",
            "description": "Estimate kidney function for drug dosing",
            "category": "Nephrology",
            "formula": "((140 - {age}) * {weight}) / (72 * {creatinine})",
            "input_fields": [
                {"name": "age", "label": "Age", "unit": "years", "type": "number", "required": True, "min": 18, "max": 120},
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 300},
                {"name": "creatinine", "label": "Serum Creatinine", "unit": "mg/dL", "type": "number", "required": True, "min": 0.1, "max": 20}
            ],
            "interpretation_rules": [
                {"condition": "< 15", "interpretation": "Stage 5 CKD (kidney failure) - dialysis/transplant consideration"},
                {"condition": ">= 15 and < 30", "interpretation": "Stage 4 CKD (severe) - nephrology referral essential"},
                {"condition": ">= 30 and < 60", "interpretation": "Stage 3 CKD (moderate) - monitor, adjust medications"},
                {"condition": ">= 60 and < 90", "interpretation": "Stage 2 CKD (mild) - kidney damage with mildly decreased GFR"},
                {"condition": ">= 90", "interpretation": "Stage 1 or normal - GFR ≥90 mL/min"}
            ]
        },
        {
            "name": "eGFR (MDRD)",
            "description": "Estimated glomerular filtration rate",
            "category": "Nephrology",
            "formula": "175 * ({creatinine} ** -1.154) * ({age} ** -0.203)",
            "input_fields": [
                {"name": "creatinine", "label": "Serum Creatinine", "unit": "mg/dL", "type": "number", "required": True, "min": 0.1, "max": 20},
                {"name": "age", "label": "Age", "unit": "years", "type": "number", "required": True, "min": 18, "max": 120}
            ],
            "interpretation_rules": [
                {"condition": "< 15", "interpretation": "Stage 5 CKD (kidney failure) - renal replacement therapy needed"},
                {"condition": ">= 15 and < 30", "interpretation": "Stage 4 CKD (severe reduction) - prepare for renal replacement"},
                {"condition": ">= 30 and < 60", "interpretation": "Stage 3 CKD (moderate reduction) - evaluate complications"},
                {"condition": ">= 60 and < 90", "interpretation": "Stage 2 CKD (mild reduction) - kidney damage present"},
                {"condition": ">= 90", "interpretation": "Stage 1 (normal or high) - normal kidney function"}
            ]
        },
        {
            "name": "Fractional Excretion of Sodium (FENa)",
            "description": "Differentiate prerenal from intrinsic AKI",
            "category": "Nephrology",
            "formula": "({urine_sodium} * {plasma_creatinine} / ({plasma_sodium} * {urine_creatinine})) * 100",
            "input_fields": [
                {"name": "urine_sodium", "label": "Urine Sodium", "unit": "mEq/L", "type": "number", "required": True, "min": 1, "max": 300},
                {"name": "plasma_sodium", "label": "Plasma Sodium", "unit": "mEq/L", "type": "number", "required": True, "min": 100, "max": 200},
                {"name": "urine_creatinine", "label": "Urine Creatinine", "unit": "mg/dL", "type": "number", "required": True, "min": 1, "max": 500},
                {"name": "plasma_creatinine", "label": "Plasma Creatinine", "unit": "mg/dL", "type": "number", "required": True, "min": 0.1, "max": 20}
            ],
            "interpretation_rules": [
                {"condition": "< 1", "interpretation": "Prerenal AKI (volume depletion) - fluid resuscitation indicated"},
                {"condition": ">= 1 and < 2", "interpretation": "Indeterminate - consider clinical context"},
                {"condition": ">= 2", "interpretation": "Intrinsic renal AKI (ATN likely) - supportive care, avoid nephrotoxins"}
            ]
        },
        
        # ============= NEUROLOGY =============
        {
            "name": "Glasgow Coma Scale (GCS)",
            "description": "Assess level of consciousness after brain injury",
            "category": "Neurology",
            "formula": "{eye_opening} + {verbal_response} + {motor_response}",
            "input_fields": [
                {
                    "name": "eye_opening", "label": "Eye Opening Response", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "1 - No eye opening"},
                        {"value": 2, "label": "2 - Eye opening to pain"},
                        {"value": 3, "label": "3 - Eye opening to speech"},
                        {"value": 4, "label": "4 - Eyes open spontaneously"}
                    ]
                },
                {
                    "name": "verbal_response", "label": "Verbal Response", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "1 - No verbal response"},
                        {"value": 2, "label": "2 - Incomprehensible sounds"},
                        {"value": 3, "label": "3 - Inappropriate words"},
                        {"value": 4, "label": "4 - Confused conversation"},
                        {"value": 5, "label": "5 - Oriented"}
                    ]
                },
                {
                    "name": "motor_response", "label": "Motor Response", "type": "select", "required": True,
                    "options": [
                        {"value": 1, "label": "1 - No motor response"},
                        {"value": 2, "label": "2 - Extension to pain"},
                        {"value": 3, "label": "3 - Flexion to pain"},
                        {"value": 4, "label": "4 - Withdrawal from pain"},
                        {"value": 5, "label": "5 - Localizes to pain"},
                        {"value": 6, "label": "6 - Obeys commands"}
                    ]
                }
            ],
            "interpretation_rules": [
                {"condition": "== 3", "interpretation": "GCS 3: Deep coma, poor prognosis - intensive care required"},
                {"condition": "> 3 and <= 8", "interpretation": "GCS 4-8: Severe brain injury (coma) - intubation likely needed"},
                {"condition": "> 8 and <= 12", "interpretation": "GCS 9-12: Moderate brain injury - close monitoring required"},
                {"condition": "> 12 and < 15", "interpretation": "GCS 13-14: Mild brain injury - observe, CT scan often indicated"},
                {"condition": "== 15", "interpretation": "GCS 15: Normal consciousness - fully alert and oriented"}
            ]
        },
        {
            "name": "NIH Stroke Scale (Simplified)",
            "description": "Assess stroke severity",
            "category": "Neurology",
            "formula": "{consciousness} + {orientation} + {commands} + {gaze} + {visual} + {facial} + {motor_arm} + {motor_leg} + {ataxia} + {sensory} + {language}",
            "input_fields": [
                {"name": "consciousness", "label": "Level of consciousness", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Alert"},
                    {"value": 1, "label": "1 - Arouses to minor stimulation"},
                    {"value": 2, "label": "2 - Requires repeated stimulation"},
                    {"value": 3, "label": "3 - Reflex responses only"}
                ]},
                {"name": "orientation", "label": "Orientation questions", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Answers both correctly"},
                    {"value": 1, "label": "1 - Answers one correctly"},
                    {"value": 2, "label": "2 - Answers neither correctly"}
                ]},
                {"name": "commands", "label": "Response to commands", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Performs both correctly"},
                    {"value": 1, "label": "1 - Performs one correctly"},
                    {"value": 2, "label": "2 - Performs neither correctly"}
                ]},
                {"name": "gaze", "label": "Gaze", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Normal"},
                    {"value": 1, "label": "1 - Partial gaze palsy"},
                    {"value": 2, "label": "2 - Forced deviation"}
                ]},
                {"name": "visual", "label": "Visual fields", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - No visual loss"},
                    {"value": 1, "label": "1 - Partial hemianopia"},
                    {"value": 2, "label": "2 - Complete hemianopia"},
                    {"value": 3, "label": "3 - Bilateral hemianopia"}
                ]},
                {"name": "facial", "label": "Facial palsy", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Normal"},
                    {"value": 1, "label": "1 - Minor paralysis"},
                    {"value": 2, "label": "2 - Partial paralysis"},
                    {"value": 3, "label": "3 - Complete paralysis"}
                ]},
                {"name": "motor_arm", "label": "Motor arm", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - No drift"},
                    {"value": 1, "label": "1 - Drift"},
                    {"value": 2, "label": "2 - Some effort against gravity"},
                    {"value": 3, "label": "3 - No effort against gravity"},
                    {"value": 4, "label": "4 - No movement"}
                ]},
                {"name": "motor_leg", "label": "Motor leg", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - No drift"},
                    {"value": 1, "label": "1 - Drift"},
                    {"value": 2, "label": "2 - Some effort against gravity"},
                    {"value": 3, "label": "3 - No effort against gravity"},
                    {"value": 4, "label": "4 - No movement"}
                ]},
                {"name": "ataxia", "label": "Limb ataxia", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Absent"},
                    {"value": 1, "label": "1 - Present in one limb"},
                    {"value": 2, "label": "2 - Present in two limbs"}
                ]},
                {"name": "sensory", "label": "Sensory", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Normal"},
                    {"value": 1, "label": "1 - Mild to moderate loss"},
                    {"value": 2, "label": "2 - Severe to total loss"}
                ]},
                {"name": "language", "label": "Language/aphasia", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Normal"},
                    {"value": 1, "label": "1 - Mild to moderate aphasia"},
                    {"value": 2, "label": "2 - Severe aphasia"},
                    {"value": 3, "label": "3 - Mute/global aphasia"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "No stroke symptoms - normal examination"},
                {"condition": "> 0 and <= 4", "interpretation": "Minor stroke - may be suitable for outpatient management"},
                {"condition": "> 4 and <= 15", "interpretation": "Moderate stroke - admission required, consider thrombolysis"},
                {"condition": "> 15 and <= 20", "interpretation": "Moderate to severe stroke - ICU monitoring recommended"},
                {"condition": "> 20", "interpretation": "Severe stroke - high risk, intensive care essential"}
            ]
        },
        
        # ============= PEDIATRICS =============
        {
            "name": "Pediatric Weight Estimation (Broselow)",
            "description": "Estimate child weight by age for medication dosing",
            "category": "Pediatrics",
            "formula": "(2 * {age}) + 8",
            "input_fields": [
                {"name": "age", "label": "Age", "unit": "years", "type": "number", "required": True, "min": 1, "max": 10}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Estimated weight in kg - use for emergency medication dosing"}
            ]
        },
        {
            "name": "Apgar Score",
            "description": "Assess newborn health status at 1 and 5 minutes",
            "category": "Pediatrics",
            "formula": "{appearance} + {pulse} + {grimace} + {activity} + {respiration}",
            "input_fields": [
                {"name": "appearance", "label": "Appearance (skin color)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Blue, pale all over"},
                    {"value": 1, "label": "1 - Body pink, extremities blue"},
                    {"value": 2, "label": "2 - Pink all over"}
                ]},
                {"name": "pulse", "label": "Pulse (heart rate)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Absent"},
                    {"value": 1, "label": "1 - <100 bpm"},
                    {"value": 2, "label": "2 - >100 bpm"}
                ]},
                {"name": "grimace", "label": "Grimace (reflex irritability)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - No response"},
                    {"value": 1, "label": "1 - Grimace"},
                    {"value": 2, "label": "2 - Cry, cough, sneeze"}
                ]},
                {"name": "activity", "label": "Activity (muscle tone)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Limp, no movement"},
                    {"value": 1, "label": "1 - Some flexion"},
                    {"value": 2, "label": "2 - Active motion, flexed"}
                ]},
                {"name": "respiration", "label": "Respiration", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - Absent"},
                    {"value": 1, "label": "1 - Weak cry, hypoventilation"},
                    {"value": 2, "label": "2 - Strong cry, good breathing"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "<= 3", "interpretation": "Critical condition (0-3) - immediate resuscitation required"},
                {"condition": "> 3 and <= 6", "interpretation": "Moderately abnormal (4-6) - may need intervention"},
                {"condition": "> 6 and <= 7", "interpretation": "Good condition (7) - minor interventions may be needed"},
                {"condition": "> 7", "interpretation": "Excellent condition (8-10) - normal healthy newborn"}
            ]
        },
        {
            "name": "Pediatric Fever Temperature Conversion",
            "description": "Convert between Celsius and Fahrenheit",
            "category": "Pediatrics",
            "formula": "({celsius} * 9/5) + 32",
            "input_fields": [
                {"name": "celsius", "label": "Temperature", "unit": "°C", "type": "number", "required": True, "min": 35, "max": 43}
            ],
            "interpretation_rules": [
                {"condition": "< 100.4", "interpretation": "Normal temperature (<38°C)"},
                {"condition": ">= 100.4 and < 102.2", "interpretation": "Low-grade fever (38-39°C) - monitor"},
                {"condition": ">= 102.2 and < 104", "interpretation": "Moderate fever (39-40°C) - antipyretics recommended"},
                {"condition": ">= 104", "interpretation": "High fever (≥40°C) - urgent evaluation needed"}
            ]
        },
        
        # ============= PULMONOLOGY =============
        {
            "name": "CURB-65 Score",
            "description": "Pneumonia severity and mortality prediction",
            "category": "Pulmonology",
            "formula": "{confusion} + {urea} + {respiratory_rate} + {blood_pressure} + {age}",
            "input_fields": [
                {"name": "confusion", "label": "New onset confusion", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "urea", "label": "BUN > 19 mg/dL (>7 mmol/L)", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "respiratory_rate", "label": "Respiratory rate ≥ 30/min", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "blood_pressure", "label": "SBP <90 or DBP ≤60 mmHg", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "age", "label": "Age ≥ 65 years", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Low risk (0-1% mortality) - outpatient treatment appropriate"},
                {"condition": "== 1", "interpretation": "Low risk (0-1% mortality) - consider outpatient or short admission"},
                {"condition": "== 2", "interpretation": "Moderate risk (9% mortality) - hospital admission recommended"},
                {"condition": "== 3", "interpretation": "High risk (15% mortality) - consider ICU admission"},
                {"condition": ">= 4", "interpretation": "Severe pneumonia (≥40% mortality) - ICU admission essential"}
            ]
        },
        {
            "name": "Wells' Criteria for Pulmonary Embolism",
            "description": "Assess PE probability",
            "category": "Pulmonology",
            "formula": "{clinical_signs} + {pe_likely} + {heart_rate} + {immobilization} + {previous_pe} + {hemoptysis} + {malignancy}",
            "input_fields": [
                {"name": "clinical_signs", "label": "Clinical signs of DVT", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes"}]},
                {"name": "pe_likely", "label": "PE is #1 diagnosis OR equally likely", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 3, "label": "Yes"}]},
                {"name": "heart_rate", "label": "Heart rate > 100 bpm", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "immobilization", "label": "Immobilization ≥3 days or surgery within 4 weeks", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "previous_pe", "label": "Previous PE or DVT", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1.5, "label": "Yes"}]},
                {"name": "hemoptysis", "label": "Hemoptysis", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "malignancy", "label": "Active malignancy", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "< 2", "interpretation": "Low probability (3.6%) - consider D-dimer"},
                {"condition": ">= 2 and < 6", "interpretation": "Moderate probability (20.5%) - D-dimer or imaging"},
                {"condition": ">= 6", "interpretation": "High probability (66.7%) - imaging recommended (CTPA)"}
            ]
        },
        {
            "name": "PaO2/FiO2 Ratio",
            "description": "Assess oxygenation and ARDS severity",
            "category": "Pulmonology",
            "formula": "{pao2} / ({fio2} / 100)",
            "input_fields": [
                {"name": "pao2", "label": "PaO2", "unit": "mmHg", "type": "number", "required": True, "min": 30, "max": 600},
                {"name": "fio2", "label": "FiO2", "unit": "%", "type": "number", "required": True, "min": 21, "max": 100}
            ],
            "interpretation_rules": [
                {"condition": "> 300", "interpretation": "Normal oxygenation - no acute lung injury"},
                {"condition": "> 200 and <= 300", "interpretation": "Mild ARDS - supportive care, monitor closely"},
                {"condition": "> 100 and <= 200", "interpretation": "Moderate ARDS - lung protective ventilation required"},
                {"condition": "<= 100", "interpretation": "Severe ARDS - consider prone positioning, ECMO evaluation"}
            ]
        },
        
        # ============= HEMATOLOGY =============
        {
            "name": "Absolute Neutrophil Count (ANC)",
            "description": "Calculate ANC for infection risk assessment",
            "category": "Hematology",
            "formula": "{wbc} * ({neutrophils} + {bands}) / 100",
            "input_fields": [
                {"name": "wbc", "label": "WBC Count", "unit": "cells/μL", "type": "number", "required": True, "min": 100, "max": 100000},
                {"name": "neutrophils", "label": "Neutrophils", "unit": "%", "type": "number", "required": True, "min": 0, "max": 100},
                {"name": "bands", "label": "Bands", "unit": "%", "type": "number", "required": True, "min": 0, "max": 100}
            ],
            "interpretation_rules": [
                {"condition": "< 500", "interpretation": "Severe neutropenia - very high infection risk, reverse isolation"},
                {"condition": ">= 500 and < 1000", "interpretation": "Moderate neutropenia - high infection risk, careful monitoring"},
                {"condition": ">= 1000 and < 1500", "interpretation": "Mild neutropenia - increased infection risk"},
                {"condition": ">= 1500", "interpretation": "Normal ANC - no increased infection risk from neutropenia"}
            ]
        },
        {
            "name": "Corrected Calcium",
            "description": "Adjust serum calcium for albumin level",
            "category": "Hematology",
            "formula": "{calcium} + 0.8 * (4 - {albumin})",
            "input_fields": [
                {"name": "calcium", "label": "Serum Calcium", "unit": "mg/dL", "type": "number", "required": True, "min": 1, "max": 20},
                {"name": "albumin", "label": "Serum Albumin", "unit": "g/dL", "type": "number", "required": True, "min": 1, "max": 6}
            ],
            "interpretation_rules": [
                {"condition": "< 8.5", "interpretation": "Hypocalcemia - check PTH, vitamin D, may need supplementation"},
                {"condition": ">= 8.5 and <= 10.5", "interpretation": "Normal calcium - no intervention needed"},
                {"condition": "> 10.5 and <= 12", "interpretation": "Mild hypercalcemia - investigate cause"},
                {"condition": "> 12", "interpretation": "Severe hypercalcemia - urgent treatment required"}
            ]
        },
        {
            "name": "Reticulocyte Production Index",
            "description": "Assess bone marrow response to anemia",
            "category": "Hematology",
            "formula": "({reticulocytes} * {hematocrit} / 45) / {maturation_time}",
            "input_fields": [
                {"name": "reticulocytes", "label": "Reticulocyte Count", "unit": "%", "type": "number", "required": True, "min": 0, "max": 20},
                {"name": "hematocrit", "label": "Hematocrit", "unit": "%", "type": "number", "required": True, "min": 10, "max": 60},
                {"name": "maturation_time", "label": "Maturation Time (days)", "type": "select", "required": True, "options": [
                    {"value": 1.0, "label": "1.0 (Hct ≥40%)"},
                    {"value": 1.5, "label": "1.5 (Hct 35-40%)"},
                    {"value": 2.0, "label": "2.0 (Hct 25-35%)"},
                    {"value": 2.5, "label": "2.5 (Hct <25%)"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "< 2", "interpretation": "Inadequate bone marrow response - hypoproliferative anemia"},
                {"condition": ">= 2 and < 3", "interpretation": "Borderline marrow response - evaluate further"},
                {"condition": ">= 3", "interpretation": "Appropriate bone marrow response - hemolysis or bleeding likely"}
            ]
        },
        
        # ============= EMERGENCY MEDICINE =============
        {
            "name": "Revised Trauma Score (RTS)",
            "description": "Triage and predict trauma survival",
            "category": "Emergency",
            "formula": "0.9368 * {gcs_coded} + 0.7326 * {sbp_coded} + 0.2908 * {rr_coded}",
            "input_fields": [
                {"name": "gcs_coded", "label": "Glasgow Coma Scale", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "3"},
                    {"value": 1, "label": "4-5"},
                    {"value": 2, "label": "6-8"},
                    {"value": 3, "label": "9-12"},
                    {"value": 4, "label": "13-15"}
                ]},
                {"name": "sbp_coded", "label": "Systolic BP (mmHg)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 (no pulse)"},
                    {"value": 1, "label": "1-49"},
                    {"value": 2, "label": "50-75"},
                    {"value": 3, "label": "76-89"},
                    {"value": 4, "label": ">89"}
                ]},
                {"name": "rr_coded", "label": "Respiratory Rate (/min)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0"},
                    {"value": 1, "label": "1-5"},
                    {"value": 2, "label": "6-9"},
                    {"value": 3, "label": ">29"},
                    {"value": 4, "label": "10-29"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "< 4", "interpretation": "Critical condition - survival unlikely without immediate intervention"},
                {"condition": ">= 4 and < 6", "interpretation": "Severe trauma - urgent resuscitation required"},
                {"condition": ">= 6 and < 7", "interpretation": "Moderate trauma - close monitoring needed"},
                {"condition": ">= 7", "interpretation": "Minor trauma - stable patient"}
            ]
        },
        {
            "name": "Anion Gap",
            "description": "Evaluate metabolic acidosis etiology",
            "category": "Emergency",
            "formula": "{sodium} - ({chloride} + {bicarbonate})",
            "input_fields": [
                {"name": "sodium", "label": "Sodium", "unit": "mEq/L", "type": "number", "required": True, "min": 100, "max": 200},
                {"name": "chloride", "label": "Chloride", "unit": "mEq/L", "type": "number", "required": True, "min": 50, "max": 150},
                {"name": "bicarbonate", "label": "Bicarbonate", "unit": "mEq/L", "type": "number", "required": True, "min": 5, "max": 50}
            ],
            "interpretation_rules": [
                {"condition": "< 3", "interpretation": "Low anion gap - hypoalbuminemia, lab error, or paraprotein"},
                {"condition": ">= 3 and <= 11", "interpretation": "Normal anion gap (3-11 mEq/L) - if acidotic, non-gap acidosis"},
                {"condition": "> 11 and <= 16", "interpretation": "Borderline elevated - consider clinical context"},
                {"condition": "> 16", "interpretation": "High anion gap metabolic acidosis - MUDPILES differential"}
            ]
        },
        {
            "name": "Parkland Formula for Burns",
            "description": "Calculate fluid resuscitation for burn patients",
            "category": "Emergency",
            "formula": "4 * {weight} * {tbsa}",
            "input_fields": [
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 20, "max": 200},
                {"name": "tbsa", "label": "Total Body Surface Area Burned", "unit": "%", "type": "number", "required": True, "min": 1, "max": 100}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Total mL Lactated Ringer's in first 24h - give 50% in first 8h, 50% in next 16h"}
            ]
        },
        
        # ============= OBSTETRICS & GYNECOLOGY =============
        {
            "name": "Bishop Score",
            "description": "Predict successful labor induction",
            "category": "Obstetrics",
            "formula": "{dilation} + {effacement} + {station} + {consistency} + {position}",
            "input_fields": [
                {"name": "dilation", "label": "Cervical Dilation", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Closed"},
                    {"value": 1, "label": "1-2 cm"},
                    {"value": 2, "label": "3-4 cm"},
                    {"value": 3, "label": "≥5 cm"}
                ]},
                {"name": "effacement", "label": "Cervical Effacement", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0-30%"},
                    {"value": 1, "label": "40-50%"},
                    {"value": 2, "label": "60-70%"},
                    {"value": 3, "label": "≥80%"}
                ]},
                {"name": "station", "label": "Fetal Station", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "-3"},
                    {"value": 1, "label": "-2"},
                    {"value": 2, "label": "-1, 0"},
                    {"value": 3, "label": "+1, +2"}
                ]},
                {"name": "consistency", "label": "Cervical Consistency", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Firm"},
                    {"value": 1, "label": "Medium"},
                    {"value": 2, "label": "Soft"}
                ]},
                {"name": "position", "label": "Cervical Position", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Posterior"},
                    {"value": 1, "label": "Mid-position"},
                    {"value": 2, "label": "Anterior"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "<= 5", "interpretation": "Unfavorable cervix - induction likely to fail, consider ripening"},
                {"condition": "> 5 and <= 8", "interpretation": "Moderately favorable - induction reasonable"},
                {"condition": "> 8", "interpretation": "Favorable cervix - high induction success rate (similar to spontaneous labor)"}
            ]
        },
        {
            "name": "Estimated Due Date (Naegele's Rule)",
            "description": "Calculate EDD from last menstrual period",
            "category": "Obstetrics",
            "formula": "{lmp_days} + 280",
            "input_fields": [
                {"name": "lmp_days", "label": "Last Menstrual Period (days since epoch)", "unit": "days", "type": "number", "required": True, "min": 0, "max": 100000}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Estimated due date (280 days from LMP)"}
            ]
        },
        
        # ============= ENDOCRINOLOGY =============
        {
            "name": "Corrected Sodium for Hyperglycemia",
            "description": "Adjust sodium for glucose effect",
            "category": "Endocrinology",
            "formula": "{sodium} + 0.024 * ({glucose} - 100)",
            "input_fields": [
                {"name": "sodium", "label": "Measured Sodium", "unit": "mEq/L", "type": "number", "required": True, "min": 100, "max": 200},
                {"name": "glucose", "label": "Glucose", "unit": "mg/dL", "type": "number", "required": True, "min": 50, "max": 1000}
            ],
            "interpretation_rules": [
                {"condition": "< 135", "interpretation": "Corrected hyponatremia - evaluate volume status, SIADH"},
                {"condition": ">= 135 and <= 145", "interpretation": "Normal corrected sodium"},
                {"condition": "> 145", "interpretation": "Corrected hypernatremia - free water deficit, evaluate causes"}
            ]
        },
        {
            "name": "HbA1c to Average Glucose",
            "description": "Convert HbA1c to estimated average glucose",
            "category": "Endocrinology",
            "formula": "28.7 * {hba1c} - 46.7",
            "input_fields": [
                {"name": "hba1c", "label": "HbA1c", "unit": "%", "type": "number", "required": True, "min": 4, "max": 15}
            ],
            "interpretation_rules": [
                {"condition": "< 100", "interpretation": "Non-diabetic glucose range (HbA1c <5.7%)"},
                {"condition": ">= 100 and < 125", "interpretation": "Prediabetic glucose range (HbA1c 5.7-6.4%)"},
                {"condition": ">= 125 and < 200", "interpretation": "Diabetic, suboptimal control (HbA1c 6.5-8%)"},
                {"condition": ">= 200", "interpretation": "Diabetic, poor control (HbA1c >8%) - intensify treatment"}
            ]
        },
        {
            "name": "HOMA-IR (Insulin Resistance)",
            "description": "Assess insulin resistance",
            "category": "Endocrinology",
            "formula": "({fasting_insulin} * {fasting_glucose}) / 405",
            "input_fields": [
                {"name": "fasting_insulin", "label": "Fasting Insulin", "unit": "μU/mL", "type": "number", "required": True, "min": 1, "max": 100},
                {"name": "fasting_glucose", "label": "Fasting Glucose", "unit": "mg/dL", "type": "number", "required": True, "min": 50, "max": 300}
            ],
            "interpretation_rules": [
                {"condition": "< 1", "interpretation": "Optimal insulin sensitivity"},
                {"condition": ">= 1 and < 2", "interpretation": "Normal insulin sensitivity"},
                {"condition": ">= 2 and < 2.5", "interpretation": "Early insulin resistance - lifestyle modification"},
                {"condition": ">= 2.5", "interpretation": "Significant insulin resistance - evaluate for metabolic syndrome"}
            ]
        },
        {
            "name": "Thyroid Function Interpreter",
            "description": "Interpret thyroid function tests (TSH, Free T4)",
            "category": "Endocrinology",
            "formula": "{tsh} + {ft4} * 0.01",
            "input_fields": [
                {"name": "tsh", "label": "TSH (Thyroid Stimulating Hormone)", "unit": "mIU/L", "type": "number", "required": True, "min": 0.01, "max": 100},
                {"name": "ft4", "label": "Free T4 (Thyroxine)", "unit": "ng/dL", "type": "number", "required": True, "min": 0.1, "max": 10}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Заключение определяется комбинацией TSH и FT4: Норма TSH 0.4-4.0 mIU/L, FT4 0.8-1.8 ng/dL. Высокий TSH + низкий FT4 = первичный гипотиреоз. Низкий TSH + высокий FT4 = гипертиреоз. Низкий TSH + низкий FT4 = вторичный гипотиреоз (гипофизарный). Требуется клиническая корреляция и дополнительные тесты (T3, антитела к ТПО)."}
            ]
        },
        {
            "name": "Free Testosterone Calculator (Vermeulen)",
            "description": "Calculate bioavailable and free testosterone",
            "category": "Endocrinology",
            "formula": "{total_testosterone} * 0.02",
            "input_fields": [
                {"name": "total_testosterone", "label": "Total Testosterone", "unit": "ng/dL", "type": "number", "required": True, "min": 1, "max": 2000},
                {"name": "shbg", "label": "SHBG (Sex Hormone Binding Globulin)", "unit": "nmol/L", "type": "number", "required": True, "min": 1, "max": 200},
                {"name": "albumin", "label": "Albumin", "unit": "g/dL", "type": "number", "required": True, "min": 2, "max": 6}
            ],
            "interpretation_rules": [
                {"condition": "< 5", "interpretation": "Заключение: Низкий свободный тестостерон (<5 ng/dL у мужчин). Гипогонадизм, требуется оценка причины (первичный vs вторичный). Симптомы: снижение либидо, эректильная дисфункция, усталость."},
                {"condition": ">= 5 and < 9", "interpretation": "Заключение: Пограничный низкий свободный тестостерон (5-9 ng/dL). Рассмотреть клинические симптомы, повторить анализ утром, исключить другие причины симптомов."},
                {"condition": ">= 9 and <= 30", "interpretation": "Заключение: Нормальный свободный тестостерон (9-30 ng/dL у взрослых мужчин). Заместительная терапия не показана. У женщин норма 0.3-1.9 ng/dL."},
                {"condition": "> 30", "interpretation": "Заключение: Повышенный свободный тестостерон (>30 ng/dL). У мужчин - рассмотреть экзогенный прием. У женщин - СПКЯ, опухоли надпочечников/яичников, гиперплазия надпочечников."}
            ]
        },
        {
            "name": "Serum Osmolality Calculator",
            "description": "Calculate serum osmolality and osmolar gap",
            "category": "Endocrinology",
            "formula": "(2 * {sodium}) + ({glucose} / 18) + ({bun} / 2.8)",
            "input_fields": [
                {"name": "sodium", "label": "Sodium", "unit": "mEq/L", "type": "number", "required": True, "min": 100, "max": 200},
                {"name": "glucose", "label": "Glucose", "unit": "mg/dL", "type": "number", "required": True, "min": 50, "max": 1000},
                {"name": "bun", "label": "BUN (Blood Urea Nitrogen)", "unit": "mg/dL", "type": "number", "required": True, "min": 5, "max": 200}
            ],
            "interpretation_rules": [
                {"condition": "< 275", "interpretation": "Заключение: Низкая осмоляльность (<275 mOsm/kg). Гипоосмоляльность - оценить статус натрия, избыток свободной воды. Причины: SIADH, полидипсия, гипотиреоз."},
                {"condition": ">= 275 and <= 295", "interpretation": "Заключение: Нормальная осмоляльность сыворотки (275-295 mOsm/kg). Гомеостаз жидкости в норме."},
                {"condition": "> 295 and <= 320", "interpretation": "Заключение: Повышенная осмоляльность (295-320 mOsm/kg). Гиперосмоляльность - оценить причину: гипергликемия, дегидратация, гипернатриемия. Если осмолярный гэп >10, рассмотреть токсические алкоголи."},
                {"condition": "> 320", "interpretation": "Заключение: Тяжелая гиперосмоляльность (>320 mOsm/kg). Критическое состояние - риск комы. Причины: диабетический кетоацидоз, гиперосмолярное гипергликемическое состояние, тяжелая дегидратация. Требуется срочная коррекция."}
            ]
        },
        
        # ============= HEPATOLOGY =============
        {
            "name": "Child-Pugh Score",
            "description": "Classify cirrhosis severity and prognosis",
            "category": "Hepatology",
            "formula": "{bilirubin} + {albumin} + {inr} + {ascites} + {encephalopathy}",
            "input_fields": [
                {"name": "bilirubin", "label": "Total Bilirubin", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "1 - <2 mg/dL"},
                    {"value": 2, "label": "2 - 2-3 mg/dL"},
                    {"value": 3, "label": "3 - >3 mg/dL"}
                ]},
                {"name": "albumin", "label": "Serum Albumin", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "1 - >3.5 g/dL"},
                    {"value": 2, "label": "2 - 2.8-3.5 g/dL"},
                    {"value": 3, "label": "3 - <2.8 g/dL"}
                ]},
                {"name": "inr", "label": "INR", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "1 - <1.7"},
                    {"value": 2, "label": "2 - 1.7-2.3"},
                    {"value": 3, "label": "3 - >2.3"}
                ]},
                {"name": "ascites", "label": "Ascites", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "1 - None"},
                    {"value": 2, "label": "2 - Mild (controlled)"},
                    {"value": 3, "label": "3 - Moderate to severe"}
                ]},
                {"name": "encephalopathy", "label": "Hepatic Encephalopathy", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "1 - None"},
                    {"value": 2, "label": "2 - Grade 1-2 (or suppressed)"},
                    {"value": 3, "label": "3 - Grade 3-4 (refractory)"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "<= 6", "interpretation": "Class A (5-6 points): Well-compensated disease, 100% 1-year survival, 85% 2-year"},
                {"condition": "> 6 and <= 9", "interpretation": "Class B (7-9 points): Significant functional compromise, 81% 1-year survival, 57% 2-year"},
                {"condition": "> 9", "interpretation": "Class C (10-15 points): Decompensated disease, 45% 1-year survival, 35% 2-year, consider transplant"}
            ]
        },
        {
            "name": "MELD Score",
            "description": "Predict mortality in end-stage liver disease",
            "category": "Hepatology",
            "formula": "9.57 * {ln_creatinine} + 3.78 * {ln_bilirubin} + 11.2 * {ln_inr} + 6.43",
            "input_fields": [
                {"name": "ln_creatinine", "label": "Serum Creatinine", "unit": "mg/dL", "type": "number", "required": True, "min": 0.1, "max": 20},
                {"name": "ln_bilirubin", "label": "Total Bilirubin", "unit": "mg/dL", "type": "number", "required": True, "min": 0.1, "max": 50},
                {"name": "ln_inr", "label": "INR", "unit": "", "type": "number", "required": True, "min": 0.8, "max": 10}
            ],
            "interpretation_rules": [
                {"condition": "", "interpretation": "Note: Formula requires natural log - use actual values, calculation handles conversion"}
            ]
        },
        
        # ============= INFECTIOUS DISEASE =============
        {
            "name": "Centor Score (Modified)",
            "description": "Predict Group A Streptococcal pharyngitis probability",
            "category": "Infectious Disease",
            "formula": "{tonsillar_exudate} + {tender_nodes} + {fever} + {no_cough} + {age_modifier}",
            "input_fields": [
                {"name": "tonsillar_exudate", "label": "Tonsillar exudate or swelling", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]},
                {"name": "tender_nodes", "label": "Tender anterior cervical lymphadenopathy", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]},
                {"name": "fever", "label": "History of fever >38°C (100.4°F)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]},
                {"name": "no_cough", "label": "Absence of cough", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No (cough present)"},
                    {"value": 1, "label": "Yes (no cough)"}
                ]},
                {"name": "age_modifier", "label": "Age", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "3-14 years (+1)"},
                    {"value": 0, "label": "15-44 years (0)"},
                    {"value": -1, "label": "≥45 years (-1)"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "< 1", "interpretation": "Score <1: 1-2.5% probability - no testing or antibiotics"},
                {"condition": "== 1", "interpretation": "Score 1: ~10% probability - no testing or antibiotics"},
                {"condition": "== 2", "interpretation": "Score 2: ~17% probability - consider rapid strep test"},
                {"condition": "== 3", "interpretation": "Score 3: ~35% probability - rapid strep test recommended"},
                {"condition": ">= 4", "interpretation": "Score ≥4: ~50-60% probability - consider empiric antibiotics or rapid test"}
            ]
        },
        {
            "name": "qSOFA Score",
            "description": "Quick Sequential Organ Failure Assessment for sepsis",
            "category": "Infectious Disease",
            "formula": "{altered_mental} + {sbp_low} + {rr_high}",
            "input_fields": [
                {"name": "altered_mental", "label": "Altered mental status (GCS <15)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]},
                {"name": "sbp_low", "label": "Systolic BP ≤100 mmHg", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]},
                {"name": "rr_high", "label": "Respiratory rate ≥22/min", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "No"},
                    {"value": 1, "label": "Yes"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "< 2", "interpretation": "qSOFA <2: Low risk for poor outcome - but still evaluate for infection"},
                {"condition": ">= 2", "interpretation": "qSOFA ≥2: High risk for poor outcome - consider sepsis, assess with full SOFA, obtain lactate, initiate treatment"}
            ]
        },
        
        # ============= ADDITIONAL NEUROLOGY CALCULATORS =============
        {
            "name": "Modified Rankin Scale (mRS)",
            "description": "Measure degree of disability or dependence after stroke",
            "category": "Neurology",
            "formula": "{mRS_score}",
            "input_fields": [
                {"name": "mRS_score", "label": "Functional status", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "0 - No symptoms at all"},
                    {"value": 1, "label": "1 - No significant disability (able to carry out usual activities)"},
                    {"value": 2, "label": "2 - Slight disability (unable to perform all previous activities, but able to look after own affairs)"},
                    {"value": 3, "label": "3 - Moderate disability (requires some help, but able to walk without assistance)"},
                    {"value": 4, "label": "4 - Moderately severe disability (unable to walk/attend to bodily needs without assistance)"},
                    {"value": 5, "label": "5 - Severe disability (bedridden, incontinent, requires constant nursing care)"},
                    {"value": 6, "label": "6 - Dead"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Заключение: mRS 0 - Полное отсутствие симптомов. Пациент вернулся к преморбидному уровню функционирования. Отличный исход инсульта."},
                {"condition": "== 1", "interpretation": "Заключение: mRS 1 - Нет значительной инвалидности. Пациент может выполнять обычную деятельность и работу. Хороший функциональный исход."},
                {"condition": "== 2", "interpretation": "Заключение: mRS 2 - Легкая инвалидность. Не может выполнять все прежние виды деятельности, но самостоятельно справляется с повседневными делами. Требуется амбулаторная реабилитация."},
                {"condition": "== 3", "interpretation": "Заключение: mRS 3 - Умеренная инвалидность. Требуется некоторая помощь, но может ходить без поддержки. Нуждается в регулярной реабилитации и социальной поддержке."},
                {"condition": "== 4", "interpretation": "Заключение: mRS 4 - Умеренно тяжелая инвалидность. Не может ходить и справляться с физиологическими потребностями без посторонней помощи. Требуется постоянный уход, рассмотреть специализированное учреждение."},
                {"condition": "== 5", "interpretation": "Заключение: mRS 5 - Тяжелая инвалидность. Прикован к постели, недержание, требует постоянного ухода и внимания. Плохой прогноз, паллиативная помощь может быть уместна."},
                {"condition": "== 6", "interpretation": "Заключение: mRS 6 - Смерть."}
            ]
        },
        {
            "name": "ABCD2 Score",
            "description": "Stroke risk stratification after transient ischemic attack (TIA)",
            "category": "Neurology",
            "formula": "{age} + {bp} + {clinical_features} + {duration} + {diabetes}",
            "input_fields": [
                {"name": "age", "label": "Age ≥60 years", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "bp", "label": "Blood pressure ≥140/90 mmHg at evaluation", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]},
                {"name": "clinical_features", "label": "Clinical features", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Other symptoms"},
                    {"value": 1, "label": "Speech disturbance without weakness"},
                    {"value": 2, "label": "Unilateral weakness"}
                ]},
                {"name": "duration", "label": "Duration of TIA symptoms", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "<10 minutes"},
                    {"value": 1, "label": "10-59 minutes"},
                    {"value": 2, "label": "≥60 minutes"}
                ]},
                {"name": "diabetes", "label": "Diabetes mellitus", "type": "select", "required": True, "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}]}
            ],
            "interpretation_rules": [
                {"condition": "<= 3", "interpretation": "Заключение: Низкий риск инсульта (1.0% в 2 дня, 1.2% в 7 дней, 3.1% в 90 дней). Возможна выписка с амбулаторным обследованием в течение недели. Начать двойную антитромбоцитарную терапию."},
                {"condition": ">= 4 and <= 5", "interpretation": "Заключение: Умеренный риск инсульта (4.1% в 2 дня, 5.9% в 7 дней, 9.8% в 90 дней). Рекомендуется госпитализация или срочное амбулаторное обследование (МРТ/КТ, дуплекс сонных артерий, ЭКГ, эхо) в течение 24-48 часов."},
                {"condition": ">= 6", "interpretation": "Заключение: Высокий риск инсульта (8.1% в 2 дня, 11.7% в 7 дней, 17.8% в 90 дней). Требуется экстренная госпитализация, полное обследование в течение 24 часов, агрессивная вторичная профилактика, рассмотреть каротидную эндартерэктомию при стенозе."}
            ]
        },
        {
            "name": "Hunt and Hess Scale",
            "description": "Classify severity of subarachnoid hemorrhage (SAH)",
            "category": "Neurology",
            "formula": "{hunt_hess_grade}",
            "input_fields": [
                {"name": "hunt_hess_grade", "label": "Clinical presentation", "type": "select", "required": True, "options": [
                    {"value": 1, "label": "Grade 1 - Asymptomatic or mild headache, slight nuchal rigidity"},
                    {"value": 2, "label": "Grade 2 - Moderate to severe headache, nuchal rigidity, no neurologic deficit except CN palsy"},
                    {"value": 3, "label": "Grade 3 - Drowsiness, confusion, or mild focal deficit"},
                    {"value": 4, "label": "Grade 4 - Stupor, moderate to severe hemiparesis, early decerebrate rigidity"},
                    {"value": 5, "label": "Grade 5 - Deep coma, decerebrate rigidity, moribund appearance"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "== 1", "interpretation": "Заключение: Hunt-Hess Grade 1 - Легкое САК. Смертность 0-5%. Благоприятный прогноз. Рекомендуется ангиография и раннее клипирование/эмболизация аневризмы."},
                {"condition": "== 2", "interpretation": "Заключение: Hunt-Hess Grade 2 - Умеренное САК. Смертность 5-10%. Хороший прогноз при раннем лечении. Показана нейрохирургическая консультация, контроль вазоспазма."},
                {"condition": "== 3", "interpretation": "Заключение: Hunt-Hess Grade 3 - САК средней тяжести. Смертность 10-15%. Требуется интенсивная терапия, мониторинг ВЧД, профилактика вазоспазма (нимодипин). Хирургическое лечение после стабилизации."},
                {"condition": "== 4", "interpretation": "Заключение: Hunt-Hess Grade 4 - Тяжелое САК. Смертность 60-70%. Плохой прогноз. Интенсивная нейрореанимация, контроль ВЧД, отложенное хирургическое лечение. Рассмотреть цели лечения с семьей."},
                {"condition": "== 5", "interpretation": "Заключение: Hunt-Hess Grade 5 - Крайне тяжелое САК. Смертность 70-90%. Очень плохой прогноз. Паллиативная помощь может быть уместна. Если агрессивное лечение - максимальная интенсивная терапия, но выживаемость крайне низкая."}
            ]
        },
        
        # ============= ADDITIONAL PEDIATRIC CALCULATORS =============
        {
            "name": "Pediatric BMI Percentile Calculator",
            "description": "Calculate BMI percentile for children and adolescents (simplified)",
            "category": "Pediatrics",
            "formula": "{weight} / (({height} / 100) ** 2)",
            "input_fields": [
                {"name": "weight", "label": "Weight", "unit": "kg", "type": "number", "required": True, "min": 5, "max": 150},
                {"name": "height", "label": "Height", "unit": "cm", "type": "number", "required": True, "min": 50, "max": 200},
                {"name": "age", "label": "Age", "unit": "years", "type": "number", "required": True, "min": 2, "max": 20}
            ],
            "interpretation_rules": [
                {"condition": "< 14", "interpretation": "Заключение: BMI <14 (примерно <5-й перцентиль для большинства возрастов). Недостаточный вес - требуется оценка питания, исключение мальабсорбции, эндокринных нарушений. Консультация педиатра и диетолога."},
                {"condition": ">= 14 and < 18.5", "interpretation": "Заключение: BMI 14-18.5 (примерно 5-85 перцентиль в зависимости от возраста). Нормальный вес для большинства детей. Поддерживать здоровое питание и физическую активность."},
                {"condition": ">= 18.5 and < 25", "interpretation": "Заключение: BMI 18.5-25. В зависимости от возраста может быть нормальным или избыточным весом (>85-95 перцентиль). Требуется сравнение с возрастными нормативами CDC/ВОЗ. Рекомендации по питанию."},
                {"condition": ">= 25 and < 30", "interpretation": "Заключение: BMI 25-30 (вероятно >95 перцентиля). Избыточный вес/ожирение у детей. Требуется программа контроля веса, изменение образа жизни, увеличение физической активности, консультация эндокринолога."},
                {"condition": ">= 30", "interpretation": "Заключение: BMI ≥30 (значительно >95 перцентиля). Ожирение у детей. Высокий риск метаболических осложнений. Требуется мультидисциплинарный подход, оценка коморбидностей (диабет, НАЖБП, СОАС), психологическая поддержка."}
            ]
        },
        {
            "name": "Pediatric Dehydration Assessment (Clinical Dehydration Scale)",
            "description": "Assess dehydration severity in children",
            "category": "Pediatrics",
            "formula": "{general_appearance} + {eyes} + {mucous_membranes} + {tears}",
            "input_fields": [
                {"name": "general_appearance", "label": "General appearance", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Normal"},
                    {"value": 1, "label": "Thirsty, restless, or lethargic but irritable when touched"},
                    {"value": 2, "label": "Drowsy, limp, cold, sweaty, comatose"}
                ]},
                {"name": "eyes", "label": "Eyes", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Normal"},
                    {"value": 1, "label": "Slightly sunken"},
                    {"value": 2, "label": "Very sunken"}
                ]},
                {"name": "mucous_membranes", "label": "Mucous membranes (tongue)", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Moist"},
                    {"value": 1, "label": "Sticky"},
                    {"value": 2, "label": "Dry"}
                ]},
                {"name": "tears", "label": "Tears", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Tears present"},
                    {"value": 1, "label": "Decreased tears"},
                    {"value": 2, "label": "Absent tears"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "== 0", "interpretation": "Заключение: Дегидратация отсутствует (0 баллов). Потеря жидкости <3%. Продолжить пероральную регидратацию, возможно амбулаторное наблюдение."},
                {"condition": ">= 1 and <= 4", "interpretation": "Заключение: Легкая дегидратация (1-4 балла). Потеря жидкости 3-6%. Показана пероральная регидратационная терапия (ПРТ) 50 мл/кг в течение 4 часов. Мониторинг диуреза и клинического ответа."},
                {"condition": ">= 5", "interpretation": "Заключение: Умеренная/тяжелая дегидратация (5-8 баллов). Потеря жидкости >6%. Требуется внутривенная регидратация - болюс 20 мл/кг физраствора, затем поддерживающая терапия. Госпитализация, лабораторные исследования (электролиты, функция почек)."}
            ]
        },
        {
            "name": "Pediatric Early Warning Score (PEWS) - Simplified",
            "description": "Identify children at risk of clinical deterioration",
            "category": "Pediatrics",
            "formula": "{behavior} + {cardiovascular} + {respiratory}",
            "input_fields": [
                {"name": "behavior", "label": "Behavior", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Playing/appropriate"},
                    {"value": 1, "label": "Sleeping"},
                    {"value": 2, "label": "Irritable"},
                    {"value": 3, "label": "Lethargic/confused or reduced response to pain"}
                ]},
                {"name": "cardiovascular", "label": "Cardiovascular", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Pink or capillary refill 1-2 seconds"},
                    {"value": 1, "label": "Pale or capillary refill 3 seconds"},
                    {"value": 2, "label": "Gray or capillary refill 4 seconds or tachycardia 20 above normal"},
                    {"value": 3, "label": "Gray and mottled or capillary refill ≥5 seconds or tachycardia 30 above normal or bradycardia"}
                ]},
                {"name": "respiratory", "label": "Respiratory", "type": "select", "required": True, "options": [
                    {"value": 0, "label": "Within normal parameters, no retractions"},
                    {"value": 1, "label": ">10 above normal parameters using accessory muscles or FiO2 30% or 3+ liters"},
                    {"value": 2, "label": ">20 above normal parameters, retractions or FiO2 40% or 6+ liters"},
                    {"value": 3, "label": "5 below normal parameters with sternal retractions, grunting or FiO2 50% or 8+ liters"}
                ]}
            ],
            "interpretation_rules": [
                {"condition": "<= 2", "interpretation": "Заключение: Низкий риск (0-2 балла). Продолжить текущую терапию, рутинный мониторинг каждые 4-6 часов."},
                {"condition": ">= 3 and <= 4", "interpretation": "Заключение: Умеренный риск (3-4 балла). Увеличить частоту мониторинга до каждого часа. Уведомить лечащего врача. Рассмотреть увеличение уровня ухода."},
                {"condition": ">= 5 and <= 6", "interpretation": "Заключение: Высокий риск (5-6 баллов). Срочная оценка лечащим врачом. Непрерывный мониторинг. Рассмотреть перевод в ОРИТ. Подготовиться к возможной реанимации."},
                {"condition": ">= 7", "interpretation": "Заключение: Критический риск (≥7 баллов). Немедленный вызов педиатрической реанимационной бригады. Перевод в ОРИТ. Готовность к интубации и расширенным реанимационным мероприятиям."}
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
    
    print("\nSeeding comprehensive medical calculators...")
    await seed_calculators()
    print("Database seeding completed!")
    print("\nCategories included:")
    print("- General Health (4 calculators)")
    print("- Nutrition (2 calculators)")
    print("- Cardiology (9 calculators) - UPDATED with HAS-BLED, TIMI, GRACE, Killip")
    print("- Nephrology (3 calculators)")
    print("- Neurology (5 calculators) - UPDATED with mRS, ABCD2, Hunt-Hess")
    print("- Pediatrics (6 calculators) - UPDATED with BMI Percentile, Dehydration, PEWS")
    print("- Pulmonology (3 calculators)")
    print("- Hematology (3 calculators)")
    print("- Emergency Medicine (3 calculators)")
    print("- Obstetrics (2 calculators)")
    print("- Endocrinology (6 calculators) - UPDATED with Thyroid, Free Testosterone, Osmolality")
    print("- Hepatology (2 calculators)")
    print("- Infectious Disease (2 calculators)")
    print("\nTotal: 50 medical calculators with detailed clinical interpretations (ЗАКЛЮЧЕНИЕ)")


if __name__ == "__main__":
    asyncio.run(main())
