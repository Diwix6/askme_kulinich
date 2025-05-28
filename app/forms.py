from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Answer, Question, Tag, Profile


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Enter your email address')
    username = forms.CharField(required=True, label="Nickname", help_text='Enter your nickname')
    
    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = user.email
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile = user.profile
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return profile

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput) 


# class RegistrationForm(UserCreationForm):
#     profile_picture = forms.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)        


class AskForm(forms.Form):
    # tags = forms.CharField(widget=forms.Textarea, required=False, label="tags",help_text='Enter up to 5 tags assosiated with you question divided by \',\'')    
    title = forms.CharField(max_length=200, label="text", help_text='Enter the title of your question')
    content = forms.CharField(widget=forms.Textarea, help_text='Enter the content of your question')
    tags = forms.CharField(max_length=100)
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    #     label="Tags",
    # )    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags_list = tags.split(',')
        if (len(tags_list) > 5):
            raise forms.ValidationError('You can\'t add more than 5 tags')
        return tags_list

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def save(self, author):
        new_question = Question.objects.create(author=author, title=self.cleaned_data['title'], content=self.cleaned_data['content'])
        tags_list = self.cleaned_data['tags']
        for tag in tags_list:
            question_tag = Tag.objects.create_or_get_tag(tag)
            new_question.tags.add(question_tag)
        new_question.save()
        return new_question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Answer", help_text='Enter your answer to the question')
    class Meta:
        model = Answer
        fields = ('text',)

    def save(self, author, question):
        new_answer = Answer.objects.create(author=author, question=question, **self.cleaned_data)
        return new_answer
    

# class ProfileForm(forms.ModelForm):
#     profile_picture = forms.ImageField(required=False)
    
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name',)

#     def save(self, **kwargs):
#         user = super().save(**kwargs)
#         profile = user.profile
#         if (self.cleaned_data.get('profile_picture')):
#             profile.profile_pic = self.cleaned_data.get('profile_picture')
#             print(profile.profile_pic)
#             profile.save()
#         return user