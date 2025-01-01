pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "amineelouadi/esp8266-dhtproject"
        SONAR_HOST_URL = "http://sonarqube:9000" // Use the service name in the Docker network
    }

    stages {
        stage('Clone Project') {
            steps {
                git branch: 'master', url: 'https://github.com/amineelouadi/esp8266-dhtProject.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Use the SonarQube Scanner plugin
                    def scannerHome = tool 'SonarQube Scanner' // Ensure this matches the name configured in Jenkins
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=esp8266-dhtproject \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Build Project') {
            steps {
                // Assuming npm and other dependencies are already installed in the container
                sh 'npm install'
                sh 'npm start'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credential', 
                                                  passwordVariable: 'DOCKER_PASSWORD', 
                                                  usernameVariable: 'DOCKER_USERNAME')]) {
                    sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                }
                sh "docker push ${DOCKER_IMAGE_NAME}:latest"
            }
        }

        stage('Deploy and Start Docker Container') {
            steps {
                sh """
                docker stop esp8266-dhtproject || true
                docker rm esp8266-dhtproject || true
                docker run -d --name esp8266-dhtproject -p 8080:8080 ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
