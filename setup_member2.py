#!/usr/bin/env python3
"""
Setup script to create Member 2 directory structure for Time Table Scheduler
"""

import os
from pathlib import Path

def create_structure():
    """Create the required directory structure and __init__.py files"""
    
    base_path = Path(r"C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler")
    directories = ["utils", "data", "agent", "tests"]
    
    print(f"Creating directory structure in: {base_path}")
    print("-" * 60)
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        init_file = dir_path / "__init__.py"
        
        try:
            # Create directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {dir_name}/")
            
            # Create __init__.py
            init_file.touch()
            print(f"✓ Created file: {dir_name}/__init__.py")
            
        except Exception as e:
            print(f"✗ Error creating {dir_name}: {e}")
    
    print("-" * 60)
    print("✓ Directory structure setup complete!")
    
    # Verify
    print("\nVerification:")
    for dir_name in directories:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
            init_file = dir_path / "__init__.py"
            if init_file.exists():
                print(f"  └─ __init__.py exists")
        else:
            print(f"✗ {dir_name}/ missing")

if __name__ == "__main__":
    create_structure()
