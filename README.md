![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Web-App CI](https://github.com/software-students-spring2025/4-containers-codeshadow/actions/workflows/web-app.yml/badge.svg?branch=)
![ML-Client CI](https://github.com/software-students-spring2025/4-containers-codeshadow/actions/workflows/ml-client.yml/badge.svg?branch=)

# Containerized App Exercise

## App Description
This is an emotion detector and tracker app. The purpose of this project is to digitize and store data about how often a person sitting behind their computer changes their emotions and maintains a single emotion during their screen time. It's a fun and interesting way to understand yourself better and learn more about how you act in certain scenarios. We believe that this could be taken to higher levels by being utilized in professional interviews and teaching courses over online sessions. It would help organizers of online events better understand their participants' reactions and attention to what is being discussed within the session.

## Team Members
- [Oluwapelumi Adesiyan](https://github.com/oadesiyan)
- [Naseem Uddin](https://github.com/naseem-student)
- [Jibril Wague](https://github.com/Jibril1010)
- [Brandon Morales](https://github.com/bamoeq)

## Project Board
You can find our project board linked [here](https://github.com/orgs/software-students-spring2025/projects/179).

## Configuration Instructions

### Environment Setup

1. **Prerequisites**
   - Docker and Docker Compose installed
   - Python 3.10 or higher
   - Git

2. **Clone the Repository**
   ```bash
   git clone https://github.com/software-students-spring2025/4-containers-codeshadow.git
   cd 4-containers-codeshadow
   ```

3. **Database Setup**
   ```bash
   docker run --name mongodb -d -p 27017:27017 mongo
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DBNAME=emotion_tracker
   SECRET_KEY=your_secret_key_here
   ```

5. **Running the Application**
   ```bash
   # Start all containers
   docker-compose up --build
   ```

   The application will be available at `http://localhost:5000`

### Subsystem Details

#### Web App
- Located in the `web-app` directory
- Built with Flask
- Handles user authentication and emotion tracking
- Provides web interface for emotion visualization

#### Machine Learning Client
- Located in the `machine-learning-client` directory
- Processes webcam feed for emotion detection
- Stores emotion data in MongoDB
- Runs analysis on user emotions

#### Database
- MongoDB container
- Stores user data and emotion tracking information
- Accessible to both web app and ML client

### Development Setup

1. **Web App Development**
   ```bash
   cd web-app
   pipenv install
   pipenv shell
   pytest tests/test_web_app.pyg
   ```

### Testing
- Run tests for web app: `cd web-app && pipenv run pytest`
- Run tests for ML client: `cd machine-learning-client && pipenv run pytest`
- Code coverage must be maintained above 80%

### Continuous Integration
- GitHub Actions workflows for both web app and ML client
- Automatic linting and testing on pull requests
- Status badges displayed at the top of this README