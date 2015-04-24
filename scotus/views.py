from django.shortcuts import render

def overview(request):
    page = 'overview.html'
    context = {'page': page};
    return render(request, page, context)
