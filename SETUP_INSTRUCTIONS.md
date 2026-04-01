DIRECTORY STRUCTURE SETUP GUIDE
================================

Due to environment constraints, here are two methods to create the required structure:

METHOD 1: Using Command Prompt (Recommended)
=============================================

1. Open Command Prompt (cmd.exe)
2. Navigate to your project:
   cd "C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler"

3. Run these commands:
   mkdir utils
   mkdir data
   mkdir agent
   mkdir tests
   
   type nul > utils\__init__.py
   type nul > data\__init__.py
   type nul > agent\__init__.py
   type nul > tests\__init__.py

4. Verify the structure:
   tree /F
   or
   dir /B /AD
   for /d %D in (utils data agent tests) do dir %D


METHOD 2: Using PowerShell (Legacy)
====================================

1. Open PowerShell (or PowerShell ISE)
2. Navigate to your project:
   cd "C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler"

3. Run this command:
   $dirs = @('utils','data','agent','tests'); foreach($d in $dirs) { mkdir $d; "" | Out-File "$d\__init__.py" }

4. Verify:
   Get-ChildItem -Recurse -Filter "__init__.py"


METHOD 3: Using Python
=====================

1. Open Command Prompt or PowerShell
2. Run:
   python "C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler\create_structure.py"

3. Or run this one-liner:
   python -c "import os; os.chdir(r'C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler'); [os.makedirs(d, exist_ok=True) or open(os.path.join(d, '__init__.py'), 'w').close() for d in ['utils','data','agent','tests']]"


Expected Final Structure
========================

Time-Table-Scheduler/
├── .git/
├── README.md
├── create_structure.py
├── setup.bat (created)
├── setup.vbs (created)
├── utils/
│   └── __init__.py
├── data/
│   └── __init__.py
├── agent/
│   └── __init__.py
└── tests/
    └── __init__.py
