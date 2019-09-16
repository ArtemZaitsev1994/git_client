import os
import json
import subprocess
from typing import Dict

users = [
    {"hostname": "VM1", "user": 'user1'},
    {"hostname": "VM1", "user": 'user2'},
    {"hostname": "VM2", "user": 'user3'},
]

def check_auth(username: str) -> str:
    # подразумевается, что ключ зашифрован rsa алгоритмом
    if os.path.isfile(f'/home/{username}/.ssh/id_rsa.pub'):
        auth_type = 'ssh'
    else:
        auth_type = 'password'
    return auth_type

def check_branch(username: str) -> Dict:
    result = {
        'vcs_type': None,
        'branch': None,
        'commit_text': None,
        'commit_hash': None,
    }
    if os.path.isdir(f'/home/{username}/bw/.git'):
        os.chdir(f'/home/{username}/bw')
        branches = subprocess.Popen('sudo git branch -v'.split(), stdout=subprocess.PIPE)
        branches = branches.communicate()[0].decode("utf-8").split('\n')
        for b in branches:
            if b.startswith('* '):
                data = b[2:].split(' ')
                result.update({
                    'vcs_type': 'git',
                    'branch': data[0],
                    'commit_text': data[-1],
                    'commit_hash': data[-2]
                })
                break
        return result
    elif os.path.isdir(f'/home/{username}/bw/svn'):
        # здесь сам доделаешь
        command = "svn info | grep '^URL:' | egrep -o '(tags|branches)/[^/]+|trunk' | egrep -o '[^/]+$'"
        branchf = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        branch = branchfanchf.communicate()[0]
        vcs_type = "svn"
    else:
        return result


if __name__ == '__main__':
    result = {}
    for item in users:
        vcs = check_branch(item['user'])
        vcs['auth_type'] = check_auth(item['user'])
        result[item['user']] = vcs

    result = json.dumps(result)
    print(result)









