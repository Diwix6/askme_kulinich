from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from app.models import Question, Profile, Reaction, Tag, Answer


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        Reaction.objects.all().delete()