import sys
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from transformers import pipeline

yaml = YAML()

print("Loading AI model for YAML fix suggestions...")
fixer = pipeline("text2text-generation", model="t5-base")

def validate_yaml(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            data = yaml.load(content)
        print(f"✅ YAML is valid: {file_path}")
        return True, content
    except YAMLError as e:
        print(f"❌ YAML syntax error in {file_path}: {e}")
        return False, content if 'content' in locals() else ''

def ai_fix_yaml(yaml_text):
    prompt = f"fix yaml syntax errors:\n{yaml_text}\nfixed yaml:"
    print("🤖 Asking AI to fix YAML...")
    result = fixer(prompt, max_length=512, do_sample=False)
    fixed_yaml = result[0]['generated_text']
    return fixed_yaml

def save_fixed_yaml(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"📝 Saved fixed YAML to {file_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 yaml_validator_autofix.py <yaml-file>")
        sys.exit(1)
    file_path = sys.argv[1]

    valid, original_content = validate_yaml(file_path)
    if valid:
        sys.exit(0)

    fixed_yaml = ai_fix_yaml(original_content)
    try:
        yaml.load(fixed_yaml)
        save_fixed_yaml(file_path, fixed_yaml)
        print("✅ AI fixed YAML is valid now!")
        sys.exit(0)
    except YAMLError as e:
        print(f"❌ AI fixed YAML still invalid: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

