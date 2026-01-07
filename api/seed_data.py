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
            print(f"Calculators already exist ({len(existing_calculators)} found). Skipping seed.")
            return
        
        # Add calculators
        for calc_data in calculators_data:
            calculator = Calculator(**calc_data)
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
