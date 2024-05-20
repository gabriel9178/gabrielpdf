# pdfoverlay/urls.py
from django.urls import path
from .views import process_lab_report, login_view ,logout_view

urlpatterns = [
    path('', login_view, name='login'),  # Redirect root URL to login page
    path('process-lab-report/', process_lab_report, name='process_lab_report'),
    path('logout/', logout_view, name='logout'),  # URL for logout
   
]
