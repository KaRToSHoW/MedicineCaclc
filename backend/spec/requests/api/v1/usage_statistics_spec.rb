require 'rails_helper'

RSpec.describe "Usage statistics", type: :request do

  # Uncomment this if controller need authentication
  let(:user) { create(:user) }
  before { api_sign_in_as(user) }

  describe "GET /usage_statistics" do
    it "returns http success" do
      get api_v1_usage_statistics_path
      expect(response).to have_http_status(:success)
      expect(response.content_type).to match(/json/)
    end
  end



end
