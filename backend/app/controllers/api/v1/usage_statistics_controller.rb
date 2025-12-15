class Api::V1::UsageStatisticsController < Api::BaseController

  def index
    # Default to last 30 days
    end_date = params[:end_date]&.to_date || Date.current
    start_date = params[:start_date]&.to_date || (end_date - 30.days)
    
    @statistics = UsageStatistic
      .by_user(Current.user.id)
      .includes(:calculator)
      .by_date_range(start_date, end_date)
      .order(performed_date: :desc)
    
    # Filter by calculator if provided
    @statistics = @statistics.by_calculator(params[:calculator_id]) if params[:calculator_id].present?
    
    # Group statistics for summary - use separate queries to avoid GROUP BY conflicts
    stats_for_summary = UsageStatistic
      .by_user(Current.user.id)
      .by_date_range(start_date, end_date)
    stats_for_summary = stats_for_summary.by_calculator(params[:calculator_id]) if params[:calculator_id].present?
    
    summary = {
      total_calculations: stats_for_summary.sum(:count),
      total_days: stats_for_summary.select('DISTINCT performed_date').count,
      by_calculator: stats_for_summary.group(:calculator_id).sum(:count),
      by_date: stats_for_summary.group(:performed_date).sum(:count)
    }
    
    render json: {
      statistics: @statistics.as_json(include: { calculator: { only: [:id, :name, :category] } }),
      summary: summary,
      date_range: {
        start: start_date,
        end: end_date
      }
    }
  end

  private
  # Write your private methods here
end
