# peek
## Overview
peek is a python tool to search directories or specific files for strings that are defined in a wordlist or argument.

```
python3 /opt/github/peek/peek.py --help
usage: peek.py [-h] (-f FILE | -d DIR) (-w WORDLIST | -s STRING) [-v] [-o OUTPUT] [--case-sensitive] [--no-banner]

Search a file or directory for words from a wordlist or a string.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the file to search in
  -d DIR, --dir DIR     Path to the directory to search in recursively
  -w WORDLIST, --wordlist WORDLIST
                        Path to the wordlist file
  -s STRING, --string STRING
                        String to search for
  -v, --verbose         Verbose mode, print each check result
  -o OUTPUT, --output OUTPUT
                        Save matched results to the specified output file
  --case-sensitive      Enable case-sensitive search (default is case-insensitive)
  --no-banner           Disable banner print
```

## Examples
### Searching a single file for string matches using a wordlist and printing a snippet where the result was found.
```
python3 ./peek.py -f <file> -w <wordlist> -v
```

### Searching the current directory recursively for string matches
```
python3 ./peek.py -d . -s 'password123' 
```