from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Question, Tag, Answer, Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, AskForm, AnswerForm
from django.shortcuts import get_object_or_404


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
            q = Question.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['content'],
                author=request.user,
            )
            raw_tags = form.cleaned_data['tags']
            name_tags = raw_tags[0].split('/')
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
    MEMBERS = User.objects.all()
    TAGS = Tag.get_all_objects()
    search_query = request.GET.get('search_query')
    if search_query:
        print(f"User searched for: {search_query}")
    return render(request, 'ask-question.html', {
        'tags': TAGS,
        'best_members': MEMBERS,
        'text': search_query,
    })


def question_detail(request, question_id):
    QUESTIONS = Question.get_all_objects()
    TAGS = Tag.get_all_objects()
    MEMBERS = User.objects.all()
    question = get_object_or_404(Question, id=question_id)
    answer = Answer.objects.filter(question=question)

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
        else:
            print('request is not POST')
            print('error:', form.errors)
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
            user = User.objects.create_user(username=nickname, email=email, password=password)
            auth_login(request, user)
            return redirect('index')
        # if login in USERS:
        #     error = 'Sorry, this login is already registered!'
        # elif any(user['email'] == email for user in USERS.values()):
        #     error = 'Sorry, this email address already registered!'
        # elif password != password2:
        #     error = 'Passwords do not match!'
        # else:
        #     USERS[login] = {
        #         'tags': TAGS,
        #         'email': email,
        #         'nickname': nickname,
        #         'password': password,
        #         'avatar': avatar
        #     }
        #     return redirect('login')

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
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'edit_profile.html', {'form': form})