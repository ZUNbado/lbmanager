import paramiko
import os
import socket, struct

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
        self.stdin=None
        self.stdout=None
        self.stderr=None

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
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)

    def close(self):
        self.ssh.close()

    def IPToNum(self,ip):
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

    def NumToIP(self,num):
        return socket.inet_ntoa(struct.pack('!L', num))
        
    def checkAndAddIP(self,ip):
        self.command("ip addr show lo |grep %s" % (ip))
        count=0
        for line in self.stdout.readlines(): count=count+1

        if count == 0:
            # ADD IP
            print "Adding IP %s" % ip
            command="ifconfig lo:%s %s netmask 255.255.255.255" % (self.IPToNum(ip), ip)
            self.command(command)

class FilesManager():
    @staticmethod
    def DirExists(path):
        if not os.path.exists(path): os.makedirs(path)

    @staticmethod
    def WriteFile(dst,content):
        hl=open(dst, 'w')
        hl.write(content)
        hl.close()
