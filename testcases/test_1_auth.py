import allure
import pytest
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

testcasedata = read_file('createAuth.json')


@allure.feature("Test Auth API")
@allure.story("Test Auth API...")
@allure.title("Verify the Auth API Positive flow")
@allure.description("verify the get API response status code and data")
@allure.severity("blocker")
@pytest.mark.Regression
@pytest.mark.Smoke
@pytest.mark.Positive
@pytest.mark.parametrize("case", testcasedata["positive"])
def test_create_authToken_positive(api_request_context,case):

    response = post_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"],payload=case["params"],header=case["headers"])
    validate_response_code(response, case["expected_status"])

    validate_schema(response=response, schema=case['expected_schema'])

    shared_data.set_data("token_id", get_value_from_response(response,'token'))


@allure.feature("Test Auth API negative flow")
@allure.severity("blocker")
@pytest.mark.Regression
@pytest.mark.Smoke
@pytest.mark.negative
@pytest.mark.parametrize("case", testcasedata["negative"])
def test_create_authToken_negative(api_request_context,case):

    response = post_request(api_request_context, base_url =baseURL, api_endpoint=case["endpoint"],payload=case["params"],header=case["headers"])
    validate_response_code(response, case["expected_status"])
    validate_schema(response=response, schema=case['expected_schema'])

