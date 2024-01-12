from django.urls import path
from . import views
from .views import UserProfileCreateView
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('thanks/',views.thanks,name='thanks'),
    path('rules/',views.rules,name='rules'),
    path('viewall/',views.view_complaint,name='view-complaints'),
    path('complaint/',views.send_complaints,name='complaint'),
    path('logout/',views.logout_view,name='logout'),
    path('add/',views.add_student,name='addstudent'),
    path('create/', UserProfileCreateView.as_view(), name='create_user_profile'),
    path('allot_room/', views.allot_room, name='allot_room'),
    path('userprofile/',views.userpro,name='userprofile'),
    path('leave/',views.leaverequest,name='leave-request'),
    path('update/',views.updateprofile,name='update-profile'),
    path('viewleave/',views.ViewLeaveRequest,name='view-leave'),
    path('attendance/',views.ViewAttendance,name='view-attendance'),
    path('allattendance/',views.AllViewAttendance,name='view-attendance-all'),
    path('fees/',views.GenerateFees,name='view-fee'),
    path('allfees/',views.AllGenerateFees,name='all-view-fee'),
    path('changepassword/',views.ChangePassword,name='change-password'),
    path('rooms/',views.FullRoom,name='full-room'),  

]