
# -*- coding:utf-8 -*-
import paramiko, os, sys, time

# configuration
ip = "192.168.1.240"        # Target IP
port = 22                   # Target Port
user = 'root'               # account's username (Target System)
password = "fa"             # account's password (Target System)

remote_path = '/root/dmhc_app/oni/'
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
            print('Connecting To Target')
            ssh.connect(ip, port, 'root', password)
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            print("Checking whether any files exists")
            #get files can be downloaded
            remote_files = sftp.listdir(remote_path)
            for file in remote_files:   #iterate all files
                print("Downloading " + file)
                local_file = os.path.join(local_path, file)
                remote_file = os.path.join(remote_path, file)
                sftp.get(remote_file, local_file, callback=progress_bar)
                print("")
                #delete downloaded file
                ssh.exec_command('rm -r "' + remote_file + '"')
        except:
            print("Error Happend")
        ssh.close()
        print("Finished Downloading")
        print("Sleeping for 2 minutes")
        time.sleep(60 * 2)

ssh_scp_get(ip, port, user, password, remote_path, local_path)
