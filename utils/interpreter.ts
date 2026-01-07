import { Calculator } from '@/types/calculators';

/**
 * Get clinical interpretation based on calculator's interpretation rules
 * Uses interpretation_ru from JSON rules for Russian localization
 */
export function getInterpretation(
  calc: Calculator,
  value: number | null,
  inputs: Record<string, any>
): string {
  // If no computed value, return empty
  if (value === null || !isFinite(value) || isNaN(value)) return '';

  // If calculator has no interpretation rules, return empty
  if (!calc.interpretationRules || calc.interpretationRules.length === 0) {
    return '';
  }

  // Try to find matching interpretation rule
  for (const rule of calc.interpretationRules) {
    if (!rule.condition || rule.condition.trim() === '') {
      // Empty condition means default/always matches
      return rule.interpretationRu || rule.interpretation || '';
    }

    // Parse and evaluate condition
    try {
      const conditionMet = evaluateCondition(rule.condition, value, inputs);
      if (conditionMet) {
        return rule.interpretationRu || rule.interpretation || '';
      }
    } catch (err) {
      console.warn('Failed to evaluate condition:', rule.condition, err);
    }
  }

  // No matching rule found
  return '';
}

/**
 * Evaluate a condition string against a value
 * Supports conditions like: "< 18.5", ">= 30", ">= 18.5 && < 25"
 */
function evaluateCondition(
  condition: string,
  value: number,
  inputs: Record<string, any>
): boolean {
  // Replace common operators for JavaScript evaluation
  let expr = condition
    .trim()
    // Replace logical operators
    .replace(/\b(and|AND)\b/g, '&&')
    .replace(/\b(or|OR)\b/g, '||');

  // Handle ranges like ">= 18.5 && < 25" or "< 18.5"
  // We need to inject the value into comparison expressions
  
  // Replace standalone comparison operators at the start
  // E.g., "< 18.5" becomes "value < 18.5"
  if (/^[<>=!]/.test(expr)) {
    expr = `value ${expr}`;
  }
  
  // Replace && with proper syntax: ">= 18.5 && < 25" -> "value >= 18.5 && value < 25"
  // Split by && and ||, inject value into each part
  const parts = expr.split(/(\&\&|\|\|)/);
  const processedParts = parts.map(part => {
    const trimmed = part.trim();
    // Skip logical operators
    if (trimmed === '&&' || trimmed === '||') return trimmed;
    // If part starts with comparison, inject value
    if (/^[<>=!]/.test(trimmed)) {
      return `value ${trimmed}`;
    }
    return trimmed;
  });
  
  expr = processedParts.join(' ');

  // Create evaluation context
  const context: Record<string, any> = {
    value,
    ...inputs,
  };

  try {
    // Use Function constructor for safe evaluation
    const func = new Function(...Object.keys(context), `return ${expr};`);
    const result = func(...Object.values(context));
    return Boolean(result);
  } catch (err) {
    console.warn('Condition evaluation failed:', expr, err);
    return false;
  }
}

export default getInterpretation;
