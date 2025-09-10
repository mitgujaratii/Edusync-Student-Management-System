from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    COURSE_CHOICES = [
        ('CE', 'Computer Engineering'),
        ('IT', 'Information Technology'),
        ('CSD', 'Computer Science and Design'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('AIDS', 'Artificial Intelligence and Data Science'),
        ('RAI', 'Robotics and AI'),
        ('CSE', 'Computer Science and Engineering'),
        ('CST', 'Computer Science and Technology'),
        ('CSIT', 'Computer Science and Information Technology'),
        ('CEA', 'Computer Engineering and Automation'),
    ]

    SEMESTER_CHOICES = [
        (str(i), f'Semester {i}') for i in range(1, 9)
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    student_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    days_present = models.IntegerField(default=0)
    days_absent = models.IntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        
        total_days = self.days_present + self.days_absent
        if total_days > 0:
            self.attendance_percentage = (self.days_present / total_days) * 100
        else:
            self.attendance_percentage = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Attendance for {self.student.first_name} {self.student.last_name}'