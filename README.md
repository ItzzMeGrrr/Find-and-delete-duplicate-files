## Find and delete all the duplicate files in the current directory recursively keeping the first one

This is a simple script that finds all the duplicate files in the current directory recursively, keeps the first copy, and deletes the rest of them.

### Usage
```
usage: FindAndDelete_DuplicateFiles.py [-h] [-d] path

Find and delete duplicate files in a directory       

positional arguments:
  path          Directory to scan for duplicates     

optional arguments:
  -h, --help    show this help message and exit      
  -d, --delete  Delete duplicate files
```

By default it will only print the duplicates, but if you add the `--delete` flag it will delete the duplicates.