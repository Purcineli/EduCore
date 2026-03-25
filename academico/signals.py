from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender='academico.AcademicYear')
def enforce_single_active_year(sender, instance, **kwargs):
    '''
    Ensure only one AcademicYear can be active at a time.
    When an instance is saved with is_active=True, deactivate all others.
    '''
    if instance.is_active:
        sender.objects.exclude(pk=instance.pk).filter(is_active=True).update(is_active=False)
