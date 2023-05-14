from django.forms import ModelForm, TextInput, Textarea, Form, BooleanField
from .models import Comment, Track, SubComment

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text']
		widgets = {
            'comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'placeholder': 'Текст комментария', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }


class AddTrackForm(ModelForm):
	class Meta:
		model = Track
		fields = ['track_title', 'track', 'image']
		widgets = {
			'track_title': TextInput(attrs={'placeholder': 'Введите название трека'})
		}

class SubCommentForm(ModelForm):
	class Meta:
		model = SubComment
		fields = ['sub_comment_text']
		widgets = {
            'sub_comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'placeholder': 'Ответить на комментарий', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }