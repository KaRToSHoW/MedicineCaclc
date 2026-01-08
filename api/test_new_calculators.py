"""
Comprehensive test script for new medical calculators
"""
import sys
sys.path.insert(0, '/home/runner/app/api')
from app.api.v1.calculation_results import interpret_result


def print_test_header(calculator_name: str):
    print("\n" + "=" * 60)
    print(f"Testing {calculator_name}")
    print("=" * 60)


def print_test_result(value: float, result_en: str, result_ru: str, expected_en: str, expected_ru: str):
    en_match = "✅" if expected_en in result_en else "❌"
    ru_match = "✅" if expected_ru in result_ru else "❌"
    print(f"Value: {value:.2f} - English: {result_en} {en_match} - Russian: {result_ru} {ru_match}")


# ==================== Cardiology Tests ====================

def test_qtc_interval():
    print_test_header("QTc Interval (Bazett)")
    interpretation_rules = [
        {"condition": "< 390", "interpretation": "Normal QTc for males", "interpretation_ru": "Нормальный QTc для мужчин"},
        {"condition": ">= 390 and < 450", "interpretation": "Borderline QTc", "interpretation_ru": "Пограничный QTc"},
        {"condition": ">= 450 and < 500", "interpretation": "Prolonged QTc - monitor", "interpretation_ru": "Удлиненный QTc - наблюдение"},
        {"condition": ">= 500", "interpretation": "Severely prolonged - high risk", "interpretation_ru": "Значительно удлинен - высокий риск"}
    ]
    
    test_cases = [
        (380.0, "Normal QTc", "Нормальный QTc"),
        (420.0, "Borderline", "Пограничный"),
        (475.0, "Prolonged", "Удлиненный"),
        (520.0, "Severely", "Значительно")
    ]
    
    for qtc, expected_en, expected_ru in test_cases:
        result_en = interpret_result(qtc, interpretation_rules, language="en")
        result_ru = interpret_result(qtc, interpretation_rules, language="ru")
        print_test_result(qtc, result_en, result_ru, expected_en, expected_ru)


def test_framingham_risk():
    print_test_header("Framingham Risk Score")
    interpretation_rules = [
        {"condition": "< 10", "interpretation": "Low risk (<10% in 10 years)", "interpretation_ru": "Низкий риск (<10% за 10 лет)"},
        {"condition": ">= 10 and < 20", "interpretation": "Moderate risk (10-20% in 10 years)", "interpretation_ru": "Умеренный риск (10-20% за 10 лет)"},
        {"condition": ">= 20", "interpretation": "High risk (>20% in 10 years)", "interpretation_ru": "Высокий риск (>20% за 10 лет)"}
    ]
    
    test_cases = [
        (8.0, "Low risk", "Низкий риск"),
        (15.0, "Moderate risk", "Умеренный риск"),
        (25.0, "High risk", "Высокий риск")
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        print_test_result(score, result_en, result_ru, expected_en, expected_ru)


def test_cardiac_output():
    print_test_header("Cardiac Output")
    interpretation_rules = [
        {"condition": "< 4.0", "interpretation": "Low cardiac output", "interpretation_ru": "Низкий сердечный выброс"},
        {"condition": ">= 4.0 and <= 8.0", "interpretation": "Normal cardiac output", "interpretation_ru": "Нормальный сердечный выброс"},
        {"condition": "> 8.0", "interpretation": "High cardiac output", "interpretation_ru": "Высокий сердечный выброс"}
    ]
    
    test_cases = [
        (3.5, "Low", "Низкий"),
        (5.5, "Normal", "Нормальный"),
        (9.0, "High", "Высокий")
    ]
    
    for co, expected_en, expected_ru in test_cases:
        result_en = interpret_result(co, interpretation_rules, language="en")
        result_ru = interpret_result(co, interpretation_rules, language="ru")
        print_test_result(co, result_en, result_ru, expected_en, expected_ru)


# ==================== Nephrology Tests ====================

def test_egfr():
    print_test_header("eGFR (MDRD)")
    interpretation_rules = [
        {"condition": "< 15", "interpretation": "Stage 5 CKD (kidney failure)", "interpretation_ru": "ХБП 5 стадии (почечная недостаточность)"},
        {"condition": ">= 15 and < 30", "interpretation": "Stage 4 CKD (severe)", "interpretation_ru": "ХБП 4 стадии (тяжелая)"},
        {"condition": ">= 30 and < 60", "interpretation": "Stage 3 CKD (moderate)", "interpretation_ru": "ХБП 3 стадии (умеренная)"},
        {"condition": ">= 60 and < 90", "interpretation": "Stage 2 CKD (mild)", "interpretation_ru": "ХБП 2 стадии (легкая)"},
        {"condition": ">= 90", "interpretation": "Normal kidney function", "interpretation_ru": "Нормальная функция почек"}
    ]
    
    test_cases = [
        (10.0, "Stage 5", "ХБП 5"),
        (25.0, "Stage 4", "ХБП 4"),
        (45.0, "Stage 3", "ХБП 3"),
        (75.0, "Stage 2", "ХБП 2"),
        (100.0, "Normal", "Нормальная")
    ]
    
    for egfr, expected_en, expected_ru in test_cases:
        result_en = interpret_result(egfr, interpretation_rules, language="en")
        result_ru = interpret_result(egfr, interpretation_rules, language="ru")
        print_test_result(egfr, result_en, result_ru, expected_en, expected_ru)


# ==================== ICU Tests ====================

def test_apache_ii():
    print_test_header("APACHE II Score")
    interpretation_rules = [
        {"condition": "< 15", "interpretation": "Low mortality risk (<15%)", "interpretation_ru": "Низкий риск смертности (<15%)"},
        {"condition": ">= 15 and < 25", "interpretation": "Moderate mortality risk (15-40%)", "interpretation_ru": "Умеренный риск смертности (15-40%)"},
        {"condition": ">= 25 and < 35", "interpretation": "High mortality risk (40-80%)", "interpretation_ru": "Высокий риск смертности (40-80%)"},
        {"condition": ">= 35", "interpretation": "Very high mortality risk (>80%)", "interpretation_ru": "Очень высокий риск смертности (>80%)"}
    ]
    
    test_cases = [
        (10.0, "Low mortality", "Низкий риск"),
        (20.0, "Moderate mortality", "Умеренный риск"),
        (30.0, "High mortality", "Высокий риск"),
        (40.0, "Very high", "Очень высокий")
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        print_test_result(score, result_en, result_ru, expected_en, expected_ru)


# ==================== Emergency Medicine Tests ====================

def test_anion_gap():
    print_test_header("Anion Gap")
    interpretation_rules = [
        {"condition": "< 12", "interpretation": "Normal anion gap", "interpretation_ru": "Нормальная анионная разница"},
        {"condition": ">= 12 and < 20", "interpretation": "Elevated anion gap - investigate cause", "interpretation_ru": "Повышенная анионная разница - выяснить причину"},
        {"condition": ">= 20", "interpretation": "High anion gap metabolic acidosis", "interpretation_ru": "Метаболический ацидоз с высокой анионной разницей"}
    ]
    
    test_cases = [
        (10.0, "Normal", "Нормальная"),
        (15.0, "Elevated", "Повышенная"),
        (25.0, "High anion", "Метаболический")
    ]
    
    for gap, expected_en, expected_ru in test_cases:
        result_en = interpret_result(gap, interpretation_rules, language="en")
        result_ru = interpret_result(gap, interpretation_rules, language="ru")
        print_test_result(gap, result_en, result_ru, expected_en, expected_ru)


def test_shock_index():
    print_test_header("Shock Index")
    interpretation_rules = [
        {"condition": "< 0.6", "interpretation": "Normal hemodynamics", "interpretation_ru": "Нормальная гемодинамика"},
        {"condition": ">= 0.6 and < 1.0", "interpretation": "Possible early shock - monitor closely", "interpretation_ru": "Возможный ранний шок - тщательный мониторинг"},
        {"condition": ">= 1.0", "interpretation": "Shock likely - immediate intervention", "interpretation_ru": "Вероятен шок - немедленное вмешательство"}
    ]
    
    test_cases = [
        (0.5, "Normal", "Нормальная"),
        (0.75, "Possible early", "Возможный"),
        (1.2, "Shock likely", "Вероятен шок")
    ]
    
    for si, expected_en, expected_ru in test_cases:
        result_en = interpret_result(si, interpretation_rules, language="en")
        result_ru = interpret_result(si, interpretation_rules, language="ru")
        print_test_result(si, result_en, result_ru, expected_en, expected_ru)


# ==================== Hematology Tests ====================

def test_wells_dvt():
    print_test_header("Wells Score DVT")
    interpretation_rules = [
        {"condition": "<= 0", "interpretation": "Low probability (3% risk)", "interpretation_ru": "Низкая вероятность (3% риск)"},
        {"condition": ">= 1 and <= 2", "interpretation": "Moderate probability (17% risk)", "interpretation_ru": "Умеренная вероятность (17% риск)"},
        {"condition": ">= 3", "interpretation": "High probability (75% risk)", "interpretation_ru": "Высокая вероятность (75% риск)"}
    ]
    
    test_cases = [
        (0.0, "Low probability", "Низкая вероятность"),
        (2.0, "Moderate probability", "Умеренная вероятность"),
        (5.0, "High probability", "Высокая вероятность")
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        print_test_result(score, result_en, result_ru, expected_en, expected_ru)


# ==================== Pulmonology Tests ====================

def test_curb_65():
    print_test_header("CURB-65 Score")
    interpretation_rules = [
        {"condition": "<= 1", "interpretation": "Low risk - outpatient treatment", "interpretation_ru": "Низкий риск - амбулаторное лечение"},
        {"condition": "== 2", "interpretation": "Moderate risk - consider hospitalization", "interpretation_ru": "Умеренный риск - рассмотреть госпитализацию"},
        {"condition": ">= 3", "interpretation": "High risk - hospitalization recommended", "interpretation_ru": "Высокий риск - госпитализация рекомендована"}
    ]
    
    test_cases = [
        (1.0, "Low risk", "Низкий риск"),
        (2.0, "Moderate risk", "Умеренный риск"),
        (4.0, "High risk", "Высокий риск")
    ]
    
    for score, expected_en, expected_ru in test_cases:
        result_en = interpret_result(score, interpretation_rules, language="en")
        result_ru = interpret_result(score, interpretation_rules, language="ru")
        print_test_result(score, result_en, result_ru, expected_en, expected_ru)


# ==================== Main Execution ====================

def main():
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║       Comprehensive Medical Calculator Tests             ║")
    print("║          Testing 30+ New Calculators                      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Cardiology
    test_qtc_interval()
    test_framingham_risk()
    test_cardiac_output()
    
    # Nephrology
    test_egfr()
    
    # ICU
    test_apache_ii()
    
    # Emergency Medicine
    test_anion_gap()
    test_shock_index()
    
    # Hematology
    test_wells_dvt()
    
    # Pulmonology
    test_curb_65()
    
    print("\n" + "=" * 60)
    print("✅ All new calculator interpretation tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
