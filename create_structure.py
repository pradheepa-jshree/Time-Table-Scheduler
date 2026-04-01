import os

base_path = r'C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler'
directories = ['utils', 'data', 'agent', 'tests']

for dir_name in directories:
    dir_path = os.path.join(base_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    
    init_file = os.path.join(dir_path, '__init__.py')
    with open(init_file, 'w') as f:
        pass
    
    print(f'Created directory: {dir_name} with __init__.py')

print('\nDirectory structure created successfully!')
print('\nDirectory listing:')
for root, dirs, files in os.walk(base_path):
    level = root.replace(base_path, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    sub_indent = ' ' * 2 * (level + 1)
    for file in files:
        if file != 'create_structure.py':
            print(f'{sub_indent}{file}')
