class CreateUsageStatistics < ActiveRecord::Migration[7.2]
  def change
    create_table :usage_statistics do |t|
      t.references :user
      t.references :calculator
      t.date :performed_date
      t.integer :count


      t.timestamps
    end
  end
end
