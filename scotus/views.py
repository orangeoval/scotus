from django.shortcuts import render

def overview(request):
    context = {'page': 'overview.html'};
    return render(request, 'overview.html', context)
