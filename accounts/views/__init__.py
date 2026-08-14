
from django.http import HttpResponse
from django.views import View

from scaffold.registrar import Registrar


accounts_router = Registrar(prefix="accounts", namespace="accounts")

@accounts_router.route("profile", name="login")
class LoginView(View):
    def get(self, request):
        return HttpResponse(f"Detail Page for {request.user.email}")