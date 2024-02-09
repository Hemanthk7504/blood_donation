from django.shortcuts import render


def home_view(request):
    # Your logic to retrieve data or perform other operations can go here
    # For now, let's just render a simple HTML template
    return render(request, 'home.html')
