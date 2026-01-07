"""
Database seeding script for calculators
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Calculator


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_calculators():
    """Seed database with calculator data"""
    calculators_data = [
        {
            "name": "BMI Calculator",
            "name_ru": "Калькулятор ИМТ",
            "description": "Calculate Body Mass Index",
            "description_ru": "Рассчитать индекс массы тела",
            "category": "General Health",
            "category_ru": "Общее здоровье",
            "formula": "{weight} / (({height} / 100) ** 2)",
            "input_fields": [
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 300
                },
                {
                    "name": "height",
                    "label": "Height (cm)",
                    "label_ru": "Рост (см)",
                    "type": "number",
                    "required": True,
                    "min_value": 100,
                    "max_value": 250
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 18.5",
                    "interpretation": "Underweight",
                    "interpretation_ru": "Недостаточный вес"
                },
                {
                    "condition": ">= 18.5 and < 25",
                    "interpretation": "Normal weight",
                    "interpretation_ru": "Нормальный вес"
                },
                {
                    "condition": ">= 25 and < 30",
                    "interpretation": "Overweight",
                    "interpretation_ru": "Избыточный вес"
                },
                {
                    "condition": ">= 30",
                    "interpretation": "Obese",
                    "interpretation_ru": "Ожирение"
                }
            ]
        },
        {
            "name": "APGAR Score",
            "name_ru": "Шкала Апгар",
            "description": "Assess newborn health status",
            "description_ru": "Оценка состояния новорожденного",
            "category": "Pediatrics",
            "category_ru": "Педиатрия",
            "formula": "{appearance} + {pulse} + {grimace} + {activity} + {respiration}",
            "input_fields": [
                {
                    "name": "appearance",
                    "label": "Appearance (color)",
                    "label_ru": "Внешний вид (цвет)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Blue/pale", "label_ru": "Синий/бледный"},
                        {"value": 1, "label": "Body pink, extremities blue", "label_ru": "Тело розовое, конечности синие"},
                        {"value": 2, "label": "All pink", "label_ru": "Весь розовый"}
                    ]
                },
                {
                    "name": "pulse",
                    "label": "Pulse (heart rate)",
                    "label_ru": "Пульс (ЧСС)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Absent", "label_ru": "Отсутствует"},
                        {"value": 1, "label": "< 100 bpm", "label_ru": "< 100 уд/мин"},
                        {"value": 2, "label": "≥ 100 bpm", "label_ru": "≥ 100 уд/мин"}
                    ]
                },
                {
                    "name": "grimace",
                    "label": "Grimace (reflex)",
                    "label_ru": "Гримаса (рефлекс)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No response", "label_ru": "Нет ответа"},
                        {"value": 1, "label": "Grimace", "label_ru": "Гримаса"},
                        {"value": 2, "label": "Cry", "label_ru": "Плач"}
                    ]
                },
                {
                    "name": "activity",
                    "label": "Activity (muscle tone)",
                    "label_ru": "Активность (мышечный тонус)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Limp", "label_ru": "Вялый"},
                        {"value": 1, "label": "Some flexion", "label_ru": "Слабое сгибание"},
                        {"value": 2, "label": "Active movement", "label_ru": "Активные движения"}
                    ]
                },
                {
                    "name": "respiration",
                    "label": "Respiration",
                    "label_ru": "Дыхание",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Absent", "label_ru": "Отсутствует"},
                        {"value": 1, "label": "Weak/irregular", "label_ru": "Слабое/нерегулярное"},
                        {"value": 2, "label": "Strong/crying", "label_ru": "Сильное/крик"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 3",
                    "interpretation": "Critically low - immediate resuscitation needed",
                    "interpretation_ru": "Критически низкий - требуется немедленная реанимация"
                },
                {
                    "condition": ">= 4 and <= 6",
                    "interpretation": "Moderately abnormal - needs assistance",
                    "interpretation_ru": "Умеренно патологический - нужна помощь"
                },
                {
                    "condition": ">= 7 and <= 10",
                    "interpretation": "Normal condition",
                    "interpretation_ru": "Нормальное состояние"
                }
            ]
        },
        {
            "name": "Pregnancy Due Date",
            "name_ru": "Предполагаемая дата родов",
            "description": "Calculate estimated delivery date",
            "description_ru": "Рассчитать предполагаемую дату родов",
            "category": "Obstetrics",
            "category_ru": "Акушерство",
            "formula": "{gestational_age} * 7",
            "input_fields": [
                {
                    "name": "gestational_age",
                    "label": "Weeks since last period",
                    "label_ru": "Недель с последних месячных",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 42
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Days since last menstrual period",
                    "interpretation_ru": "Дней с последней менструации"
                }
            ]
        },
        {
            "name": "Ideal Body Weight",
            "name_ru": "Идеальная масса тела",
            "description": "Calculate ideal weight (Devine formula)",
            "description_ru": "Рассчитать идеальный вес (формула Дивайна)",
            "category": "General Health",
            "category_ru": "Общее здоровье",
            "formula": "50 + 2.3 * (({height} / 2.54) - 60)",
            "input_fields": [
                {
                    "name": "height",
                    "label": "Height (cm)",
                    "label_ru": "Рост (см)",
                    "type": "number",
                    "required": True,
                    "min_value": 100,
                    "max_value": 250
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Ideal body weight in kg (male formula)",
                    "interpretation_ru": "Идеальная масса тела в кг (формула для мужчин)"
                }
            ]
        },
        {
            "name": "Body Surface Area",
            "name_ru": "Площадь поверхности тела",
            "description": "Calculate BSA (Mosteller formula)",
            "description_ru": "Рассчитать ППТ (формула Мостеллера)",
            "category": "General Health",
            "category_ru": "Общее здоровье",
            "formula": "(({height} * {weight}) / 3600) ** 0.5",
            "input_fields": [
                {
                    "name": "height",
                    "label": "Height (cm)",
                    "label_ru": "Рост (см)",
                    "type": "number",
                    "required": True,
                    "min_value": 100,
                    "max_value": 250
                },
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 300
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Body surface area in m²",
                    "interpretation_ru": "Площадь поверхности тела в м²"
                }
            ]
        },
        {
            "name": "Corrected QT Interval",
            "name_ru": "Скорректированный интервал QT",
            "description": "Calculate QTc (Bazett formula)",
            "description_ru": "Рассчитать QTc (формула Базетта)",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{qt_interval} / ({rr_interval} ** 0.5)",
            "input_fields": [
                {
                    "name": "qt_interval",
                    "label": "QT Interval (ms)",
                    "label_ru": "Интервал QT (мс)",
                    "type": "number",
                    "required": True,
                    "min_value": 200,
                    "max_value": 600
                },
                {
                    "name": "rr_interval",
                    "label": "RR Interval (s)",
                    "label_ru": "Интервал RR (с)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.4,
                    "max_value": 2.0
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 430",
                    "interpretation": "Normal QTc",
                    "interpretation_ru": "Нормальный QTc"
                },
                {
                    "condition": ">= 430 and < 450",
                    "interpretation": "Borderline QTc",
                    "interpretation_ru": "Пограничный QTc"
                },
                {
                    "condition": ">= 450",
                    "interpretation": "Prolonged QTc - risk of arrhythmia",
                    "interpretation_ru": "Удлиненный QTc - риск аритмии"
                }
            ]
        },
        {
            "name": "Anion Gap",
            "name_ru": "Анионная разница",
            "description": "Calculate serum anion gap",
            "description_ru": "Рассчитать анионную разницу сыворотки",
            "category": "Laboratory",
            "category_ru": "Лабораторная диагностика",
            "formula": "{sodium} - ({chloride} + {bicarbonate})",
            "input_fields": [
                {
                    "name": "sodium",
                    "label": "Sodium (mEq/L)",
                    "label_ru": "Натрий (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 120,
                    "max_value": 160
                },
                {
                    "name": "chloride",
                    "label": "Chloride (mEq/L)",
                    "label_ru": "Хлорид (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 80,
                    "max_value": 120
                },
                {
                    "name": "bicarbonate",
                    "label": "Bicarbonate (mEq/L)",
                    "label_ru": "Бикарбонат (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 10,
                    "max_value": 40
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 8",
                    "interpretation": "Low anion gap",
                    "interpretation_ru": "Низкая анионная разница"
                },
                {
                    "condition": ">= 8 and <= 12",
                    "interpretation": "Normal anion gap",
                    "interpretation_ru": "Нормальная анионная разница"
                },
                {
                    "condition": "> 12",
                    "interpretation": "High anion gap - metabolic acidosis",
                    "interpretation_ru": "Высокая анионная разница - метаболический ацидоз"
                }
            ]
        },
        {
            "name": "Fractional Sodium Excretion",
            "name_ru": "Фракционная экскреция натрия",
            "description": "Differentiate causes of acute kidney injury",
            "description_ru": "Дифференцировать причины острого повреждения почек",
            "category": "Nephrology",
            "category_ru": "Нефрология",
            "formula": "(({urine_sodium} / {plasma_sodium}) / ({urine_creatinine} / {plasma_creatinine})) * 100",
            "input_fields": [
                {
                    "name": "urine_sodium",
                    "label": "Urine Sodium (mEq/L)",
                    "label_ru": "Натрий мочи (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 200
                },
                {
                    "name": "plasma_sodium",
                    "label": "Plasma Sodium (mEq/L)",
                    "label_ru": "Натрий плазмы (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 120,
                    "max_value": 160
                },
                {
                    "name": "urine_creatinine",
                    "label": "Urine Creatinine (mg/dL)",
                    "label_ru": "Креатинин мочи (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 10,
                    "max_value": 300
                },
                {
                    "name": "plasma_creatinine",
                    "label": "Plasma Creatinine (mg/dL)",
                    "label_ru": "Креатинин плазмы (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.5,
                    "max_value": 15
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 1",
                    "interpretation": "Prerenal azotemia (volume depletion)",
                    "interpretation_ru": "Преренальная азотемия (дефицит объема)"
                },
                {
                    "condition": ">= 1 and < 2",
                    "interpretation": "Borderline",
                    "interpretation_ru": "Пограничное значение"
                },
                {
                    "condition": ">= 2",
                    "interpretation": "Acute tubular necrosis",
                    "interpretation_ru": "Острый тубулярный некроз"
                }
            ]
        },
        {
            "name": "CHADS2 Score",
            "name_ru": "Шкала CHADS2",
            "description": "Stroke risk in atrial fibrillation",
            "description_ru": "Риск инсульта при фибрилляции предсердий",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{chf} + {hypertension} + {age} + {diabetes} + (2 * {stroke_tia})",
            "input_fields": [
                {
                    "name": "chf",
                    "label": "Congestive Heart Failure",
                    "label_ru": "Сердечная недостаточность",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "hypertension",
                    "label": "Hypertension",
                    "label_ru": "Гипертензия",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "age",
                    "label": "Age ≥ 75 years",
                    "label_ru": "Возраст ≥ 75 лет",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "diabetes",
                    "label": "Diabetes Mellitus",
                    "label_ru": "Сахарный диабет",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "stroke_tia",
                    "label": "Prior Stroke/TIA",
                    "label_ru": "Инсульт/ТИА в анамнезе",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "= 0",
                    "interpretation": "Low risk (1.9% annual stroke risk)",
                    "interpretation_ru": "Низкий риск (1.9% годовой риск инсульта)"
                },
                {
                    "condition": "= 1",
                    "interpretation": "Low-moderate risk (2.8% annual)",
                    "interpretation_ru": "Низкий-умеренный риск (2.8% годовой)"
                },
                {
                    "condition": "= 2",
                    "interpretation": "Moderate risk (4.0% annual)",
                    "interpretation_ru": "Умеренный риск (4.0% годовой)"
                },
                {
                    "condition": ">= 3",
                    "interpretation": "High risk (>5.9% annual) - anticoagulation recommended",
                    "interpretation_ru": "Высокий риск (>5.9% годовой) - рекомендована антикоагуляция"
                }
            ]
        },
        {
            "name": "Wells DVT Score",
            "name_ru": "Шкала Уэллса для ТГВ",
            "description": "Assess probability of deep vein thrombosis",
            "description_ru": "Оценка вероятности тромбоза глубоких вен",
            "category": "Hematology",
            "category_ru": "Гематология",
            "formula": "{active_cancer} + {paralysis} + {bedridden} + {localized_tenderness} + {entire_leg_swollen} + {calf_swelling} + {pitting_edema} + {collateral_veins} + {alternative_diagnosis}",
            "input_fields": [
                {
                    "name": "active_cancer",
                    "label": "Active cancer",
                    "label_ru": "Активный рак",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "paralysis",
                    "label": "Paralysis/recent plaster",
                    "label_ru": "Паралич/недавний гипс",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "bedridden",
                    "label": "Bedridden >3 days/surgery",
                    "label_ru": "Постельный режим >3 дней/операция",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "localized_tenderness",
                    "label": "Localized tenderness along veins",
                    "label_ru": "Локальная болезненность вдоль вен",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "entire_leg_swollen",
                    "label": "Entire leg swollen",
                    "label_ru": "Отек всей ноги",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "calf_swelling",
                    "label": "Calf swelling >3cm vs other leg",
                    "label_ru": "Отек икры >3см vs другая нога",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "pitting_edema",
                    "label": "Pitting edema",
                    "label_ru": "Ямочный отек",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "collateral_veins",
                    "label": "Collateral superficial veins",
                    "label_ru": "Коллатеральные поверхностные вены",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "alternative_diagnosis",
                    "label": "Alternative diagnosis likely",
                    "label_ru": "Альтернативный диагноз вероятен",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": -2, "label": "Yes", "label_ru": "Да"},
                        {"value": 0, "label": "No", "label_ru": "Нет"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 0",
                    "interpretation": "Low probability (3% DVT risk)",
                    "interpretation_ru": "Низкая вероятность (3% риск ТГВ)"
                },
                {
                    "condition": ">= 1 and <= 2",
                    "interpretation": "Moderate probability (17% DVT risk)",
                    "interpretation_ru": "Умеренная вероятность (17% риск ТГВ)"
                },
                {
                    "condition": ">= 3",
                    "interpretation": "High probability (75% DVT risk) - imaging required",
                    "interpretation_ru": "Высокая вероятность (75% риск ТГВ) - требуется визуализация"
                }
            ]
        },
        {
            "name": "Albumin-Globulin Ratio",
            "name_ru": "Соотношение альбумин/глобулин",
            "description": "Assess liver and kidney function",
            "description_ru": "Оценка функции печени и почек",
            "category": "Laboratory",
            "category_ru": "Лабораторная диагностика",
            "formula": "{albumin} / ({total_protein} - {albumin})",
            "input_fields": [
                {
                    "name": "albumin",
                    "label": "Albumin (g/dL)",
                    "label_ru": "Альбумин (г/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 1.0,
                    "max_value": 6.0
                },
                {
                    "name": "total_protein",
                    "label": "Total Protein (g/dL)",
                    "label_ru": "Общий белок (г/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 3.0,
                    "max_value": 10.0
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 1.0",
                    "interpretation": "Low ratio - possible liver disease or inflammation",
                    "interpretation_ru": "Низкое соотношение - возможна болезнь печени или воспаление"
                },
                {
                    "condition": ">= 1.0 and <= 2.5",
                    "interpretation": "Normal albumin-globulin ratio",
                    "interpretation_ru": "Нормальное соотношение альбумин/глобулин"
                },
                {
                    "condition": "> 2.5",
                    "interpretation": "High ratio - possible dehydration or protein loss",
                    "interpretation_ru": "Высокое соотношение - возможна дегидратация или потеря белка"
                }
            ]
        },
        {
            "name": "Basal Metabolic Rate",
            "name_ru": "Базальный метаболизм",
            "description": "Calculate daily calorie needs",
            "description_ru": "Рассчитать суточную потребность в калориях",
            "category": "Nutrition",
            "category_ru": "Питание",
            "formula": "88.362 + (13.397 * {weight}) + (4.799 * {height}) - (5.677 * {age})",
            "input_fields": [
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 300
                },
                {
                    "name": "height",
                    "label": "Height (cm)",
                    "label_ru": "Рост (см)",
                    "type": "number",
                    "required": True,
                    "min_value": 100,
                    "max_value": 250
                },
                {
                    "name": "age",
                    "label": "Age (years)",
                    "label_ru": "Возраст (лет)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 120
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Daily calorie needs calculated",
                    "interpretation_ru": "Суточная потребность в калориях рассчитана"
                }
            ]
        },
        {
            "name": "HEART Score",
            "name_ru": "Шкала HEART",
            "description": "Assess chest pain risk",
            "description_ru": "Оценка риска при боли в груди",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{history} + {ecg} + {age} + {risk_factors} + {troponin}",
            "input_fields": [
                {
                    "name": "history",
                    "label": "History",
                    "label_ru": "Анамнез",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Slightly suspicious", "label_ru": "Слабо подозрительный"},
                        {"value": 1, "label": "Moderately suspicious", "label_ru": "Умеренно подозрительный"},
                        {"value": 2, "label": "Highly suspicious", "label_ru": "Высоко подозрительный"}
                    ]
                },
                {
                    "name": "ecg",
                    "label": "ECG",
                    "label_ru": "ЭКГ",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Normal", "label_ru": "Нормальная"},
                        {"value": 1, "label": "Non-specific changes", "label_ru": "Неспецифические изменения"},
                        {"value": 2, "label": "Significant changes", "label_ru": "Значительные изменения"}
                    ]
                },
                {
                    "name": "age",
                    "label": "Age",
                    "label_ru": "Возраст",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "< 45 years", "label_ru": "< 45 лет"},
                        {"value": 1, "label": "45-64 years", "label_ru": "45-64 лет"},
                        {"value": 2, "label": "≥ 65 years", "label_ru": "≥ 65 лет"}
                    ]
                },
                {
                    "name": "risk_factors",
                    "label": "Risk Factors",
                    "label_ru": "Факторы риска",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "None", "label_ru": "Нет"},
                        {"value": 1, "label": "1-2 factors", "label_ru": "1-2 фактора"},
                        {"value": 2, "label": "≥ 3 factors", "label_ru": "≥ 3 фактора"}
                    ]
                },
                {
                    "name": "troponin",
                    "label": "Troponin",
                    "label_ru": "Тропонин",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "Normal", "label_ru": "Нормальный"},
                        {"value": 1, "label": "1-3x normal", "label_ru": "1-3x норма"},
                        {"value": 2, "label": "> 3x normal", "label_ru": "> 3x норма"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 3",
                    "interpretation": "Low risk",
                    "interpretation_ru": "Низкий риск"
                },
                {
                    "condition": ">= 4 and < 7",
                    "interpretation": "Moderate risk",
                    "interpretation_ru": "Умеренный риск"
                },
                {
                    "condition": ">= 7",
                    "interpretation": "High risk",
                    "interpretation_ru": "Высокий риск"
                }
            ]
        },
        {
            "name": "Mean Arterial Pressure",
            "name_ru": "Среднее артериальное давление",
            "description": "Calculate MAP from blood pressure",
            "description_ru": "Рассчитать САД по артериальному давлению",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{diastolic} + ({systolic} - {diastolic}) / 3",
            "input_fields": [
                {
                    "name": "systolic",
                    "label": "Systolic BP (mmHg)",
                    "label_ru": "Систолическое АД (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 60,
                    "max_value": 250
                },
                {
                    "name": "diastolic",
                    "label": "Diastolic BP (mmHg)",
                    "label_ru": "Диастолическое АД (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 40,
                    "max_value": 150
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 70",
                    "interpretation": "Low MAP",
                    "interpretation_ru": "Низкое САД"
                },
                {
                    "condition": ">= 70 and <= 100",
                    "interpretation": "Normal MAP",
                    "interpretation_ru": "Нормальное САД"
                },
                {
                    "condition": "> 100",
                    "interpretation": "High MAP",
                    "interpretation_ru": "Высокое САД"
                }
            ]
        },
        {
            "name": "Creatinine Clearance",
            "name_ru": "Клиренс креатинина",
            "description": "Calculate kidney function (Cockcroft-Gault)",
            "description_ru": "Рассчитать функцию почек (Кокрофт-Голт)",
            "category": "Nephrology",
            "category_ru": "Нефрология",
            "formula": "((140 - {age}) * {weight}) / (72 * {creatinine})",
            "input_fields": [
                {
                    "name": "age",
                    "label": "Age (years)",
                    "label_ru": "Возраст (лет)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 120
                },
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 300
                },
                {
                    "name": "creatinine",
                    "label": "Serum Creatinine (mg/dL)",
                    "label_ru": "Креатинин сыворотки (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.1,
                    "max_value": 20
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 30",
                    "interpretation": "Severe kidney disease",
                    "interpretation_ru": "Тяжелое заболевание почек"
                },
                {
                    "condition": ">= 30 and < 60",
                    "interpretation": "Moderate kidney disease",
                    "interpretation_ru": "Умеренное заболевание почек"
                },
                {
                    "condition": ">= 60 and < 90",
                    "interpretation": "Mild kidney disease",
                    "interpretation_ru": "Легкое заболевание почек"
                },
                {
                    "condition": ">= 90",
                    "interpretation": "Normal kidney function",
                    "interpretation_ru": "Нормальная функция почек"
                }
            ]
        },
        {
            "name": "Glasgow Coma Scale",
            "name_ru": "Шкала комы Глазго",
            "description": "Assess level of consciousness",
            "description_ru": "Оценка уровня сознания",
            "category": "Neurology",
            "category_ru": "Неврология",
            "formula": "{eye_opening} + {verbal_response} + {motor_response}",
            "input_fields": [
                {
                    "name": "eye_opening",
                    "label": "Eye Opening",
                    "label_ru": "Открывание глаз",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 1, "label": "No response", "label_ru": "Нет ответа"},
                        {"value": 2, "label": "To pain", "label_ru": "На боль"},
                        {"value": 3, "label": "To speech", "label_ru": "На речь"},
                        {"value": 4, "label": "Spontaneous", "label_ru": "Спонтанное"}
                    ]
                },
                {
                    "name": "verbal_response",
                    "label": "Verbal Response",
                    "label_ru": "Речевой ответ",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 1, "label": "No response", "label_ru": "Нет ответа"},
                        {"value": 2, "label": "Incomprehensible sounds", "label_ru": "Невнятные звуки"},
                        {"value": 3, "label": "Inappropriate words", "label_ru": "Неадекватные слова"},
                        {"value": 4, "label": "Confused", "label_ru": "Спутанная речь"},
                        {"value": 5, "label": "Oriented", "label_ru": "Ориентирован"}
                    ]
                },
                {
                    "name": "motor_response",
                    "label": "Motor Response",
                    "label_ru": "Двигательный ответ",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 1, "label": "No response", "label_ru": "Нет ответа"},
                        {"value": 2, "label": "Decerebrate posture", "label_ru": "Децеребрация"},
                        {"value": 3, "label": "Decorticate posture", "label_ru": "Декортикация"},
                        {"value": 4, "label": "Withdraws from pain", "label_ru": "Отдергивание на боль"},
                        {"value": 5, "label": "Localizes pain", "label_ru": "Локализует боль"},
                        {"value": 6, "label": "Obeys commands", "label_ru": "Выполняет команды"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 8",
                    "interpretation": "Severe (Coma)",
                    "interpretation_ru": "Тяжелое (Кома)"
                },
                {
                    "condition": ">= 9 and <= 12",
                    "interpretation": "Moderate",
                    "interpretation_ru": "Умеренное"
                },
                {
                    "condition": ">= 13",
                    "interpretation": "Mild",
                    "interpretation_ru": "Легкое"
                }
            ]
        },
        {
            "name": "Pediatric Weight Estimation",
            "name_ru": "Оценка веса у детей",
            "description": "Estimate child weight by age (Broselow)",
            "description_ru": "Оценка веса ребенка по возрасту (Броселоу)",
            "category": "Pediatrics",
            "category_ru": "Педиатрия",
            "formula": "(2 * {age}) + 8",
            "input_fields": [
                {
                    "name": "age",
                    "label": "Age (years)",
                    "label_ru": "Возраст (лет)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 10
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Estimated weight in kg",
                    "interpretation_ru": "Оценочный вес в кг"
                }
            ]
        }
    ]
    
    async with AsyncSessionLocal() as session:
        # Check if calculators already exist
        result = await session.execute(select(Calculator))
        existing_calculators = result.scalars().all()
        
        if existing_calculators:
            print(f"Found {len(existing_calculators)} existing calculators. Deleting...")
            for calc in existing_calculators:
                await session.delete(calc)
            await session.commit()
            print("Existing calculators deleted.")
        
        # Add calculators
        # Define valid Calculator fields to filter out Russian translations
        valid_fields = {'name', 'description', 'category', 'formula', 'input_fields', 'interpretation_rules'}
        
        for calc_data in calculators_data:
            # Filter out unsupported fields (Russian translations)
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
