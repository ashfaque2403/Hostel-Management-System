from django import forms


class RoomAllotmentForm(forms.Form):
    student_name = forms.CharField(max_length=100)
    room_number = forms.CharField(max_length=10)
    # Add other fields as needed




