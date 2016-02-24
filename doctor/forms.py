from django import forms
from doctor import constants
from doctor.models import AvailableTime


class ScheduleAppointmentForm(forms.Form):
    """
    Form for schedule appointment
    """
    start_date = forms.DateInput(label='Start Date', format=('%d-%m-%Y'))
    no_of_days = forms.IntegerField(label="Number of Days", initial=constants.MAX_NUMBER_OF_DAYS,
                                    min_value=constants.MIN_NUMBER_OF_DAYS,
                                    max_value=constants.MAX_NUMBER_OF_DAYS)
    start_time = forms.ModelChoiceField(label='Start Time',
                                        queryset=AvailableTime.get_timelist(),
                                        empty_label='Select Time')
    am_pm = forms.ChoiceField(label=False, choices=constants.AM_PM_CHOICE)
    duration = forms.IntegerField(label="Duration In hours", requied=False,
                                  initial=constants.MIN_DURATION,
                                  min_value=constants.MIN_DURATION,
                                  max_value=constants.MAX_DURATION)
