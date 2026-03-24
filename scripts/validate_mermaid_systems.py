import os
import re
import sys
import yaml

def load_systems(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    return {sys['id']: sys for sys in data.get('systems', [])}

def extract_mermaid_blocks(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if file_path.endswith('.mmd'):
        return [content]

    # Find all mermaid blocks in markdown
    pattern = r'```mermaid\n(.*?)```'
    return re.findall(pattern, content, re.DOTALL)

def validate_c4_diagram(mermaid_code, valid_system_ids, file_path):
    lines = mermaid_code.strip().split('\n')
    is_c4 = False
    for line in lines:
        if line.strip().startswith('C4Container') or line.strip().startswith('C4Context') or line.strip().startswith('C4Component'):
            is_c4 = True
            break
            
    if not is_c4:
        # We only validate C4 diagrams
        return []

    errors = []
    current_system_boundary = None

    for i, line in enumerate(lines):
        line = line.strip()
        # Check for system boundary
        boundary_match = re.match(r'^System_Boundary\s*\(\s*([a-zA-Z0-9_-]+)\s*,', line)
        if boundary_match:
            sys_id = boundary_match.group(1)
            if sys_id not in valid_system_ids:
                errors.append(f"Line {i+1}: Unknown system boundary '{sys_id}'. Must be defined in software_systems.yaml.")
            current_system_boundary = sys_id
            continue
            
        if line.startswith('}'):
            current_system_boundary = None
            continue

        # Check for container declarations
        container_match = re.match(r'^(?:Container|ContainerDb|ContainerQueue|Container_Ext)\s*\(', line)
        if container_match:
            if not current_system_boundary:
                errors.append(f"Line {i+1}: Container created outside of a System_Boundary. All containers must belong to a correct software system.")
            elif current_system_boundary not in valid_system_ids:
                errors.append(f"Line {i+1}: Container created in an invalid System_Boundary '{current_system_boundary}'.")

    return errors

def main():
    if not os.path.exists('software_systems.yaml'):
        print("Error: software_systems.yaml not found.")
        sys.exit(1)

    systems = load_systems('software_systems.yaml')
    valid_ids = set(systems.keys())

    adr_dir = 'docs/adr'
    if not os.path.exists(adr_dir):
        print("No docs/adr directory found.")
        sys.exit(0)

    has_errors = False
    
    for root, _, files in os.walk(adr_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.mmd'):
                file_path = os.path.join(root, file)
                blocks = extract_mermaid_blocks(file_path)
                for block_idx, block in enumerate(blocks):
                    errors = validate_c4_diagram(block, valid_ids, file_path)
                    if errors:
                        print(f"Validation failed in {file_path} (diagram {block_idx + 1}):")
                        for err in errors:
                            print(f"  - {err}")
                        has_errors = True

    if has_errors:
        print("\nADR Validation Failed!")
        sys.exit(1)
    else:
        print("\nADR Validation Passed!")
        sys.exit(0)

if __name__ == '__main__':
    main()
