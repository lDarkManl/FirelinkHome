from django.forms import *
from .models import Article, Comment, SubComment
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text']
		widgets = {
            'comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'id':'comment', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }

class AddArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ['article_title', 'article_image', 'article_game', 'article_category', 'article_video', 'article_content', 'is_published']
		widgets = {
			'article_content': Textarea(attrs={'rows': 3, 'maxlength': 500, 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'}),
		}
		
class AddPhotoForm(Form):
	photo = ImageField(required=False)

class SubCommentForm(ModelForm):
	class Meta:
		model = SubComment
		fields = ['sub_comment_text']
		widgets = {
            'sub_comment_text': Textarea(attrs={'rows': 3, 'maxlength': 500, 'id':'sub_comment', 'oninput':'auto_grow(this)', 'class':'form-control bg-dark text-light'})
        }