from allauth.account.models import EmailAddress
from django.shortcuts import render
from django.views import View

from scaffold.registrar import Registrar


accounts_router = Registrar(prefix="accounts", namespace="accounts")

@accounts_router.route("profile", name="profile")
class ProfileView(View):
    def get(self, request):
        user = request.user
        email_addresses = EmailAddress.objects.filter(
            user=user,
            email=user.email,
        )
        context = {
            "user": user,
            "email_addresses": email_addresses,
        }
        return render(request, "accounts/profile.html", context)