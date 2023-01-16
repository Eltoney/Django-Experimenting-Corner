from django.db import models

# Create your models here.
# Dept = ('CS', 'IT', 'IS', 'SE')
Dept = (
    (('CS'), ('CS')),
    (('CS'), ('IT')),
    (('CS'), ('IS')),
    (('CS'), ('SE'))
)


class Course(models.Model):
    title = models.CharField(max_length=50)
    credit_hours = models.IntegerField()
    depatment = models.CharField(choices=Dept, max_length=2)
    total_students = models.IntegerField(default=0)

    def __str__(self):
        return self.title # TODO
