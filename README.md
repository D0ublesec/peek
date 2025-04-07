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

## Creating Wordlists
[Cook](https://github.com/glitchedgitz/cook) is a great tool to create wordlists.

If you know the small set of data to search for such as a password, you can append variations of the data into the wordlist to search with.
```
$ ~/go/bin/cook -f: wordlist.txt f -m b64e,md5,sha1,sha256,sha512 >> wordlist.txt

$ cat wordlist.txt
password1234
secret
cGFzc3dvcmQxMjM0
c2VjcmV0
bdc87b9c894da5168059e00ebffb9077
5ebe2294ecd0e0f08eab7690d2a6ee69
e6b6afbd6d76bb5d2041542d7d2e3fac5bb05593
e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4
b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3
2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b
8c7c9d16278ac60a19776f204f3109b1c2fc782ff8b671f42426a85cf72b1021887dd9e4febe420dcd215ba499ff12e230daf67afffde8bf84befe867a8822c4
bd2b1aaf7ef4f09be9f52ce2d8d599674d81aa9d6a4421696dc4d93dd0619d682ce56b4d64a9ef097761ced99e0f67265b5f76085e5b0ee7ca4696b2ad6fe2b2
```

