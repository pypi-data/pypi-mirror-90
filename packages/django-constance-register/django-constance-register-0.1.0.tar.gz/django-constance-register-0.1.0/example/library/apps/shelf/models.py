from django.db import models


class Book(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255)
    published_at = models.DateTimeField(verbose_name='Published at')

    shelf = models.ForeignKey(
        'BooksShelf', verbose_name='Shelf', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-published_at']

    def __str__(self) -> str:
        return self.title


class BooksShelf(models.Model):
    room = models.IntegerField(verbose_name='Room number')
    position = models.IntegerField(verbose_name='Position')

    class Meta:
        verbose_name = 'Books shelf'
        verbose_name_plural = 'Books shelves'
        ordering = ['room']

    def __str__(self) -> str:
        return f'Shelf at room #{self.room}'
