from django.db import models


class NoteCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория заметки'
        verbose_name_plural = 'Категории заметок'


class Note(models.Model):
    ARCHIVE = 'archive'
    PUBLIC = 'public'
    STATUS_CHOICES = [
        (ARCHIVE, 'В архиве'),
        (PUBLIC, 'Опубилковано')
    ]

    title = models.CharField(max_length=255, verbose_name='название')
    text = models.TextField(verbose_name='текст')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    image = models.FileField(verbose_name='картинка', null=True, blank=True)
    category = models.ForeignKey(
        NoteCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='категория заметки'
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PUBLIC)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
