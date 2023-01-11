from django.shortcuts import render
from django.views import View
from django.views.generic import ListView , DetailView
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from datetime import date
from .models import Post
from .forms import CommentForm
from django.urls import reverse
# Create your views here.

class Index(ListView):
    template_name = "blogs/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class Posts(ListView):
    template_name = "blogs/posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


class PostDetails(View):
    # template_name = "blogs/post_details.html"
    # model = Post
    def is_stored_post(self, request , post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self , request , slug):
        try:
            post = Post.objects.get(slug = slug)
            response = render(request, "blogs/post_details.html",{
                "post" : post,
                "tags" : post.tags.all(),
                "comment_form" : CommentForm(),
                "comments" : post.comments.all().order_by("-id"),
                "saved_for_later" : self.is_stored_post(request , post.id)
            })
            return HttpResponse(response)
        except:
            raise Http404("File not found")
    
    def post(self , request , slug) :
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug = slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment_form.save()
            return HttpResponseRedirect(reverse("post-details-page" , args=[slug]))

        context = {
                "post" : post,
                "tags" : post.tags.all(),
                "comment_form" : CommentForm(),
                "comments" : post.comments.all().order_by("-id"),
                "saved_for_later" : self.is_stored_post(request , post.id)
        }
        return render(request, "blogs/post_details.html" , context)

        


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")   # returns id of stored data
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
            
        return render(request, "blogs/stored-posts.html" , context)

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts :
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")






    
    # def get(self , request):
    #     all_posts = Post.objects.all()
    #     response = render(request, "blogs/posts.html",{
    #         "posts" : all_posts
    #     })
    #     return HttpResponse(response)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context

















# all_posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Maximilian",
#         "date": date(2021, 7, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
#         "content": """
#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     },
# ]