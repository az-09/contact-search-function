from django.db import models
from django.db.models import Q

from functools import reduce
import operator

# Create your models here.
class ContactImage(models.Model):
	image = models.ImageField(upload_to='documents/', default='documents/avatar.svg')
	def __str__(self):
		return self.image.url

class ContactQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			keywords = query.split()
			fields = ['{}__icontains'.format(field.name) for field in Contact._meta.get_fields() if field.name in ['name', 'site', 'department', 'title']] #eg.'name__icontains'
			qs = [Q(**{field:keyword}) for field in fields for keyword in keywords]
			return self.filter(reduce(operator.or_, qs)).distinct()
		return self
	
	def id_search(self, query):
		return self.filter(id=query)
	

class Contactanager(models.Manager):
	def get_queryset(self):
		return ContactQuerySet(self.model, using=self._db)

	def search(self, query):
		return self.get_queryset().search(query)

	def id_search(self, query):
		return self.get_queryset().id_search(query)

class Contact(models.Model):

	name = models.CharField(max_length=100)
	site = models.CharField(max_length=200, blank=True)
	phone = models.CharField(max_length=17, blank=True)
	ext = models.CharField(max_length=10, blank=True)
	email = models.EmailField(max_length=100, blank=True)
	department = models.CharField(max_length=100, blank=True)
	title = models.CharField(max_length=50, blank=True)
	image = models.ImageField(upload_to='documents/', default='documents/avatar.svg')

	class Meta:
		ordering = ('name',)

	objects = Contactanager()

	def __str__ (self):
		return self.name



