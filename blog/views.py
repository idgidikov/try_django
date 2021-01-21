from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
#from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm
from django.contrib.admin.views.decorators import staff_member_required

# def blog_post_detail_page(request,slug):
#     # queryset = BlogPost.objects.filter(slug = slug)
#     # if queryset.count() == 0:
#     #     raise Http404
#     # obj = queryset.first()
#     # obj = BlogPost.objects.get(slug=slug)
    
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = "blog_post_detail.html"
#     context = {"object": obj}
#     return render(request, template_name, context)

def blog_post_list_view(request):
    # list out objects
    #could be search
    #now = timezone.now() to do in models
    qs = BlogPost.objects.all().published() # queryset -> list of python object
    #qs = BlogPost.objects.filter(publish_date__lte=now)
    if request.user.is_authenticated:
       my_qs = BlogPost.objects.filter(user=request.user)
       qs = (qs | my_qs).distinct()
    template_name = "blog/list.html"
    context = {"object_list" : qs}
    return render(request,template_name,context)

@staff_member_required
#@login_required
def blog_post_create_view(request):
    #create objects
    #? use a form
    # request.user -> return something
    form = BlogPostModelForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
       # obj = BlogPost.objects.create(**form.cleaned_data)
        form = BlogPostModelForm()
        

    template_name = "form.html"
    context = {"form" : form}
    return render(request,template_name,context)

def blog_post_detail_view(request,slug):
    # 1object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/detail.html"
    context = {"object": obj}
    return render(request,template_name,context)


@staff_member_required
def blog_post_update_view(request,slug):
    
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
    template_name = "form.html"
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request,slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/delete.html"
    if request.method == "POST" :
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)