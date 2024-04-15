from django import forms

from posts.models import Contact, Comment, Posts


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("body", )


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('category', 'title', 'text', 'tags', 'image')
