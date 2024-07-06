# Playwright_API_Python_Framework
This repository contains a comprehensive API testing framework built using Python and Playwright. The framework is designed to streamline your API testing process and provide detailed reports with Allure.

## Project Structure

```plaintext
Playwright_API_Python_Framework/
    │
    ├── testcases/  	
    │   ├── conftest.py             
    │   ├── test_1_auth.py       
    │   ├── test_2_create_booking.py       
    │   ├── test_3_update_booking_by_ID.py       
    │	  ├── test_4_get_booking_by_ID.py       
    │	  ├── test_5_delete_booking_by_ID.py            
    │   └── ...
    ├── testData/                   
    │   ├── createAuth.json      
    │   ├── createBooking.json     
    │   ├── updateBooking.json 
    │   ├── getBookingByID.json	
    │   ├── deleteBookingByID.json
    │   └── ...
    ├── API_Utilities/
    │   ├── api_actions.py  
    │   ├── api_utilities.py  
    │   ├── api_validations.py  
    │	  ├── file_reader.py  
    │   ├── logger_utility.py  
    │	  ├── Shared_API_Data.py  
    │   └── ...
    ├── AutoLogs/
    ├── allure-results/
    ├── execution_reports/
    ├── pytest.ini              
    ├── requirements.txt  
    ├── .env
