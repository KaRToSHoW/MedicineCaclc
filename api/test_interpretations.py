"""
Test interpretation system directly
"""
import asyncio
import sys
sys.path.insert(0, '/home/runner/app/api')

from app.api.v1.calculation_results import interpret_result


def test_bmi_interpretation():
    """Test BMI interpretation rules"""
    print("=" * 60)
    print("Testing BMI Calculator Interpretations")
    print("=" * 60)
    
    interpretation_rules = [
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
    
    # Test cases: weight=70kg, height=175cm -> BMI = 70 / (1.75^2) = 22.86
    test_cases = [
        (17.0, "Underweight", "Недостаточный вес"),
        (22.86, "Normal weight", "Нормальный вес"),
        (27.5, "Overweight", "Избыточный вес"),
        (32.0, "Obese", "Ожирение"),
    ]
    
    for bmi, expected_en, expected_ru in test_cases:
        result_en = interpret_result(bmi, interpretation_rules, language="en")
        result_ru = interpret_result(bmi, interpretation_rules, language="ru")
        
        print(f"\nBMI: {bmi}")
        print(f"  English: {result_en} {'✅' if result_en == expected_en else '❌ Expected: ' + expected_en}")
        print(f"  Russian: {result_ru} {'✅' if result_ru == expected_ru else '❌ Expected: ' + expected_ru}")


def test_heart_score_interpretation():
    """Test HEART Score interpretation rules"""
    print("\n" + "=" * 60)
    print("Testing HEART Score Interpretations")
    print("=" * 60)
    
    interpretation_rules = [
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
    
    test_cases = [
        (2, "Low risk", "Низкий риск"),
        (5, "Moderate risk", "Умеренный риск"),
        (8, "High risk", "Высокий риск"),
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        
        print(f"\nScore: {score}")
        print(f"  English: {result_en} {'✅' if result_en == expected_en else '❌ Expected: ' + expected_en}")
        print(f"  Russian: {result_ru} {'✅' if result_ru == expected_ru else '❌ Expected: ' + expected_ru}")


def test_apgar_interpretation():
    """Test APGAR Score interpretation rules"""
    print("\n" + "=" * 60)
    print("Testing APGAR Score Interpretations")
    print("=" * 60)
    
    interpretation_rules = [
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
    
    test_cases = [
        (2, "Critically low - immediate resuscitation needed", "Критически низкий - требуется немедленная реанимация"),
        (5, "Moderately abnormal - needs assistance", "Умеренно патологический - нужна помощь"),
        (9, "Normal condition", "Нормальное состояние"),
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        
        print(f"\nScore: {score}")
        print(f"  English: {result_en} {'✅' if result_en == expected_en else '❌ Expected: ' + expected_en}")
        print(f"  Russian: {result_ru} {'✅' if result_ru == expected_ru else '❌ Expected: ' + expected_ru}")


if __name__ == "__main__":
    test_bmi_interpretation()
    test_heart_score_interpretation()
    test_apgar_interpretation()
    print("\n" + "=" * 60)
    print("✅ All interpretation tests completed!")
    print("=" * 60)
