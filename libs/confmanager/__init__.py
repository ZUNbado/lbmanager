import paramiko
import os
import socket, struct
from libs.debinterface.interfaces import interfaces

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
            command="ip addr add %s/32 dev lo label lo:%s" % (ip, self.IPToNum(ip))
            #command="ifconfig lo:%s %s netmask 255.255.255.255" % (self.IPToNum(ip), ip)
            self.command(command)

    def checkAndConfigIP(self,ips,lodef='iface lo inet loopback',netfile='/etc/network/interfaces'):
        sftp=self.ssh.open_sftp()
        adapters = interfaces(sftp)
        new_adapters = []
        for adapter in adapters.adapters:
            if adapter.export()['name'] == 'lo':
                updown = []
                for ip in ips:
                    updownline = 'ip addr add %s/32 dev $IFACE label $IFACE:%s' % ( ip, self.IPToNum(ip) )
                    updown.append(updownline)
                adapter.setDown(updown)
                adapter.setUp(updown)

            new_adapters.append(adapter)

        adapters.adapters = new_adapters
        adapters.writeInterfaces()

#    def checkAndConfigIP(self,ip,lodef='iface lo inet loopback',netfile='/etc/network/interfaces'):
#        conf = "up ip addr add %s/32 dev lo label lo:%s" % (ip, self.IPToNum(ip))
#        match = False
#        addafter = None
#        sftp=self.ssh.open_sftp()
#        with sftp.file(netfile, 'r') as file:
#            data=file.readlines()
#            for lineno, cur_line in enumerate(data):
#                if cur_line.strip('\t\r\n ') == lodef:
#                    addafter = lineno
#                if cur_line.strip('\t\r\n ') == conf:
#                    match = True
#
#        if match == False:
#            data.insert(addafter + 1, str("\t"+conf+"\n"))
#            with sftp.file(netfile, 'w') as write:
#                write.writelines(data)

class FilesManager():
    @staticmethod
    def DirExists(path):
        if not os.path.exists(path): os.makedirs(path)

    @staticmethod
    def WriteFile(dst,content):
        hl=open(dst, 'w')
        hl.write(content)
        hl.close()
