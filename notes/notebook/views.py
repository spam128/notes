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

from notes.notebook.models import Note, Type, Category
from notes.notebook.forms import NoteModelForm, PhotoFormSet, CategoryModelForm, TypeModelForm

User = get_user_model()


class NoteCreateView(LoginRequiredMixin, CreateView):
    form_class = NoteModelForm

    def get_initial(self, *args, **kwargs):
        initial = super(NoteCreateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user.id
        return initial

    def get(self, request, *args, **kwargs):
        photo_formset = PhotoFormSet()
        context = {
            'form': NoteModelForm(),
            'photo_formset': photo_formset,
            'types': Type.objects.all().select_related()
        }
        return render(request, 'notebook/note_create.html', context)

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

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context

class NoteByCategoryListView(LoginRequiredMixin, ListView):
    template_name = 'notebook/notebook-list.html'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context

class NoteUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    template_name = 'notebook/notebook-detail.html'
    object_name = 'flower'
    form_class = NoteModelForm

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = CategoryModelForm
    template_name = 'notebook/create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context


class TypeCreateView(LoginRequiredMixin, CreateView):
    form_class = TypeModelForm
    template_name = 'notebook/create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().select_related()
        return context
