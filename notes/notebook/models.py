from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Category(models.Model):
    full_name = models.CharField(max_length=200)
    type = models.ForeignKey('Type', on_delete=models.PROTECT, blank=True, null=True, related_name='notes')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['full_name', ]

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    #     return reverse('university_detail', args=[str(self.id)])


class Type(models.Model):
    full_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Note type'
        verbose_name_plural = 'Note types'
        ordering = ['full_name', ]

    def __str__(self):
        return self.full_name

    def get_list_url(self):
        return reverse('notebook:{type_full_name}-list'.format(type_full_name=self.full_name.lower().replace(' ', '_')))


class Note(models.Model):
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='notes', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['full_name', ]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('notebook:note-detail', args=[str(self.id), ])


class Photo(models.Model):
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    photo = models.ImageField()

    note = models.ForeignKey(Note, related_name='photos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        ordering = ['note', ]

    def __str__(self):
        return self.full_name
