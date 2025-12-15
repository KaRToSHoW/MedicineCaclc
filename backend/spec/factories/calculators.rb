FactoryBot.define do
  factory :calculator do

    name { "BMI Calculator" }
    description { "Body Mass Index calculator" }
    formula { "{weight} / (({height} / 100) ** 2)" }
    category { "General" }
    input_fields do
      [
        { name: 'weight', label: 'Weight', type: 'number', unit: 'kg', min: 0, max: 500 },
        { name: 'height', label: 'Height', type: 'number', unit: 'cm', min: 0, max: 300 }
      ]
    end
    interpretation_rules do
      [
        { min: 0, max: 18.5, category: 'Underweight', severity: 'caution' },
        { min: 18.5, max: 25, category: 'Normal', severity: 'normal' },
        { min: 25, max: 30, category: 'Overweight', severity: 'warning' },
        { min: 30, max: 100, category: 'Obese', severity: 'danger' }
      ]
    end

  end
end
