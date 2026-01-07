import { create, all } from 'mathjs';

const math = create(all, {});

// Prepare a safe evaluate function: convert placeholder-style formula with {var}
// into an expression using variable names and evaluate with provided scope.
export function evaluateFormula(formula: string, inputs: Record<string, any>): number | null {
  if (!formula) return null;
  // Normalize exponent operator (** -> ^) and replace placeholders {var} with var
  const expr = formula.replace(/\*\*/g, '^').replace(/\{\s*([a-zA-Z0-9_]+)\s*\}/g, (_, name) => name);

  // Special-case date math like "{lmp} + 280 days"
  const daysMatch = formula.match(/\{\s*([a-zA-Z0-9_]+)\s*\}\s*\+\s*(\d+)\s*days/i);
  if (daysMatch) {
    const field = daysMatch[1];
    const days = parseInt(daysMatch[2], 10);
    const raw = inputs[field];
    const date = raw ? new Date(raw) : null;
    if (!date || isNaN(date.getTime())) return null;
    const resDate = new Date(date.getTime() + days * 24 * 60 * 60 * 1000);
    return resDate.getTime();
  }

  // Provide inputs as scope to mathjs
  try {
    const scope: Record<string, any> = {};
    Object.keys(inputs).forEach((k) => {
      const v = inputs[k];
      scope[k] = typeof v === 'string' && v.trim() === '' ? null : v;
    });

    // Evaluate using mathjs
    const result = math.evaluate(expr, scope);
    if (typeof result === 'number' && isFinite(result)) return result;
    return Number(result) || null;
  } catch (err) {
    console.warn('Formula evaluation error:', err, 'expr=', expr, 'inputs=', inputs);
    return null;
  }
}

export default evaluateFormula;
