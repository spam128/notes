from django.views.generic import TemplateView
from notes.notebook.models import Type


class HomeView(TemplateView):
    template_name = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context
