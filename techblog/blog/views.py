from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import PostModel,CommentModel
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(ListView):
    model = PostModel
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    # paginate_by = 10
    # paginate_orphans = 5

    def get_queryset(self):
        return PostModel.objects.filter(published_date__lte = timezone.now()).order_by('-published_date','title')



class PostDetailView(DetailView):
    model = PostModel
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

class PostNewLikeView(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs['pk']
        post = PostModel.objects.get(pk=pk)
        post.likes+=1
        post.save()

        return HttpResponseRedirect(reverse('blog:detail',kwargs={'pk':post.pk}))

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    
    form_class = PostForm
    model = PostModel
    template_name = 'blog/post_form.html'

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    
    form_class = PostForm
    model = PostModel
    template_name = 'blog/post_form.html'

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = PostModel
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_confirm_delete.html'

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = PostModel
    template_name = 'blog/post_drafts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return PostModel.objects.filter(published_date__isnull = True).order_by('-created_date')


#########################################Comments######################################

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(PostModel,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(CommentModel,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(CommentModel,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(PostModel,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=post.pk)