import logging

import pytest
from faker import Faker
from API_Utilities.api_actions import get_request, post_request, put_request, patch_request,delete_request
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
# Get the base URL from environment variables
baseURL = os.getenv('base_url')

testcasedata = read_file('createBooking.json')

# Initialize Faker
fake = Faker()

@pytest.mark.parametrize("case", testcasedata["positive"])
def test_create_booking(api_request_context,case):

    first_name=fake.first_name()
    last_name=fake.last_name()
    case["params"]["firstname"] = first_name
    case["params"]["lastname"] = last_name

    # Add Authorization header
    headers = case.get("headers", {})
    headers["Authorization"] = f"Bearer "

    response = post_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"],payload=case["params"],header=headers)
    validate_response_code(response, case["expected_status"])

    validate_in_response_body(response, 'booking.firstname', first_name,'first_name not matches')
    validate_in_response_body(response, 'booking.lastname', last_name, 'last_name not matches')
    validate_schema(response=response, schema=case['expected_schema'])

    shared_data.set_data("booking_id", get_value_from_response(response,'bookingid'))



@pytest.mark.parametrize("case", testcasedata["negative"])
def test_create_booking_negative(api_request_context,case):

    # Add Authorization header
    headers = case.get("headers", {})
    headers["Authorization"] = f"Bearer "

    response = post_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"],payload=case["params"],header=headers)
    validate_response_code(response, case["expected_status"])
    validate_schema(response=response, schema=case['expected_schema'])
