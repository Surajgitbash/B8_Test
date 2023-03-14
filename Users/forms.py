from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)


	class Meta:
		model = User
		fields = ("first_name", "last_name", "username", "email", "password1", "password2")

	# def save(self, commit=True):	# over-ridden save method from UserCreationForm
	# 	print("in over-ridden save method")
	# 	user = super(NewUserForm, self).save(commit=False)
	# 	print(user.__dict__)
	# 	user.email = self.cleaned_data['email']
	# 	user.first_name = self.cleaned_data['first_name']
	# 	user.last_name = self.cleaned_data['last_name']
	# 	if commit:
	# 		user.save()
	# 	return user 



############----- Create Django Login And Logout -----------------#####################################
# ----- Step ----------------
# 1) form create
# 2) html file create
# 3) html me pass karne ke iy ik views banana padega.................
# 4) Urls 
# 5) views.py 


#################### Class Base Views ############################################
# ---------------- 24 / 12 / 2022 -------------------------------------------------------------



