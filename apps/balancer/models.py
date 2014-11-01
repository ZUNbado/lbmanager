from django.db import models


class BalancerDefaults(models.Model):
	enabled = models.BooleanField(default=True)
	def __str__(self):
		return self.name

	class Meta:
		abstract = True


class Backend(BalancerDefaults):
	name = models.CharField(max_length=200)
	address = models.IPAddressField()

class Director(BalancerDefaults):
	TYPES = (
		( 'Random', (
			( 'random', 'Random'),
			( 'client', 'Client'),
			( 'hash', 'Hash' ),
		),
		),
		( 'round-robin', 'Round Robin' ),
		( 'dns', 'DNS' ),
		( 'fallback', 'Fallback' )
	)
	name = models.CharField(max_length=200)
	backends = models.ManyToManyField(Backend)
	dirtype = models.CharField(max_length=200,choices=TYPES,default='round-robin')
