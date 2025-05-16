from django.contrib import admin
from .models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

# admin.site.register(Profile)
# admin.site.register(Tag)
# admin.site.register(Question)
# admin.site.register(Answer)
# admin.site.register(QuestionLike)
# admin.site.register(AnswerLike)


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['user', 'avatar']

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['name']

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['title', 'text', 'author', 'tags', 'created_at', 'rating']

@admin.register(QuestionLike)
class QuestionLikenModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['user', 'question', 'value']

@admin.register(AnswerLike)
class AnswerLikeModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['user', 'answer', 'value']

@admin.register(Answer)
class AnswerModelAdmin(admin.ModelAdmin):
    link_display_fields  = ['question', 'author', 'text', 'created_at', 'is_correct', 'rating']

