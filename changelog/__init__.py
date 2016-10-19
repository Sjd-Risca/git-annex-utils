#!/usr/bin/env python
"""Show changelog and available versions for a given file"""
import subprocess
from sys import argv
from os import path

PATH = argv[1:][0]

def run(command):
    """Interface for running shell commands"""
    runner = command
    exe = subprocess.Popen(runner, stdout=subprocess.PIPE)
    out, err = exe.communicate()
    return [out, err, exe.returncode]

COMMITS = run(['git', 'log', '--format="%H"', PATH])[0].strip().replace('"', \
                '').split('\n')
#print COMMITS

def shaname(commit, filepath):
    """Return the file's sha at a certain commit"""
    pointer = run(['git', 'show', '{0}:{1}'.format(commit, filepath)])[0]
    return path.basename(pointer)

def sha_exists(sha):
    """Return true if the file exists"""
    command = ['git', 'annex', 'whereis', '--key', sha]
    test = run(command)
    return test[2]

def allshaname(filepath):
    """Return all file's sha associated to a path"""
    info = run(['git', 'log', '--format="%H"', PATH])[0]
    commits = info.strip().replace('"', '').split('\n')
    for commit in commits:
        print shaname(commit, filepath)

