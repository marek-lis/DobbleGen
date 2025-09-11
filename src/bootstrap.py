
import sys
import os

# Automatically add the main folder to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
print(project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
