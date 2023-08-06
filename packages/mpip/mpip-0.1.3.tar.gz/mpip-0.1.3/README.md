`mpip` ("managed pip") is a thin wrapper around pip that helps you manage your `requirements.txt` file.

### Installation
```bash
pip install mpip
```

### Basic Usage
```bash
mpip install django # adds "django" to your requirements file
mpip install django==3.1.5 # adds "django==3.1.5" to your requirements file
mpip uninstall django # removes any version of django from your requirements file 
```

For more detailed usage information, see `mpip --help`. 

The CLI is built using [`python-fire`](https://github.com/google/python-fire), so for more details about the specific mechanics of argument parsing, that would be the first place to look. Generally speaking, it will try to parse arguments as python objects, e.g.
`--quiet True`

### Features
* Creates `requirements.txt` if one is not detected
* Handles pip versioning semantics such as `<`, `>`, `>=`, `==`
* Deletes `requirements.txt` if all requirements have been uninstalled