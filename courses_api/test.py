# backend/test.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smjaya_driving_school.settings')
django.setup()

from courses_api.models import *
print("✅ Berhasil terhubung ke models!")