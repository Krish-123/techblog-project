from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('posts',views.IndexView.as_view(),name='post_list'),     #Index page
    path('details/post<int:pk>',views.PostDetailView.as_view(),name='post_detail'),     #Detail view page
    path('details/post<int:pk>/like',views.PostNewLikeView.as_view(),name='like'),    #Like View
    path('about',views.AboutView.as_view(),name='about'),    #About page
    path('post/new',views.CreatePostView.as_view(),name='post_new'),
    path('post/edit/post<int:pk>',views.PostUpdateView.as_view(),name='post_edit'),
    path('post/delete/post<int:pk>',views.PostDeleteView.as_view(),name='post_remove'),
    path('drafts',views.DraftListView.as_view(),name='post_draft_list'),
    path('post/post<int:pk>/comment',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/post<int:pk>/approve',views.comment_approve,name='comment_approve'),
    path('comment/post<int:pk>/remove',views.comment_remove,name='comment_remove'),
    path('post/publish/post<int:pk>',views.post_publish,name='post_publish'),
]