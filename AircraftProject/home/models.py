from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

def default_timenow():
   return timezone.now()

def default_duedate():
   return timezone.now()

class Task( models.Model):
    class Zone_choice(models.TextChoices):
        Cockpit = 'Cockpit', "Cockpit"
        Cabin = 'Cabin', "Cabin"
        Wing = 'Wing', "Wing"
        Landing_Gear = 'Landing Gear', "Landing Gear"
        Fuselage = 'Fuselage', "Fuselage"
        Engine = 'Engine', "Engine"
        Empennage = 'Empennage', "Empennage"
        Avionic = 'Avionic', "Avionic"
    CreateBy = models.CharField(max_length=127)
    Task_name = models.CharField(max_length=127)
    Zone = models.CharField(max_length=127,choices=Zone_choice.choices,default=Zone_choice.Cockpit)
    Task_Detail = models.TextField()
    Assign = models.CharField(max_length=127)
    DueDate = models.DateTimeField(blank=True,default=default_timenow,null=True)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Update_Date = models.DateTimeField(default=default_timenow,blank=True)
    Update_By = models.CharField(max_length=127)
    Task_Performed = models.TextField()
    Reviewed = models.BooleanField(default=False,null=True,blank=True)
    Update_By_ID = models.CharField(max_length=127)
    def __str__(self):
        return self.Task_name


class Profile(models.Model):
    class Position_choice(models.TextChoices):
        Planner = '0', "Planner"
        Mechanic = '1', "Mechanic"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=127,choices=Position_choice.choices,default=Position_choice.Mechanic)
    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() 