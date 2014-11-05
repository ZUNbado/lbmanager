import paramiko
import os

class ConfManager():
    def __init__(self, host, user, passwd, port):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.port=port
        self.connected=False
        self.error_msg=None
        self.ssh=None
        self.ftp=None
        self.connect()

    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, username=self.user, password=self.passwd, port=self.port, timeout=5)
            self.ssh=ssh
            self.connected=True
        except Exception, e:
            self.connected=False
            self.error_msg=e

    def copy(self,src,dst):
        ftp=self.ssh.open_sftp()
        ftp.put(src,dst)
        self.ftp=ftp

    def command(self,command):
        stdin, stdout, stderr = self.ssh.exec_command(command)

    def close(self):
        self.ssh.close()


class FilesManager():
    @staticmethod
    def DirExists(path):
        if not os.path.exists(path): os.makedirs(path)

    @staticmethod
    def WriteFile(dst,content):
        hl=open(dst, 'w')
        hl.write(content)
        hl.close()
