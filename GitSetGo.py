import subprocess
import os
import sys


class GitObject:
    remote = {}
    branch = 'master'
    staged_files = {}
    unstaged_files = {}
    unmodified_files = {}
    conflicted_files = {}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def status():
    try:
        for file in GitObject.unstaged_files.keys():
            print str(file)  + ' ' + GitObject.unstaged_files[file]


    except subprocess.CalledProcessError:
        print '{0}[-] Some Error Occured Please Retry! {1}'.format(bcolors.FAIL, bcolors.ENDC)
        menu()


def pull_code():
    remote = raw_input('{0}[?] Select  {1}'.format(bcolors.FAIL, bcolors.ENDC))
    print '{0}[*] Pulling From'


def populate_staged_files(file_index,status):
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
            if file[1] and not file[0] == ' ' and not file[0] == '?':
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
                GitObject.conflicted_files[file_index] = 'Untracked File : ' + file[3:]
    return file_index


def populate_merge_conflicts(file_index):
    conflicted_files = subprocess.Popen(['git', 'diff', '--name-only', '--diff-filter=U'], stdout=subprocess.PIPE).communicate()[0]
    for file in conflicted_files:
        file_index +=1
        conflicted_files[file_index] = file
    return file_index



def populate_gitobject():
    try:
        branches = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE).communicate()[0]
        for branch in branches:
            if branch.startswith('*'):
                GitObject.branch = branch

        remotes = subprocess.Popen(['git', 'remote', '-v'], stdout=subprocess.PIPE).communicate()[0]
        for remote in remotes.split('\n'):
            if remote:
                stream_name = remote.split()[0]
                stream_url = remote.split()[1]
                if not GitObject.remote.has_key(stream_name):
                    GitObject.remote[stream_name] = stream_url

        status_porcelain = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE).communicate()[0]
        status_porcelain =  status_porcelain.split('\n')
        file_index = 0
        file_index = populate_staged_files(file_index,status_porcelain)
        file_index = populate_unstaged_files(file_index , status_porcelain)
        file_index = populate_untracked_files(file_index, status_porcelain)
        file_index = populate_merge_conflicts(file_index)




    except subprocess.CalledProcessError:
        print '{0}[-] Some Error Occured Please Retry! {1}'.format(bcolors.FAIL, bcolors.ENDC)


def menu_when_a_git_repo(current_dir):
    populate_gitobject()

    print  bcolors.OKBLUE + '''
[1] Pull Code
[2] Status of Files
[3] Add Files To Stage
[4] Remove Files From Stage
[5] Commit with Message
[6] Push Code
[7] Manage Branches
[8] Other Miscellaneous Operations
    [5] Remote Operations
    [6] Configure Git
[*] Exit Application
            ''' + bcolors.ENDC
    choice = input('{0}[?] Choice : {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
    try:
        if choice == 1:
            pull_code()

        if choice == 2:
            status()

        elif choice == 3:
            setup_ssh()

        elif choice == 8:
            configure_git()


        else:
            raise RuntimeError

    except RuntimeError:
        print '{0}[+] Exiting {1}'.format(bcolors.WARNING, bcolors.ENDC)
        sys.exit(0)


def configure_git():
    print  bcolors.OKBLUE + '''
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
            username = raw_input('{0}[?] Enter Your Username: {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
            assert username
            username = '"' + username + '"'
            subprocess.check_call(['git', 'config', flag, 'user.name', username])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        elif choice == 2:
            email = raw_input('{0}[?] Enter Your Username: {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
            assert email
            subprocess.check_call(['git', 'config', flag, 'user.email', email])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        elif choice == 3:
            editor = raw_input(
                '{0}[?] Enter Your Editor (vim , nano , emacs) :{1}'.format(bcolors.OKBLUE, bcolors.ENDC))
            assert editor
            subprocess.check_call(['git', 'config', flag, 'core.editor', editor])
            print '{0}[*] Success {1}'.format(bcolors.OKBLUE, bcolors.ENDC)

        else:
            raise RuntimeError

    except RuntimeError:
        menu()
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
    print  bcolors.OKBLUE + '''
[1] Clone a repository
[2] Configure SSH
[3] Initialize a Git Repository at this location
[*] Exit Application
        ''' + bcolors.ENDC
    choice = input('{0}[?] Choice : {1}'.format(bcolors.OKBLUE, bcolors.ENDC))
    try:
        if choice == 1:
            clone_repository(current_dir)

        elif choice == 2:
            setup_ssh()

        elif choice == 3:
            initialize_git()

        else:
            raise RuntimeError

    except RuntimeError:
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
            print  '[+] SSH Key Already Exists'
        else:
            print '[+] Generating SSH Key'
            email = raw_input('Enter your email for rsa generation')
            subprocess.check_call(['ssh-keygen', '-t', 'rsa', '-C', '"' + email + '"', '-b 4096'])

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
    menu()
