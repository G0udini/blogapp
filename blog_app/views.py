from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

from .models import Comment, Post
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = (
            Post.published.select_related("author")
            .prefetch_related("tags")
            .only("id", "title", "publish", "slug", "tags", "author__username", "image")
        )
        tag = kwargs.get("tag_slug", None)
        page = request.GET.get("page", 1)
        form = SearchForm()
        if tag:
            posts = posts.filter(tags__name__in=[tag])
        if "search" in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                search = form.cleaned_data["search"]
                posts = (
                    posts.annotate(
                        similarity=TrigramSimilarity("title", search)
                        + TrigramSimilarity("body", search)
                    )
                    .filter(similarity__gte=0.3)
                    .order_by("-similarity")
                )
        paginator = Paginator(posts, 4)
        posts = paginator.get_page(page)

        context = {
            "posts": posts,
            "page": page,
            "page_limit": paginator.num_pages,
            "tag": tag,
            "form": form,
        }

        template_name = "blog_app/post/list.html"
        if self.request.is_ajax():
            template_name = "blog_app/post/list_wrapper.html"

        return render(request, template_name, context)


class PostShare(View):
    template_name = "blog_app/post/share.html"

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status="published")
        sent = False
        form = EmailPostForm()
        return render(
            request,
            self.template_name,
            {"post": post, "form": form, "sent": sent},
        )

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status="published")
        sent = False
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            if request.user.is_authenticated:
                subject_prefix = f"{request.user.username} recommends"
            else:
                subject_prefix = "I recommend"
            subject = f"{subject_prefix} you to read {post.title}"
            massage = (
                f"Read '{post.title}' at " f"{post_url}\n\nComments: {cd['comments']}"
            )
            send_mail(subject, massage, "ruspro1927@gmail.com", [cd["to"]])
            sent = True
            return render(
                request,
                self.template_name,
                {"post": post, "form": form, "sent": sent},
            )


class PostDeatail(View):
    template_name = "blog_app/post/detail.html"

    def get_context_data(self, **kwargs):
        post = get_object_or_404(
            Post.published.select_related("author").only(
                "id", "title", "publish", "slug", "author__username", "image", "body"
            ),
            slug=kwargs["post"],
            publish__year=kwargs["year"],
            publish__month=kwargs["month"],
            publish__day=kwargs["day"],
        )
        comments = (
            Comment.objects.filter(active=True, post=post.id)
            .select_related("commentator")
            .only("commentator__username", "created", "body")
        )
        tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=tags_ids).exclude(id=post.id)
        similar_posts = (
            similar_posts.annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-publish")[:5]
            .values("title")
        )
        return {
            "post": post,
            "similar_posts": similar_posts,
            "comments": comments,
        }

    def get(self, request, *args, **kwargs):
        comment_form = CommentForm()
        context = self.get_context_data(**kwargs)
        context["comment_form"] = comment_form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        context = self.get_context_data(**kwargs)
        if comment_form.is_valid() and request.user.is_authenticated:
            new_comment = comment_form.save(commit=False)
            new_comment.commentator = request.user
            new_comment.post = context["post"]
            new_comment.save()
        context["comment_form"] = comment_form
        return render(request, self.template_name, context)


class PostAdd(View):
    template_name = "blog_app/post/create.html"

    def get(self, request, *args, **kwargs):
        post_form = PostForm()
        context = {"post_form": post_form, "saved_form": False}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        context = {"saved_form": True}
        return render(request, self.template_name, context)
