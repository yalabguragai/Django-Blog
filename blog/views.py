from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import (ListView,
                                 DetailView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView
  )
from .models import post

# posts=[
# {
#     'author':'Yalab Guragai',
#     'title':'blog Post 1',
#     'content':'First  post Content',
#     'date_posted':'May 7,2020'
# },
# {
#     'author':'Preyas Guragai',
#     'title':'blog Post 2',
#     'content':'Second  post Content',
#     'date_posted':'May 8,2020'
# }
# ]

def home(request):
    context={
    'postss':post.objects.all()
    }
    #Django  Shortcut method to render the template
    #render function still return the Httpresponse
    #done after the settings of blog is copied to settings of the project
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'  #<app</<model>_<viewtype>.html
    context_object_name = 'postss'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'  #<app</<model>_<viewtype>.html
    context_object_name = 'postss'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #take that instance and set the author equal to current login useer
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #take that instance and set the author equal to current login useer
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url='/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request,'blog/about.html',{'title':'About'})


