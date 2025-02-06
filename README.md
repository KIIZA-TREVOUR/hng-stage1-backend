# Overview

This API classifies a given number by providing interesting mathematical properties about it along with a fun fact sourced from the Numbers API.

# Features

Classifies numbers based on mathematical properties.
Returns a fun fact about the number.
Handles CORS and provides JSON-formatted responses.
API Specification

# Endpoint:

GET https://web-production-74f0.up.railway.app/api/classify-number?number=371

# Required JSON Response Format (200 OK):

{
"number": 371,
"is_prime": false,
"is_perfect": false,
"properties": ["armstrong", "odd"],
"digit_sum": 11,
"fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

# Required JSON Response Format (400 Bad Request):

{
"number": "alphabet",
"error": true
}

# Acceptance Criteria:

Handles valid integer inputs.
Returns appropriate HTTP status codes.
Ensures response time is under 500ms.
Provides basic error handling and input validation.

# Requirements

# Technology Stack:

Python

# Deployment:

The API is deployed on railway via https://web-production-74f0.up.railway.app/api/classify-number?number=371

# Additional Notes:

Use the Numbers API to get fun facts about numbers.
