from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Classic Blog Design"
        return context


class PostByCategory(ListView):
    template_name = 'blog/category.html'
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F("views") + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostByTag(ListView):
    template_name = "blog/category.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])


class Search(ListView):
    template_name = "blog/search.html"
    context_object_name = 'posts'
    paginate_by = 4
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f's={self.request.GET.get("s")}&'
        return context

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))