from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.forms import fields
from django.forms.models import ModelForm

class NewUserForm(UserCreationForm):
   email = forms.EmailField(required=True)

   class Meta:
      model = User
      fields = ("first_name", "last_name" , "email", "password1", "password2")

   def save(self, commit=True):
      user = super(NewUserForm, self).save(commit=False)
      user.email = self.cleaned_data['email']
      if commit:
         user.save()
      return user

class UpgradeToBloggerForm(UserChangeForm):
   password=None
   class Meta:
      model = User
      fields = ('username',)

   def save(self, commit=True):
      user = super(UpgradeToBloggerForm, self).save(commit=False)
      user.username = self.cleaned_data['username']
      if commit:
         user.save()
      return user