from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Question, Tag, Answer
from django.shortcuts import redirect



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
    question = Question.get_by_id(question_id)

    if request.method == 'POST':
        answer_text = request.POST.get('new_answer')
        if answer_text:
            Answer.objects.create(
                question=question,
                author=request.user,
                text=answer_text,
                created_at=timezone.now()
            )
            return redirect('question_detail', question_id=question.id)

    # question = next((q for q in QUESTIONS if q == question_id), None)
    if not question:
        return render(request, '404.html', status=404)

    return render(request, 'question-detail.html', {
        'question': question,
        'tags': TAGS,
        'best_members': MEMBERS,
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
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = USERS.get(login)
        if user and user['password'] == password:
            global CURRENT_USER
            CURRENT_USER = login
            return redirect('settings')
        error = 'Sorry, wrong password!'

    return render(request, 'login.html', {'error': error})

def register(request):
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

        if login in USERS:
            error = 'Sorry, this login is already registered!'
        elif any(user['email'] == email for user in USERS.values()):
            error = 'Sorry, this email address already registered!'
        elif password != password2:
            error = 'Passwords do not match!'
        else:
            USERS[login] = {
                'tags': TAGS,
                'email': email,
                'nickname': nickname,
                'password': password,
                'avatar': avatar
            }
            return redirect('login')

        return render(request, 'register.html', {
            'error': error,
            'login': login,
            'email': email,
            'nickname': nickname,
        })

    return render(request, 'register.html')