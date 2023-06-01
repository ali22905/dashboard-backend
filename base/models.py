from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)


class Profile(models.Model):
  access_levels = [('user', 'user'), ('manager', 'manager'), ('agent', 'agent'), ('admin', 'admin')]

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  firstname = models.CharField(max_length=25, null=True)
  lastname = models.CharField(max_length=25, null=True)
  phone = models.IntegerField(null=True)
  address1 = models.CharField(max_length=100, null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  access_level = models.CharField(choices=access_levels, max_length=50, default='user')

  created = models.DateTimeField(auto_now_add=True, null=True)
  updated = models.DateTimeField(auto_now=True, null=True)


  # avatar = models.ImageField(null=True, default="avatar.svg")
  def __str__(self):
    return self.user.username

  class Meta:
    ordering = ['-updated', '-created']

