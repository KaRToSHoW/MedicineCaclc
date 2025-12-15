class Api::V1::CalculatorsController < Api::BaseController
  skip_before_action :authenticate, only: [:index, :show]

  def index
    @calculators = Calculator.all
    
    # Filter by category if provided
    @calculators = @calculators.where(category: params[:category]) if params[:category].present?
    
    render json: @calculators
  end

  def show
    @calculator = Calculator.find(params[:id])
    render json: @calculator
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Calculator not found' }, status: :not_found
  end

  private
  # Write your private methods here
end
