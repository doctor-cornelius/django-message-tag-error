from django.shortcuts import render
from django.contrib import messages

def index(request):
    messages.success(request, "This is a success message")
    messages.warning(request, "This is a warning message")
    messages.info(request, "This is an info message")
    messages.error(request, "This is an error message")
    return render(request, "demo/index.html")
