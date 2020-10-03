from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView, DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.db import IntegrityError, transaction

from notes.notebook.models import Note, Type, Category
from notes.notebook.forms import NoteModelForm, PhotoFormSet, CategoryModelForm, TypeModelForm, DeleteModelForm

User = get_user_model()


def add_navbar_variables(context, selected_type=None):
    context['types'] = Type.objects.all().select_related()
    context['selected_type'] = selected_type
    return context


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
        }
        add_navbar_variables(context, self.kwargs.get('type'))
        return render(request, 'notebook/note_create.html', context)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        files = request.FILES
        data['user'] = request.user
        form = NoteModelForm(data)
        photo_formset = None
        try:
            with transaction.atomic():
                if form.is_valid():
                    note_instance = form.save()
                    photo_formset = PhotoFormSet(data, files)
                    for photo_form in photo_formset.forms:
                        photo_form.instance.note = note_instance
                    if photo_formset.is_valid():
                        photo_formset.save()
                    else:
                        raise IntegrityError()
                    return redirect(form.instance.get_absolute_url())
        except:
            context = {
                'form': form,
                'photo_formset': photo_formset if photo_formset else PhotoFormSet(data, files)
            }
            add_navbar_variables(context, kwargs.get('type'))
            return render(request, 'notebook/note_create.html', context)


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'notebook/notebook-list.html'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        add_navbar_variables(context, self.kwargs.get('pk'))
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
        storage = messages.get_messages(self.request)
        context = super().get_context_data(**kwargs)
        add_navbar_variables(context, self.kwargs.get('pk'))
        context['messages'] = storage
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        message = _("form {} successfully updated".format(self.object))
        messages.add_message(request, messages.INFO, message=message)
        return response


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    form_class = DeleteModelForm
    template_name = 'notebook/notebook-delete.html'

    def get_success_url(self):
        message = _("{} successfully deleted".format(self.object))
        messages.add_message(self.request, messages.INFO, message=message)
        return reverse_lazy('notebook:note-list', args=[self.object.category.type.id, ])

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args,**kwargs)
        add_navbar_variables(context, context['note'].category.type.id)
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
