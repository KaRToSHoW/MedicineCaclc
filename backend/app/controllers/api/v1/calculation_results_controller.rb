class Api::V1::CalculationResultsController < Api::BaseController
  before_action :set_calculation_result, only: [:show]

  def index
    @results = Current.user.calculation_results.includes(:calculator).recent
    
    # Filter by calculator if provided
    @results = @results.by_calculator(params[:calculator_id]) if params[:calculator_id].present?
    
    # Pagination
    page = params[:page]&.to_i || 1
    per_page = params[:per_page]&.to_i || 20
    
    @results = @results.limit(per_page).offset((page - 1) * per_page)
    
    render json: @results.as_json(include: { calculator: { only: [:id, :name, :category] } })
  end

  def show
    render json: @calculation_result.as_json(include: { calculator: { only: [:id, :name, :category] } })
  end

  def create
    calculator = Calculator.find(params[:calculator_id])
    
    # Calculate result based on calculator formula
    result_value = calculate_result(calculator, params[:input_data])
    interpretation = interpret_result(calculator, result_value)
    
    @calculation_result = Current.user.calculation_results.build(
      calculator: calculator,
      input_data: params[:input_data],
      result_value: result_value,
      interpretation: interpretation
    )
    
    if @calculation_result.save
      # Record usage statistics
      UsageStatistic.record_usage(Current.user.id, calculator.id)
      
      render json: @calculation_result.as_json(include: { calculator: { only: [:id, :name, :category] } }), status: :created
    else
      render json: { errors: @calculation_result.errors.full_messages }, status: :unprocessable_entity
    end
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Calculator not found' }, status: :not_found
  rescue => e
    render json: { error: e.message }, status: :unprocessable_entity
  end

  private

  def set_calculation_result
    @calculation_result = Current.user.calculation_results.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Calculation result not found' }, status: :not_found
  end

  def calculate_result(calculator, input_data)
    # Evaluate the formula with input data
    # This is a simplified implementation - in production, use a safe evaluation method
    formula = calculator.formula.dup
    
    input_data.each do |key, value|
      formula.gsub!("{#{key}}", value.to_s)
    end
    
    # Use Ruby's eval with caution - sanitize input in production
    eval(formula).to_f.round(2)
  end

  def interpret_result(calculator, result_value)
    rules = calculator.interpretation_rules
    
    return 'No interpretation available' if rules.blank?
    
    # Find matching interpretation rule
    rules.each do |rule|
      if evaluate_condition(result_value, rule['condition'])
        return rule['interpretation']
      end
    end
    
    'Result is within normal range'
  end

  def evaluate_condition(value, condition)
    # Parse condition like "< 18.5" or ">= 25 and < 30"
    return true if condition.blank?
    
    condition.split('and').all? do |part|
      part = part.strip
      
      if part.match?(/^>=\s*[\d.]+/)
        threshold = part.match(/[\d.]+/)[0].to_f
        value >= threshold
      elsif part.match?(/^>\s*[\d.]+/)
        threshold = part.match(/[\d.]+/)[0].to_f
        value > threshold
      elsif part.match?(/^<=\s*[\d.]+/)
        threshold = part.match(/[\d.]+/)[0].to_f
        value <= threshold
      elsif part.match?(/^<\s*[\d.]+/)
        threshold = part.match(/[\d.]+/)[0].to_f
        value < threshold
      else
        false
      end
    end
  end
end
