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

testcasedata = read_file('updateBooking.json')

# Initialize Faker
fake = Faker()

@pytest.mark.parametrize("case", testcasedata["positive"])
def test_update_booking_by_id(api_request_context,case):

    first_name=fake.first_name()
    last_name=fake.last_name()
    case["params"]["firstname"] = first_name
    case["params"]["lastname"] = last_name
    shared_data.set_data("first_name", case["params"]["firstname"])
    shared_data.set_data("last_name", case["params"]["lastname"])
    shared_data.set_data("totalprice", case["params"]["totalprice"])
    shared_data.set_data("additionalneeds", case["params"]["additionalneeds"])

    token=shared_data.get_data("token_id")
    booking_id = shared_data.get_data("booking_id")

    # Add Authorization header
    headers = case.get("headers", {})
    headers["Cookie"] = f"token={token}"
    response = put_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"]+f"/{booking_id}",payload=case["params"],header=headers)
    validate_response_code(response, case["expected_status"])

    validate_in_response_body(response, 'firstname', first_name,'first_name not matches')
    validate_in_response_body(response, 'lastname', last_name, 'last_name not matches')
    validate_schema(response=response, schema=case['expected_schema'])
