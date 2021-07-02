from django.db import models


class Signup(models.Model):
   email= models.EmailField()
   added_time= models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
      return self.email
