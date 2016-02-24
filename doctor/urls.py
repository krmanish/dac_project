from django.conf.urls import url
from doctor.views import ScheduleAppointmentViews


urlpatterns = [
    url(r'appointment/$', ScheduleAppointmentViews.as_view(), name='schedule_appointment')
]
