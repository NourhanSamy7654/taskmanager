from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOISE=[
         ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20 , choices=STATUS_CHOICES,default='pending')
    priority=models.CharField(max_length=10,choices=PRIORITY_CHOISE,default='medium')
    due_date=models.DateField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name='task')
    updated_at=models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): # function to print data
        return f"{self.title} - {self.status} - {self.priority}[{self.get_status_display()}]"


    class Meta:
        ordering = ['-created_at'] # show task from new to last










        

# class Course(models.Model):
#   title = models.CharField(max_length=100)
#   def __str__(self):
#    return self.title
# class Student(models.Model):
#   name = models.CharField(max_length=100)
#   courses = models.ManyToManyField(
#  Course,
# blank=True # student can have zero courses
# )
#   def __str__(self):
#    return self.name
  