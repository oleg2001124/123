from django.urls import path
from . import views

urlpatterns = [


    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('categories/<int:category_id>', views.category_articles, name='category_articles'),
    path('articles/<int:article_id>', views.article_detail, name='article_detail'),
    path('article/create/', views.create_article_view, name='create'),
    path('article/<int:pk>/update/', views.UpdateArticle.as_view(), name='update'),
    path('article/<int:pk>/delete/', views.DeleteArticle.as_view(), name='delete'),
    path('users/<str:username>/articles/', views.author_articles, name='author_articles'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('<str:obj_type>/<int:obj_id>/<str:obj_action>/', views.add_vote, name='add_vote'),
    path('search/', views.SearchResultView.as_view(), name='search')
]
