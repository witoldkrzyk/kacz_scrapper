from django.core.management.base import BaseCommand
from app.robots.kaczmarski import KaczmarskiSelenium


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sdp = KaczmarskiSelenium('PL5270103824')
        sdp.run()
