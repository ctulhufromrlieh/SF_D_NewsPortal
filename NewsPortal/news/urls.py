from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, SearchedPostList, PostDetail
from .views import NewCreate, NewUpdate, NewDelete


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('search/', SearchedPostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', NewCreate.as_view(), name='new_create'),
   path('<int:pk>/edit/', NewUpdate.as_view(), name='new_update'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   # path('subscriptions/', subscriptions, name='subscriptions'),
]