from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View


class LoginView(View):
    template_name = 'home/login.html'
    message = ''

    def render_home(self, request):
        return render_to_response(
            'home/home.html',
            context_instance=RequestContext(request),
        )

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return self.render_home(request)
        else:
            try:
                key = form.errors.keys()[0]
                self.message = form.errors.get(key)[0]
            except Exception, e:
                self.message = 'Datos erroneos'
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.render_home(request)
        ctx = {
            'message': self.message,
            'next': request.GET.get('next'),
        }
        return render_to_response(
            self.template_name,
            context=ctx,
            context_instance=RequestContext(request),
        )


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home_app:login'))
