class CreateCalculationResults < ActiveRecord::Migration[7.2]
  def change
    create_table :calculation_results do |t|
      t.references :user
      t.references :calculator
      t.json :input_data
      t.float :result_value
      t.text :interpretation
      t.datetime :performed_at


      t.timestamps
    end
  end
end
