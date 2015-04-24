from django.shortcuts import render

def overview(request):
    template = 'overview.html'
    context = {'template': template};
    return render(request, template, context)
