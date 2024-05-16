from django.db import models

# Create your models here.
class GatePass(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    image = models.ImageField(upload_to='gate_pass_images/')
    contact_no = models.CharField(max_length=15)
    DEPARTMENT_CHOICES = (
        ('CSE', 'Computer Science and Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
    )
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    reason_to_meet = models.TextField()

    def __str__(self):
        return self.name