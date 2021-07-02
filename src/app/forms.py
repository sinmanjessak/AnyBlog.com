from django import forms
from tinymce.widgets import TinyMCE
from .models import *


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostmodelForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    overview=forms.CharField(widget=forms.Textarea( attrs={
        'class':'form-control'
          
    }))
   
                          
    class Meta:
        model = Postmodel
        fields = ('title','overview','content','thumbnails','category','featured','previous_post','next_post')
        
        
class Commentform(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea( attrs={
        'class':'form-control',
        'placeholder':"Type your comment" ,
        'id':'usercomment'      
    }))
    class Meta:
        model= Commentmodel
        fields=('content',)
    