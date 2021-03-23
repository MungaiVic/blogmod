from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
meUser = get_user_model()


class NewUserForm(UserCreationForm):
   email = forms.EmailField(required=True)

   class Meta:
      model = meUser
      fields = ("first_name", "last_name" , "user_name" ,"email", "password1", "password2")

   def save(self, commit=True):
      user = super(NewUserForm, self).save(commit=False)
      user.email = self.cleaned_data['email']
      if commit:
         user.save()
      return user

class UpgradeToBloggerForm(UserChangeForm):
   password=None #? This prevents django from thinking that we want to create a new password as well.
   class Meta:
      model = meUser
      fields = ('user_name', 'bio')

   def save(self, commit=True):
      user = super(UpgradeToBloggerForm, self).save(commit=False)
      user.username = self.cleaned_data['user_name']
      user.bio = self.cleaned_data['bio']
      if commit:
         user.save()
      return user