import datetime
import os
import hashlib
import sys
from colorama import Fore
import argparse


parser = argparse.ArgumentParser(
    description='Find and delete duplicate files in a directory')
parser.add_argument('path', metavar="path",
                    help='Directory to scan for duplicates')
parser.add_argument(
    '-d', '--delete', help='Delete duplicate files', action='store_true')


def get_files_from_path(path):
    '''Iterate through all files in a directory and return a list of file paths'''
    print(
        f"{Fore.GREEN}[+]{Fore.RESET} Scanning {path} for files {Fore.RESET}")
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


def get_hash(filename):
    '''Calculate the hash of a file'''
    hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash.update(chunk)
    return hash.hexdigest()


def find_duplicate_files_with_hash(path):
    '''Find duplicate files in a directory and return a dictionary of hashes and file paths'''
    files = get_files_from_path(path)
    hashes = {}
    dups = 0
    print(
        f"{Fore.GREEN}[+]{Fore.RESET} Calculating hashes... {Fore.RESET}")
    for filename in files:
        hash = get_hash(filename)
        if hash in hashes:
            hashes[hash].append(filename)
            dups += 1
        else:
            hashes[hash] = [filename]
    return hashes, dups


def print_duplicate_files(hashes, dupes):
    '''Print duplicate files in a directory'''
    print(f"{Fore.GREEN}[+]{Fore.RESET} Found {dupes} duplicate files")
    for hash, filenames in hashes.items():
        if len(filenames) > 1:
            print(f"{Fore.RED}{hash}{Fore.RESET}")
            for filename in filenames:
                print(f"{Fore.YELLOW}"+'\t%s' % filename, f"{Fore.RESET}")


def delete_duplicate_files(hashes, dupes):
    '''Delete duplicate files keeping one copy'''
    print(f"{Fore.GREEN}[+]{Fore.RESET} Deleting duplicate files")
    with open('deleted_files.txt', 'a') as f:
        f.write(
            f"-------------------{datetime.datetime.now()}-------------------\n")
    with open('kept_files.txt', 'a') as f:
        f.write(
            f"-------------------{datetime.datetime.now()}-------------------\n")
    for hash, filenames in hashes.items():
        if len(filenames) > 1:
            for fileNo, filename in enumerate(filenames):
                if not fileNo == 0:
                    os.remove(filename)
                    with open('deleted_files.txt', 'a') as f:  # log deleted files
                        f.write(f"{filename}\n")
                else:
                    with open("kept_files.txt", "a") as f:  # log kept files
                        f.write(filename+"\n")
    print(f"{Fore.GREEN}[+]{Fore.RESET} {dupes} Duplicate files deleted")


if __name__ == '__main__':
    try:
        path = parser.parse_args().path
        delete = parser.parse_args().delete
        hashes, dupes = find_duplicate_files_with_hash(path)
        print_duplicate_files(hashes, dupes)
        if delete:
            delete_duplicate_files(hashes, dupes)
    except Exception as e:
        print(f"{Fore.RED}[-]{Fore.RESET} {e}")
        sys.exit(1)
