#!/usr/bin/env python
"""Show changelog and available versions for a given file"""
import subprocess
from sys import argv
from os import path

PATH = '/home/risca/Annex/document'

def run(command):
    """Just an interface for running shell commands"""
    runner = command
    exe = subprocess.Popen(runner, stdout=subprocess.PIPE)
    out, err = exe.communicate()
    return [out, err, exe.returncode]

def shaname(_commit, filepath):
    """Return the sha of a certain filepath at a certain commit history"""
    pointer = run(['git', 'show', '{0}:{1}'.format(_commit, filepath)])
    return path.basename(pointer[0])

def sha_exists(_sha):
    """Return true if the sha file exists on any reposiroty"""
    command = ['git', 'annex', 'whereis', '--key', _sha]
    test = run(command)
    return not test[2]

def allshaname(filepath):
    """Return all commit where the filepath has been changed"""
    info = run(['git', 'log', '--format="%H"', filepath])[0]
    commits = info.strip().replace('"', '').split('\n')
    return commits



if __name__ == "__main__":
    """Usage:

    python myscript 'Path/Of/File'

    It will return all sha still available"""
    PATH = argv[1:][0]
    print PATH
    for commit in allshaname(PATH):
        sha = shaname(commit, PATH)
        if sha_exists(sha):
            print 'change at {} with {}'.format(commit, sha)

