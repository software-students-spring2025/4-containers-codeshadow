![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Web-App CI](https://github.com/software-students-spring2025/4-containers-codeshadow/actions/workflows/web-app.yml/badge.svg?branch=)
![ML-Client CI](https://github.com/software-students-spring2025/4-containers-codeshadow/actions/workflows/ml-client.yml/badge.svg?branch=)

## App Description
This is an emotion detector and tracker app. This project aims to digitize and store data about how often a person sitting behind their computer changes their emotions and maintains a single emotion during their screen time. It's a fun and engaging way to understand yourself better and learn more about how you act in certain scenarios. We believe that this could be taken to higher levels by being utilized in professional interviews and teaching courses over online sessions. It would help organizers of online events better understand their participants' reactions and attention to what is being discussed within the session.

## Prerequisites

- Docker and Docker Compose are installed on your system
- Python 3.x (if running locally without Docker)
- Git

## Project Structure

```
.
├── web-app/                  # Flask web application
│   ├── app.py                # Main application file
│   ├── requirements.txt      # Python dependencies
│   ├── templates/            # HTML templates
│   └── .env                  # Environment Variables for MongoDB (app.py usage)
│   └── static/               # Static files (CSS, JS, images)
├── machine-learning-client/  # ML service
│   ├── ai.py                 # ML service implementation
│   └── requirements.txt      # ML service dependencies
├── .env                      # Environment Variables for MongoDB (docker usage)
└── docker-compose.yml        # Docker configuration
```

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd 4-containers-codeshadow
   ```

2. Create environment files:
   - Copy `web-app/env.example` to `web-app/.env`
   - Fill in the required environment variables in `web-app/.env`:
     ```
     MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<appname>
     MONGO_DBNAME=<your_database_name>
     SECRET_KEY=<your_secret_key>
     ```
   - Copy the .env file within your web-app folder and paste it into the .env folder
   - Note: You should have two .env files, one in the web-app folder and one in the root directory 4-containers-codeshadow

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. The application will be available at:
   - Web application: http://localhost:5000
   - ML service: http://localhost:6000
   - MongoDB: localhost:27017


### Running Locally (Without Docker)

1. Set up Python virtual environment:
   ```bash
   cd web-app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables as described in the Docker section

4. Run the application:
   ```bash
   python app.py
   ```

## Troubleshooting

If you encounter any issues:

1. Check that all environment variables are properly set
2. Ensure MongoDB is running and accessible
3. Verify that all required ports (5000, 6000, 27017) are available
4. Check Docker logs for any service-specific errors:
   ```bash
   docker-compose logs <service_name>
   ```

#### Web App
- Located in the `web-app` directory
- Built with Flask
- Handles user authentication and emotion tracking
- Provides a web interface for emotion visualization

#### Machine Learning Client
- Located in the `machine-learning-client` directory
- Processes webcam feed for emotion detection
- Stores emotion data in MongoDB
- Runs analysis on user emotions

#### Database
- MongoDB container
- Stores user data and emotion tracking information
- Accessible to both the web app and the ML client

### Testing
- Run tests for web app and ML: `cd web-app && python -m pytest tests/test_web_app.py`
This will run 5 tests that check our homepage, login/signup, database changing with emotions, error checking fields of the signup/login, and error checking for no camera. Altogether testing allows us to know our code is running successfully. 


### Continuous Integration
- GitHub Actions workflows for both the web app and the ML client
- Automatic linting and testing on pull requests
- Status badges are displayed at the top of this README

## Task Board
Take a look at our task board [here](https://github.com/orgs/software-students-spring2025/projects/179/views/1)!
