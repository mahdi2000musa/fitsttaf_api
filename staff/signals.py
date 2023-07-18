from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from staff.models import Profile, Team


@receiver(post_save, sender=Profile)
def add_num_of_member(sender, instance, created, **kwargs):
    if created:
        t_id = instance.team.id
        obj = Team.objects.get(id=t_id)
        num = obj.num_of_member + 1
        obj.num_of_member = num
        obj.save()


@receiver(post_delete, sender=Profile)
def sub_num_of_member(sender, instance, **kwargs):
    t_id = instance.team.id
    obj = Team.objects.get(id=t_id)
    num = obj.num_of_member - 1
    obj.num_of_member = num
    obj.save()

