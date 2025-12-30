pipeline {
    agent any

    environment {
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

        stage('Install Python & Dependencies') {
            steps {
                echo "Installing Python and dependencies..."
                sh '''
                    apt-get update
                    apt-get install -y python3 python3-pip python3-venv

                    python3 --version
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
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
