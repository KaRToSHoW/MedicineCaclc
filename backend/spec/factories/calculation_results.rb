FactoryBot.define do
  factory :calculation_result do

    association :user
    association :calculator
    input_data { { weight: 70, height: 175 } }
    result_value { 22.86 }
    interpretation { "Normal - Your BMI is within the healthy weight range" }
    performed_at { Time.current }

  end
end
