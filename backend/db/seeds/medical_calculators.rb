# Medical Calculators Seed Data

puts "🏥 Creating medical calculators..."

# BMI Calculator (Body Mass Index)
Calculator.find_or_create_by(name: "Body Mass Index (BMI)") do |calc|
  calc.description = "Calculates Body Mass Index based on height and weight. BMI is a measure of body fat based on height and weight that applies to adult men and women."
  calc.category = "general"
  calc.formula = "{weight} / (({height} / 100) * ({height} / 100))"
  calc.input_fields = [
    { name: "weight", label: "Weight", unit: "kg", type: "number", min: 20, max: 300 },
    { name: "height", label: "Height", unit: "cm", type: "number", min: 100, max: 250 }
  ]
  calc.interpretation_rules = [
    { condition: "< 16", interpretation: "Severe Thinness - Seek immediate medical attention", severity: "critical" },
    { condition: ">= 16 and < 17", interpretation: "Moderate Thinness - Consult with a healthcare provider", severity: "warning" },
    { condition: ">= 17 and < 18.5", interpretation: "Mild Thinness - Consider nutritional counseling", severity: "caution" },
    { condition: ">= 18.5 and < 25", interpretation: "Normal Weight - Maintain healthy lifestyle", severity: "normal" },
    { condition: ">= 25 and < 30", interpretation: "Overweight - Consider lifestyle modifications", severity: "caution" },
    { condition: ">= 30 and < 35", interpretation: "Obese Class I - Consult with healthcare provider", severity: "warning" },
    { condition: ">= 35 and < 40", interpretation: "Obese Class II - Medical evaluation recommended", severity: "danger" },
    { condition: ">= 40", interpretation: "Obese Class III (Severe) - Immediate medical intervention needed", severity: "critical" }
  ]
end

# Heart Rate Maximum
Calculator.find_or_create_by(name: "Maximum Heart Rate") do |calc|
  calc.description = "Estimates the maximum heart rate based on age. Used for exercise intensity calculations."
  calc.category = "cardiology"
  calc.formula = "220 - {age}"
  calc.input_fields = [
    { name: "age", label: "Age", unit: "years", type: "number", min: 1, max: 120 }
  ]
  calc.interpretation_rules = [
    { condition: ">= 190", interpretation: "Very high maximum heart rate - typical for young individuals", severity: "normal" },
    { condition: ">= 160 and < 190", interpretation: "High maximum heart rate - moderate exercise recommended", severity: "normal" },
    { condition: ">= 140 and < 160", interpretation: "Moderate maximum heart rate - adjust exercise intensity accordingly", severity: "normal" },
    { condition: "< 140", interpretation: "Lower maximum heart rate - typical for older individuals, exercise with caution", severity: "caution" }
  ]
end

# Blood Pressure Classification
Calculator.find_or_create_by(name: "Blood Pressure Classification") do |calc|
  calc.description = "Classifies blood pressure readings according to clinical guidelines."
  calc.category = "cardiology"
  calc.formula = "{systolic}"
  calc.input_fields = [
    { name: "systolic", label: "Systolic BP", unit: "mmHg", type: "number", min: 60, max: 250 },
    { name: "diastolic", label: "Diastolic BP", unit: "mmHg", type: "number", min: 40, max: 150 }
  ]
  calc.interpretation_rules = [
    { condition: "< 90", interpretation: "Hypotension - Low blood pressure, may cause dizziness", severity: "warning" },
    { condition: ">= 90 and < 120", interpretation: "Normal - Optimal blood pressure range", severity: "normal" },
    { condition: ">= 120 and < 130", interpretation: "Elevated - Lifestyle changes recommended", severity: "caution" },
    { condition: ">= 130 and < 140", interpretation: "Hypertension Stage 1 - Consult healthcare provider", severity: "warning" },
    { condition: ">= 140 and < 180", interpretation: "Hypertension Stage 2 - Medical treatment recommended", severity: "danger" },
    { condition: ">= 180", interpretation: "Hypertensive Crisis - Seek emergency medical attention", severity: "critical" }
  ]
end

# Ideal Body Weight (Devine Formula)
Calculator.find_or_create_by(name: "Ideal Body Weight") do |calc|
  calc.description = "Calculates ideal body weight using the Devine formula. Note: Different formulas may be more appropriate for certain populations."
  calc.category = "general"
  calc.formula = "50 + 2.3 * (({height} - 152.4) / 2.54)"
  calc.input_fields = [
    { name: "height", label: "Height", unit: "cm", type: "number", min: 100, max: 250 },
    { name: "gender", label: "Gender", type: "select", options: ["male", "female"] }
  ]
  calc.interpretation_rules = [
    { condition: "", interpretation: "This is your calculated ideal body weight based on the Devine formula. Compare with your actual weight.", severity: "normal" }
  ]
end

# Basal Metabolic Rate (Harris-Benedict)
Calculator.find_or_create_by(name: "Basal Metabolic Rate (BMR)") do |calc|
  calc.description = "Estimates the number of calories your body needs at rest using the Harris-Benedict equation."
  calc.category = "endocrinology"
  calc.formula = "88.362 + (13.397 * {weight}) + (4.799 * {height}) - (5.677 * {age})"
  calc.input_fields = [
    { name: "weight", label: "Weight", unit: "kg", type: "number", min: 20, max: 300 },
    { name: "height", label: "Height", unit: "cm", type: "number", min: 100, max: 250 },
    { name: "age", label: "Age", unit: "years", type: "number", min: 1, max: 120 },
    { name: "gender", label: "Gender", type: "select", options: ["male", "female"] }
  ]
  calc.interpretation_rules = [
    { condition: "< 1200", interpretation: "Low BMR - May need nutritional assessment", severity: "caution" },
    { condition: ">= 1200 and < 1800", interpretation: "Normal BMR range for most adults", severity: "normal" },
    { condition: ">= 1800 and < 2500", interpretation: "Higher BMR - typical for active or larger individuals", severity: "normal" },
    { condition: ">= 2500", interpretation: "Very high BMR - typical for very active or large individuals", severity: "normal" }
  ]
end

# Glasgow Coma Scale (simplified)
Calculator.find_or_create_by(name: "Glasgow Coma Scale") do |calc|
  calc.description = "Assesses level of consciousness in patients. Sum of eye, verbal, and motor responses."
  calc.category = "neurology"
  calc.formula = "{eye_response} + {verbal_response} + {motor_response}"
  calc.input_fields = [
    { name: "eye_response", label: "Eye Response", type: "number", min: 1, max: 4 },
    { name: "verbal_response", label: "Verbal Response", type: "number", min: 1, max: 5 },
    { name: "motor_response", label: "Motor Response", type: "number", min: 1, max: 6 }
  ]
  calc.interpretation_rules = [
    { condition: "<= 8", interpretation: "Severe Brain Injury - Immediate emergency care required", severity: "critical" },
    { condition: ">= 9 and <= 12", interpretation: "Moderate Brain Injury - Urgent medical attention needed", severity: "danger" },
    { condition: ">= 13 and <= 14", interpretation: "Mild Brain Injury - Medical evaluation recommended", severity: "warning" },
    { condition: "= 15", interpretation: "Normal - Fully conscious and oriented", severity: "normal" }
  ]
end

# Pediatric Weight Estimation (Age-based)
Calculator.find_or_create_by(name: "Pediatric Weight Estimation") do |calc|
  calc.description = "Estimates pediatric weight based on age for emergency situations when actual weight is unavailable."
  calc.category = "pediatrics"
  calc.formula = "2 * ({age} + 4)"
  calc.input_fields = [
    { name: "age", label: "Age", unit: "years", type: "number", min: 1, max: 10 }
  ]
  calc.interpretation_rules = [
    { condition: "", interpretation: "Estimated weight for emergency medication dosing. Use actual weight when available.", severity: "normal" }
  ]
end

puts "✅ Created #{Calculator.count} medical calculators"
