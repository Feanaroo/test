# Project Title

Numbers API Project

## Project Description

This project is a simple web service that interacts with the Numbers API to fetch trivia about numbers and store them in a database. It also provides an endpoint to retrieve the stored trivia.

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/Feanaroo/test.git
   cd test
   ```

2. Build the Docker image:
   ```sh
   docker build -t numbers-api .
   ```

3. Run the Docker container:
   ```sh
   docker run -p 5858:5858 numbers-api
   ```

4. Initialize the database:
   ```sh
   docker exec -it <container_id> alembic upgrade head
   ```

## Usage Examples

1. Fetch trivia about a specific number:
   ```sh
   curl http://127.0.0.1:5858/numbers/65
   ```

2. Fetch trivia about numbers from 50 to 1000:
   ```sh
   curl http://127.0.0.1:5858/numbers
   ```

3. Update the database with trivia about prime numbers:
   ```sh
   curl -X POST http://127.0.0.1:5858/numbers
   ```

## Running Tests

1. Run the database tests:
   ```sh
   docker exec -it <container_id> python -m unittest tests/tests_db.py
   ```

2. Run the handler tests:
   ```sh
   docker exec -it <container_id> python -m unittest tests/tests_handler.py
   ```
