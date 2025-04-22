pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                // For example: sh 'npm install' or sh 'make build'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                // For example: sh 'pytest tests/' or sh 'npm test'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // For example: sh './deploy.sh'
            }
        }
    }
}
