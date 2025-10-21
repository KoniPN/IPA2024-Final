import subprocess
import os
import glob

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'backup_config.yaml']
    result = subprocess.run(command, capture_output=True, text=True)
    result_output = result.stdout
    
    if 'failed=0' in result_output and 'ok=' in result_output:
        pattern = "show_run_66070136_*.txt"
        files = glob.glob(pattern)
        if files:
            return 'ok'
        else:
            return 'Error: Ansible - File not created'
    else:
        return 'Error: Ansible'
