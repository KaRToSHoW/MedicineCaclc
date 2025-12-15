FactoryBot.define do
  factory :usage_statistic do

    association :user
    association :calculator
    performed_date { Date.today }
    count { 1 }

  end
end
