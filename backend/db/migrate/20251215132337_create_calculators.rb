class CreateCalculators < ActiveRecord::Migration[7.2]
  def change
    create_table :calculators do |t|
      t.string :name
      t.text :description
      t.text :formula
      t.string :category
      t.json :input_fields
      t.json :interpretation_rules


      t.timestamps
    end
  end
end
