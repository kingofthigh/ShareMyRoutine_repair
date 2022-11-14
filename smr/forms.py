from django import forms
from .models import User, Wkout, WkRecord, Comment, Part, Exercise, Post, Profile

class WkoutMemoForm(forms.ModelForm):
    class Meta:
        model = Wkout
        fields = ["memo","ex_part",]

        widgets = {
            "ex_part": forms.Select,
        }

class WkRecordForm(forms.ModelForm):
    class Meta:
        model = WkRecord
        fields = ["exercise", "weight", "reps",]

        widgets ={
            "exercise": forms.Select,
        }

        def clean(self):
            form_data = self.cleaned_data
            if form_data['weight'] < 0:
                raise forms.ValidationError['0이상의 무게를 입력해주세요']
            return form_data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]

        widgets = {
            "content": forms.Textarea,
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "nickname",
            "profile_pic",
            "intro",
            "career",
            "age",
            "height",
            "weight",
            "muscle_mass",
            "body_fat",
            "squat",
            "deadlift",
            "benchpress",
        ]
        widget = {
            "intro": forms.Textarea,
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]
        widgets = {
            'content': forms.Textarea,
        }

