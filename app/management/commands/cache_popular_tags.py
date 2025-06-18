from django.core.management.base import BaseCommand

from app.services import cache_best_members, get_best_members

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def handle(self, *args, **kwargs):
        cache_best_members()
        with open("/home/artem/Desktop/tmp.txt", "a") as file:
            file.write('Hello from python')