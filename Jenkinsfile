pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('Test') {
            steps {
                httpRequest url: 'http://0.0.0.0:8000', validResponseCodes: '200'
            }
        }
    }
}