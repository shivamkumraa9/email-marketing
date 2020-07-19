from django.db import models
from users.models import MyUser


class ContactList(models.Model):
	name = models.CharField(max_length = 30)
	user = models.ForeignKey(MyUser,on_delete = models.CASCADE)

	def __str__(self):
		return self.name


class Contact(models.Model):
	name = models.CharField(max_length = 30)
	email = models.EmailField()
	contact_list = models.ForeignKey(ContactList,on_delete = models.CASCADE)

	def __str__(self):
		return self.name

