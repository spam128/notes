from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render

from notes.notebook.models import Note
from notes.notebook.forms import NoteModelForm, PhotoFormSet

User = get_user_model()


class NoteCreateView(LoginRequiredMixin, CreateView):
    form_class = NoteModelForm

    def get_initial(self, *args, **kwargs):
        initial = super(NoteCreateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user.id
        return initial

    def get(self, request, *args, **kwargs):
        photo_formset = PhotoFormSet()
        return render(request, 'notebook/note_create.html', {'form': NoteModelForm(), 'photo_formset': photo_formset})

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['user'] = request.user
        form = NoteModelForm(data)
        if form.is_valid():
            form.save()
            return redirect(form.instance.get_absolute_url())
        else:
            return render(request, 'notebook/note_create.html', {'form': form})


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'notebook/notebook-list.html'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    template_name = 'notebook/notebook-detail.html'
    object_name = 'flower'
    form_class = NoteModelForm

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
