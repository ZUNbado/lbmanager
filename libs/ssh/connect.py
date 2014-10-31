import paramiko

class Connect():
	def __init__(self, host, user, passwd, port):
		self.host=host
		self.user=user
		self.passwd=passwd
		self.port=port
		self.ssh=None
		self.ftp=None
		self.connect()

	def connect(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.host, username=self.user, password=self.passwd, port=self.port)
		self.ssh=ssh

	def copy(self,src,dst):
		ftp=self.ssh.open_sftp()
		ftp.put(src,dst)
		self.ftp=ftp

	def command(self,command):
		stdin, stdout, stderr = self.ssh.exec_command(command)
