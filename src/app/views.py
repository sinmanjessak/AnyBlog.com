from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views import  View
from.models import *
from accounts.models import Signup
from django.db.models import Count,Q
from app.forms import Commentform,PostmodelForm

def get_categories_count():
   queryset=Postmodel\
      .objects\
      .values('category__title')\
      .annotate(Count('category__title'))
   return queryset


def search(request):
   bloglistt=Postmodel.objects.all()
   q= request.GET.get("q")   
   if q:                     
      search_result= bloglistt.filter(Q(title__icontains=q)|Q(overview__icontains=q)).distinct()
   data={
      'search':search_result
   }
   return render(request,'search_result.html',data)


def get_author(user):
   qs= Author.objects.filter(user=user)
   if qs.exists():
      return qs[0]
   return None

      


class Index(View):
   def get(self,request):
      featured= Postmodel.objects.filter(featured=True)
      latest= Postmodel.objects.order_by('-timestamb')[0:3]
      
      data={
         'posts': featured,
         'latest': latest
      }
      return render(request,'index.html',data)
   
   def post(self,request):     
      postdata=request.POST
      email=postdata.get('email')
      new_signup= Signup()
      new_signup.email= email
      new_signup.save()
      return redirect('/')
   

      
         
   
   
class Blog(View):
   def get(self,request):
      category_count= get_categories_count()     
      bloglist= Postmodel.objects.all()    
      most_recent=Postmodel.objects.order_by('-timestamb')[:3]
      paginator= Paginator(bloglist,4)
      page_request= "page"
      page_number= request.GET.get("page_request")
      
      try:
         page_obj= paginator.page(page_number)
      except PageNotAnInteger:
         page_obj= paginator.page(1)
      except EmptyPage:
         page_obj= paginator.page(paginator.num_pages)
      data={
                
         'page_obj':page_obj ,
         'latest':most_recent,        
         'page_request':page_request,
         'category_count':category_count
         
                  
         }
      return render(request,'blog.html',data)
   

def Post(request,id):
      category_count= get_categories_count() 
      post=get_object_or_404( Postmodel,id=id)
      most_recent=Postmodel.objects.order_by('-timestamb')[:3]
      form=Commentform(request.POST or None)
      if request.user.is_authenticated:
         Postview.objects.get_or_create(user=request.user ,post=post)

      
      if request.method=='POST' and  form.is_valid(): 
         form.instance.user = request.user 
         form.instance.post = post                  
         form.save()
         return redirect(reverse("post-details",kwargs={
            'id':post.id
         }))
      else:
         form= Commentform()
         
      data={
         'post':post,
         'category_count':category_count,
         "latest":most_recent,
         'form':form
      }
      return render(request,'Post.html',data)
   
   
def post_create(request):
   title="Create Your"
   form =PostmodelForm(request.POST or None, request.FILES or None)
   author= get_author(request.user)
   if request.method=="POST":
      if form.is_valid():
         form.instance.author=author
         form.save()
         return redirect(reverse('post-details',kwargs={
            "id":form.instance.id
         }))
   data={
      "title":title,
      'form':form
   }
   return render(request,'post_created.html',data)
   

def post_update(request,id):
   title="Update Your"
   post=get_object_or_404( Postmodel,id=id)
   form =PostmodelForm(request.POST or None, request.FILES or None,instance=post)
   author= get_author(request.user)
   if request.method=="POST":
      if form.is_valid():
         form.instance.author=author
         form.save()
         return redirect(reverse('post-details',kwargs={
            "id":form.instance.id
         }))
   data={
      "title":title,
      'form':form
   }
   return render(request,'post_created.html',data)

def post_delete(request,id):
   post=get_object_or_404( Postmodel,id=id)
   post.delete()
   return redirect(reverse('post-list'))
   
      
      
   
      
      
      
      

