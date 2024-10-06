import os
import sys
import argparse
import textwrap
import fnmatch

def load_ignore_patterns(ignore_file_path):
    """
    Loads ignore patterns from the .projectinspector.ignore file.

    Parameters:
        ignore_file_path (str): Path to the ignore file.

    Returns:
        List[str]: A list of patterns to ignore.
    """
    patterns = []
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace and ignore comments and blank lines
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    patterns.append(stripped)
    return patterns

def should_ignore(path, ignore_patterns, root):
    """
    Determines if a given path should be ignored based on the ignore patterns.

    Parameters:
        path (str): The path to check.
        ignore_patterns (List[str]): List of ignore patterns.
        root (str): The root directory being inspected.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    # Compute the relative path from the root
    rel_path = os.path.relpath(path, root).replace(os.sep, '/')
    basename = os.path.basename(path)
    is_dir = os.path.isdir(path)

    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            # Directory-specific pattern
            pattern_dir = pattern.rstrip('/')
            if is_dir:
                # Match the relative path
                if fnmatch.fnmatch(rel_path, pattern_dir) or fnmatch.fnmatch(basename, pattern_dir):
                    return True
        else:
            # File or directory pattern
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(basename, pattern):
                return True
    return False

def print_tree(startpath, ignore_patterns, root, prefix=""):
    """Recursively prints the directory tree structure, excluding ignored files and folders."""
    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        print(prefix + "└── [Permission Denied]")
        return
    entries_count = len(entries)
    for index, entry in enumerate(entries):
        path = os.path.join(startpath, entry)
        if should_ignore(path, ignore_patterns, root):
            continue  # Skip ignored files and directories
        connector = "├── " if index < entries_count - 1 else "└── "
        if os.path.isdir(path):
            print(prefix + connector + entry + "/")
            extension = "│   " if index < entries_count - 1 else "    "
            print_tree(path, ignore_patterns, root, prefix + extension)
        else:
            print(prefix + connector + entry)

def list_files_with_contents(startpath, ignore_patterns, root):
    """Lists all files with their names, paths, and contents, excluding ignored files and folders."""
    print("\n\n=== Files and Their Contents ===\n")
    for current_root, dirs, files in os.walk(startpath):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(current_root, d), ignore_patterns, root)]
        for file in files:
            filepath = os.path.join(current_root, file)
            if should_ignore(filepath, ignore_patterns, root):
                continue  # Skip ignored files
            print(f"Filename: {file}")
            print(f"Filepath: {filepath}")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Optionally, wrap the content for better readability
                wrapped_content = textwrap.fill(content, width=80)
                print("Content:")
                print(wrapped_content)
            except Exception as e:
                print(f"Content: [Could not read file: {e}]")
            print("\n" + "-"*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Project Folder Inspector with Ignore Functionality")
    parser.add_argument('directory', nargs='?', default='.', 
                        help='Path to the project directory (default: current directory)')
    args = parser.parse_args()
    startpath = os.path.abspath(args.directory)

    if not os.path.exists(startpath):
        print(f"Error: The directory '{startpath}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(startpath):
        print(f"Error: The path '{startpath}' is not a directory.")
        sys.exit(1)

    ignore_file = os.path.join(startpath, '.projectinspector.ignore')
    ignore_patterns = load_ignore_patterns(ignore_file)

    if ignore_patterns:
        print(f"Loaded ignore patterns from {ignore_file}:")
        for pattern in ignore_patterns:
            print(f"  - {pattern}")
        print("\n")

    print(f"Directory Tree for: {startpath}\n")
    print_tree(startpath, ignore_patterns, startpath)
    list_files_with_contents(startpath, ignore_patterns, startpath)

if __name__ == "__main__":
    main()
