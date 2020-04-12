
# -*- coding:utf-8 -*-
import paramiko, os, sys, time

# configuration
ip = "192.168.1.240"        # Target IP
port = 22                   # Target Port
user = 'root'               # account's username (Target System)
password = "fa"             # account's password (Target System)

remote_paths = ['/root/dmhc_app/oni/*.oni', '/root/dmhc_app/video/*.bin']
local_path = os.path.abspath('../download')


#display progress
def progress_bar(transferred, toBeTransferred, suffix=''):
    print ("\rFinished " + str(round(100 * transferred / float(toBeTransferred))) + "%", end="")

#download file
def ssh_scp_get(ip, port, user, password, remote_path, local_path):
    while True:
        ssh = paramiko.SSHClient()
        try:
            #connect to target
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, 'root', password)
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            for remote_path in remote_paths:
                # Check whether any file can be downloaded
                stdin, stdout, stderr = ssh.exec_command('find ' + remote_path + ' -mmin +1 -exec basename {} \;')
                stdout, stderr = stdout.read().decode(), stderr.read().decode() 

                remote_files = list(filter(None, stdout.split('\n')))
                for file in remote_files:
                    # Download File
                    local_file = os.path.join(local_path, file)
                    remote_file = os.path.join(os.path.dirname(remote_path), file)

                    sftp.get(remote_file, local_file, callback=progress_bar)

                    # Remove Downloaded File
                    ssh.exec_command('rm -r "' + remote_file + '"')
        except Exception as e:
            print("Error Happend:" +str(e))
        ssh.close()
        time.sleep(10)

ssh_scp_get(ip, port, user, password, remote_path, local_path)
