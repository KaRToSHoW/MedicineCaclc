class Calculator < ApplicationRecord
  has_many :calculation_results, dependent: :destroy
  has_many :usage_statistics, dependent: :destroy

  validates :name, presence: true
  validates :category, presence: true
  validates :formula, presence: true
  validates :input_fields, presence: true
  validates :interpretation_rules, presence: true

  # Category constants
  CATEGORIES = %w[cardiology endocrinology general neurology pediatrics].freeze
end
