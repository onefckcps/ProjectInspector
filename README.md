# Project Inspector

`project_inspector` (or `pi`) is a command-line tool for inspecting the structure of a project directory. It generates a tree view of the directory and lists each file, including its content. The tool also supports excluding specified files and folders based on a custom ignore file.

## Features

- **Directory Tree Overview**: Display the structure of a project folder in a tree-like format.
- **File Listing**: List every file along with its filepath and content.
- **Ignore Functionality**: Optionally ignore certain files and directories using an ignore file.
- **Customizable Ignore File**: Specify a custom ignore file using command-line options.

## Installation

1. Clone the repository or download the `project_inspector.py` script.

2. Make the script executable:

   ```bash
   chmod +x project_inspector.py
   ```

3. Move it to a directory in your system's `PATH` for easy access:

   ```bash
   mv project_inspector.py ~/.local/bin/pi
   ```

   Ensure `~/.local/bin` is in your `PATH`. You can add the following line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):

   ```bash
   export PATH=$PATH:~/.local/bin
   ```

4. Reload your shell configuration:

   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

Now, you can use the command `pi` from anywhere in your terminal.

## Usage

### Basic Command

```bash
pi <directory>
```

- `<directory>`: The path to the project directory you want to inspect.

### Optional Arguments

- `-i`, `--ignore`: Specify the path to an ignore file. This file should contain patterns for files and folders to ignore during inspection. If not provided, the tool will look for a `.projectinspector.ignore` file in the root of the specified directory.

### Examples

1. **Inspect the Current Directory**:

   ```bash
   pi .
   ```

2. **Inspect a Specific Directory**:

   ```bash
   pi /path/to/your/project
   ```

3. **Use a Custom Ignore File**:

   ```bash
   pi /path/to/your/project -i /path/to/custom.ignore
   ```

### Ignore File Format

The ignore file follows a similar pattern to `.gitignore` files:

- Each line represents a pattern to ignore.
- Lines starting with `#` are comments and will be ignored.
- Blank lines are also ignored.

#### Example `.projectinspector.ignore`

```
# Ignore build and temporary directories
build/
tmp/
*.temp/

# Ignore cache directories
.cache/

# Ignore specific files
.env.example
backup_*.sql
```

## Output

The output of the command includes:

1. **Directory Tree Overview**: Displays the folder structure, excluding ignored files and directories.

2. **Files and Their Contents**: Lists each file along with its name, path, and content.

#### Example Output

```
Loaded ignore patterns from /path/to/your/project/.projectinspector.ignore:
  - build/
  - tmp/
  - .cache/
  - .env.example

Directory Tree for: /path/to/your/project

├── .env
├── src/
│   ├── main.py
│   └── utils.py
└── README.md


=== Files and Their Contents ===

Filename: main.py
Filepath: /path/to/your/project/src/main.py
Content:
# Content of main.py wrapped to 80 characters...

--------------------------------------------------------------------------------

Filename: utils.py
Filepath: /path/to/your/project/src/utils.py
Content:
# Content of utils.py wrapped to 80 characters...

--------------------------------------------------------------------------------
```

## Error Handling

- If the specified directory does not exist or is not a directory, an error message will be printed and the program will exit.
- If the ignore file cannot be read, the script will continue without ignoring any files.

## Troubleshooting

- **Permission Denied**: Ensure you have the correct permissions to read the specified directory and files.
- **No Output for Files**: If no files are being listed, check the ignore file to make sure it is not excluding all files.

## Contributing

Feel free to contribute to this project by submitting issues, suggesting new features, or creating pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

Thanks to the open-source community for providing tools and ideas that helped shape this project.
