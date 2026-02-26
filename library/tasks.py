from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from datetime import date, datetime
from .models import Loan

import logging

logger = logging.getLogger(__name__)


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    try:
        due_loans_qs = Loan.objects.filter(is_returned=False, due_date__lt=datetime.now().date()).select_related(
            'member__user', 'book')

        # TODO: group the loans with members while building the queryset, then send one email per user for all the due
        # loans using proper email template
        for loan in due_loans_qs:
            member_email = loan.member.user.email
            book_title = loan.book.title
            try:
                send_mail(
                    subject='Book Loaned Successfully',
                    message=f'Hello {loan.member.user.username},\n\nYour loan of "{book_title}" is overdue.\nPlease return it as soon as possible or renew the due date.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[member_email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"email sending failed for the user email - {member_email}, error: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"error occurred while checking due loans: {e}", exc_info=True)
