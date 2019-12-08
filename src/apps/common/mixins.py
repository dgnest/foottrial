from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(
            function=view,
            redirect_field_name='next',
            login_url=reverse_lazy('home_app:login'),
        )
