from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks_module.models import Task
from .models import Transaction

@receiver(post_save, sender=Task)
def create_task_transaction(sender, instance, created, **kwargs):
    if created:
        # Transaction for task creator (admin)
        Transaction.objects.create(
            user=instance.created_by,
            transaction_type='TASK_SEND',
            task=instance,
            related_user=instance.assigned_to,
            description=f"Task '{instance.title}' sent to {instance.assigned_to.username}"
        )
        
        # Transaction for assigned user
        Transaction.objects.create(
            user=instance.assigned_to,
            transaction_type='TASK_RECEIVE',
            task=instance,
            related_user=instance.created_by,
            description=f"Task '{instance.title}' received from {instance.created_by.username}"
        )
    
    # When task is completed
    elif instance.status == 'COMPLETED':
        Transaction.objects.create(
            user=instance.assigned_to,
            transaction_type='TASK_COMPLETE',
            task=instance,
            related_user=instance.created_by,
            description=f"Task '{instance.title}' completed"
        )
