from django.http import HttpResponse


def django_greetings(request) -> HttpResponse:
    return HttpResponse(
        "<h1>Greetings from the Django APP!!! :)</h1>"
    )


def user_greetings(request, name) -> HttpResponse:
    return HttpResponse(
        f"<h2>Hello, {name} .</h2>"
    )

