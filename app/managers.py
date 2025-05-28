from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import datetime

class QuestionQuerySet(models.QuerySet):
    def new(self):
        return self.order_by('-time_created')

    def hot(self):
        return self.order_by('-rating')

    def questions_by_tag(self, tag: str):
        return self.filter(tags__name=tag)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(model=self.model, using=self._db)
    
    def get_by_id(self, id: int):
        try:
            question = self.get(pk=id)
        except ObjectDoesNotExist:
            return None
        return question

    def new(self):
        try:
            new_questions = self.get_queryset().new()[:100]
        except ObjectDoesNotExist:
            return None
        return new_questions
    
    def hot(self):
        try:
            hot_questions = self.get_queryset().hot()[:100]
        except ObjectDoesNotExist:
            return None
        return hot_questions

    def questions_by_tag(self, tag: str):
        try:
            questions = self.get_queryset().questions_by_tag(tag)
        except ObjectDoesNotExist:
            return None
        return questions

    def count_rating(self):
        rating = self.reactions__positive.filter(positive = True)
        rating -= self.reactions__positive.filter(positive = False)
        self.rating = rating
        return rating


class AnswerManager(models.Manager):
    def count_rating(self):
        rating = self.reactions__positive.filter(positive = True)
        rating -= self.reactions__positive.filter(positive = False)
        self.rating = rating
        return rating
    

class TagManager(models.Manager):
    def popular_tags(self, count: int):
        # three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
        return self.annotate(total_questions=models.Count('question')).order_by('-total_questions')[:count]
    
    def create_or_get_tag(self, tag: str):
        tag = ''.join(tag.split())
        try:
            tag_obj = self.get(name=tag)
        except ObjectDoesNotExist:
            tag_obj = self.create(name=tag)
        return tag_obj


class ProfileQuerySet(models.QuerySet):   
    def profile_by_username(self, username: str):
        return self.get(user__username=username)      


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(model=self.model, using=self._db)

    def profile_by_username(self, username: str):
        try:
            user = self.get_queryset().profile_by_username(username)
        except ObjectDoesNotExist:
            return None
        return user
    
    def count_rating(self) -> int:
        rating = self.reaction__positive.filter(positive = True)
        rating -= self.reaction__positive.filter(positive = False)
        self.rating = rating
        return rating
    
    def best_members(self, count: int):
        return self.all().order_by('-rating')[:count]


class ReactionManager(models.Manager):
    def add_reaction(self, author, object, positive):
        if (positive == 'true'):
            positive = True
        else:
            positive = False

        obj_type = ContentType.objects.get_for_model(object)
        try:
            reaction = self.get(author=author, content_type=obj_type, object_id=object.id)
            object.author.delete_vote(reaction.positive)
            object.delete_vote(reaction.positive)
            reaction.delete()
            if (reaction.positive != positive):
                self.create(author=author, positive=positive, content_type=obj_type, object_id=object.id)
                object.author.add_vote(positive)
                object.add_vote(positive)

        except ObjectDoesNotExist:
            self.create(author=author, positive=positive, content_type=obj_type, object_id=object.id)
            object.author.add_vote(positive)
            object.add_vote(positive)

        return object.rating
        
  