from django.db import IntegrityError, models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    room_no=models.IntegerField()
    available=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.room_no)
   

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,primary_key=False,related_name='profile')
    name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField()
    phone=models.IntegerField(null=True, blank=True)
    address=models.CharField(max_length=250,null=True, blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    # photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name

class Complaint(models.Model):
    user=models.ForeignKey(User,related_name='compuser',on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    subject=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

class RoomAllotment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class LeaveRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    start_date=models.DateField()
    end_date=models.DateField()
    reason=models.CharField(max_length=550)
    
    def __str__(self):
        return f"{self.user.username} {self.start_date}"

class Attendance(models.Model):
    user=models.ForeignKey(User,related_name='attentance',on_delete=models.CASCADE,null=True, blank=True)
    attendance_status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    date=models.DateField(auto_now_add=False, null=True, blank=True)

    class Meta:
        # Add a unique constraint for the combination of user and date
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.attendance_status} - {self.date}"
    

class Fees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,primary_key=False)
    attendance=models.ForeignKey(Attendance,on_delete=models.CASCADE,null=True, blank=True)
    fee=models.IntegerField(max_length=5)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    
    @classmethod
    def delete_completed_fees(cls):
        completed_fees = cls.objects.filter(status='completed')
        for fee in completed_fees:
            fee.delete()

    def __str__(self):
        return f"{self.user.username} - {self.fee} - {self.status}"
    

