class CalculationResult < ApplicationRecord
  belongs_to :user
  belongs_to :calculator

  validates :input_data, presence: true
  validates :result_value, presence: true
  validates :interpretation, presence: true
  validates :performed_at, presence: true

  before_validation :set_performed_at, on: :create

  scope :recent, -> { order(performed_at: :desc) }
  scope :by_calculator, ->(calculator_id) { where(calculator_id: calculator_id) }
  scope :by_user, ->(user_id) { where(user_id: user_id) }

  private

  def set_performed_at
    self.performed_at ||= Time.current
  end
end
