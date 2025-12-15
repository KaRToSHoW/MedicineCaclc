require 'rails_helper'

RSpec.describe "Calculators", type: :request do

  # Uncomment this if controller need authentication
  # let(:user) { create(:user) }
  # before { api_sign_in_as(user) }

  describe "GET /calculators" do
    it "returns http success" do
      get api_v1_calculators_path
      expect(response).to have_http_status(:success)
      expect(response.content_type).to match(/json/)
    end
  end

  describe "GET /calculators/:id" do
    let(:calculator_record) { create(:calculator) }


    it "returns http success" do
      get api_v1_calculator_path(calculator_record)
      expect(response).to have_http_status(:success)
      expect(response.content_type).to match(/json/)
    end
  end


end
