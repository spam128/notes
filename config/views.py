from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from notes.notebook.models import Type


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context
