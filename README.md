# Project instructions.

Technical specifications:

Python version 3.8.2
MongoDB 4.0  (installing mongodb is really easy in any OS)

## Build

1. Create a python [virtual environment](https://docs.python.org/3/library/venv.html). he next link.
2. Activate the environment and install required packages with the command: `pip install -r requirements.txt`

## Running

You can test all the functionalities of the project by running the tests: `pytest -v` in the project root directory
(remember to activate the virtual environment).

Or you can start a test http server by: `flask run`. Use `curl` for sending requests to the server. In order
to get insight of the expected json format you can take a look at the test in the file `tests/test_api.py`.

## Running the periodic task
DB_NAME=musala_test celery -A celery_application worker -l DEBUG -B
