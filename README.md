# Users management API
This project is designed for user management. API contain user's username, email and registration date.

# Main functions
- Create user
- Update user's data
- Delete user
- Get one user
- Get users (with optional pagination)
- Get top 5 users with the longest username
- Get number of users registered for last week
- Get proportion of users with email with specified domain

## How to run

1. Clone repository to work directory
```shell
git clone https://github.com/Tireon003/users_api_flask.git
```
2. Enter to project folder
3. Configure virtual environment (the following is an example for Windows)
```shell
python -m venv venv

./venv/Scripts/activate
```
4. Create .env and .env_test files in root of project Here is variables for .env and .env_test respectively.
```editorconfig
//.env
DB_URL="sqlite:///users.db"

API_HOST="0.0.0.0"
API_PORT=5001

LOG_LEVEL="INFO"
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"

IS_DEBUG=1
```
```editorconfig
//.env_test
DB_URL="sqlite:///users_test.db"

API_HOST="0.0.0.0"
API_PORT=5001

LOG_LEVEL="INFO"
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"

IS_DEBUG=1
```
5. You can run tests
```shell
pytest .
```
6. Start server with command
```shell
python app/main.py
```

## How to use

You can learn about all possible methods on the Swagger documentation page located at (with settings provided in readme):
```
http://localhost:5001/api/docs/
```
The documentation site has a detailed view of all available endpoints, request and response schemes for various statuses.