import sys
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from transformers import pipeline

yaml = YAML()
fixer = pipeline("text2text-generation", model="t5-base")

def validate_yaml(content):
    try:
        yaml.load(content)
        return True, None
    except YAMLError as e:
        return False, str(e)

def get_ai_suggestion(content):
    prompt = f"Suggest minimal YAML syntax fixes or explain errors for:\n{content}"
    print("🤖 Asking AI for minimal fix suggestions...")
    result = fixer(prompt, max_new_tokens=64, do_sample=False)
    suggestion = result[0]['generated_text']
    return suggestion.strip()

def auto_fix_simple_errors(content):
    # Simple heuristic fixes
    fixed_content = content
    # Fix unmatched quotes: if odd count, add closing quote
    for quote_char in ['"', "'"]:
        if fixed_content.count(quote_char) % 2 != 0:
            fixed_content += quote_char
    # Could add more heuristics here if needed
    return fixed_content

def main(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    valid, error = validate_yaml(content)
    if valid:
        print(f"✅ YAML is valid: {file_path}")
        return 0

    print(f"❌ YAML invalid: {error}")
    ai_suggestion = get_ai_suggestion(content)
    print(f"💡 AI suggests:\n{ai_suggestion}")

    fixed_content = auto_fix_simple_errors(content)

    valid_after_fix, error_after_fix = validate_yaml(fixed_content)
    if valid_after_fix:
        with open(file_path, 'w') as f:
            f.write(fixed_content)
        print(f"✅ Auto-fixed YAML saved: {file_path}")
        return 0
    else:
        print(f"❌ Still invalid after auto-fix: {error_after_fix}")
        print("⚠️ Please review AI suggestions and fix manually.")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 yaml_validator_autofix.py <yaml-file>")
        sys.exit(1)
    exit_code = main(sys.argv[1])
    sys.exit(exit_code)
