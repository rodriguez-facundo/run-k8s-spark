import re
import os
import sys
import json
from subprocess import Popen, PIPE

'''
    Use: 
        - python kubectl.py file.py

    Notes:
        - We copy file.py to spark-master container at DEST_FOLDER. So make sure
          the folder exists in the container.
'''
# ------------------------------------------------------------------------------
#            DEFINITIONS                                                       #
# ------------------------------------------------------------------------------
# Script path
SCRIPT = sys.argv[1]
FILE = os.path.basename(SCRIPT)

# Load config params
with open('config.json') as f:
    params = json.load(f)
# Define the namespace
NAMESPACE = params['NAMESPACE']['value']
# Folder in master spark container running in k8s (the folder must exist)
DEST_FOLDER = params['DEST_FOLDER']['value']
# Match this name when looking which pod to pick to run the script
MATCH_NAME = params['MATCH_NAME']['value']

# ------------------------------------------------------------------------------
#        AUXILIAR FUNCTIONS                                                    #
# ------------------------------------------------------------------------------
bts = lambda pipe : (pipe[0].decode(), pipe[1].decode())

def header(title, level='info'):
    color = '42' if level == 'info' else '41'
    print(f"\033[{color};3m  {title} \033[0m \n")

def kubectl(cmd, verbose=True):
    if verbose:
        header('Executing command')
        print(''.join([l + ' ' for l in cmd]))

    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    a, e = bts(p.communicate())
    
    if verbose:
        if a:
            header('Answer')
            print(a)
        if e:
            header('Error', level='error')
            print(e)

    return a, e

# -------------------------------------------------------------------------------
#              SCRIPT                                                           #
# -------------------------------------------------------------------------------

print(f"\033[36;3m Connection to k8s... \033[0m \n")

cmd1 = f"kubectl -n {NAMESPACE} get pods".split()
answer, error = kubectl(cmd1, verbose=True)
POD_NAME = [ pod.split()[0] for pod in answer.splitlines()[1:] if MATCH_NAME in pod][0]

# Copy the script provided to spark master container
cmd2 = f"kubectl cp {SCRIPT} {NAMESPACE}/{POD_NAME}:{DEST_FOLDER}".split()
answer, error = kubectl(cmd2, verbose=False)

# Run job from within the cluster
cmd3 = f"kubectl -n {NAMESPACE} exec -it {POD_NAME} -- spark-submit {os.path.join(DEST_FOLDER, FILE)}".split()
answer, error = kubectl(cmd3)

# ------------------------------------------------------------------------------ #