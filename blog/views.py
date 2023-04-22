from django.shortcuts import render
from django.views import generic
from .models import Posts
from django.core.paginator import Paginator


class PostOverview(generic.ListView):
    model = Posts
    queryset = Posts.objects.filter(status=1).order_by("-created_on")
    template_name = "posts_overview.html"
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        """
        This view renders the blog page and also all published posts
        """
        posts = Posts.objects.all()
        print(posts)
        paginator = Paginator(Posts.objects.all(), 6)
        page = request.GET.get('page')
        postings = paginator.get_page(page)

        return render(
            request, 'blog/posts_overview.html',  {'posts': posts, 'postings': postings})

