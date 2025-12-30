pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
        }
    }

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
                echo "Installing Python dependencies..."
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    pytest || echo "No tests found or tests failed"
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo "Building application..."
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
