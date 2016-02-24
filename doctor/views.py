from datetime import datetime, timedelta

import six
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.edit import FormView
from doctor.forms import ScheduleAppointmentForm
from doctor.models import AvailableDay, BookingStatus, DoctorSchedule


class ScheduleAppointmentViews(FormView):
    """
    ScheduleAppointmentView will support all the request
    """
    template_name = 'doctor/schedule_appointment.html'
    form_class = ScheduleAppointmentForm
    success_url = reverse('schedule_appointment')

    def _convert_to_24_hour(self, start_time, meridiem):
        """
        convert time from 12 hour to 24 hour format

        Args:
            start_time: Hours in Number from 1 - 12
            meridiem: AM/PM

        Returns:
            Time in 24 hour format
        """
        strptime_format = '%I %p'
        start_time = '%s %s' % (six.text_type(start_time), meridiem)
        time_obj = datetime.strptime(start_time, strptime_format)
        in_24_hour = datetime.strftime(time_obj, '%H')
        return int(in_24_hour)

    def _get_doctor_list(self, form):
        """
        Get All doctor list
        """
        available_doctors = []
        start_date = form.cleaned_up['start_date']
        no_of_days = form.cleaned_up['no_of_days']
        start_time = form.cleaned_up['start_time']
        am_pm = form.cleaned_up['am_pm']
        duration = form.cleaned_up['duration']
        start_time = int(self._convert_to_24_hour(start_time, am_pm))

        start_weekday_id = start_date.weekday() + 1  # +1 because weekday start from 0 till 6 but in db it is 1 to 7
        end_weekday_id = (start_weekday_id + no_of_days) % 7
        end_time = (start_time + duration) % 24

        end_date = start_date + timedelta(no_of_days)

        avail_days_obj = AvailableDay.get_days_by_ids(start_weekday_id, end_weekday_id)
        all_available_doctors = DoctorSchedule.get_doctorlist(avail_days_obj, start_time, end_time)

        if all_available_doctors:
            already_booked_doctors = BookingStatus.is_available(start_date, end_date, start_time, end_time)

            all_booked_doctor = set([booked.schedule.id for booked in already_booked_doctors])
            for available_doc in all_available_doctors:
                if all_booked_doctor and available_doc.id not in all_booked_doctor:
                    available_doctors.apppend(available_doc)

        return available_doctors

    def form_valid(self, form):
        """
        Upon form Validation check the availability and return the doctor list
        """
        doctors = self._get_doctor_list(form)

        if doctors:
            template_name = 'available_doctor_list.html'
            context_data = {'doctors': doctors}
            return render(self.request, template_name, context_data)

        # Return error message
        self.form_invalid(form)
