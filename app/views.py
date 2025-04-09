from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse


QUESTIONS  = [
    {
        'id': 1,
        'title': 'How to build a moon park ?',
        'text': 'Guys, I have trouble with a moon park. Can\'t find the black-jack...',
        'tags': ['black-jack', 'bender'],
        'votes': 5,
        'answer_count': 3,
        'image_url': 'https://i.namu.wiki/i/dnZQPPFWEI0SD-tpxtirXzuHWUcFeklRAlSWlVbQtDaEUcbrvZQ3RHXs5jdNcPC4xGXIKchwwaPO1qrELmhK5ujn0A0zT7m3el8C0NvdGWL0e0Q9Kbn6KjPrDSH5d7RUPU8u8m866z3pnin4N21hjg.webp',
        'answers': [
            {'text': 'Russia is huge and needs to be made habitable.', 'votes': 5, 'is_correct': True},
            {'text': 'Same thought here.', 'votes': 3, 'is_correct': False},
        ]
    },
    {
        "id": 2,
        "title": "How to use Django templates?",
        "description": "I'm trying to render data using Django templates. Any tips?",
        "image_url": "https://i.namu.wiki/i/apGZ4E5LnxUul1137rSThfzQqQUDBEBjHQnPnCJs89sbE1GQkQ6tGg73RfHPhgtU7J8Xgxow1tj4dZ5FsYRzTAHWvszjjPdcVJwzu8lASckk8Pnq0vMVI4i8Qo7EbOgv12-Z5R7-vdhRViRKn7VQhg.webp",
        "votes": 5,
        "answers_count": 3,
        "tags": ["django", "templates", "python"], 
        'answers': [
            {'text': 'Russia is huge and needs to be made habitable.', 'votes': 5, 'is_correct': True},
            {'text': 'Same thought here.', 'votes': 3, 'is_correct': False},
        ]
    },
    {
        "id": 3,
        "title": "How does Python list comprehension work?",
        "description": "I'm confused about how list comprehensions work in Python.",
        "image_url": "https://i.namu.wiki/i/5MDQI0Cof2M500ftaX-ZC92csXtOvDKOYj50Z2E5P3Su0LdDL_DVDmkpgc2Rc4zNRs3ZjDT0xqQ3OLgplzAXFc53fc7rNk_8PKnu6XaDg4DQy9M96-m7_DHBvxbW0ojkGizMM6ZNErm4G58vsnSrUg.webp",
        "votes": 8,
        "answers_count": 5,
        "tags": ["python", "lists"], 
        'answers': [
            {'text': 'Russia is huge and needs to be made habitable.', 'votes': 5, 'is_correct': True},
            {'text': 'Same thought here.', 'votes': 3, 'is_correct': False},
        ],
    },
    {
        "id": 4,
        "title": "What is the difference between a list and a tuple in Python?",
        "description": "Can anyone explain the key differences between a Python list and a tuple?",
        "image_url": "",
        "votes": 12,
        "answers_count": 4,
        "tags": ["python", "lists", "tuples"],
        "answers": [
            {"text": "Lists are mutable, while tuples are immutable.", "votes": 6, "is_correct": True},
            {"text": "Both are the same, just different names.", "votes": 2, "is_correct": False},
        ],
    },
    {
        "id": 5,
        "title": "What is a decorator in Python?",
        "description": "I'm having trouble understanding Python decorators. Can someone explain them in simple terms?",
        "image_url": "",
        "votes": 15,
        "answers_count": 3,
        "tags": ["python", "decorators"],
        "answers": [
            {"text": "A decorator is a function that modifies the behavior of another function.", "votes": 9, "is_correct": True},
            {"text": "Decorators are just for styling your code.", "votes": 1, "is_correct": False},
        ],
    },
    {
        "id": 6,
        "title": "How to use list comprehension with if conditions?",
        "description": "Can you give examples of how to use list comprehension with an if condition in Python?",
        "image_url": "",
        "votes": 10,
        "answers_count": 4,
        "tags": ["python", "list comprehension"],
        "answers": [
            {"text": "[x for x in range(10) if x % 2 == 0]", "votes": 5, "is_correct": True},
            {"text": "[x for x in range(10) if x > 5]", "votes": 3, "is_correct": False},
        ],
    },
]

TAGS = ["django", "python", "html", "css", "bootstrap", "flask"]
MEMBERS = ["Alice", "Bob", "Charlie", "Dana"]

USERS = {
    'dr_pepper': {
        'email': 'dr.pepper@mail.ru',
        'nickname': 'Dr. Pepper',
        'password': '12345678',
        'avatar': None
    }
}

# Текущий пользователь (вместо сессии)
CURRENT_USER = 'dr_pepper'


def index(request):
    paginator = Paginator(QUESTIONS, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "questions": QUESTIONS,
        "tags": TAGS,
        "best_members": MEMBERS,
        "page": page_obj
    }
    return render(request, 'index.html', context)

def ask_question(request):
    search_query = request.GET.get('search_query')  # Получаем текст из поля поиска
    if search_query:
        # Обрабатываем запрос
        print(f"User searched for: {search_query}")
    return render(request, 'ask-question.html', {
        'tags': TAGS,
        'best_members': MEMBERS,
        'text': search_query,
    })


def question_detail(request, question_id):
    question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    if not question:
        return render(request, '404.html', status=404)

    return render(request, 'question-detail.html', {
        'question': question,
        'tags': TAGS,
        'best_members': MEMBERS,
    })


def tag_view(request, tag):
    filtered_questions = [q for q in QUESTIONS if tag in q['tags']]
    return render(request, 'tag-question.html', {
        'tag': tag,
        'questions': filtered_questions,
        'tags': TAGS,
        'best_members': MEMBERS,
    })

def settings(request):
    user = USERS.get(CURRENT_USER)
    if request.method == 'POST':
        user['email'] = request.POST.get('email')
        user['nickname'] = request.POST.get('nickname')
        user['avatar'] = request.FILES.get('avatar')
        return redirect('settings')  # обновить страницу

    return render(request, 'settings.html', {
        'login': CURRENT_USER,
        'email': user['email'],
        'nickname': user['nickname'],
    })

def login(request):
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