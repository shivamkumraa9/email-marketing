from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseNotFound


from contacts.models import ContactList,Contact
from contacts.forms import NewListForm,FileForm,ContactForm



@login_required
def new_list(request):
	if request.method == "POST":
		form = NewListForm(request.POST,request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			contact_list = ContactList.objects.filter(name = name)
			if contact_list:
				form.add_error("name", "Name Already exists")
			else:
				if request.FILES.get("file"):
					raw = b''
					for i in request.FILES['file'].chunks():
						raw += i
					raw = raw.decode('utf-8').replace("\r","").split("\n")
					headers = raw[0].split(",")
					raw = raw[1:]
					if len(headers) == 2 and headers[0].lower() == 'email' and headers[1].lower() == 'name':
						new = ContactList.objects.create(name = name,user = request.user)
						for row in raw:
							data = row.split(",")
							if (len(data) == 2) and (data[0]!=''):
								if not Contact.objects.filter(email = data[0],contact_list = new):
									Contact.objects.create(email = data[0],name = data[1],contact_list = new)
					else:
						form.add_error("file","Csv file at max should contain 2 rows where email should be the first row and second should be name row.")
						form.add_error("file","Also first column of the file should be email,name")
						return render(request,"contacts/new_list.html",{'form':form})
				else:
					new = ContactList.objects.create(name = name,user = request.user)
				messages.success(request, 'Contact List Has Been Created')
				return redirect("users:profile")
	else:
		form = NewListForm()
	return render(request,"contacts/new_list.html",{'form':form})


@login_required
def add(request,list_id):
	lis = get_object_or_404(ContactList,pk = list_id , user = request.user)
	if request.method == "POST":
		form = FileForm(request.POST,request.FILES)
		if form.is_valid():
			raw = b''
			for i in request.FILES['file'].chunks():
				raw += i
			raw = raw.decode('utf-8').replace("\r","").split("\n")
			headers = raw[0].split(",")
			raw = raw[1:]
			if len(headers) == 2 and headers[0].lower() == 'email' and headers[1].lower() == 'name':
				for row in raw:
					data = row.split(",")
					if (len(data) == 2) and (data[0]!=''):
						if not Contact.objects.filter(email = data[0],contact_list = lis):
							Contact.objects.create(email = data[0],name = data[1],contact_list = lis)
				messages.success(request, 'Contacts has been Updated')
				return redirect("contacts:get_all",list_id)
			else:
				form.add_error("file","Csv file at max should contain 2 rows where email should be the first row and second should be name row.")
				form.add_error("file","Also first column of the file should be email,name")
	else:
		form = FileForm()
	return render(request,"contacts/add.html",{'form':form})




@login_required
def add_single(request,list_id):
	lis = get_object_or_404(ContactList,pk = list_id , user = request.user)
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			if not Contact.objects.filter(email = form.cleaned_data['email'],contact_list = lis):
				Contact.objects.create(email = form.cleaned_data['email'],name = form.cleaned_data['name'],contact_list = lis)
				messages.success(request,"Contact Added")
				return redirect("contacts:get_all",list_id)
			else:
				form.add_error("email","Email Already exists in your contacts")
	else:
		form = ContactForm()
	return render(request,"contacts/add_single.html",{'form':form})


@login_required
def get_all(request,list_id):
	lis = get_object_or_404(ContactList,pk = list_id , user = request.user)
	return render(request,"contacts/get_all.html",{'c_list':lis})


@login_required
def delete(request,list_id):
	lis = get_object_or_404(ContactList,pk = list_id , user = request.user)
	lis.delete()
	messages.success(request,"List Deleted!")
	return redirect("users:profile")


@login_required
def remove(request,list_id):
	lis = get_object_or_404(ContactList,pk = list_id , user = request.user)
	if request.method == "POST":
		checks = request.POST.getlist("check")
		for i in checks:
			try:
				Contact.objects.get(contact_list = lis,pk = int(i)).delete()
			except:
				pass
		messages.success(request,"Contact Deleted!")
		return redirect("contacts:get_all",lis.pk)
	else:
		return HttpResponseNotFound("Invalid")