from django.db import models
from django.contrib.auth.models import User


from django.db.models import signals
from profiles.signals import create_profile
 
# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)

class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

   
    phone_number = models.IntegerField(max_length=7,default=8)
    address = models.CharField(max_length=20,default='Please enter your address')

