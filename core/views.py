from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives    


from core.forms import SendEmail
from contacts.models import ContactList,Contact

import threading


def index(request):
	return render(request,"core/index.html",{"title":"Home Page"})

@login_required
def send(request):
	if len(request.user.contactlist_set.all()) == 0:
		messages.success(request,"Inorder to send emails you need to create contact list")
		return redirect("users:profile")
	if request.method == "POST":
		form = SendEmail(request.POST)
		if form.is_valid():
			contact_id = request.POST.get("list")
			if contact_id:
				contact_list = ContactList.objects.get(pk = int(contact_id))
				contacts = Contact.objects.filter(contact_list = contact_list)
				names = [i.name for i in contacts]
				contacts = [i.email for i in contacts]

				sender = form.cleaned_data['sender']
				subject = form.cleaned_data['subject']

				body = form.cleaned_data['body']
				x = threading.Thread(target=run_t, args=(contacts,names,body,subject,sender))
				x.start()
				messages.success(request,"Mails Will Send Shortly!")
				return redirect("core:send")
			else:
				messages.warning(request,"Please Select the Contacts")
	else:
		form = SendEmail()
	return render(request,"core/send.html",{"title":"Send Page","form":form,"lists":ContactList.objects.filter(user = request.user)})


def run_t(contacts,names,body,subject,sender):
	for i in range(len(contacts)):
		s = body.replace("[[ name ]]",names[i]).replace("[[ email ]]",contacts[i])
		plain_message = strip_tags(s)
		# plain_message = s
		msg = EmailMultiAlternatives(subject, plain_message, sender+' '+settings.EMAIL_HOST_USER, [contacts[i]])
		msg.attach_alternative(plain_message, "text/html")
		msg.send()
