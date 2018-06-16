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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def print_file(file_type,color_code):
    for key in file_type:
        print '{0} {1:<5d} |  {2} {3}'.format(color_code,key, file_type[key] , bcolors.ENDC)



def status():
    try:

        if GitObject.staged_files:
            print '{0}[+] Staged Files i.e Files Going on Next Commit {1} \n\n'.format(bcolors.OKGREEN, bcolors.ENDC)
            print_file(GitObject.staged_files, bcolors.OKGREEN)
        if GitObject.unstaged_files:
            print '\n\n{0}[-] Unstaged Files i.e Files Changed but not going on Next Commit {1} \n\n'.format(bcolors.WARNING, bcolors.ENDC)
            print_file(GitObject.unstaged_files, bcolors.WARNING)
        if GitObject.untracked_files:
            print '\n\n{0}[?] Files Not Being Tracked by GIT {1} \n\n'.format(bcolors.FAIL, bcolors.ENDC)
            print_file(GitObject.untracked_files, bcolors.FAIL)
        if GitObject.conflicted_files:
            print '\n\n{0}[$] Conficted Files Fix Before pushing or pulling code{1} \n\n'.format(bcolors.HEADER,bcolors.ENDC)
            print_file(GitObject.conflicted_files, bcolors.HEADER)

        menu()


    except subprocess.CalledProcessError:
        print '{0}[-] Some Error Occured Please Retry! {1}'.format(bcolors.FAIL, bcolors.ENDC)
        menu()


def pull_code():
    print '{0} Current Branch is: {1}{2} {3}'.format(bcolors.OKBLUE, bcolors.OKGREEN, GitObject.branch, bcolors.OKBLUE)
    branch_change = raw_input('    Do you wish to change branch ? (y/n) {0}'.format(bcolors.ENDC))
    if branch_change is 'y' or 'Y':
        # Change Branch Code
        pass
    print '{0}[?] Select Remote:'.format(bcolors.OKBLUE)
    for remote in GitObject.remote.keys():
        print remote + ' ---> ' + GitObject.remote[remote]
    remote = raw_input('Press Q to cancel Push \nChoice : ')
    try:
        if remote == 'q' or remote == 'Q':
            raise RuntimeError
        if not GitObject.remote.has_key(remote):
            raise AssertionError

        print '{0}{1} Pulling Branch {2} from {3}{4}'.format(bcolors.ENDC, bcolors.OKGREEN, GitObject.branch,remote,bcolors.ENDC )
        subprocess.check_call(['git','pull', remote, GitObject.branch])

    except AssertionError:
        print '{0}[-] Please Select a valid remote {1}'.format(bcolors.FAIL, bcolors.ENDC)
        pull_code()

    except RuntimeError:
        print '{0}[*] Pushing Cancelled by User {1}'.format(bcolors.FAIL, bcolors.ENDC)
        menu()

def push_code():
    print '{0} Current Branch is: {1}{2} {3}'.format(bcolors.OKBLUE, bcolors.OKGREEN, GitObject.branch, bcolors.OKBLUE)
    branch_change = raw_input('    Do you wish to change branch ? (y/n) {0}'.format(bcolors.ENDC))
    if branch_change is 'y' or 'Y':
        # Change Branch Code
        pass
    print '{0}[?] Select Remote:'.format(bcolors.OKBLUE)
    for remote in GitObject.remote.keys():
        print remote + ' ---> ' + GitObject.remote[remote]
    remote = raw_input('Press Q to cancel Push \nChoice : ')
    try:
        if remote == 'q' or remote == 'Q':
            raise RuntimeError
        if not GitObject.remote.has_key(remote):
            raise AssertionError

        print '{0}{1} Pushing Branch {2} to {3}{4}'.format(bcolors.ENDC, bcolors.OKGREEN, GitObject.branch,remote,bcolors.ENDC )
        subprocess.check_call(['git','push', remote, GitObject.branch])

    except AssertionError:
        print '{0}[-] Please Select a valid remote {1}'.format(bcolors.FAIL, bcolors.ENDC)
        push_code()

    except RuntimeError:
        print '{0}[*] Pushing Cancelled by User {1}'.format(bcolors.FAIL, bcolors.ENDC)
        menu()



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
    conflicted_files = subprocess.Popen(['git', 'diff', '--name-only', '--diff-filter=U'], stdout=subprocess.PIPE).communicate()[0]
    for file in conflicted_files:
        file_index +=1
        GitObject.conflicted_files[file_index] = file
    return file_index



def populate_gitobject():
    try:
        branches = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE).communicate()[0].split('\n')
        for branch in branches:
            if branch.startswith('*'):
                GitObject.branch = branch.replace('*','').strip()

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
[*] Options :

[1] Pull Code                                                       [5] Commit with Message
[2] Status of Files                                                 [6] Push Code
[3] Add Files To Stage                                              [7] Manage Branches
[4] Remove Files From Stage                                         [8] Other Miscellaneous Operations


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

        elif choice == 6:
            push_code()

        elif choice == 8:
            #Other Options
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
