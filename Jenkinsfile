pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtualenv and Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Validate & Auto-fix YAML') {
            steps {
                script {
                    def yamlFiles = findFiles(glob: 'sample-yamls/*.yaml')
                    def failed = false

                    for (file in yamlFiles) {
                        echo "Processing file: ${file}"
                        def status = sh(
                            script: ". venv/bin/activate && python yaml_validator_autofix.py ${file}",
                            returnStatus: true
                        )
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
