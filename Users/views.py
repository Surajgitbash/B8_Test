from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
# -----------------------------------------------------------
from django.contrib.auth import login, authenticate, logout         # add this 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm        #  add this


def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("register")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


# ------------------- Login Create funtion ---------------



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')	# admin
			password = form.cleaned_data.get('password')	# admin 
			user = authenticate(username=username, password=password) # return user object	# ye database me comparision karata hai user name & password sahi hai kya........ 
			print(user, user.__dict__) 
			if user:
				login(request, user)	# databse save in entery session save karata hai 
				return redirect("home_page")
			else:
				pass
		else:
			pass
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_user(request):
	logout(request)
	return redirect("login_user")

# --------------------------------------------------------------------------------------------------------------------

##################### Login Views Class in Django #######################################

# ---------------------------------- 24 / 12 / 2022 ------------------------------------------------- 

from django.views.generic import View
from django.contrib.auth import forms 


class LoginPageView(View):
    template_name = 'login.html'    # instance variables
    form_class = AuthenticationForm
    
    def get(self, request):
        print("in get method")
        form = self.form_class()
        return render(request, self.template_name, context={'login_form': form})
        
    def post(self, request):
        print("in post method")
        form = self.form_class(data=request.POST)
        if form.is_valid():
            print("in valid?")
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'],)
            if user:
                login(request, user)
                return redirect('home_page ')
        return render(request, self.template_name, context={'login_form': form})