from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_staff_group(sender, instance, created, **kwargs):
    if created:  # Only for new users
        staff_group = Group.objects.get(name='Staff Members')  
        instance.groups.add(staff_group)
        instance.is_staff = True
        instance.save()