from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import User
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib import messages


class CustomLoginView(LoginView):
    model = User
    template_name = 'users/login.html'
    fields = ('username', 'password')
    success_url = reverse_lazy('education:index')


class CustomLogOutView(LogoutView):
    template_name = 'education/index.html'
    next_page = reverse_lazy('education:index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('education:index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Akkauntingizni faollashtiring'
        message = render_to_string('users/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return HttpResponse('Tasdiqlash havolasi emailingizga yuborildi.')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Sizning akkauntingiz faollashtirildi.')
    else:
        return HttpResponse('Aktivatsiya linki yaroqsiz yoki muddati o‘tgan.')


