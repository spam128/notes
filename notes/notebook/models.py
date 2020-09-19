from django.urls import reverse
from django.db import models


class Category(models.Model):
    full_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['full_name', ]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('university_detail', args=[str(self.id)])


class Note(models.Model):
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='notes')

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['full_name', ]  # TODO buttons to reorder

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('university_detail', args=[str(self.id)])


class Photo(models.Model):
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    note = models.ForeignKey(Note, related_name='photos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        ordering = ['note', ]

    def __str__(self):
        return self.full_name
