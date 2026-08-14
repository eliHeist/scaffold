
from django.shortcuts import render
from django.views import View

from scaffold.registrar import Registrar


accounts_router = Registrar(prefix="accounts", namespace="accounts")

@accounts_router.route("profile", name="profile")
class ProfileView(View):
    def get(self, request):
        return render(request, "accounts/profile.html", {"user": request.user})