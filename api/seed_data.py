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
        },
        # NEW CALCULATORS - Cardiology
        {
            "name": "QTc Interval (Bazett)",
            "name_ru": "Корригированный интервал QT (Базетт)",
            "description": "Calculate corrected QT interval",
            "description_ru": "Рассчитать корригированный интервал QT",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{qt_interval} / (({rr_interval} / 1000) ** 0.5)",
            "input_fields": [
                {
                    "name": "qt_interval",
                    "label": "QT Interval (ms)",
                    "label_ru": "Интервал QT (мс)",
                    "type": "number",
                    "required": True,
                    "min_value": 200,
                    "max_value": 700
                },
                {
                    "name": "rr_interval",
                    "label": "RR Interval (ms)",
                    "label_ru": "Интервал RR (мс)",
                    "type": "number",
                    "required": True,
                    "min_value": 400,
                    "max_value": 2000
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 390",
                    "interpretation": "Normal QTc for males",
                    "interpretation_ru": "Нормальный QTc для мужчин"
                },
                {
                    "condition": ">= 390 and < 450",
                    "interpretation": "Borderline QTc",
                    "interpretation_ru": "Пограничный QTc"
                },
                {
                    "condition": ">= 450 and < 500",
                    "interpretation": "Prolonged QTc - monitor",
                    "interpretation_ru": "Удлиненный QTc - наблюдение"
                },
                {
                    "condition": ">= 500",
                    "interpretation": "Severely prolonged - high risk",
                    "interpretation_ru": "Значительно удлинен - высокий риск"
                }
            ]
        },
        {
            "name": "Framingham Risk Score (Simple)",
            "name_ru": "Фремингемская шкала риска (упрощенная)",
            "description": "10-year cardiovascular disease risk",
            "description_ru": "10-летний риск сердечно-сосудистых заболеваний",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "({age} * 0.5) + ({total_chol} / 10) + ({hdl_chol} / -5) + ({systolic_bp} / 10) + ({smoking} * 7) + ({diabetes} * 5)",
            "input_fields": [
                {
                    "name": "age",
                    "label": "Age (years)",
                    "label_ru": "Возраст (лет)",
                    "type": "number",
                    "required": True,
                    "min_value": 30,
                    "max_value": 74
                },
                {
                    "name": "total_chol",
                    "label": "Total Cholesterol (mg/dL)",
                    "label_ru": "Общий холестерин (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 100,
                    "max_value": 400
                },
                {
                    "name": "hdl_chol",
                    "label": "HDL Cholesterol (mg/dL)",
                    "label_ru": "Холестерин ЛПВП (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 100
                },
                {
                    "name": "systolic_bp",
                    "label": "Systolic BP (mmHg)",
                    "label_ru": "Систолическое АД (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 90,
                    "max_value": 200
                },
                {
                    "name": "smoking",
                    "label": "Current Smoker",
                    "label_ru": "Курит в настоящее время",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "diabetes",
                    "label": "Diabetes",
                    "label_ru": "Диабет",
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
                    "condition": "< 10",
                    "interpretation": "Low risk (<10% in 10 years)",
                    "interpretation_ru": "Низкий риск (<10% за 10 лет)"
                },
                {
                    "condition": ">= 10 and < 20",
                    "interpretation": "Moderate risk (10-20% in 10 years)",
                    "interpretation_ru": "Умеренный риск (10-20% за 10 лет)"
                },
                {
                    "condition": ">= 20",
                    "interpretation": "High risk (>20% in 10 years)",
                    "interpretation_ru": "Высокий риск (>20% за 10 лет)"
                }
            ]
        },
        {
            "name": "Cardiac Output",
            "name_ru": "Сердечный выброс",
            "description": "Calculate cardiac output",
            "description_ru": "Рассчитать сердечный выброс",
            "category": "Cardiology",
            "category_ru": "Кардиология",
            "formula": "{stroke_volume} * {heart_rate} / 1000",
            "input_fields": [
                {
                    "name": "stroke_volume",
                    "label": "Stroke Volume (mL)",
                    "label_ru": "Ударный объем (мл)",
                    "type": "number",
                    "required": True,
                    "min_value": 30,
                    "max_value": 150
                },
                {
                    "name": "heart_rate",
                    "label": "Heart Rate (bpm)",
                    "label_ru": "ЧСС (уд/мин)",
                    "type": "number",
                    "required": True,
                    "min_value": 40,
                    "max_value": 200
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 4.0",
                    "interpretation": "Low cardiac output",
                    "interpretation_ru": "Низкий сердечный выброс"
                },
                {
                    "condition": ">= 4.0 and <= 8.0",
                    "interpretation": "Normal cardiac output",
                    "interpretation_ru": "Нормальный сердечный выброс"
                },
                {
                    "condition": "> 8.0",
                    "interpretation": "High cardiac output",
                    "interpretation_ru": "Высокий сердечный выброс"
                }
            ]
        },
        # Nephrology
        {
            "name": "eGFR (MDRD)",
            "name_ru": "рСКФ (MDRD)",
            "description": "Estimated Glomerular Filtration Rate",
            "description_ru": "Расчетная скорость клубочковой фильтрации",
            "category": "Nephrology",
            "category_ru": "Нефрология",
            "formula": "175 * ({creatinine} ** -1.154) * ({age} ** -0.203)",
            "input_fields": [
                {
                    "name": "creatinine",
                    "label": "Serum Creatinine (mg/dL)",
                    "label_ru": "Креатинин сыворотки (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.1,
                    "max_value": 20
                },
                {
                    "name": "age",
                    "label": "Age (years)",
                    "label_ru": "Возраст (лет)",
                    "type": "number",
                    "required": True,
                    "min_value": 18,
                    "max_value": 120
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 15",
                    "interpretation": "Stage 5 CKD (kidney failure)",
                    "interpretation_ru": "ХБП 5 стадии (почечная недостаточность)"
                },
                {
                    "condition": ">= 15 and < 30",
                    "interpretation": "Stage 4 CKD (severe)",
                    "interpretation_ru": "ХБП 4 стадии (тяжелая)"
                },
                {
                    "condition": ">= 30 and < 60",
                    "interpretation": "Stage 3 CKD (moderate)",
                    "interpretation_ru": "ХБП 3 стадии (умеренная)"
                },
                {
                    "condition": ">= 60 and < 90",
                    "interpretation": "Stage 2 CKD (mild)",
                    "interpretation_ru": "ХБП 2 стадии (легкая)"
                },
                {
                    "condition": ">= 90",
                    "interpretation": "Normal kidney function",
                    "interpretation_ru": "Нормальная функция почек"
                }
            ]
        },
        {
            "name": "Fractional Excretion of Sodium",
            "name_ru": "Фракционная экскреция натрия",
            "description": "Calculate FENa for acute kidney injury",
            "description_ru": "Расчет FENa при острой почечной недостаточности",
            "category": "Nephrology",
            "category_ru": "Нефрология",
            "formula": "(({urine_na} * {serum_cr}) / ({serum_na} * {urine_cr})) * 100",
            "input_fields": [
                {
                    "name": "urine_na",
                    "label": "Urine Sodium (mEq/L)",
                    "label_ru": "Натрий мочи (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 300
                },
                {
                    "name": "serum_na",
                    "label": "Serum Sodium (mEq/L)",
                    "label_ru": "Натрий сыворотки (мЭкв/л)",
                    "type": "number",
                    "required": True,
                    "min_value": 120,
                    "max_value": 160
                },
                {
                    "name": "urine_cr",
                    "label": "Urine Creatinine (mg/dL)",
                    "label_ru": "Креатинин мочи (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 10,
                    "max_value": 300
                },
                {
                    "name": "serum_cr",
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
                    "condition": "< 1",
                    "interpretation": "Pre-renal azotemia (volume depletion)",
                    "interpretation_ru": "Преренальная азотемия (гиповолемия)"
                },
                {
                    "condition": ">= 1 and < 2",
                    "interpretation": "Indeterminate",
                    "interpretation_ru": "Неопределенный результат"
                },
                {
                    "condition": ">= 2",
                    "interpretation": "Acute tubular necrosis",
                    "interpretation_ru": "Острый тубулярный некроз"
                }
            ]
        },
        # Endocrinology & Diabetes
        {
            "name": "HbA1c to Average Glucose",
            "name_ru": "HbA1c в средний уровень глюкозы",
            "description": "Convert HbA1c to estimated average glucose",
            "description_ru": "Перевести HbA1c в средний уровень глюкозы",
            "category": "Endocrinology",
            "category_ru": "Эндокринология",
            "formula": "({hba1c} * 28.7) - 46.7",
            "input_fields": [
                {
                    "name": "hba1c",
                    "label": "HbA1c (%)",
                    "label_ru": "HbA1c (%)",
                    "type": "number",
                    "required": True,
                    "min_value": 4,
                    "max_value": 15
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 100",
                    "interpretation": "Normal glucose control (eAG <100 mg/dL)",
                    "interpretation_ru": "Нормальный контроль глюкозы (eAG <100 мг/дл)"
                },
                {
                    "condition": ">= 100 and < 154",
                    "interpretation": "Good glucose control (HbA1c <7%)",
                    "interpretation_ru": "Хороший контроль глюкозы (HbA1c <7%)"
                },
                {
                    "condition": ">= 154 and < 183",
                    "interpretation": "Fair glucose control (HbA1c 7-8%)",
                    "interpretation_ru": "Удовлетворительный контроль (HbA1c 7-8%)"
                },
                {
                    "condition": ">= 183",
                    "interpretation": "Poor glucose control (HbA1c >8%)",
                    "interpretation_ru": "Плохой контроль глюкозы (HbA1c >8%)"
                }
            ]
        },
        {
            "name": "Insulin Sensitivity Index",
            "name_ru": "Индекс чувствительности к инсулину",
            "description": "Calculate insulin sensitivity (QUICKI)",
            "description_ru": "Расчет чувствительности к инсулину (QUICKI)",
            "category": "Endocrinology",
            "category_ru": "Эндокринология",
            "formula": "1 / (({glucose} ** 0.3010) + ({insulin} ** 0.3010))",
            "input_fields": [
                {
                    "name": "glucose",
                    "label": "Fasting Glucose (mg/dL)",
                    "label_ru": "Глюкоза натощак (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 50,
                    "max_value": 400
                },
                {
                    "name": "insulin",
                    "label": "Fasting Insulin (μU/mL)",
                    "label_ru": "Инсулин натощак (мкЕд/мл)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 100
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 0.30",
                    "interpretation": "Insulin resistant",
                    "interpretation_ru": "Инсулинорезистентность"
                },
                {
                    "condition": ">= 0.30 and < 0.45",
                    "interpretation": "Decreased insulin sensitivity",
                    "interpretation_ru": "Сниженная чувствительность к инсулину"
                },
                {
                    "condition": ">= 0.45",
                    "interpretation": "Normal insulin sensitivity",
                    "interpretation_ru": "Нормальная чувствительность к инсулину"
                }
            ]
        },
        {
            "name": "Thyroid Hormone Dose",
            "name_ru": "Доза тиреоидных гормонов",
            "description": "Calculate levothyroxine dose by weight",
            "description_ru": "Расчет дозы левотироксина по весу",
            "category": "Endocrinology",
            "category_ru": "Эндокринология",
            "formula": "{weight} * 1.6",
            "input_fields": [
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 200
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Estimated levothyroxine dose in mcg/day",
                    "interpretation_ru": "Ориентировочная доза левотироксина в мкг/сут"
                }
            ]
        },
        # ICU & Critical Care
        {
            "name": "APACHE II Score (Simplified)",
            "name_ru": "Шкала APACHE II (упрощенная)",
            "description": "Acute Physiology and Chronic Health Evaluation",
            "description_ru": "Оценка острой физиологии и хронического здоровья",
            "category": "ICU",
            "category_ru": "Реанимация",
            "formula": "{age_points} + {temp_points} + {map_points} + {hr_points} + {rr_points} + {gcs_deficit}",
            "input_fields": [
                {
                    "name": "age_points",
                    "label": "Age Points (0-6)",
                    "label_ru": "Баллы за возраст (0-6)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 6
                },
                {
                    "name": "temp_points",
                    "label": "Temperature Points (0-4)",
                    "label_ru": "Баллы за температуру (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "map_points",
                    "label": "MAP Points (0-4)",
                    "label_ru": "Баллы за САД (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "hr_points",
                    "label": "Heart Rate Points (0-4)",
                    "label_ru": "Баллы за ЧСС (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "rr_points",
                    "label": "Respiratory Rate Points (0-4)",
                    "label_ru": "Баллы за ЧД (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "gcs_deficit",
                    "label": "GCS Deficit (15-GCS)",
                    "label_ru": "Дефицит ШКГ (15-ШКГ)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 12
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 15",
                    "interpretation": "Low mortality risk (<15%)",
                    "interpretation_ru": "Низкий риск смертности (<15%)"
                },
                {
                    "condition": ">= 15 and < 25",
                    "interpretation": "Moderate mortality risk (15-40%)",
                    "interpretation_ru": "Умеренный риск смертности (15-40%)"
                },
                {
                    "condition": ">= 25 and < 35",
                    "interpretation": "High mortality risk (40-80%)",
                    "interpretation_ru": "Высокий риск смертности (40-80%)"
                },
                {
                    "condition": ">= 35",
                    "interpretation": "Very high mortality risk (>80%)",
                    "interpretation_ru": "Очень высокий риск смертности (>80%)"
                }
            ]
        },
        {
            "name": "SOFA Score (Simplified)",
            "name_ru": "Шкала SOFA (упрощенная)",
            "description": "Sequential Organ Failure Assessment",
            "description_ru": "Последовательная оценка органной недостаточности",
            "category": "ICU",
            "category_ru": "Реанимация",
            "formula": "{resp_points} + {coag_points} + {liver_points} + {cardio_points} + {cns_points} + {renal_points}",
            "input_fields": [
                {
                    "name": "resp_points",
                    "label": "Respiration Points (0-4)",
                    "label_ru": "Баллы за дыхание (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "coag_points",
                    "label": "Coagulation Points (0-4)",
                    "label_ru": "Баллы за коагуляцию (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "liver_points",
                    "label": "Liver Points (0-4)",
                    "label_ru": "Баллы за печень (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "cardio_points",
                    "label": "Cardiovascular Points (0-4)",
                    "label_ru": "Баллы за ССС (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "cns_points",
                    "label": "CNS Points (0-4)",
                    "label_ru": "Баллы за ЦНС (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "renal_points",
                    "label": "Renal Points (0-4)",
                    "label_ru": "Баллы за почки (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 6",
                    "interpretation": "Low mortality risk (<10%)",
                    "interpretation_ru": "Низкий риск смертности (<10%)"
                },
                {
                    "condition": ">= 6 and < 10",
                    "interpretation": "Moderate mortality risk (15-20%)",
                    "interpretation_ru": "Умеренный риск смертности (15-20%)"
                },
                {
                    "condition": ">= 10 and < 15",
                    "interpretation": "High mortality risk (40-50%)",
                    "interpretation_ru": "Высокий риск смертности (40-50%)"
                },
                {
                    "condition": ">= 15",
                    "interpretation": "Very high mortality risk (>80%)",
                    "interpretation_ru": "Очень высокий риск смертности (>80%)"
                }
            ]
        },
        {
            "name": "Ventilator Settings",
            "name_ru": "Настройки вентилятора",
            "description": "Calculate initial tidal volume for ventilation",
            "description_ru": "Расчет начального дыхательного объема для ИВЛ",
            "category": "ICU",
            "category_ru": "Реанимация",
            "formula": "{ideal_body_weight} * 6",
            "input_fields": [
                {
                    "name": "ideal_body_weight",
                    "label": "Ideal Body Weight (kg)",
                    "label_ru": "Идеальная масса тела (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 30,
                    "max_value": 120
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Tidal volume in mL (lung-protective strategy: 6 mL/kg IBW)",
                    "interpretation_ru": "Дыхательный объем в мл (легочно-протективная стратегия: 6 мл/кг ИМТ)"
                }
            ]
        },
        # Pulmonology
        {
            "name": "Alveolar-arterial Gradient",
            "name_ru": "Альвеолярно-артериальный градиент",
            "description": "Calculate A-a gradient for hypoxemia",
            "description_ru": "Расчет А-а градиента при гипоксемии",
            "category": "Pulmonology",
            "category_ru": "Пульмонология",
            "formula": "(({fio2} * (760 - 47)) - ({paco2} / 0.8)) - {pao2}",
            "input_fields": [
                {
                    "name": "fio2",
                    "label": "FiO2 (fraction, e.g., 0.21 for room air)",
                    "label_ru": "FiO2 (доля, например 0.21 для воздуха)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.21,
                    "max_value": 1.0
                },
                {
                    "name": "paco2",
                    "label": "PaCO2 (mmHg)",
                    "label_ru": "PaCO2 (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 100
                },
                {
                    "name": "pao2",
                    "label": "PaO2 (mmHg)",
                    "label_ru": "PaO2 (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 40,
                    "max_value": 600
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 15",
                    "interpretation": "Normal A-a gradient",
                    "interpretation_ru": "Нормальный А-а градиент"
                },
                {
                    "condition": ">= 15 and < 30",
                    "interpretation": "Mildly elevated - V/Q mismatch possible",
                    "interpretation_ru": "Слегка повышен - возможно V/Q несоответствие"
                },
                {
                    "condition": ">= 30",
                    "interpretation": "Significantly elevated - shunt or severe V/Q mismatch",
                    "interpretation_ru": "Значительно повышен - шунт или тяжелое V/Q несоответствие"
                }
            ]
        },
        {
            "name": "CURB-65 Score",
            "name_ru": "Шкала CURB-65",
            "description": "Pneumonia severity assessment",
            "description_ru": "Оценка тяжести пневмонии",
            "category": "Pulmonology",
            "category_ru": "Пульмонология",
            "formula": "{confusion} + {urea} + {resp_rate} + {bp} + {age}",
            "input_fields": [
                {
                    "name": "confusion",
                    "label": "Confusion present",
                    "label_ru": "Нарушение сознания",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "urea",
                    "label": "Urea >7 mmol/L",
                    "label_ru": "Мочевина >7 ммоль/л",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "resp_rate",
                    "label": "Respiratory rate ≥30/min",
                    "label_ru": "ЧД ≥30/мин",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "bp",
                    "label": "BP <90/60 mmHg",
                    "label_ru": "АД <90/60 мм рт.ст.",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "age",
                    "label": "Age ≥65 years",
                    "label_ru": "Возраст ≥65 лет",
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
                    "condition": "<= 1",
                    "interpretation": "Low risk - outpatient treatment",
                    "interpretation_ru": "Низкий риск - амбулаторное лечение"
                },
                {
                    "condition": "== 2",
                    "interpretation": "Moderate risk - consider hospitalization",
                    "interpretation_ru": "Умеренный риск - рассмотреть госпитализацию"
                },
                {
                    "condition": ">= 3",
                    "interpretation": "High risk - hospitalization recommended",
                    "interpretation_ru": "Высокий риск - госпитализация рекомендована"
                }
            ]
        },
        # Hematology
        {
            "name": "Corrected Reticulocyte Count",
            "name_ru": "Корригированный счет ретикулоцитов",
            "description": "Correct reticulocyte count for anemia",
            "description_ru": "Корригировать ретикулоциты при анемии",
            "category": "Hematology",
            "category_ru": "Гематология",
            "formula": "{reticulocyte_pct} * ({hematocrit} / 45)",
            "input_fields": [
                {
                    "name": "reticulocyte_pct",
                    "label": "Reticulocyte % ",
                    "label_ru": "Ретикулоциты %",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 20
                },
                {
                    "name": "hematocrit",
                    "label": "Hematocrit (%)",
                    "label_ru": "Гематокрит (%)",
                    "type": "number",
                    "required": True,
                    "min_value": 10,
                    "max_value": 60
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 2",
                    "interpretation": "Inadequate bone marrow response",
                    "interpretation_ru": "Неадекватный ответ костного мозга"
                },
                {
                    "condition": ">= 2",
                    "interpretation": "Appropriate bone marrow response",
                    "interpretation_ru": "Адекватный ответ костного мозга"
                }
            ]
        },
        {
            "name": "Wells Score DVT",
            "name_ru": "Шкала Уэллса для ТГВ",
            "description": "Deep Vein Thrombosis probability",
            "description_ru": "Вероятность тромбоза глубоких вен",
            "category": "Hematology",
            "category_ru": "Гематология",
            "formula": "{active_cancer} + {paralysis} + {bedridden} + {leg_tenderness} + {leg_swelling} + {calf_swelling} + {pitting_edema} + {collateral_veins} + {alternative_dx}",
            "input_fields": [
                {
                    "name": "active_cancer",
                    "label": "Active cancer (1 point)",
                    "label_ru": "Активный рак (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "paralysis",
                    "label": "Paralysis or recent immobilization (1 point)",
                    "label_ru": "Паралич или иммобилизация (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "bedridden",
                    "label": "Bedridden >3 days or surgery (1 point)",
                    "label_ru": "Постельный режим >3 дней или операция (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "leg_tenderness",
                    "label": "Tenderness along deep veins (1 point)",
                    "label_ru": "Болезненность по ходу вен (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "leg_swelling",
                    "label": "Entire leg swelling (1 point)",
                    "label_ru": "Отек всей ноги (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "calf_swelling",
                    "label": "Calf swelling >3cm vs other leg (1 point)",
                    "label_ru": "Отек икры >3см в сравнении (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "pitting_edema",
                    "label": "Pitting edema (1 point)",
                    "label_ru": "Ямочный отек (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "collateral_veins",
                    "label": "Collateral superficial veins (1 point)",
                    "label_ru": "Коллатеральные поверхностные вены (1 балл)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": 1, "label": "Yes", "label_ru": "Да"}
                    ]
                },
                {
                    "name": "alternative_dx",
                    "label": "Alternative diagnosis likely (-2 points)",
                    "label_ru": "Альтернативный диагноз вероятен (-2 балла)",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": 0, "label": "No", "label_ru": "Нет"},
                        {"value": -2, "label": "Yes", "label_ru": "Да"}
                    ]
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 0",
                    "interpretation": "Low probability (3% risk)",
                    "interpretation_ru": "Низкая вероятность (3% риск)"
                },
                {
                    "condition": ">= 1 and <= 2",
                    "interpretation": "Moderate probability (17% risk)",
                    "interpretation_ru": "Умеренная вероятность (17% риск)"
                },
                {
                    "condition": ">= 3",
                    "interpretation": "High probability (75% risk)",
                    "interpretation_ru": "Высокая вероятность (75% риск)"
                }
            ]
        },
        # Emergency Medicine
        {
            "name": "Anion Gap",
            "name_ru": "Анионная разница",
            "description": "Calculate anion gap for metabolic acidosis",
            "description_ru": "Расчет анионной разницы при метаболическом ацидозе",
            "category": "Emergency Medicine",
            "category_ru": "Неотложная медицина",
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
                    "min_value": 5,
                    "max_value": 40
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 12",
                    "interpretation": "Normal anion gap",
                    "interpretation_ru": "Нормальная анионная разница"
                },
                {
                    "condition": ">= 12 and < 20",
                    "interpretation": "Elevated anion gap - investigate cause",
                    "interpretation_ru": "Повышенная анионная разница - выяснить причину"
                },
                {
                    "condition": ">= 20",
                    "interpretation": "High anion gap metabolic acidosis",
                    "interpretation_ru": "Метаболический ацидоз с высокой анионной разницей"
                }
            ]
        },
        {
            "name": "Parkland Formula",
            "name_ru": "Формула Паркленда",
            "description": "Fluid resuscitation for burn patients",
            "description_ru": "Инфузионная терапия при ожогах",
            "category": "Emergency Medicine",
            "category_ru": "Неотложная медицина",
            "formula": "4 * {weight} * {burn_percent}",
            "input_fields": [
                {
                    "name": "weight",
                    "label": "Weight (kg)",
                    "label_ru": "Вес (кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 20,
                    "max_value": 200
                },
                {
                    "name": "burn_percent",
                    "label": "Total Body Surface Area Burned (%)",
                    "label_ru": "Площадь ожога тела (%)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 100
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Total mL of Ringer's Lactate in first 24h (give 50% in first 8h)",
                    "interpretation_ru": "Всего мл раствора Рингера за 24ч (50% за первые 8ч)"
                }
            ]
        },
        {
            "name": "Shock Index",
            "name_ru": "Индекс шока",
            "description": "Assess hemodynamic instability",
            "description_ru": "Оценка гемодинамической нестабильности",
            "category": "Emergency Medicine",
            "category_ru": "Неотложная медицина",
            "formula": "{heart_rate} / {systolic_bp}",
            "input_fields": [
                {
                    "name": "heart_rate",
                    "label": "Heart Rate (bpm)",
                    "label_ru": "ЧСС (уд/мин)",
                    "type": "number",
                    "required": True,
                    "min_value": 40,
                    "max_value": 200
                },
                {
                    "name": "systolic_bp",
                    "label": "Systolic BP (mmHg)",
                    "label_ru": "Систолическое АД (мм рт.ст.)",
                    "type": "number",
                    "required": True,
                    "min_value": 60,
                    "max_value": 250
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 0.6",
                    "interpretation": "Normal hemodynamics",
                    "interpretation_ru": "Нормальная гемодинамика"
                },
                {
                    "condition": ">= 0.6 and < 1.0",
                    "interpretation": "Possible early shock - monitor closely",
                    "interpretation_ru": "Возможный ранний шок - тщательный мониторинг"
                },
                {
                    "condition": ">= 1.0",
                    "interpretation": "Shock likely - immediate intervention",
                    "interpretation_ru": "Вероятен шок - немедленное вмешательство"
                }
            ]
        },
        # Neurology
        {
            "name": "NIHSS Score (Simplified)",
            "name_ru": "Шкала инсульта NIH (упрощенная)",
            "description": "Stroke severity assessment",
            "description_ru": "Оценка тяжести инсульта",
            "category": "Neurology",
            "category_ru": "Неврология",
            "formula": "{consciousness} + {gaze} + {visual} + {facial} + {motor_arm} + {motor_leg} + {limb_ataxia} + {sensory} + {language} + {dysarthria} + {extinction}",
            "input_fields": [
                {
                    "name": "consciousness",
                    "label": "Level of Consciousness (0-3)",
                    "label_ru": "Уровень сознания (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "gaze",
                    "label": "Best Gaze (0-2)",
                    "label_ru": "Взор (0-2)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                },
                {
                    "name": "visual",
                    "label": "Visual Fields (0-3)",
                    "label_ru": "Поля зрения (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "facial",
                    "label": "Facial Palsy (0-3)",
                    "label_ru": "Парез лица (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "motor_arm",
                    "label": "Motor Arm (0-4)",
                    "label_ru": "Двигательная рука (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "motor_leg",
                    "label": "Motor Leg (0-4)",
                    "label_ru": "Двигательная нога (0-4)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 4
                },
                {
                    "name": "limb_ataxia",
                    "label": "Limb Ataxia (0-2)",
                    "label_ru": "Атаксия конечностей (0-2)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                },
                {
                    "name": "sensory",
                    "label": "Sensory (0-2)",
                    "label_ru": "Чувствительность (0-2)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                },
                {
                    "name": "language",
                    "label": "Language/Aphasia (0-3)",
                    "label_ru": "Речь/Афазия (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "dysarthria",
                    "label": "Dysarthria (0-2)",
                    "label_ru": "Дизартрия (0-2)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                },
                {
                    "name": "extinction",
                    "label": "Extinction/Inattention (0-2)",
                    "label_ru": "Игнорирование/Невнимание (0-2)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "== 0",
                    "interpretation": "No stroke symptoms",
                    "interpretation_ru": "Нет симптомов инсульта"
                },
                {
                    "condition": ">= 1 and <= 4",
                    "interpretation": "Minor stroke",
                    "interpretation_ru": "Малый инсульт"
                },
                {
                    "condition": ">= 5 and <= 15",
                    "interpretation": "Moderate stroke",
                    "interpretation_ru": "Умеренный инсульт"
                },
                {
                    "condition": ">= 16 and <= 20",
                    "interpretation": "Moderate to severe stroke",
                    "interpretation_ru": "Умеренно-тяжелый инсульт"
                },
                {
                    "condition": "> 20",
                    "interpretation": "Severe stroke",
                    "interpretation_ru": "Тяжелый инсульт"
                }
            ]
        },
        # Gastroenterology
        {
            "name": "Child-Pugh Score",
            "name_ru": "Шкала Чайлд-Пью",
            "description": "Liver cirrhosis severity",
            "description_ru": "Тяжесть цирроза печени",
            "category": "Gastroenterology",
            "category_ru": "Гастроэнтерология",
            "formula": "{bilirubin_points} + {albumin_points} + {inr_points} + {ascites_points} + {encephalopathy_points}",
            "input_fields": [
                {
                    "name": "bilirubin_points",
                    "label": "Bilirubin Points (1-3)",
                    "label_ru": "Баллы за билирубин (1-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 3
                },
                {
                    "name": "albumin_points",
                    "label": "Albumin Points (1-3)",
                    "label_ru": "Баллы за альбумин (1-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 3
                },
                {
                    "name": "inr_points",
                    "label": "INR Points (1-3)",
                    "label_ru": "Баллы за МНО (1-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 3
                },
                {
                    "name": "ascites_points",
                    "label": "Ascites Points (1-3)",
                    "label_ru": "Баллы за асцит (1-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 3
                },
                {
                    "name": "encephalopathy_points",
                    "label": "Encephalopathy Points (1-3)",
                    "label_ru": "Баллы за энцефалопатию (1-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 1,
                    "max_value": 3
                }
            ],
            "interpretation_rules": [
                {
                    "condition": ">= 5 and <= 6",
                    "interpretation": "Class A (well-compensated, 1-year survival 100%)",
                    "interpretation_ru": "Класс A (хорошо компенсирован, годовая выживаемость 100%)"
                },
                {
                    "condition": ">= 7 and <= 9",
                    "interpretation": "Class B (significant functional compromise, 1-year survival 80%)",
                    "interpretation_ru": "Класс B (значительные нарушения функции, годовая выживаемость 80%)"
                },
                {
                    "condition": ">= 10",
                    "interpretation": "Class C (decompensated, 1-year survival 45%)",
                    "interpretation_ru": "Класс C (декомпенсирован, годовая выживаемость 45%)"
                }
            ]
        },
        {
            "name": "MELD Score",
            "name_ru": "Шкала MELD",
            "description": "Model for End-Stage Liver Disease",
            "description_ru": "Модель терминальной болезни печени",
            "category": "Gastroenterology",
            "category_ru": "Гастроэнтерология",
            "formula": "10 * ((0.957 * ({creatinine} ** 0.3010)) + (0.378 * ({bilirubin} ** 0.3010)) + (1.12 * ({inr} ** 0.3010)) + 0.643)",
            "input_fields": [
                {
                    "name": "creatinine",
                    "label": "Serum Creatinine (mg/dL)",
                    "label_ru": "Креатинин сыворотки (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.5,
                    "max_value": 10
                },
                {
                    "name": "bilirubin",
                    "label": "Total Bilirubin (mg/dL)",
                    "label_ru": "Общий билирубин (мг/дл)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.5,
                    "max_value": 40
                },
                {
                    "name": "inr",
                    "label": "INR",
                    "label_ru": "МНО",
                    "type": "number",
                    "required": True,
                    "min_value": 0.8,
                    "max_value": 5.0
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "< 10",
                    "interpretation": "Low risk (3-month mortality <2%)",
                    "interpretation_ru": "Низкий риск (3-месячная смертность <2%)"
                },
                {
                    "condition": ">= 10 and < 20",
                    "interpretation": "Moderate risk (3-month mortality 6%)",
                    "interpretation_ru": "Умеренный риск (3-месячная смертность 6%)"
                },
                {
                    "condition": ">= 20 and < 30",
                    "interpretation": "High risk (3-month mortality 20%)",
                    "interpretation_ru": "Высокий риск (3-месячная смертность 20%)"
                },
                {
                    "condition": ">= 30",
                    "interpretation": "Very high risk (3-month mortality >50%)",
                    "interpretation_ru": "Очень высокий риск (3-месячная смертность >50%)"
                }
            ]
        },
        # Obstetrics
        {
            "name": "Bishop Score",
            "name_ru": "Шкала Бишопа",
            "description": "Cervical readiness for labor induction",
            "description_ru": "Готовность шейки матки к родам",
            "category": "Obstetrics",
            "category_ru": "Акушерство",
            "formula": "{dilation} + {effacement} + {station} + {consistency} + {position}",
            "input_fields": [
                {
                    "name": "dilation",
                    "label": "Cervical Dilation (0-3 points)",
                    "label_ru": "Раскрытие шейки (0-3 балла)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "effacement",
                    "label": "Cervical Effacement (0-3 points)",
                    "label_ru": "Сглаживание шейки (0-3 балла)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "station",
                    "label": "Fetal Station (0-3 points)",
                    "label_ru": "Расположение плода (0-3 балла)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "consistency",
                    "label": "Cervical Consistency (0-2 points)",
                    "label_ru": "Консистенция шейки (0-2 балла)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                },
                {
                    "name": "position",
                    "label": "Cervical Position (0-2 points)",
                    "label_ru": "Положение шейки (0-2 балла)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 2
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 5",
                    "interpretation": "Unfavorable cervix - induction likely to fail",
                    "interpretation_ru": "Неблагоприятная шейка - индукция вероятно неуспешна"
                },
                {
                    "condition": ">= 6 and <= 8",
                    "interpretation": "Intermediate - induction may succeed",
                    "interpretation_ru": "Промежуточное состояние - индукция может быть успешной"
                },
                {
                    "condition": ">= 9",
                    "interpretation": "Favorable cervix - high success rate",
                    "interpretation_ru": "Благоприятная шейка - высокая вероятность успеха"
                }
            ]
        },
        # Pediatrics
        {
            "name": "Pediatric Early Warning Score",
            "name_ru": "Педиатрическая шкала раннего предупреждения",
            "description": "Identify children at risk of deterioration",
            "description_ru": "Выявление детей с риском ухудшения",
            "category": "Pediatrics",
            "category_ru": "Педиатрия",
            "formula": "{behavior} + {cardiovascular} + {respiratory}",
            "input_fields": [
                {
                    "name": "behavior",
                    "label": "Behavior Points (0-3)",
                    "label_ru": "Баллы за поведение (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "cardiovascular",
                    "label": "Cardiovascular Points (0-3)",
                    "label_ru": "Баллы за ССС (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                },
                {
                    "name": "respiratory",
                    "label": "Respiratory Points (0-3)",
                    "label_ru": "Баллы за дыхание (0-3)",
                    "type": "number",
                    "required": True,
                    "min_value": 0,
                    "max_value": 3
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "<= 2",
                    "interpretation": "Low risk - routine monitoring",
                    "interpretation_ru": "Низкий риск - обычный мониторинг"
                },
                {
                    "condition": ">= 3 and <= 4",
                    "interpretation": "Moderate risk - increased monitoring",
                    "interpretation_ru": "Умеренный риск - усиленный мониторинг"
                },
                {
                    "condition": ">= 5",
                    "interpretation": "High risk - urgent medical review",
                    "interpretation_ru": "Высокий риск - срочный медицинский осмотр"
                }
            ]
        },
        # Nutrition
        {
            "name": "Basal Metabolic Rate (Harris-Benedict)",
            "name_ru": "Базальный метаболизм (Харрис-Бенедикт)",
            "description": "Calculate BMR for males",
            "description_ru": "Расчет БМ для мужчин",
            "category": "Nutrition",
            "category_ru": "Нутрициология",
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
                    "min_value": 15,
                    "max_value": 100
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Basal Metabolic Rate in kcal/day",
                    "interpretation_ru": "Базальный метаболизм в ккал/сут"
                }
            ]
        },
        {
            "name": "Protein Requirement",
            "name_ru": "Потребность в белке",
            "description": "Daily protein needs",
            "description_ru": "Суточная потребность в белке",
            "category": "Nutrition",
            "category_ru": "Нутрициология",
            "formula": "{weight} * {protein_factor}",
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
                    "name": "protein_factor",
                    "label": "Protein Factor (0.8-2.0 g/kg)",
                    "label_ru": "Фактор белка (0.8-2.0 г/кг)",
                    "type": "number",
                    "required": True,
                    "min_value": 0.8,
                    "max_value": 2.5
                }
            ],
            "interpretation_rules": [
                {
                    "condition": "",
                    "interpretation": "Daily protein requirement in grams",
                    "interpretation_ru": "Суточная потребность в белке в граммах"
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
        # Include all fields including Russian translations
        valid_fields = {'name', 'name_ru', 'description', 'description_ru', 'category', 'category_ru', 'formula', 'input_fields', 'interpretation_rules'}
        
        for calc_data in calculators_data:
            # Filter to include only valid Calculator model fields
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
