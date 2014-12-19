import shlex, subprocess

class RRDError(Exception):
	def __init__(self, message):
		self.message = message
                print self.message

def render(command, end, start, format):
	args = ['rrdtool','graph','-','--imgformat',format,'--base', '1024', '--width', '450', '--start', str(start), '--end', str(end) ] + shlex.split(command)
	p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	code = p.wait()
	if code != 0:
		raise RRDError(p.stderr.read())
	return p.stdout.read()
