from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import models

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def hot(self):
        return self.order_by('-rating')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', related_name='questions')
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    @staticmethod
    def get_by_id(id):
        return Question.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return Question.objects.all()

    @staticmethod
    def new():
        return Question.objects.order_by('-created_at')

    def __str__(self):
        return self.title

    def get_url(self):
        return f"/question/{self.pk}/"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    @staticmethod
    def get_by_id(id):
        return Answer.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return Answer.objects.all()

    @staticmethod
    def new():
        return Answer.objects.order_by('-created_at')

    def __str__(self):
        return f"Answer by {self.author.username}"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    @staticmethod
    def get_by_id(id):
        return Tag.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return Tag.objects.all()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    @staticmethod
    def get_by_id(id):
        return Profile.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return Profile.objects.all()

    @staticmethod
    def new():
        return Profile.objects.order_by('-created_at')
    
    def __str__(self):
        return self.user.username


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    @staticmethod
    def get_by_id(id):
        return QuestionLike.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return QuestionLike.objects.all()

    class Meta:
        unique_together = ('user', 'question')
    
    @staticmethod
    def new():
        return Answer.objects.order_by('-created_at')


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    @staticmethod
    def get_by_id(id):
        return AnswerLike.objects.get(id=id)

    @staticmethod
    def get_all_objects():
        return AnswerLike.objects.all()

    class Meta:
        unique_together = ('user', 'answer')

    @staticmethod
    def new():
        return Answer.objects.order_by('-created_at')


def paginate(request, queryset, per_page=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
