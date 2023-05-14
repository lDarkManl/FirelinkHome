from django.forms import ModelForm, TextInput, Textarea, Form, BooleanField
from .models import Comment, Art, SubComment

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text']
		widgets = {
            'comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'placeholder': 'Текст комментария', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }

class AddArtForm(ModelForm):
	class Meta:
		model = Art
		fields = ['title', 'image', 'content', 'tags']
		widgets = {
			'title': TextInput(attrs={'placeholder': 'Введите название арта'})
		}
		
class SubCommentForm(ModelForm):
	class Meta:
		model = SubComment
		fields = ['sub_comment_text']
		widgets = {
            'sub_comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'placeholder': 'Ответить на комментарий', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }