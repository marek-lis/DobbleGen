from disk_scanner import *

print("\nScanning current directory and searching for files: ")

files = scan_dir_for_files("./")
for file in files:
    print(file)

print("\nScanning current directory tree and searching for files: ")

files = scan_tree_for_files("./")
for file in files:
    print(file)
