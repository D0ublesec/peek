# peek
## Overview
Peek is a python tool to search directories or specific files for strings that are defined in a wordlist or as a single argument.

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
### Searching the target directory recursively for string matches using a wordlist and printing a snippet where the result was found.
Wordlist:
```
password1234
secret
```
Command:
```
python3 ./peek.py -d <directory> -w <wordlist> -v
```
Output:
![image](https://github.com/user-attachments/assets/11b58c36-6c56-4e00-ab79-fa3ed7e2f88b)

### Searching the target directory recursively for string matches and printing a snippet where the result was found.
Command:
```
python3 ./peek.py -d <directory> -s 'password1234' -v
```
Output:
![image](https://github.com/user-attachments/assets/91bcd6d4-7a3d-4dab-99ec-ee8dab230587)
