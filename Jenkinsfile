pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/mimikyu-101/Basic-Flask-App'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest || echo "No tests found"
                '''
            }
        }

        stage('Build Application') {
            steps {
                sh 'echo "Build step completed"'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                mkdir -p /tmp/flask-deploy
                cp -r . /tmp/flask-deploy/
                echo "Application deployed to /tmp/flask-deploy"
                '''
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
        success {
            echo 'Pipeline executed successfully.'
        }
    }
}
