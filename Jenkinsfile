pipeline {
    agent any

    environment {
        GIT_USER_EMAIL = 'jenkins@example.com'
        GIT_USER_NAME = 'Jenkins CI'
        GIT_REPO_URL = 'https://github.com/Gunjan16/ai-yaml-validator-demo.git' // Replace with your repo URL
    }

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
                    def yamlFiles = sh(script: "ls sample-yamls/*.yaml", returnStdout: true).trim().split("\\n")
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

        stage('Commit and Push Fixes') {
            steps {
                script {
                    sh """
                        git config user.email "${env.GIT_USER_EMAIL}"
                        git config user.name "${env.GIT_USER_NAME}"
                    """

                    def changes = sh(script: 'git status --porcelain', returnStdout: true).trim()

                    if (changes) {
                        echo "Detected changes, committing and pushing to GitHub..."

                        sh 'git add .'
                        sh 'git commit -m "Auto-fixed YAML syntax errors via Jenkins pipeline"'

                        withCredentials([string(credentialsId: 'yaml-pat', variable: 'GIT_PAT')]) {
                            sh """
                                git remote set-url origin https://${GIT_PAT}@${env.GIT_REPO_URL.replace('https://','')}
                                git push origin HEAD:main
                            """
                        }
                    } else {
                        echo "No changes detected, nothing to commit."
                    }
                }
            }
        }
    }
}
