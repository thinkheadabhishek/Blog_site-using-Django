from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view() , name="starting-page"),
    path("posts" , views.Posts.as_view() , name="all-posts-page"),
    path("posts/<slug:slug>" , views.PostDetails.as_view()  , name="post-details-page"),
    path("read-later" , views.ReadLaterView.as_view() , name="read-later-page"),
]