#find duplicate file from given directory
import os
import hashlib
import sys
from colorama import Fore


def get_files_from_path(path):
    print(f"{Fore.GREEN}[+]{Fore.RESET} Scanning {path} for files {Fore.RESET}")
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


def get_hash(filename):
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash.update(chunk)
    return hash.hexdigest()


def find_duplicate_files_with_hash(path):
    print(f"{Fore.GREEN}[+]{Fore.RESET} Checking for duplicate files in {path}")
    files = get_files_from_path(path)
    hashes = {}
    dups = 0
    for filename in files:
        hash = get_hash(filename)
        if hash in hashes:
            hashes[hash].append(filename)
            dups += 1
        else:
            hashes[hash] = [filename]
    return hashes, dups


def print_duplicate_files(hashes, dupes):
    print(f"{Fore.GREEN}[+]{Fore.RESET} Found {dupes} duplicate files")
    for hash, filenames in hashes.items():
        if len(filenames) > 1:
            print(f"{Fore.RED}{hash}{Fore.RESET}")
            for filename in filenames:
                print(f"{Fore.YELLOW}"+'\t%s' % filename,f"{Fore.RESET}")


#keep only one of copy the duplicate files
def delete_duplicate_files(hashes, dupes):
    print(f"{Fore.GREEN}[+]{Fore.RESET} Deleting duplicate files")
    for hash, filenames in hashes.items():
        if len(filenames) > 1:
            for fileNO,filename in enumerate(filenames):
                if not fileNO == 0:
                    os.remove(filename)
                else:
                    with open("duplicate_files.txt", "a") as f:
                        f.write(filename+"\n")
    print(f"{Fore.GREEN}[+]{Fore.RESET} {dupes} Duplicate files deleted")
                


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <path>' % sys.argv[0])
        sys.exit(1)
    hashes, dupes = find_duplicate_files_with_hash(sys.argv[1])    
    print_duplicate_files(hashes, dupes)
    delete_duplicate_files(hashes, dupes)
    sys.exit(0)

