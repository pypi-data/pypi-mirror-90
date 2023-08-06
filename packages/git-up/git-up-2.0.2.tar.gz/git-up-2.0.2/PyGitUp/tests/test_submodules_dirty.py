# System imports
import os
from os.path import join

from git import *
from PyGitUp.tests import basepath, init_master, update_file, write_file

test_name = 'submodule-dirty'
repo_path = join(basepath, test_name + os.sep)


def _read_file(path):
    with open(path) as f:
        return f.read()


def setup():
    master_path, master = init_master(test_name)

    # Prepare master repo
    master.git.checkout(b=test_name)

    # Crate test repo
    path = join(basepath, test_name)
    master.clone(path, b=test_name)
    repo = Repo(path, odbt=GitCmdObjectDB)
    # repo = Repo.init(path)
    # update_file(repo, 'Initial commit')

    os.chdir(path)
    assert repo.working_dir == path

    # Rename test repo branch
    repo.git.branch(test_name + '_renamed', m=True)

    # Add subrepo
    write_file(join(path, '.gitmodules'), '')
    repo.create_submodule('sub', 'sub', master_path)
    repo.git.add('.gitmodules', 'sub/')
    repo.git.commit(m='Added submodule')
    repo.git.submodule('init')

    # Modify file in master
    update_file(master, test_name)


def test_submodules_dirty():
    """ Run 'git up' with submodules in a dirty repo """
    repo = Repo(repo_path)
    repo_head = repo.head.commit.hexsha
    submod_head = repo.submodules[0].hexsha

    # Change file in submodule
    write_file('sub/file', 'submodule changed')

    from PyGitUp.gitup import GitUp
    gitup = GitUp(testing=True)

    # PyGitUp uses the main repo
    assert repo_head == gitup.git.repo.head.commit.hexsha

    gitup.run()

    assert len(gitup.states) == 1
    assert gitup.states[0] == 'rebasing'
