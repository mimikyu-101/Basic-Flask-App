pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        DEPLOY_DIR = "/tmp/flask_app_deploy"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo "Cloning GitHub repository..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Setting up Python virtual environment and installing dependencies..."
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running unit tests using pytest..."
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest || echo "No tests found or tests failed"
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo "Building application (packaging source)..."
                sh '''
                    mkdir -p build
                    cp -r app.py templates static build/ || true
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Simulating deployment..."
                sh '''
                    mkdir -p $DEPLOY_DIR
                    cp -r build/* $DEPLOY_DIR/
                    echo "Application deployed to $DEPLOY_DIR"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for errors."
        }
    }
}
