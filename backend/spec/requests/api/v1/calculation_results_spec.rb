require 'rails_helper'

RSpec.describe "Calculation results", type: :request do

  # Uncomment this if controller need authentication
  let(:user) { create(:user) }
  before { api_sign_in_as(user) }

  describe "GET /calculation_results" do
    it "returns http success" do
      get api_v1_calculation_results_path
      expect(response).to have_http_status(:success)
      expect(response.content_type).to match(/json/)
    end
  end

  describe "GET /calculation_results/:id" do
    let(:calculation_result_record) { create(:calculation_result, user: user) }


    it "returns http success" do
      get api_v1_calculation_result_path(calculation_result_record)
      expect(response).to have_http_status(:success)
      expect(response.content_type).to match(/json/)
    end
  end


end
