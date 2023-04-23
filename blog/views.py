from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Posts, Thoughts
from .forms import CommentForm


class PostOverview(generic.ListView):
    model = Posts
    queryset = Posts.objects.filter(status=1).order_by("-created_on")
    template_name = "posts_overview.html"
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        """
        This view renders the blog page and also all published posts
        """
        posts = Posts.objects.all()
        paginator = Paginator(Posts.objects.all(), 6)
        page = request.GET.get('page')
        postings = paginator.get_page(page)

        return render(
            request, 'blog/posts_overview.html',  {'posts': posts, 'postings': postings})


class SinglePost(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Posts.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog/single_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Posts.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blog/single_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Posts, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('single_post', args=[slug]))
