#!/usr/bin/env python

import subprocess
import os
import sys


class GitObject:
    remote = {}
    branch = 'master'
    staged_files = {}
    unstaged_files = {}
    untracked_files = {}
    conflicted_files = {}
    total_files = 0

    @staticmethod
    def empty():
        GitObject.remote = {}
        GitObject.branch = 'master'
        GitObject.staged_files = {}
        GitObject.unstaged_files = {}
        GitObject.untracked_files = {}
        GitObject.conflicted_files = {}
        GitObject.total_files = 0


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_file(file_type, color_code):
    for key in file_type:
        print'{0} {1:<5d} |  {2} {3}'.format(color_code, key, file_type[key], bcolors.ENDC)


def status():
    populate_gitobject()
    try:

        show_staged_files()
        show_unstaged_files()
        show_untracked_files()
        show_confliced_files()

        print '\n\n'
    except subprocess.CalledProcessError:
        print '{0}[-] Some Error Occured Please Retry! {1}'.format(bcolors.FAIL, bcolors.ENDC)


def show_confliced_files():
    if GitObject.conflicted_files:
        print '\n\n{0}[$] Conflicted Files Fix Before pushing or pulling code{1} \n\n'.format(bcolors.HEADER,
                                                                                              bcolors.ENDC)
        print_file(GitObject.conflicted_files, bcolors.HEADER)


def show_untracked_files():
    if GitObject.untracked_files:
        print '\n\n{0}[?] Files Not Being Tracked by GIT {1} \n\n'.format(bcolors.BOLD, bcolors.ENDC)
        print_file(GitObject.untracked_files, bcolors.BOLD)


def show_unstaged_files():
    if GitObject.unstaged_files:
        print '\n\n{0}[-] Unstaged Files i.e Files Changed but not going on Next Commit {1} \n\n'.format(bcolors.FAIL,
                                                                                                         bcolors.ENDC)
        print_file(GitObject.unstaged_files, bcolors.FAIL)


def show_staged_files():
    if GitObject.staged_files:
        print '\n\n{0}[+] Staged Files i.e Files Going on Next Commit {1} \n\n'.format(bcolors.WARNING, bcolors.ENDC)
        print_file(GitObject.staged_files, bcolors.WARNING)


def pull_code():
    print '{0} Current Branch is: {1}{2} {3}'.format(bcolors.OKBLUE, bcolors.OKGREEN, GitObject.branch, bcolors.OKBLUE)
    branch_change = raw_input(
        'Do you wish to change branch ? (y/n) {0}'.format(bcolors.ENDC))
    if branch_change is 'y' or branch_change is 'Y':
        change_branch_from_branches()

    print '{0}[?] Select Remote from available list of Remotes::'.format(bcolors.OKBLUE)
    for remote in GitObject.remote.keys():
        print 'Remote Name: ' + bcolors.HEADER + remote + bcolors.OKBLUE + ' points to url : ' + GitObject.remote[
            remote]
    remote = raw_input(
        '[*]Press Q to cancel pull \nChoice of Remote (origin , upstream) : {0}'.format(bcolors.ENDC))
    try:
        if remote == 'q' or remote == 'Q':
            raise RuntimeError
        if not GitObject.remote.has_key(remote):
            raise AssertionError

        print '{0}{1} Pulling Branch {2} from {3}{4}'.format(bcolors.ENDC, bcolors.OKGREEN, GitObject.branch, remote,
                                                             bcolors.ENDC)
        subprocess.check_call(['git', 'pull', remote, GitObject.branch])
        print '{0}[+] Pull Successful {1}'.format(bcolors.OKGREEN, bcolors.ENDC)

    except AssertionError:
        print '{0}[-] Please Select a valid remote {1}'.format(bcolors.FAIL, bcolors.ENDC)
        pull_code()

    except RuntimeError:
        print '{0}[*] Pushing Cancelled by User {1}'.format(bcolors.FAIL, bcolors.ENDC)


def push_code():
    print '{0} Current Branch is: {1}{2} {3}'.format(bcolors.OKBLUE, bcolors.OKGREEN, GitObject.branch, bcolors.OKBLUE)
    branch_change = raw_input(
        'Do you wish to change branch ? (y/n) {0}'.format(bcolors.ENDC))
    if branch_change is 'y' or branch_change is 'Y':
        change_branch_from_branches()

    print '{0}[?] Select Remote From List of Remotes:'.format(bcolors.OKBLUE)
    for remote in GitObject.remote.keys():
        print remote + ' ---> ' + GitObject.remote[remote]
    remote = raw_input(
        '[*]Press Q to cancel Push \nChoice (origin, upstream) : {0}'.format(bcolors.ENDC))
    try:
        if remote == 'q' or remote == 'Q':
            raise RuntimeError
        if not GitObject.remote.has_key(remote):
            raise AssertionError

        print '{0}{1} Pushing Branch {2} to {3}{4}'.format(bcolors.ENDC, bcolors.OKGREEN, GitObject.branch, remote,
                                                           bcolors.ENDC)
        subprocess.check_call(['git', 'push', remote, GitObject.branch])
        print '{0}[+] Push Successful {1}'.format(bcolors.OKGREEN, bcolors.ENDC)

    except AssertionError:
        print '{0}[-] Please Select a valid remote {1}'.format(bcolors.FAIL, bcolors.ENDC)
        push_code()

    except RuntimeError:
        print '{0}[*] Pushing Cancelled by User {1}'.format(bcolors.FAIL, bcolors.ENDC)


def populate_staged_files(file_index, status):
    for file in status:
        if file:
            if not file[0] == ' ' and not file[0] == '?':
                if 'M' == file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Modifed : ' + file[3:]
                elif 'A' == file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Added : ' + file[3:]
                elif 'R' == file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Renamed : ' + file[3:]
                elif 'D' == file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Deleted : ' + file[3:]
                elif 'C' == file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Copied : ' + file[3:]
                elif '?' != file[0]:
                    file_index += 1
                    GitObject.staged_files[file_index] = 'Unkown Thing But Staged : ' + file
    return file_index


def populate_unstaged_files(file_index, status):
    for file in status:
        if file:
            if file[1] and file[0] == ' ' and not file[0] == '?':
                if 'M' == file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Modifed : ' + file[3:]
                elif 'A' == file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Added : ' + file[3:]
                elif 'R' == file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Renamed : ' + file[3:]
                elif 'D' == file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Deleted : ' + file[3:]
                elif 'C' == file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Copied : ' + file[3:]
                elif '?' != file[1]:
                    file_index += 1
                    GitObject.unstaged_files[file_index] = 'Unkown Thing But Not Staged : ' + file
    return file_index


def populate_untracked_files(file_index, status):
    for file in status:
        if file:
            if file[0] == '?':
                file_index += 1
                GitObject.untracked_files[file_index] = 'Untracked File : ' + file[3:]
    return file_index


def populate_merge_conflicts(file_index):
    conflicted_files = \
        subprocess.Popen(['git', 'diff', '--name-only', '--diff-filter=U'],
                         stdout=subprocess.PIPE).communicate()[0]
    for file in conflicted_files:
        file_index += 1
        GitObject.conflicted_files[file_index] = file
    return file_index


def populate_gitobject():
    GitObject.empty()
    try:
        GitObject.branch = populate_current_branch()
        populate_remotes()
        status_porcelain = subprocess.Popen(
            ['git', 'status', '--porcelain'], stdout=subprocess.PIPE).communicate()[0]
        status_porcelain = status_porcelain.split('\n')
        file_index = 0
        file_index = populate_staged_files(file_index, status_porcelain)
        file_index = populate_unstaged_files(file_index, status_porcelain)
        file_index = populate_untracked_files(file_index, status_porcelain)
        file_index = populate_merge_conflicts(file_index)
        GitObject.total_files = file_index

    except subprocess.CalledProcessError:
        print '{0}[-] Some Error Occured Please Retry! {1}'.format(bcolors.FAIL, bcolors.ENDC)


def populate_remotes():
    remotes = subprocess.Popen(
        ['git', 'remote', '-v'], stdout=subprocess.PIPE).communicate()[0]
    for remote in remotes.split('\n'):
        if remote:
            stream_name = remote.split()[0]
            stream_url = remote.split()[1]
            if not GitObject.remote.has_key(stream_name):
                GitObject.remote[stream_name] = stream_url


def populate_current_branch():
    current_branch = ''
    branches = subprocess.Popen(
        ['git', 'branch'], stdout=subprocess.PIPE).communicate()[0].split('\n')
    for branch in branches:
        if branch.startswith('*'):
            current_branch = branch.replace('*', '').strip()
    return current_branch


def add_files_to_stage():
    status()
    try:
        print '{0}[*] Press Q to Back Menu {1}'.format(bcolors.WARNING, bcolors.ENDC)
        file_id = input('{0}[?] Enter the ID of the file to Stage: {1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))
        assert file_id
        file_key = ''
        if GitObject.staged_files.has_key(file_id):
            file_key = GitObject.staged_files[file_id]
        elif GitObject.unstaged_files.has_key(file_id):
            file_key = GitObject.unstaged_files[file_id]
        elif GitObject.untracked_files.has_key(file_id):
            file_key = GitObject.untracked_files[file_id]

        elif GitObject.conflicted_files.has_key(file_id):
            raise RuntimeError
        else:
            raise AssertionError

        file_name = file_key.split(':')[1].strip()
        print '{0}[+] Adding File : {1} to stage {2}'.format(bcolors.HEADER, file_name, bcolors.ENDC)
        subprocess.check_call(['git', 'add', file_name])

    except AssertionError:
        print '{0}[-] Invalid File ID Detected {1}'.format(bcolors.FAIL, bcolors.ENDC)

    except RuntimeError:
        print '{0}[-] File is Conflicted Fix merges before adding it to Stage{1}'.format(bcolors.FAIL, bcolors.ENDC)

    except subprocess.CalledProcessError:
        print '{0}[-] Fatal Error ! Please Retry'.format(bcolors.FAIL, bcolors.ENDC)

    except NameError:
        print '{0}[-] Back To Main Menu'.format(bcolors.FAIL, bcolors.ENDC)


def remove_files_from_stage():
    status()
    try:
        print '{0}[*] Press Q to Back Menu {1}'.format(bcolors.WARNING, bcolors.ENDC)
        file_id = input(
            '{0}[?] Enter ID to unstage files, changes will not be committed then :{1}'.format(bcolors.OKBLUE,
                                                                                               bcolors.ENDC))
        assert file_id
        file_key = ''
        if GitObject.staged_files.has_key(file_id):
            file_key = GitObject.staged_files[file_id]
        else:
            raise AssertionError

        file_name = file_key.split(':')[1].strip()
        print '{0}[+] Removing File : {1} from stage {2}'.format(bcolors.HEADER, file_name, bcolors.ENDC)
        subprocess.check_call(['git', 'reset', file_name])

    except AssertionError:
        print '{0}[-] Invalid File ID Detected {1}'.format(bcolors.FAIL, bcolors.ENDC)


def commit_code():
    try:
        show_staged_files()
        print '{0}[*] Enter Q to abort commit{1}'.format(bcolors.WARNING, bcolors.ENDC)
        commit_message = raw_input(
            '{0}[=] Commit Message : {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
        assert commit_message
        if commit_message is 'Q' or commit_message is 'q':
            raise RuntimeError

        subprocess.check_call(['git', 'commit', '-m', commit_message])

        print '{0}[+] Commit Successful {1}'.format(bcolors.OKGREEN, bcolors.ENDC)

    except AssertionError:
        print '{0}[-] Commit Message Cannot be empty {1}'.format(bcolors.FAIL, bcolors.ENDC)

    except RuntimeError:
        print '{0}[-] Going back to menu {1}'.format(bcolors.FAIL, bcolors.ENDC)


def remote_branches_for_remote(remote_name):
    branches = subprocess.Popen(['git', 'ls-remote', '--heads', remote_name],
                                stdout=subprocess.PIPE).communicate()[0].split('\n')
    branch_with_id = {}
    id = 0
    for branch in branches:
        if branch:
            id += 1
            branch_with_id[id] = branch

    return branch_with_id


def track_remote_branches():
    try:
        print '{0}[?] Which Remote You want to Track To ? '.format(bcolors.OKGREEN)
        for remote in GitObject.remote:
            print '{0} {1} {2}'.format(bcolors.HEADER, remote, bcolors.ENDC)

        remote_name = raw_input(
            '{0}[*] Enter Remote Name: {1}'.format(bcolors.HEADER, bcolors.ENDC))
        if not GitObject.remote.has_key(remote_name):
            raise AssertionError

        branches = remote_branches_for_remote(remote_name)

        for id in branches.keys():
            print '{0}{1:<3d} | {2} {3}'.format(bcolors.HEADER, id, branches[id], bcolors.ENDC)

        branch_id = input('{0}[?] Enter the Remote Branch ID to track{1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))
        assert branch_id
        remote_branch_name = branches[branch_id].split('/')[2]
        local_branch_name = raw_input(
            '{0}[?] Enter The Local Branch Name{1}'.format(bcolors.OKBLUE, bcolors.ENDC))

        print '{0}[*] Tracking local branch {1} to remote branch {2}{3} of remote {4}'.format(bcolors.BOLD, local_branch_name, remote_branch_name, remote_name, bcolors.ENDC)
        remote_link = '{0}/{1}'.format(remote_name, remote_branch_name)
        subprocess.check_call(
            ['git', 'branch', local_branch_name, remote_link])
        print '{0}[*] Branch {1} Successfully tracked to remote {2} {3}'.format(bcolors.OKGREEN, local_branch_name, remote_link, bcolors.ENDC)

    except AssertionError:
        print '{0}[-] Invalid Remote Back to Menu {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except SyntaxError:
        print '{0}[-] Invalid Value For Remoted Branch ID {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except:
        print '{0}[-] Fatal Error | Please Contact Developer {1}'.format(bcolors.FAIL, bcolors.ENDC)


def show_all_branches_r():
    print '{0}[*] List of All Branches including local and remote: {1}'.format(bcolors.HEADER, bcolors.ENDC)
    subprocess.check_call(['git', 'branch', '-a'])


def delete_a_branch():
    try:
        print '{0}[+] List of Local Branch {1}'.format(bcolors.OKBLUE, bcolors.ENDC)
        branches_with_id = get_all_local_branch_with_ids()
        print '{0}[?] Enter the ID of branch to delete {1}'.format(bcolors.OKBLUE, bcolors.ENDC)
        branch_id = input(
            '{0}[*] Branch Id:{1}'.format(bcolors.OKBLUE, bcolors.ENDC))
        if not branches_with_id.has_key(branch_id):
            raise AssertionError
        branch_name = branches_with_id[branch_id]
        choice = raw_input('{0}[*] Are you sure you want to delete branch {1} : (y/n) {2} '.format(
            bcolors.WARNING, branch_name, bcolors.ENDC))
        if choice is 'N' or choice is 'n':
            raise RuntimeError

        subprocess.check_call(['git', 'branch', '-d', branch_name])

    except AssertionError:
        print '{0}[-] Invalid Remote ID Back to Menu {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except RuntimeError:
        print '{0}[-] Cancelling Delete Back to Menu {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except subprocess.CalledProcessError:
        print '{0}[-] Fatal Error Deleting a branch, Back to Menu {1}'.format(bcolors.FAIL, bcolors.ENDC)


def get_all_local_branch_with_ids():
    branches_with_id = {}
    branches = subprocess.Popen(
        ['git', 'branch'], stdout=subprocess.PIPE).communicate()[0].split('\n')
    id = 0
    start_color = bcolors.HEADER
    for branch in branches:
        if branch:
            if branch.startswith('*'):
                branch = branch.replace('*', '').strip()
                start_color = bcolors.WARNING
            else:
                branch = branch.strip()
            id += 1
            branches_with_id[id] = branch
            print '{0} {1:<3d} | {2} {3}'.format(start_color, id, branch, bcolors.ENDC)
    return branches_with_id


def manage_branches():
    print bcolors.OKBLUE + '''
[*] Options:
[1] Change Branch                           [4] Delete A Branch
[2] Setup A branch To Track Remote Branch
[3] Show All Branches
[9] Back To Main Menu

[*] Choice:
    ''' + bcolors.ENDC
    try:
        choice = input('{0}[?] Choice : {1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))

        if choice == 1:
            change_branch_from_branches()

        elif choice == 2:
            track_remote_branches()

        elif choice == 3:
            show_all_branches_r()

        elif choice == 4:
            delete_a_branch()

        elif choice == 9:
            raise RuntimeError

        else:
            raise AssertionError

    except AssertionError:
        print '{0}[-] Invalid Branch ID {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except RuntimeError:
        pass
    except:
        print '{0}[-] Fatal Error| Maybe that was because of Invalid Input ! Please Retry {1}'.format(bcolors.FAIL,
                                                                                                      bcolors.ENDC)


def change_branch_from_branches():
    try:
        branches = list_branches()
        choice = input('{0}[?] Enter The Branch ID to switch: {1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))
        if not branches.has_key(choice):
            raise AssertionError
        branch_name = branches[choice]
        subprocess.check_call(['git', 'checkout', branch_name])
        print '{0}[+] Branch switched to {1} Successfully {2}'.format(bcolors.OKGREEN, branch_name, bcolors.ENDC)
    except AssertionError:
        print '{0}[-] Invalid Branch ID {1}'.format(bcolors.FAIL, bcolors.ENDC)


def list_branches():
    print '{0}[+] List of Available branches :{1}'.format(bcolors.HEADER, bcolors.ENDC)
    list_of_branches = subprocess.Popen(
        ['git', 'branch'], stdout=subprocess.PIPE).communicate()[0].split('\n')
    branches = {}
    initial_number = 0
    for branch in list_of_branches:
        if branch:
            start_color = ''
            if branch.startswith('*'):
                start_color = bcolors.OKGREEN
            else:
                start_color = bcolors.FAIL

            initial_number += 1
            branches[initial_number] = branch.replace("*", "").strip()
            print '{0}{1:<3d}: {2}{3}'.format(start_color, initial_number, branch, bcolors.ENDC)
    return branches


def menu_when_a_git_repo(current_dir):
    populate_gitobject()

    print bcolors.OKBLUE + '''
[*] Options :

[1] Pull Code                                                       [5] Commit with Message
[2] Status of Files                                                 [6] Push Code
[3] Add Files To Stage                                              [7] Manage Branches
[4] Remove Files From Stage                                         [8] Configure Git

Options To Be Added Soon:
[*] Remote Operations
[*] Diff's And Patches


                                                                    [9] Exit Application
            ''' + bcolors.ENDC
    try:
        choice = input('{0}[?] Choice : {1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))

        if choice == 1:
            pull_code()

        elif choice == 2:
            status()

        elif choice == 3:
            add_files_to_stage()

        elif choice == 4:
            remove_files_from_stage()

        elif choice == 5:
            commit_code()

        elif choice == 6:
            push_code()

        elif choice == 7:
            manage_branches()

        elif choice == 8:
            # Other Options
            configure_git()

        elif choice == 9:
            raise RuntimeError

    except RuntimeError:
        print '{0}[+] Exiting {1}'.format(bcolors.WARNING, bcolors.ENDC)
        sys.exit(0)


def configure_git():
    print bcolors.OKBLUE + '''
    [1] Configure Username
    [2] Configure Email
    [3] Configure Default Editor
    [*] Back To Previous Menu
            ''' + bcolors.ENDC
    choice = input('{0}[?] Choice : {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
    if choice < 4:
        change_env = input(
            '{0}[?] Want To Make Local or Global Changes: {1}[1] Local [2] Global{2}'.format(bcolors.WARNING,
                                                                                             bcolors.OKBLUE,
                                                                                             bcolors.ENDC))
        flag = '--global' if change_env == 1 else '--local'

    try:
        if choice == 1:
            username = raw_input('{0}[?] Enter Your Username: {1}'.format(
                bcolors.OKBLUE, bcolors.ENDC))
            assert username
            username = '"' + username + '"'
            subprocess.check_call(
                ['git', 'config', flag, 'user.name', username])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        elif choice == 2:
            email = raw_input('{0}[?] Enter Your Username: {1}'.format(
                bcolors.OKBLUE, bcolors.ENDC))
            assert email
            subprocess.check_call(['git', 'config', flag, 'user.email', email])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        elif choice == 3:
            editor = raw_input(
                '{0}[?] Enter Your Editor (vim , nano , emacs) :{1}'.format(bcolors.OKBLUE, bcolors.ENDC))
            assert editor
            subprocess.check_call(
                ['git', 'config', flag, 'core.editor', editor])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        else:
            pass

    except AssertionError:
        print '{0}[-] Value Cannot Be Empty {1}'.format(bcolors.FAIL, bcolors.ENDC)
    except subprocess.CalledProcessError:
        print '{0} [-] Error While Updating Configurations{1}'.format(bcolors.FAIL, bcolors.ENDC)


def menu():
    current_dir = os.getcwd()
    if not os.path.isdir('.git'):
        menu_when_not_a_git_repo(current_dir)
    else:
        menu_when_a_git_repo(current_dir)


def menu_when_not_a_git_repo(current_dir):
    print bcolors.OKBLUE + '''
[1] Clone a repository
[2] Configure SSH
[3] Initialize a Git Repository at this location
[9] Exit Application
        ''' + bcolors.ENDC
    try:
        choice = input('{0}[?] Choice : {1}'.format(
            bcolors.OKBLUE, bcolors.ENDC))
        if choice == 1:
            clone_repository(current_dir)

        elif choice == 2:
            setup_ssh()

        elif choice == 3:
            initialize_git()

        elif choice == 9:
            raise RuntimeError

    except RuntimeError:
        print '{0}[+] Exiting {1}'.format(bcolors.OKGREEN, bcolors.ENDC)
        sys.exit(0)
    except:
        print '{0}[+] Exiting {1}'.format(bcolors.OKGREEN, bcolors.ENDC)
        sys.exit(0)


def initialize_git():
    try:
        print '{0}[+] Initializing Git Repository'.format(bcolors.OKGREEN)
        subprocess.check_call(['git', 'init'])
        print '{0}'.format(bcolors.ENDC)
    except subprocess.CalledProcessError:
        print '{0}[-] Could Not Initialize Repository! Some error occurred {1}'.format(bcolors.FAIL, bcolors.ENDC)


def setup_ssh():
    try:
        if not 'mac' == os.name:
            raise OSError
        home_path = os.path.expanduser('~')
        ssh_keyname = '.ssh/id_rsa.pub'
        sshfile = os.path.join(home_path, ssh_keyname)
        if os.path.exists(sshfile):
            print '[+] SSH Key Already Exists'
        else:
            print '[+] Generating SSH Key'
            email = raw_input('Enter your email for rsa generation')
            email = '"' + email + '"'
            subprocess.check_call(
                ['ssh-keygen', '-t', 'rsa', '-C', email, '-b', '4096'])

        subprocess.check_call("cat " + sshfile + " | pbcopy", shell=True)
        print '{0}[+] SSH Key Copied {1}'.format(bcolors.OKGREEN, bcolors.ENDC)

    except OSError:
        print '{0}[-] Windows Not Supported for SSH {1}'.format(bcolors.FAIL, bcolors.ENDC)


def clone_repository(current_dir):
    repository_location = raw_input('[?] Enter Repository location : ')
    try:
        assert repository_location
        subprocess.check_call(['git', 'clone', repository_location])
        print '{0}[+] Successfully Cloned {1} to {2} {3}'.format(bcolors.OKGREEN, repository_location, current_dir,
                                                                 bcolors.ENDC)

    except AssertionError:
        print '{0}[-] Repository Name Cannot be empty{1}'.format(bcolors.FAIL, bcolors.ENDC)
    except subprocess.CalledProcessError:
        print '{0}[-] Fatal Error Could Not Clone repository{1}'.format(bcolors.FAIL, bcolors.ENDC)


def message():
    print bcolors.HEADER + """
      ________.______________   _________       __      ________
     /  _____/|   \__    ___/  /   _____/ _____/  |_   /  _____/  ____
    /   \  ___|   | |    |     \_____  \_/ __ \   __\ /   \  ___ /  _ \\
    \    \_\  \   | |    |     /        \  ___/|  |   \    \_\  (  <_> )
     \______  /___| |____|    /_______  /\___  >__|    \______  /\____/
            \/                        \/     \/               \/
        """ + bcolors.ENDC


def check_git_directory():
    current_dir = os.getcwd()
    if not os.path.isdir('.git'):
        print '{0}[-] {1} is not a valid git repository {2}'.format(bcolors.FAIL, current_dir, bcolors.ENDC)
    else:
        print '{0}[+] {1} is a valid git repository {2}'.format(bcolors.OKGREEN, current_dir, bcolors.ENDC)


if __name__ == '__main__':
    message()
    check_git_directory()
    while True:
        menu()
