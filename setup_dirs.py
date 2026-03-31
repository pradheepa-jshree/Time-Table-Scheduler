#!/usr/bin/env python3
import os
import sys

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

base_path = script_dir
directories = ['utils', 'data', 'agent', 'tests']

print(f"Working directory: {base_path}")
print(f"Creating directories...\n")

for dir_name in directories:
    dir_path = os.path.join(base_path, dir_name)
    try:
        os.makedirs(dir_path, exist_ok=True)
        init_file = os.path.join(dir_path, '__init__.py')
        with open(init_file, 'w') as f:
            pass
        print(f'Created directory: {dir_name} with __init__.py')
    except Exception as e:
        print(f'Error creating {dir_name}: {e}')
        sys.exit(1)

print('\nDirectory structure created successfully!')
print('\nDirectory listing:')
for root, dirs, files in os.walk(base_path):
    level = root.replace(base_path, '').count(os.sep)
    indent = ' ' * 2 * level
    basename = os.path.basename(root) or 'Time-Table-Scheduler'
    print(f'{indent}{basename}/')
    sub_indent = ' ' * 2 * (level + 1)
    for file in sorted(files):
        if file != 'create_structure.py' and file != 'setup_dirs.py':
            print(f'{sub_indent}{file}')
