from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from django.views.generic.edit import FormMixin, FormView
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import View

from .models import Post, Comment
from .forms import CommentForm, EmailPostForm, UserLoginForm


class PostListView(ListView):
    paginate_by = 10
    template_name = 'blog/post-list.html'

    def get_queryset(self, **kwargs):
        queryset = Post.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        query = self.request.GET.get('query')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        if query:
            paginate_by = 8
            search = Post.objects.filter(title__contains=query)
            queryset = search
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get('tag_slug')
        context["query"] = self.request.GET.get('query')
        return context


class PostDetailView(FormMixin, DetailView):
    template_name = 'blog/post-detail.html'
    form_class = CommentForm

    def get_object(self):
        obj = get_object_or_404(Post, status='published',
                                slug=self.kwargs.get('slug'),
                                )
        return obj

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids)\
            .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
            .order_by('-same_tags', '-publish')[:4]

        comments = Comment.objects.filter(post=post, active=True)
        context["similar_posts"] = similar_posts
        context['comments'] = comments
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return self.form_valid(form)
        else:
            print("Invalid form")
            return self.form_invalid(form)


class PostShareView(FormView):
    form_class = EmailPostForm
    template_name = 'blog/post-share.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(
            Post, id=self.kwargs.get('post_id'))
        context["sent"] = False
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # Send Email
        cd = form.cleaned_data
        post = context['post']
        post_url = self.request.build_absolute_uri(
            post.get_absolute_url()
        )
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
        send_mail(subject, message, 'admin@myblog.com', [cd['to']])

        context['sent'] = True
        context['form'] = form
        return self.render_to_response(context)


def robots(request):
    template = 'robots.txt'
    return render(request, template)


class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = '/account/login.html'
    context_object = {"login_form": UserLoginForm}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = UserLoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Login Successful ! "
                                          f"Welcome {user.username}.")
                return redirect('/robots.txt')

            else:
                messages.error(request,
                               f"Invalid Login details: {username}, {password} "
                               f"are not valid username and password !!! Please "
                               f"enter a valid username and password.")
                return render(request, self.template_name, self.context_object)

        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context_object)

