from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Question, Tag, Answer, Profile, QuestionLike
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, AskForm, AnswerForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import Reaction

def index(request):
    QUESTIONS = Question.get_all_objects()
    for i in QUESTIONS:
        print(i.tags)
    paginator = Paginator(QUESTIONS, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    TAGS = Tag.get_all_objects()
    MEMBERS = User.objects.all()
    context = {
        "questions": page_obj,
        "tags": TAGS,
        "best_members": MEMBERS,
        "page": page_obj
        # "answers_count": counter
    }
    return render(request, 'index.html', context)

def hot_questions(request):
    hot_questions = Question.objects.order_by('-rating')[:10]
    return render(request, 'layouts/question_list.html', {'questions': hot_questions})

def ask_question(request):
    if request.method == 'POST':
        print('request is POST')
        form = AskForm(request.POST)
        if form.is_valid():
            print('form is valid')
            # question = form.save(commit=False)
            # question.author = request.user
            # # question.title = form.cleaned_data['title']
            # # question.text = form.cleaned_data['content']
            # question.save()
            # form.save_m2m()
            author=request.user.profile
            q = Question.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['content'],
                author=author,
            )
            raw_tags = form.cleaned_data['tags']
            name_tags = raw_tags[0].split('/')
            author.add_question()
            print(raw_tags, name_tags)
            for name in name_tags:
                tag, created = Tag.objects.get_or_create(name=name.lower())
                q.tags.add(tag)
            return redirect('question_detail', question_id=q.id)
        else:
            print('form is not valid')
            for field, errors in form.errors.items():
                print(f"Error in {field}: {errors}")
            form = AskForm()
    else:
        form = AskForm()
    return render(request, 'ask-question.html', {'form': form})
    

def question_detail(request, question_id):
    QUESTIONS = Question.get_all_objects()
    TAGS = Tag.get_all_objects()
    MEMBERS = User.objects.all()
    question = get_object_or_404(Question, id=question_id)
    answer = Answer.objects.filter(question=question)

    # if request.user.is_authenticated:
    #     user_has_voted = Vote.objects.filter(question=question, user=request.user).exists()
    # else:
    #     user_has_voted = False
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                question=question,
                author=request.user,
                text=form.cleaned_data['text'],
                created_at=timezone.now(),
                rating=0,
                is_correct=False
            )
            # return redirect(f'question_detail/{question.id}/#answer-{answer.id}')
            return redirect('question_detail', question_id=question.id)
        # else:
        #     print('request is not POST')
        #     print('error:', form.errors)
    else:
        form = AnswerForm()
    # question = next((q for q in QUESTIONS if q == question_id), None)
    if not question:
        return render(request, '404.html', status=404)

    return render(request, 'question-detail.html', {
        'question': question,
        'tags': TAGS,
        'best_members': MEMBERS,
        'form': form,
    })


def tag_view(request, tag):
    QUESTIONS = Question.get_all_objects()
    TAGS = Tag.get_all_objects()
    MEMBERS = User.objects.all()
    filtered_questions = [q for q in QUESTIONS if tag in [t.name for t in q.tags.all()]]
    return render(request, 'tag-question.html', {
        'tag': tag,
        'questions': filtered_questions,
        'tags': TAGS,
        'best_members': MEMBERS,
    })

def settings(request):
    TAGS = Tag.get_all_objects()
    USERS = User.objects.all()
    user = USERS.get(CURRENT_USER)
    if request.method == 'POST':
        user['email'] = request.POST.get('email')
        user['nickname'] = request.POST.get('nickname')
        user['avatar'] = request.FILES.get('avatar')
        return redirect('settings')

    return render(request, 'settings.html', {
        'login': CURRENT_USER,
        'tags': TAGS,
        'email': user['email'],
        'nickname': user['nickname'],
    })

def login(request):
    USERS = User.objects.all()
    error = None
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        continue_url = request.POST.get('next', 'index')
        user = authenticate(request, username=username, password=password)
        # user = USERS.get(login)
        # if user and user['password'] == password:
        #     global CURRENT_USER
        #     CURRENT_USER = login
        #     return redirect('settings')
        if user is not None:
            auth_login(request, user)
            return redirect(continue_url)
        else:
            messages.error(request, 'Wrong login or password')
            
    return render(request, 'login.html')

def signup(request):
    TAGS = Tag.get_all_objects()
    USERS = User.objects.all()
    error = None
    if request.method == 'POST':
        login = request.POST.get('login')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')
        if User.objects.filter(username=nickname).exists():
            messages.error(request, 'Sorry, this login is already registered!')
        else:
            # user = User.objects.create_user(username=nickname, email=email, password=password)
            auth_login(request, user)
            return redirect('index')

        return render(request, 'signup.html', {
            'error': error,
            'login': login,
            'email': email,
            'nickname': nickname,
        })
    return render(request, 'signup.html')


def logout_views(request):
    next_url = request.GET.get('next', 'index')
    logout(request)
    return redirect(next_url)


@login_required
def edit_profile(request):
    profile = request.user.profile
    # profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
        else:
            print(form.errors)
    else:
        # form = ProfileForm(instance=profile, user=request.user)
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@csrf_protect
def answer_vote_handler(request):
    print('answer_vote_handler')
    if (request.user.is_anonymous):
        return JsonResponse({'error': 1, 'message': 'You have to login for voting!'})
    
    answer_id = request.POST.get('answer_id')
    positive = request.POST.get('positive')
    answer = get_object_or_404(Answer, id=answer_id)
    if (answer.author != request.user.profile):
        rating = Reaction.objects.add_reaction(author=request.user.profile, object=answer, positive=positive)
    else:
        return JsonResponse({'error': 1, 'message': 'You can\'t rate self-created objects!'})
    return JsonResponse({'error': 0, 'rating': rating})


@csrf_protect
def question_vote_handler(request):
    print('question_vote_handler')
    if (request.user.is_anonymous):
        return JsonResponse({'error': 1, 'message': 'You have to login for voting!'})
    
    question_id = request.POST.get('question_id')
    positive = request.POST.get('positive')
    question = get_object_or_404(Question, id=question_id)
    # if not hasattr(request.user, 'profile'):
        # print('User has no profile')
        # return JsonResponse({'message': 'User has no profile'}, status=400)
    if (question.author != request.user.profile):
        print(request.user, question.author)
        print('question.author != request.user')
        rating = Reaction.objects.add_reaction(author=request.user, object=question, positive=positive)
    else:
        print('question.author == request.user')
        return JsonResponse({'error': 1, 'message': 'You can\'t rate self-created objects!'})
    print('rating:', rating)
    return JsonResponse({'error': 0, 'rating': rating})