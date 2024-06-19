from django.db import models


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
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES)
    return_time = models.TimeField(null=True, blank=True)
    nap_time = models.FloatField(null=True, blank=True, help_text='単位は時間です')
    note1 = models.TextField(null=True, blank=True)
    note2 = models.TextField(null=True, blank=True)
    note3 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'date'

    def __str__(self):
        return self.date.strftime('%Y/%m/%d')


class StatusEntry(models.Model):
    TIME_OF_DAY_CHOICES = [
        ('Morning', '起床'),
        ('Return', '帰宅'),
        ('Bedtime', '就寝'),
    ]
    id = models.AutoField(primary_key=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    time_of_day = models.CharField(max_length=10, choices=TIME_OF_DAY_CHOICES)
    physical = models.IntegerField(null=True, blank=True, help_text='1から10の整数で入力してください')
    mental = models.IntegerField(null=True, blank=True, help_text='1から10の整数で入力してください')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'time_of_day'], name='unique_entry')
        ]
        db_table = 'status_entry'


class Minimum(models.Model):
    date = models.OneToOneField(Date, on_delete=models.CASCADE, primary_key=True)
    min_physical = models.IntegerField(null=True, blank=True)
    min_mental = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'minimum'