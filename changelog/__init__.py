#!/usr/bin/env python
"""Show changelog and available versions for a given file"""
import subprocess
import re
from sys import argv
from os import path

PATH = '/home/risca/Annex/document'

def run(command):
    """Just an interface for running shell commands"""
    runner = command
    exe = subprocess.Popen(runner, stdout=subprocess.PIPE)
    out, err = exe.communicate()
    return [out, err, exe.returncode]

def sha_name(commit, filepath):
    """Return the sha of a certain filepath at a certain commit history"""
    pointer = run(['git', 'show', '{0}:{1}'.format(commit, filepath)])
    return path.basename(pointer[0])

def sha_exists(sha):
    """Return true if the sha file exists on any reposiroty"""
    command = ['git', 'annex', 'whereis', '--key', sha]
    test = run(command)
    return not test[2]

def commit_date(commit):
    """Return the author commit date"""
    command = ['git', 'show', '-s', '--pretty=format:%aD', commit]
    test = run(command)
    return test[0]

def all_sha_name(filepath):
    """Return all commit where the filepath has been changed"""
    info = run(['git', 'log', '--format="%H"', filepath])[0]
    commits = info.strip().replace('"', '').split('\n')
    return commits

def size_from_sha_name(sha, human=False):
    """Return the size embeded into the sha name"""
    size = re.search('-s(\d*)--', sha).group(1)
    if human:
        return humansize(size)
    else:
        return size

def humansize(nbytes):
    """Return a human readable size"""
    suffixes = ['B', 'K', 'M', 'G', 'T', 'P']
    nbytes = float(nbytes)
    if nbytes == 0: return '0B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s%s' % (f, suffixes[i])

if __name__ == "__main__":
    """Usage:

    python myscript 'Path/Of/File'

    It will return all sha still available"""
    PATH = argv[1:][0]
    print PATH
    for commit in all_sha_name(PATH):
        sha = sha_name(commit, PATH)
        if sha_exists(sha):
            size = size_from_sha_name(sha, human=True)
            date = commit_date(commit)
            print 'change at {} with {}: {} [{}]'.format(date, size, sha, commit)

