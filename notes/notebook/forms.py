from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django.forms import modelformset_factory

from notes.notebook.models import Note, Photo

User = get_user_model()


class NoteModelForm(forms.ModelForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = Note
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user', None)
        super(NoteModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class PhotoForm(forms.ModelForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = Photo
        fields = '__all__'


PhotoFormSet = modelformset_factory(Photo, fields=('full_name', 'description', 'photo'), extra=3)
