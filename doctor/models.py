from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from doctor import constants


class DACDatetime(models.Model):
    """
    Abstract model for datetime
    """
    created_ts = models.DateTimeField(auto_now_add=True, help_text="Created timespan")
    updated_ts = models.DateTimeField(auto_now_add=False, auto_now=True, help_text="Updated timestamp")

    class Meta:
        abstract = True


class Doctor(DACDatetime):
    """
    Doctor's record
    """
    user = models.OneToOneField(User)
    specialist = models.CharField(max_length=5, choices=constants.SPECIALIST_LIST, default='GP')
    gender = models.CharField(max_length=10, choices=constants.GENDER_TYPES, default='F')
    address = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        return '% %' % (self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return self.full_name


class AvailableDay(models.Model):
    """
    Store all available days
    Example:
        Monday with id-1, Tuesday with id-2 ... Sunday with id-7
    """
    day = models.CharField(max_length=20, help_text="Day as Monday/Tuesday")
    short_name = models.CharField(max_length=5, help_text='Abbreviation of week days like Mon/Tue ')

    @classmethod
    def get_datelist(cls):
        """
        Return all days in descending order
        """
        return cls.objects.all().order_by('-id')

    @classmethod
    def get_days_by_ids(cls, start_id, end_id):
        """
        Get days object by given range of id
        """
        return cls.objects.filter(id__in=(start_id, end_id))


class AvailableTime(models.Model):
    """
    Store all available time
    Example:
        0, 1, 2, 3, 4 ... 12, 13, 14, ... 23
    """
    time = models.PositiveSmallIntegerField(help_text="All available time in 24 hour format")

    @classmethod
    def get_timelist(cls):
        """
        Get time list in 12 hour format
        """
        return cls.objects.filter(time__in=(1, 12))

    @classmethod
    def get_times_by_ids(cls, start_time, end_time):
        """
        Get times object by given range of id
        """
        return cls.objects.filter(time__in=(start_time, end_time))


class DoctorSchedule(DACDatetime):
    """
    Maintain the doctor Availability data
    """
    doctor = models.ForeignKey(Doctor)
    day = models.ForeignKey(AvailableDay, help_text="Day")
    start_time = models.ForeignKey(AvailableTime, related_name="start_time")
    end_time = models.ForeignKey(AvailableTime, related_name="end_time")
    is_active = models.BooleanField(default=True, help_text="Active/Inactive Flag")

    class Meta:
        unique_together = ('doctor', 'day', 'start_time')

    @classmethod
    def get_doctorlist(cls, avail_days_obj, start_time, end_time):
        """
        Get all available doctor list by given dates and times
        """
        return cls.objects.filter(day__in=avail_days_obj, start_time__time__lte=start_time,
                                  end_time__time__gte=end_time,
                                  is_active=True)


class BookingStatus(DACDatetime):
    """
    Booking status for
    """
    schedule = models.ForeignKey(DoctorSchedule)
    start_time = models.ForeignKey(AvailableTime, related_name="book_start_time", help_text="Start time in 24 hour format")
    end_time = models.ForeignKey(AvailableTime, related_name="book_end_time", help_text="End time in 24 hour format")
    booked_date = models.DateField(help_text="Booked Date")

    @classmethod
    def is_available(cls, start_date, end_date, start_time, end_time):
        """
        Return list of object of already booked detail else empty list
        """

        # May return redundant info in case of multiple appointment on same day for a doctor
        # Need to use aggregator to return unique record by schedule object
        already_booked_obj = cls.objects.filter(
            Q(start_time__time__lte=start_time, end_time__time__gte=start_time) | Q(end_time__time__lte=end_time, end_time__time__gte=end_time),
            booked_date__in=(start_date, end_date))

        return already_booked_obj
