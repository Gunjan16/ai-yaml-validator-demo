pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Python dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Validate & Auto-fix YAML') {
            steps {
                script {
                    def yamlFiles = findFiles(glob: 'sample-yamls/*.yaml')
                    def failed = false
                    for (file in yamlFiles) {
                        echo "Processing file: ${file}"
                        def status = sh(script: "python3 yaml_validator_autofix.py ${file}", returnStatus: true)
                        if (status != 0) {
                            failed = true
                            echo "❌ Validation or auto-fix failed for ${file}"
                        } else {
                            echo "✅ Validation passed or auto-fixed: ${file}"
                        }
                    }
                    if (failed) {
                        error("One or more YAML files failed validation/fixing.")
                    }
                }
            }
        }
    }
}
EOF
