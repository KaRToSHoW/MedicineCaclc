class UsageStatistic < ApplicationRecord
  belongs_to :user
  belongs_to :calculator

  validates :performed_date, presence: true
  validates :count, presence: true, numericality: { greater_than_or_equal_to: 0 }

  scope :by_date_range, ->(start_date, end_date) { where(performed_date: start_date..end_date) }
  scope :by_calculator, ->(calculator_id) { where(calculator_id: calculator_id) }
  scope :by_user, ->(user_id) { where(user_id: user_id) }

  def self.record_usage(user_id, calculator_id, date = Date.current)
    stat = find_or_initialize_by(user_id: user_id, calculator_id: calculator_id, performed_date: date)
    stat.count ||= 0
    stat.count += 1
    stat.save
  end
end
