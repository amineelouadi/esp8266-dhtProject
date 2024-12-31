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

        stage('Install Node.js and npm') {
            steps {
                script {
                    // Install Node.js and npm (Ubuntu-based Jenkins image)
                    sh 'curl -sL https://deb.nodesource.com/setup_16.x | bash -'
                    sh 'apt-get install -y nodejs'
                }
            }
        }

        stage('Create Virtual Environment and Install Dependencies') {
            steps {
                script {
                    // Create a virtual environment in /tmp/venv (writable directory)
                    sh 'python3 -m venv /tmp/venv'

                    // Activate virtual environment and install dependencies using bash
                    sh '''
                        /bin/bash -c "source /tmp/venv/bin/activate && pip install -r requirements.txt"
                    '''
                }
            }
        }

        stage('Build Project') {
            steps {
                sh 'npm install'
                sh 'npm run build'
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
