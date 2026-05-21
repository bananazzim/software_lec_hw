from django.views.generic import TemplateView, ListView, DetailView
from .models import Post


class HomeView(TemplateView):
    template_name = 'board/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recent_posts'] = Post.objects.order_by('-created_at')[:3]

        return context


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'

class AboutView(TemplateView):
    template_name = 'board/about.html'


class ProjectsView(TemplateView):
    template_name = 'board/projects.html'