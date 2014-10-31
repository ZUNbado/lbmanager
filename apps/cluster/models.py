from django.db import models

class ClusterDefaults(models.Model):
	enabled = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True

class Member(ClusterDefaults):
	name = models.CharField(max_length=200)
	address = models.IPAddressField()

class Cluster(ClusterDefaults):
	name = models.CharField(max_length=200)
	backends = models.ManyToManyField(Member)
