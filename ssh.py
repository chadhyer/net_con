import paramiko
import json

def check_interfaces(host:str, user:str, rsa_key_file:str) -> list:
    """Returns a list of dictionaries describing the status of all networking 
       inter faces for device

    Parameters
    ----------
    host (str): Hostname for device
    user (str): ssh user for device
    rsa_key_file (str): RSA Key file to use for ssh connection

    Returns list of dictionaries
    """

    ssh = paramiko.SSHClient()

    key = paramiko.RSAKey.from_private_key_file(rsa_key_file)

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    ssh.connect(hostname=host, username=user, pkey=key, timeout=4)

    ssh_command = 'ip -j link'
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(ssh_command)

    data = json.loads(ssh_stdout.read())
  
    return data
