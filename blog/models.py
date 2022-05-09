from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="Url", unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Url")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=255, verbose_name='Url')
    author = models.CharField(max_length=100, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Теги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']
