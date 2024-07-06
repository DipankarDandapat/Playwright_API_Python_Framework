from API_Utilities.api_utilities import get_response_data, get_value_from_response, get_response_code
from jsonschema import validate, ValidationError

import pprint
from API_Utilities import logger_utility


log = logger_utility.customLogger()
def validate_response_code(response, expected_response_code):
    """
    Method to validate the response code
    :param expected_response_code:
    :param response:
    :return:
    """
    actual_status_code = get_response_code(response)
    assert actual_status_code == expected_response_code
    log.info(f'Expected response code: {expected_response_code} is matches the actual code: {actual_status_code}')



def validate_entire_response_body_data(response, expected_response_data):
    """
    Method to validate response entire body
    :param expected_response_data:
    :param response:
    :return:
    """
    actual_response_data = get_response_data(response)
    assert actual_response_data == expected_response_data
    log.info(f'{expected_response_data} is same as  {response}')

def validate_in_response_body(response, jsonpath_expression, expected_value, message_on_failure):
    """
    Method to validate data in the response body
    :param jsonpath_expression:
    :param message_on_failure:
    :param expected_value:
    :param response:
    :return:
    """

    data_value = get_value_from_response(response, jsonpath_expression)

    if isinstance(expected_value, (int, float)) or isinstance(data_value, (int, float)):
        data_verified = expected_value == data_value
    else:
        data_verified = expected_value in data_value

    log.info(f'{expected_value} is present in the response')
    assert data_verified, message_on_failure



def validate_schema(response, schema):
    """
    Validates the response against the provided schema.

    :param response: JSON response from the API
    :param schema: JSON schema to validate against
    :return: None
    """
    try:
        response1 = get_response_data(response)
        validate(instance=response1, schema=schema)
        log.info("Schema validation passed.")
    except ValidationError as e:
        log.info(f"Schema validation failed: {e.message}")