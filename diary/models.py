from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Date(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ('Sunday', '日'),
        ('Monday', '月'),
        ('Tuesday', '火'),
        ('Wednesday', '水'),
        ('Thursday', '木'),
        ('Friday', '金'),
        ('Saturday', '土'),
    ]
    date = models.DateField(primary_key=True)
    up = models.TimeField(null=True, blank=True)
    down = models.TimeField(null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES)
    return_time = models.TimeField(null=True, blank=True)
    nap_time = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(6)], help_text='単位は時間です')
    sleep_quality = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], help_text='1から10の整数で入力してください')
    note1 = models.TextField(null=True, blank=True)
    note2 = models.TextField(null=True, blank=True)
    note3 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'date'

    def __str__(self):
        return self.date.strftime('%Y/%m/%d')


class StatusEntry(models.Model):
    class TimeOfDay(models.TextChoices):
        MORNING = '1', '起床'
        RETURN = '2', '帰宅'
        BEDTIME = '3', '就寝'

    id = models.AutoField(primary_key=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='statusentry')
    time_of_day = models.CharField(max_length=10, choices=TimeOfDay.choices)
    physical = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], help_text='1から10の整数で入力してください')
    mental = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], help_text='1から10の整数で入力してください')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'time_of_day'], name='unique_entry')
        ]
        db_table = 'status_entry'


class Minimum(models.Model):
    date = models.OneToOneField(Date, on_delete=models.CASCADE, primary_key=True, related_name='minimum')
    min_physical = models.IntegerField(null=True, blank=True)
    min_mental = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'minimum'
