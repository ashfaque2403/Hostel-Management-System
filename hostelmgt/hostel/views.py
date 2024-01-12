from django.utils import timezone  
from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from .models import Room,UserProfile,Complaint,RoomAllotment,LeaveRequest,Attendance,Fees
from django.views import View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from django.db.models import Sum, F, Case, When, IntegerField

@login_required
# Create your views here.
def index(request):
    return render(request,'index.html')

def thanks(request):
    return render(request,'thanks.html')

def rules(request):
    return render(request,'rules.html')
@login_required
def view_complaint(request):
    view_all=Complaint.objects.order_by('created_at')
    return render(request,'view_complaints.html',{'view_all':view_all})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()  # Use first() to get the first matching user or None

        if not user_obj:
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_authenticated = authenticate(request, username=username, password=password)

        if not user_authenticated:
            messages.warning(request, 'Invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request, user_authenticated)
        return redirect('/')  # Redirect to the desired page after successful login

    return render(request, 'login.html')

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)
        if user_obj.exists():
            messages.warning(request,'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        user=User.objects.create(username=username,email=email,password=password)
        user.set_password(password)
        user.save()
        return redirect('login')


    return render(request,'register.html')
@login_required
def add_student(request):
    if request.method=='POST':
        # username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(email=email)
        if user_obj.exists():
            messages.warning(request,'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        user=User.objects.create(email=email,password=password)
        user.set_password(password)
        user.save()
        return redirect('create_user_profile')


    context = {
    }
    return render(request, 'add_student.html', context)




class UserProfileCreateView(View):
    template_name = 'create_user_profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # username=request.POST.get('username')
        name=request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date_of_birth_str  = request.POST.get('date_of_birth')

        # Create a user and set the password
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()

        today = datetime.now().date()
        if date_of_birth >= today:
            messages.warning(request, 'Recheck the date of birth')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if User.objects.filter(username=name).exists():
            messages.warning(request,'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
        
            user_ob = User.objects.create_user(username=name, email=email, password=phone)

        # Create a user profile associated with the user
        user_profile = UserProfile.objects.create(user=user_ob, name=name,phone=phone, email=email,address=address, date_of_birth=date_of_birth)
        
        success = True  # or False based on your conditions
        if success:
           
            return redirect(reverse('thanks'))

        return render(request, self.template_name, {'success': success})
    



def logout_view(request):
    logout(request)
    return redirect(index)
@login_required
def send_complaints(request):
    if request.method == 'POST':
        user=request.user
        username = request.POST.get('username')
        subject = request.POST.get('subject')

        
        Complaint.objects.create(name=username, subject=subject,user=user)
        messages.success(request,'Thank You for your response')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'complaint.html')

@login_required
def allot_room(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        room_number = request.POST.get('room_number')

        user = User.objects.filter(username=student_name).first()
        room = Room.objects.filter(room_no=room_number).first()

        if user and room:
            # Check if the room is available
            if not RoomAllotment.objects.filter(user=user).exists():
                # Check if the room has less than 3 allotments
                if RoomAllotment.objects.filter(room=room).count() < 3:
                    # Room is available, create allotment
                    allotment = RoomAllotment(user=user, room=room)
                    allotment.save()

                    # Update room status
                    room.available = False
                    room.save()

                    return render(request, 'allotment_success.html', {'allotment': allotment})
                else:
                    return render(request, 'allotment_failure.html', {'error_message': 'Room is full (maximum 3 users).'})
            else:
                return render(request, 'allotment_failure.html', {'error_message': 'Room not available.'})
        else:
            return render(request, 'allotment_failure.html', {'error_message': 'Student does not exist.'})
    else:
        # If it's not a POST request, handle accordingly
        available_rooms = Room.objects.filter(available=True)
        return render(request, 'allot_room.html', {'available_rooms': available_rooms})
    
    
@login_required
def userpro(request):
    profile = UserProfile.objects.filter(user_id=request.user)
    room_detail = RoomAllotment.objects.filter(user_id=request.user)
    context={
        'profile':profile,
        'room_detail':room_detail,
    }
    return render(request,'userpro.html',context)
@login_required
def leaverequest(request):
    if request.method=='POST':
        user=request.user
        start_date_str=request.POST.get('startdate')
        end_date_str=request.POST.get('enddate')
        reason=request.POST.get('reason')

        starting = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        ending = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()

        if starting < today or ending < today:
            messages.warning(request, 'Cannot select a start date before today.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        LeaveRequest.objects.create(user=user,start_date=start_date_str,end_date=end_date_str,reason=reason)
        
        messages.success(request,'Request has been sent')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context={

    }
    return render(request,'leaverequest.html',context)
@login_required
def updateprofile(request):
    update_profile = UserProfile.objects.get(user=request.user)

        # Pre-fill the form with the current data
    form_data = {
            'name': update_profile.name,
            'email': update_profile.email,
            'phone': update_profile.phone,
            'address': update_profile.address,
            'date_of_birth': update_profile.date_of_birth,
        }
    if request.method=='POST':
        name=request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')

        date_of_birth_str  = request.POST.get('date_of_birth')

        # Create a user and set the password
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()

        today = datetime.now().date()
        if date_of_birth >= today:
            messages.warning(request, 'Recheck the date of birth')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        update_profile=UserProfile.objects.get(user=request.user)

        update_profile.name=name
        update_profile.email=email
        update_profile.phone=phone
        update_profile.address=address
        update_profile.date_of_birth=date_of_birth
        update_profile.save()

        messages.success(request, 'Profile updated successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context={
        'form_data':form_data,
    }
    return render(request,'updateprofile.html',context)
@login_required
def ViewLeaveRequest(request):
    leave=LeaveRequest.objects.all()

    context={
        'leave':leave,
    }
    return render(request,'view_leave.html',context)


def ViewAttendance(request):
    
    students=Attendance.objects.filter(user_id=request.user)
    
    allattendance=Attendance.objects.all()
    context={
        'students':students,
        'allattendance':allattendance
    }
    return render(request,'view_attendance.html',context)
@login_required
def AllViewAttendance(request):
    allattendance=Attendance.objects.all()
    context={
        'allattendance':allattendance
    }
    return render(request,'view_all.html',context)

def GenerateFees(request):
    user = request.user
    view_fees = Fees.objects.filter(user=user)
    view_fees_all = Fees.objects.all()

    # Count absents for the user
    absents_count = Attendance.objects.filter(user=user, attendance_status='absent').count()

    # Calculate total fees with penalty for absents
    total_fees_result = Fees.objects.filter(user=user).aggregate(
        total_fees=Sum(
            Case(
                When(attendance__attendance_status='absent', then=F('fee') - 100),
                default=F('fee'),
                output_field=IntegerField()
            )
        )
    )

    # Extract total_fees or set default value if it is None
    total_fees = total_fees_result['total_fees'] if total_fees_result['total_fees'] is not None else 0

    added_amount_per_absent = 100
    total_absent_money = absents_count * added_amount_per_absent

    view = Fees.objects.filter(user=user)

    if view.exists():
        # If there are fees for the user
        finalize = [fee.fee - total_absent_money for fee in view]
        # Now, finalize_list contains the result for each fee in the queryset
    else:
        # If there are no fees for the user
        finalize = []

    completed_fees = Fees.objects.filter(status='completed')

    # Loop through completed fees and delete them
    for fee in completed_fees:
        fee.delete()

    context = {
        'view_fees': view_fees,
        'view_fees_all': view_fees_all,
        'absents_count': absents_count,
        'total_fees': total_fees,
        'total_absent_money': total_absent_money,
        'finalize': finalize,
    }

    return render(request, 'fees.html', context)

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the old password is correct
        if not authenticate(request, username=user.username, password=old_password):
            messages.error(request, 'Incorrect old password.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Update the session to prevent the user from being logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password successfully changed.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'changepassword.html')


def AllGenerateFees(request): 
    view_fees_all = Fees.objects.all()
    
    context = {
        
        'view_fees_all': view_fees_all,
        
    }

    return render(request, 'allfee.html', context)

def FullRoom(request):
    room=RoomAllotment.objects.all()

    context={
        'room':room,
    }
    return render(request,'fullroom.html',context)

