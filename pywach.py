from pprint import pprint
from typing import Dict, List
import os
import sys
import time


Filename = str
MTime = float
SLEEP_TIME_SECS = 0.5


def valid_file(filename: str) -> bool:
    return os.path.isfile(filename) and filename.endswith('.py')


def valid_dir(filename: str) -> bool:
    return os.path.isdir(filename) and os.path.basename(filename) not in (
      '__pycache__',
      'venv',
    )


def traverse(root) -> List[Filename]:
    all_paths = [
       root + '/' + fp 
       for fp in os.listdir(root)
    ]

    valid_paths = [
      p for p in all_paths
      if valid_file(p)
    ]

    for fp in all_paths:
        if valid_dir(fp):
            sub_files = traverse(root=fp)
            valid_paths.extend(sub_files)

    return valid_paths
        

def all_files(root) -> Dict[Filename, MTime]:
    return dict( 
        (path, os.path.getmtime(path))
        for path in traverse(root='.')
    )


pprint(dict(enumerate(sys.argv)))

cmd = ' '.join(sys.argv[1:])

pprint(all_files(root='.'))

old_files = None

while True:
    new_files = all_files(root='.')

    if new_files != old_files:
        os.system('clear')
        os.system(cmd)
        old_files = new_files

    time.sleep(SLEEP_TIME_SECS)


