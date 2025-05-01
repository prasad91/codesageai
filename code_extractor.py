import re

def extract_java_methods(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    methods = []
    in_method = False
    brace_count = 0
    method_lines = []

    for line in lines:
        stripped = line.strip()

        # Start of method (heuristic based on access + return type + method name)
        if re.match(r'(public|private|protected|static|final|abstract|synchronized|default|native|strictfp)\s+[\w\<\>\[\]]+\s+\w+\s*\(.*\)\s*\{?', stripped):
            in_method = True
            brace_count = line.count('{') - line.count('}')
            method_lines = [line]
            continue

        if in_method:
            method_lines.append(line)
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0:
                methods.append(''.join(method_lines).strip())
                in_method = False
                method_lines = []

    return methods

