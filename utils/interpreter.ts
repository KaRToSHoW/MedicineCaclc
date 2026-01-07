import { Calculator } from '@/types/calculators';

export function getInterpretation(calc: Calculator, value: number | null, inputs: Record<string, any>): string {
  if (value === null) return '';
  const name = (calc.name || '').toLowerCase();

  // BMI
  if (name.includes('bmi')) {
    if (value < 18.5) return 'Недостаточная масса тела (дефицит)';
    if (value < 25) return 'Норма';
    if (value < 30) return 'Избыточная масса тела (избыточная масса)';
    return 'Ожирение';
  }

  // BSA — no standard clinical interpretation
  if (name.includes('bsa')) return '';

  // Cockcroft-Gault / eGFR-like interpretation
  if (name.includes('cockcroft') || name.includes('egfr') || name.includes('creatinine')) {
    if (value >= 90) return 'Норма (CKD G1)';
    if (value >= 60) return 'Лёгкое снижение функции (CKD G2)';
    if (value >= 30) return 'Умеренное снижение (CKD G3)';
    if (value >= 15) return 'Тяжёлая недостаточность (CKD G4)';
    return 'Почечная недостаточность (CKD G5)';
  }

  // PaO2/FiO2
  if (name.includes('pao2') || name.includes('pa02') || name.includes('pa o2') || name.includes('pao2/')) {
    if (value > 300) return 'Нормальная оксигенация';
    if (value > 200) return 'Легкая дыхательная недостаточность';
    if (value > 100) return 'Тяжелая дыхательная недостаточность (ARDS)';
    return 'Критическая гипоксемия';
  }

  // HOMA-IR
  if (name.includes('homa')) {
    if (value < 1) return 'Норма инсулиночувствительности';
    if (value < 2.5) return 'Промежуточная инсулинорезистентность';
    return 'Инсулинорезистентность';
  }

  // GCS
  if (name.includes('glasgow') || name.includes('gcs')) {
    if (value >= 13) return 'Лёгкое нарушение сознания';
    if (value >= 9) return 'Умеренное нарушение сознания';
    return 'Тяжёлое нарушение сознания';
  }

  // BAI
  if (name.includes('bai')) {
    // No widely used categorical interpretation; return empty
    return '';
  }

  // CHA2DS2-VASc
  if (name.includes('cha2ds2') || name.includes('cha2ds2-vasc')) {
    const score = Number(value);
    if (score === 0) return 'Низкий риск инсульта — антитромботическая терапия может не требоваться (мужчины)';
    if (score === 1) return 'Низкий-поcредственный риск — обсудите антикоагуляцию с врачом';
    return 'Высокий риск инсульта — рекомендована антикоагуляция';
  }

  // HAS-BLED
  if (name.includes('has-bled') || name.includes('hasbled')) {
    const s = Number(value);
    if (s <= 2) return 'Риск кровотечения низкий-приемлемый';
    return 'Повышенный риск кровотечения — оцените факторы и контроль';
  }

  // CURB-65
  if (name.includes('curb')) {
    const s = Number(value);
    if (s === 0) return 'Низкий риск — амбулаторное лечение можно рассмотреть';
    if (s <= 2) return 'Средний риск — обычно госпитализация';
    return 'Высокий риск — срочная госпитализация/интубация возможна';
  }

  // qSOFA
  if (name.includes('qsofa')) {
    const s = Number(value);
    if (s >= 2) return 'Высокая вероятность неблагоприятного исхода — срочно оцените на наличие сепсиса';
    return 'Низкий риск по qSOFA';
  }

  // SIRS
  if (name.includes('sirs')) {
    const s = Number(value);
    if (s >= 2) return 'Позитивные критерии SIRS — оценивайте на наличие инфекции/системного воспаления';
    return 'Мало признаков системного воспаления';
  }

  // eGFR MDRD
  if (name.includes('egfr mdrd') || name.includes('egfr mdrd') || name.includes('egfr')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v >= 90) return 'Норма (CKD G1)';
    if (v >= 60) return 'Лёгкое снижение функции (CKD G2)';
    if (v >= 30) return 'Умеренное снижение (CKD G3)';
    if (v >= 15) return 'Тяжёлая недостаточность (CKD G4)';
    return 'Почечная недостаточность (CKD G5)';
  }

  // 24h Creatinine Clearance
  if (name.includes('24h creatinine') || name.includes('24h creatinine clearance')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v >= 90) return 'Нормальный клиренс';
    if (v >= 60) return 'Лёгкое снижение';
    if (v >= 30) return 'Умеренное снижение';
    return 'Выраженное снижение функции почек';
  }

  // FENa
  if (name.includes('fena')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v < 1) return 'Симптомы указывают на преренальную причину';
    if (v < 2) return 'Пограничное значение';
    return 'Вероятна внутрипочечная причина (ATN)';
  }

  // A-a gradient
  if (name.includes('a-a gradient') || name.includes('a-a')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v < 10) return 'Нормальный A–a градиент';
    if (v <= 20) return 'Лёгкое увеличение';
    return 'Значительно повышенный A–a градиент — вентиляционно-перфузионный дефект или шунт';
  }

  // FEV1/FVC
  if (name.includes('fev1/fvc') || name.includes('fev1')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v >= 0.7) return 'Обычно в пределах нормы';
    return 'Обструкция дыхательных путей (вероятно)';
  }

  // ESR expected
  if (name.includes('esr expected') || name.includes('esr')) {
    return `Ожидаемая СОЭ ≈ ${value}`;
  }

  // MCV / MCHC
  if (name.includes('mcv') || name.includes('mchc')) {
    const mcv = Number(inputs.mcv || inputs.hct && inputs.rbc ? (inputs.hct * 10 / inputs.rbc) : NaN);
    if (!isNaN(mcv)) {
      if (mcv < 80) return 'Микроцитарная анемия';
      if (mcv <= 100) return 'Нормоцитарная';
      return 'Макроцитарная анемия';
    }
  }

  // APGAR
  if (name.includes('apgar')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v >= 7) return 'Нормальный статус новорождённого';
    if (v >= 4) return 'Умеренное состояние — требует наблюдения';
    return 'Тяжёлое состояние — требуется реанимация/специализированный уход';
  }

  // MEWS
  if (name.includes('mews')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v >= 5) return 'Высокий риск клинического ухудшения — срочно оцените';
    if (v >= 3) return 'Средний риск — наблюдение/расширенная оценка';
    return 'Низкий риск';
  }

  // MELD
  if (name.includes('meld')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v < 10) return 'Низкий прогнозный риск';
    if (v < 20) return 'Умеренный риск';
    return 'Высокий риск смертности — рассматривайте лист ожидания ТПХ/трансплантацию';
  }

  // QTc
  if (name.includes('qtc')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v > 500) return 'Выраженная пролонгация QT — высокий риск torsades de pointes';
    if (v > 450) return 'Удлинённый QT — требуется оценка лекарств и электролитов';
    return 'QTc в пределах нормы';
  }

  // Sokolow-Lyon
  if (name.includes('sokolow') || name.includes('lvh')) {
    const v = Number(value);
    if (isNaN(v)) return '';
    if (v > 35) return 'Соответствует критериям LVH по Sokolow-Lyon';
    return 'Не соответствует критериям LVH';
  }

  // Default: no interpretation
  return '';
}

export default getInterpretation;
