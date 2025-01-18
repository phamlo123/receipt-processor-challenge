To install, follow the steps below:
1. Make sure Docker desktop is installed on your machine
2. Navigate to the repository directory (/receipt-processor-challenge)
3. Run docker-compose up --build to create the Docker image and start up the application
4. The application can now be accessed at `localhost`. Use curl/postman/browser to GET localhost/ to confirm
5. The application supports the following API endpoints:
- POST localhost/receipts/process/
- GET localhost/receipts/:receipt_id/points

Note:
- The application is set to reload automatically from file changes. Data will not persist if the source code is changed while the application is running.

Tech Stacks:
- FastAPI, uvicorn.
- pydantic for serializer and validation.