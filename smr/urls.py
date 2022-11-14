from django.urls import path
from . import views

urlpatterns = [
    # index 메인페이지
    path('', views.index.as_view(), name='index'),
    # post 관련 페이지
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/', views.PostAllListView.as_view(), name='post-list'),
    path('postlist/<int:user_id>/posts/', views.UserPostListView.as_view(), name='user-post-list'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name="post-detail"),
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name="post-update"),
    path('posts/new/<int:wkout_id>', views.PostCreateView.as_view(), name="post-create"),
    
    # 운동 기록 페이지
    path('wkoutlist/', views.WkoutListView.as_view(), name="wkout-list"),
    path("wkoutlist/new/", views.WkoutCreateView.as_view(), name='wkout-create'),
    path('wkoutlist/<int:wkout_id>/edit/', views.WkoutUpdateView.as_view(), name="wkout-update"),
    path('wkout/<int:pk>/delete/', views.WkoutDeleteView.as_view(), name='wkout-delete'),
    # 운동 기록 작성 페이지
    path('workrecord/<int:wkout_id>/', views.WkRecordCreateView.as_view(), name='wkrecord-list'),
    path('workrecord/<int:wkrecord_id>/edit/', views.WkRecordUpdateView.as_view(), name='wkrecord-update'),
    path('workrecord/<int:wkout_id>/<int:pk>/delete/', views.WkRecordDeleteView.as_view(), name="wkrecord-delete"),
    # 프로필 페이지
    path('users/<int:user_id>/', views.ProfileView.as_view(), name="profile"),
    path('set-profile/', views.ProfileSetView.as_view(), name="profile-set"),
    path('edit-profile/', views.ProfileUpdateView.as_view(), name="profile-update"),
    # 댓글
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    # 좋아요
    path(
        'like/<int:content_type_id>/<int:object_id>/',
        views.ProcessLikeView.as_view(),
        name='process-like'
    ),
    # 팔로우
    path(
        'users/<int:user_id>/follow/',
        views.ProcessFollowView.as_view(),
        name='process-follow'
    ),
    # 루틴 카피
    path(
        'copyroutine/<int:wkout_id>/new/', 
        views.CopyWkoutView.as_view(), 
        name='copy-wkout'
    ),
    path(
        'copyroutine/<int:wkout_id>/wkoutlist/new/', 
        views.CopyWkoutCreateView.as_view(), 
        name='copy-wkout-create'
    )
]