from django.contrib.auth.models import User
from django.shortcuts           import render


def inicio(request):
	template_name="base.html"
	return render(request,template_name)


