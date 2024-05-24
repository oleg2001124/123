from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Article, Comment, ArticleViewsCount, Like, Dislike
from .forms import LoginFrom, RegistrationForm, ArticleForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView, ListView
from django.contrib.auth.models import User
# Create your views here.





def author_articles(request, username):
    from django.utils.timezone import now
    user = get_object_or_404(User, username=username)
    articles = Article.objects.filter(author=user)
    total = sum([article.views for article in articles])
    days = (now() - user.date_joined).days
    comments_count = user.comment_set.all().count()
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    context = {
        'articles': articles,
        'days': days,
        'comments_count': comments_count,
        'total': total,
        'total_likes':total_likes,
        'total_dislikes': total_dislikes
    }
    return render(request, 'core/author_articles.html', context)


def home_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }

    return render(request, 'core/index.html', context)

class HomeView(ListView):
    model = Article
    template_name = 'core/index.html'
    context_object_name = 'articles'


class SearchResultView(HomeView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(name__iregex=query)


def about_view(request):
    return render(request, 'core/about.html')


def contacts_view(request):
    return render(request, 'core/contacts.html')


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = Article.objects.filter(category=category)
    is_active = str(category_id) in request.path

    context = {
        'id': category_id,
        'articles': articles,
        'is_active': is_active
    }
    return render(request, 'core/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()

            try:
                form.likes
            except Exception as e:
                Like.objects.create(comment=form)

            try:
                form.dislikes
            except Exception as e:
                Dislike.objects.create(comment=form)

            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

        comments = Comment.objects.filter(article=article)
        # comments = article.comment_set.all()
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        is_viewed = ArticleViewsCount.objects.filter(session_id=session_key, article=article)
        if is_viewed.count() == 0 and session_key != 'None':
            obj = ArticleViewsCount()
            obj.session_id = session_key
            obj.article = article
            obj.save()
            article.views += 1
            article.save()
        try:
            article.likes
        except Exception as e:
            Like.objects.create(article=article)

        try:
            article.dislikes
        except Exception as e:
            Dislike.objects.create(article=article)
        total_likes = article.likes.user.all().count()
        total_dislikes = article.dislikes.user.all().count()
        comment_total_likes = {comment.pk: comment.likes.user.all().count() for comment in comments}
        comment_total_dislikes = {comment.pk: comment.dislikes.user.all().count() for comment in comments}

        context = {
             'article': article,
             'form': form,
             'comments': comments,
             'total_likes': total_likes,
             'total_dislike': total_dislikes,
             'comment_total_likes': comment_total_likes,
             'comment_total_dislikes': comment_total_dislikes

    }
    return render(request, 'core/detail.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginFrom(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ЗАшли')
                return redirect('home')
    else:
        form = LoginFrom()
    context = {
        'form': form
    }

    return render(request, 'core/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(date=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт был создан')
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'core/register.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы зашли в ваш аккаунт')
    messages.info(request, 'Вы вышли с аккаунта')
    return redirect('home')


@login_required(login_url='login')
def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article_detail')
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'core/article_form.html', context)


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'core/article_form.html'


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'core/article_confirm_delete.html'
    success_url = '/'


def add_vote(request, obj_type, obj_id, obj_action):
    from django.shortcuts import get_object_or_404
    obj = None
    if obj_type == 'article':
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == 'comment':
        obj = get_object_or_404(Comment, pk=obj_id)
    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)
    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if obj_action == 'add_like':
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)

    if obj_action == 'add_dislike':
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)
    return redirect(request.environ['HTTP_REFERER'])

