from django import forms
from ..models import Post_Tmp, Post, Comment, Reaction

class CreatePostTmpForm(forms.ModelForm):
    class Meta:
        model = Post_Tmp
        #fields = "__all__"
        fields = [
                    "title",
                    "tag",
                    "text_probrem",
                    "text_solution",
                    "reference_url",
                  ]
        
    def clean_reference_url(self):
      reference_url = self.cleaned_data.get("reference_url")
      
      if reference_url != None:#nullチェック
        if 'http:' not in reference_url and 'https:' not in reference_url:
          raise forms.ValidationError("urlを正しく入力してください。")
      return reference_url