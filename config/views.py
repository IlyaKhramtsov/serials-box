from django.shortcuts import render


def custom_page_not_found(request, exception):
    return render(
        request, 'misc/404.html', {'path': request.path}, status=404)


def custom_server_error(request):
    return render(request, 'misc/500.html', status=500)
