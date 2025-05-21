from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from task_manager.models import Task


@receiver(post_save, sender=Task)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    if created:
        return

    if hasattr(instance, '_original_status') and instance.status != instance._original_status:
        if instance.owner and instance.owner.email:
            subject = f"Статус вашей задачи изменён: {instance.title}"
            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient = instance.owner.email

            context = {
                "username": instance.owner.username,
                "task_title": instance.title,
                "new_status": instance.status,
            }

            text_body = render_to_string("status_changed.txt", context)
            html_body = render_to_string("status_changed.html", context)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=sender_email,
                to=[recipient]
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()

        instance._original_status = instance.status
