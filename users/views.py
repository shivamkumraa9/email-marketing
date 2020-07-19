from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from users.models import MyUser
from users.forms import LoginForm,PasswordValidationForm,CustomUserCreationForm


def userlogin(request):

	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				user = MyUser.objects.get(email = email)
				user = authenticate(request,username = user.username,password = password)
				if user:
					login(request,user)
					return redirect("users:profile")
				else:
					messages.error(request, 'Invalid Email/Password.')
			except MyUser.DoesNotExist:
				messages.error(request, 'Invalid Email/Password.')
	else:
		form = LoginForm()

	return render(request,"users/login.html",{"form":form})



def userregister(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, 'Account has been created')
			return redirect("users:login")
	else:
		form = CustomUserCreationForm()
	return render(request,"users/register.html",{"form":form})



@login_required
def delete(request):
	if request.method == "POST":
		form = PasswordValidationForm(request.POST)

		if form.is_valid():
			password = form.cleaned_data['password']
			user = request.user
			user = authenticate(request,username = user.username,password = password)
			if user:
				user.delete()
				messages.success(request, 'Account has been deleted')
				return redirect("users:login")
			else:
				messages.error(request, 'Invalid Password')
	else:
		form = PasswordValidationForm()
	return render(request,"users/delete.html",{"form":form})


@login_required
def profile(request):
	return render(request,"users/profile.html",{"lists":request.user.contactlist_set.all()})


@login_required
def userlogout(request):
	logout(request)
	messages.success(request, 'User has been logged out')
	return redirect("users:login")

