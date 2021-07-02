from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()
class Postview(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   post=models.ForeignKey('Postmodel',on_delete=models.CASCADE)
   
   def __str__(self):
      return str(self.user.username)
   


class Author(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   profile_picture=models.ImageField()
   
   def __str__(self):
      return str(self.user)
   
class Commentmodel(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   timestamb= models.DateTimeField(auto_now_add=True)
   content=models.TextField()
   post=models.ForeignKey('Postmodel',related_name="comments",on_delete=models.CASCADE)
   
   def __str__(self):
      return str(self.user.username)
   
  
   
class Category(models.Model):
   title=models.CharField(max_length=25)
   
   def __str__(self):
      return self.title
      
   
   
class Postmodel(models.Model):
   title=models.CharField(max_length=200)
   overview=models.CharField(max_length=250)
   content = HTMLField()
   timestamb=models.DateTimeField(auto_now_add=True)
   # view_count= models.IntegerField(default=0)
   # comment=models.IntegerField(default=0)
   author= models.ForeignKey(Author, on_delete=models.CASCADE)
   thumbnails=models.ImageField()
   category=models.ManyToManyField(Category)
   previous_post=models.ForeignKey('self',related_name='previous',on_delete=models.SET_NULL,blank=True,null=True)
   next_post=models.ForeignKey('self',related_name='next',on_delete=models.SET_NULL,blank=True,null=True)
   featured =models.BooleanField()
   
   def __str__(self):
      return self.title
   
   def get_absolute_url(self):
      return reverse('post-details', kwargs={'id':self.id})
   
   def get_update_url(self):
      return reverse('post-update', kwargs={'id':self.id})
   
   def get_delete_url(self):
      return reverse('post-delete', kwargs={'id':self.id})
   
   @property
   def get_comments(self):
      return self.comments.all()
   
   @property
   def comment_count(self):
      return Commentmodel.objects.filter(post=self).count()
   
   @property
   def view_count(self):
      return Postview.objects.filter(post=self).count()
   

   

   
   
   