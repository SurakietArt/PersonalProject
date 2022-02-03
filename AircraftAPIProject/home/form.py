from django import forms
from django.db.models import fields,Q
from django.db.models.expressions import Value
from django.forms import ModelForm
from django.http import request
from .models import *

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('Task_name','Zone','Task_Detail','Assign','DueDate')
        mechanic = User.objects.filter(profile__position='1')
        mechanic_choice = [ (i.first_name,'ID : '+str(i.id)+' '+i.first_name) for i in mechanic ]       
        widgets = {
            'Task_name': forms.TextInput(attrs={'class':'form-control'}),
            'Zone': forms.Select(attrs={'class':'form-control'},choices=Task.Zone_choice),
            'Task_Detail': forms.Textarea(attrs={'class':'form-control'}),
            'Assign': forms.Select(attrs={'class':'form-control'},choices=mechanic_choice),
            'DueDate': forms.DateInput(
                format="%m/%d/%Y",
                attrs={'class': 'form-control', 
               'type': 'date'
              }),              
        }
        
 
class UpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ('Task_name','Zone','Task_Detail','Assign','DueDate','Reviewed','Task_Performed')
        mechanic = User.objects.filter(profile__position='1').values_list('first_name', flat=True)
        mechanic_choice = [ (i, i) for i in mechanic ]         
        widgets = {
            'Task_name': forms.TextInput(attrs=({'class':'form-control'})),
            'Zone': forms.Select(attrs={'class':'form-control'},choices=Task.Zone_choice),
            'Task_Detail': forms.Textarea(attrs={'class':'form-control'}),
            'Task_Performed': forms.Textarea(attrs={'class':'form-control'}),
            'Assign': forms.Select(attrs={'class':'form-control'},choices=mechanic_choice),
            'DueDate': forms.DateInput(
                format="%m/%d/%Y",
                attrs={'class': 'form-control', 
               'type': 'date'
              }),
            'Reviewed': forms.CheckboxInput(),
        }
        
 