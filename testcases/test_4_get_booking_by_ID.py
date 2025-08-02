import pytest
from API_Utilities.api_actions import get_request
from API_Utilities.api_utilities import get_response_data, get_value_from_response
from API_Utilities.api_validations import validate_response_code, validate_in_response_body,validate_schema
from API_Utilities.file_reader import read_file
from API_Utilities.Shared_API_Data import shared_data
from dotenv import load_dotenv
import os

from API_Utilities import logger_utility

log = logger_utility.customLogger()

# Load environment variables from .env file
load_dotenv()


testcasedata = read_file('getBookingByID.json')

@pytest.mark.parametrize("case", testcasedata["positive"])
def test_update_booking_by_id(api_request_context,case):
    # Get the base URL from environment variables
    baseURL = os.getenv('BASE_URL')


    booking_id=shared_data.get_data("booking_id")
    response = get_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"]+f"/{booking_id}",header=case['headers'])
    validate_response_code(response, case["expected_status"])

    validate_in_response_body(response, 'firstname', shared_data.get_data("first_name"),'first_name not matches')
    validate_in_response_body(response, 'lastname', shared_data.get_data("last_name"), 'last_name not matches')
    validate_in_response_body(response, 'totalprice', shared_data.get_data("totalprice"), 'totalprice not matches')
    validate_in_response_body(response, 'additionalneeds', shared_data.get_data("additionalneeds"), 'additionalneeds not matches')
    validate_schema(response=response, schema=case['expected_schema'])
