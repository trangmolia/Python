from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.core.mail import EmailMessage, get_connection
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site


from config.settings.local import EMAIL_HOST_USER
from .forms import UserCreationForm
from .models import User
from .tokens import account_activation_token


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:success')


    def form_valid(self, form):
        # import pdb; pdb.set_trace()

        user = form.save()
        current_site = get_current_site(self.request)
        from_email = EMAIL_HOST_USER
        subject = 'Activate your elevennote account'
        to_email = form.cleaned_data.get('email')
        connection = get_connection(username=None, password=None, fail_silently=False)
        body = render_to_string('../templates/registration/activation.html', {
            'user': to_email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }) 

        email = EmailMessage(subject, body, from_email, to=[to_email], connection=connection)

        email.send()
        
        return super(RegisterView, self).form_valid(form)
    

def ActivationView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
    else:
        return HttpResponse('Activation link is invalid!')
