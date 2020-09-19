from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotebookConfig(AppConfig):
    name = "notes.notebook"
    verbose_name = _("Notebook")

