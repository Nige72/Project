pipeline {
    agent any
    
    stages {
//this stage sets up the virtual environment for the unit tests
    stage('Setup') {
        steps {
            sh """sudo apt install python3-venv -y 
            python3 -m venv venv
            . ./venv/bin/activate
            pip3 install -r requirements.txt
            """
            }
        }
        stage('Test') {
        steps {
            sh """source venv/Scripts/activate
            python3 -m pytest \
                --cov=application \
                --cov=-report term-missing \
                --cov=-report xml:coverage.xml \
                --junitxml=junit_report.xml
                 """
            }
        }
    }

}