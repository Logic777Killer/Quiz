from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Topic, Survey
from .forms import SurveyForm
from .forms import QuestionForm
from .models import Question, Choice, Answer
from django.db.models import Count



def index(request):
    return render(request, 'surveys/index.html')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'surveys/profile.html', {"profile": profile})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        gender = request.POST.get("gender")
        country = request.POST.get("country")
        age = request.POST.get("age")

        if password1 != password2:
            return render(request, "surveys/register.html", {"error": "Пароли не совпадают"})

        if User.objects.filter(username=username).exists():
            return render(request, "surveys/register.html", {"error": "Такой логин уже существует"})

        user = User.objects.create_user(username=username, password=password1)

        Profile.objects.create(
            user=user,
            gender=gender,
            country=country,
            age=age
        )

        return redirect("/")

    return render(request, "surveys/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "surveys/login.html", {"error": "Неверный логин или пароль"})

        login(request, user)
        return redirect("/")

    return render(request, "surveys/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile.gender = request.POST.get("gender")
        profile.country = request.POST.get("country")
        profile.age = request.POST.get("age")
        profile.save()
        return redirect("/profile/")

    return render(request, "surveys/edit_profile.html", {"profile": profile})


def topics_list(request):
    topics = Topic.objects.all()
    return render(request, "surveys/topics_list.html", {"topics": topics})


def topic_surveys(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    surveys = Survey.objects.filter(topic=topic)
    return render(request, "surveys/topic_surveys.html", {
        "topic": topic,
        "surveys": surveys
    })


def create_survey(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.author = request.user
            survey.save()
            return redirect(f'/survey/{survey.id}/add-questions/')
    else:
        form = SurveyForm()

    return render(request, 'surveys/create_survey.html', {'form': form})

def add_questions(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.survey = survey
            question.save()

            # сохраняем варианты
            choices = request.POST.getlist('choices[]')
            for c in choices:
                if c.strip():
                    Choice.objects.create(question=question, text=c.strip())

            return redirect(f'/survey/{survey.id}/add-questions/')
    else:
        q_form = QuestionForm()

    questions = Question.objects.filter(survey=survey)

    return render(request, 'surveys/add_questions.html', {
        'survey': survey,
        'q_form': q_form,
        'questions': questions
    })

def delete_survey(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    if survey.author != request.user:
        return redirect('/')

    survey.delete()
    return redirect('/')

def take_survey(request, survey_id, question_index):
    survey = Survey.objects.get(id=survey_id)
    questions = list(Question.objects.filter(survey=survey))

    if not questions:
        return render(request, 'surveys/empty_survey.html')

    if question_index >= len(questions):
        return render(request, 'surveys/survey_finished.html')

    question = questions[question_index]
    choices = Choice.objects.filter(question=question)

    if request.method == 'POST':
        choice_id = request.POST.get('choice')

        if not choice_id:
            return render(request, 'surveys/take_survey.html', {
                'survey': survey,
                'question': question,
                'choices': choices,
                'error': 'Выберите вариант ответа',
                'question_index': question_index,
                'total_questions': len(questions)
            })

        Answer.objects.create(
            survey=survey,
            choice_id=choice_id,
            user=request.user
        )

        # переходим к следующему вопросу
        return redirect(f'/survey/{survey.id}/question/{question_index + 1}/')

    return render(request, 'surveys/take_survey.html', {
        'survey': survey,
        'question': question,
        'choices': choices,
        'question_index': question_index,
        'total_questions': len(questions)
    })

def start_survey(request, survey_id):
    return redirect(f'/survey/{survey_id}/question/0/')

def stats_user_passed(request):
    return render(request, 'surveys/stats_user_passed.html')


def stats_my_surveys(request):
    surveys = (
        Survey.objects
        .filter(author=request.user)
        .annotate(
            questions_count=Count('question', distinct=True),
            total_answers=Count('answer', distinct=True)
        )
        .order_by('-created_at')
    )

    # вычисляем количество прохождений
    for s in surveys:
        if s.questions_count > 0:
            s.answers_count = s.total_answers // s.questions_count
        else:
            s.answers_count = 0

    return render(request, 'surveys/stats_my_surveys.html', {
        'surveys': surveys
    })


def stats_all_surveys(request):
    return render(request, 'surveys/stats_all_surveys.html')

from django.db.models import Count

def stats_my_survey_detail(request, survey_id):
    survey = Survey.objects.get(id=survey_id, author=request.user)

    questions = Question.objects.filter(survey=survey)

    questions_stats = []

    for q in questions:
        choices = (
            Choice.objects
            .filter(question=q)
            .annotate(votes=Count('answer'))
        )

        total_votes = sum(c.votes for c in choices) or 0

        choice_stats = []
        for c in choices:
            percent = round(c.votes * 100 / total_votes, 1) if total_votes > 0 else 0
            choice_stats.append({
                'choice': c,
                'votes': c.votes,
                'percent': percent,
            })

        questions_stats.append({
            'question': q,
            'choices': choice_stats,
            'total_votes': total_votes,
        })

    return render(request, 'surveys/stats_my_survey_detail.html', {
        'survey': survey,
        'questions_stats': questions_stats,
    })

def stats_all_surveys(request):
    surveys = (
        Survey.objects
        .annotate(
            questions_count=Count('question', distinct=True),
            total_answers=Count('answer', distinct=True)
        )
        .order_by('-created_at')
    )

    for s in surveys:
        if s.questions_count > 0:
            s.answers_count = s.total_answers // s.questions_count
        else:
            s.answers_count = 0

    return render(request, 'surveys/stats_all_surveys.html', {
        'surveys': surveys
    })

def stats_all_surveys_detail(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    questions = Question.objects.filter(survey=survey)
    questions_stats = []

    for q in questions:
        choices = (
            Choice.objects
            .filter(question=q)
            .annotate(votes=Count('answer'))
        )

        total_votes = sum(c.votes for c in choices) or 0

        choice_stats = []
        for c in choices:
            percent = round(c.votes * 100 / total_votes, 1) if total_votes > 0 else 0
            choice_stats.append({
                'choice': c,
                'votes': c.votes,
                'percent': percent,
            })

        questions_stats.append({
            'question': q,
            'choices': choice_stats,
            'total_votes': total_votes,
        })

    return render(request, 'surveys/stats_all_surveys_detail.html', {
        'survey': survey,
        'questions_stats': questions_stats,
    })

def stats_user_passed(request):
    # все опросы, где пользователь оставил хотя бы один ответ
    surveys = (
        Survey.objects
        .filter(answer__user=request.user)
        .annotate(
            questions_count=Count('question', distinct=True),
            total_answers=Count('answer', distinct=True)
        )
        .distinct()
        .order_by('-created_at')
    )

    for s in surveys:
        if s.questions_count > 0:
            s.answers_count = s.total_answers // s.questions_count
        else:
            s.answers_count = 0

    return render(request, 'surveys/stats_user_passed.html', {
        'surveys': surveys
    })

def stats_user_passed_detail(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    questions = Question.objects.filter(survey=survey)
    questions_stats = []

    for q in questions:
        choices = (
            Choice.objects
            .filter(question=q)
            .annotate(votes=Count('answer'))
        )

        total_votes = sum(c.votes for c in choices) or 0

        choice_stats = []
        for c in choices:
            percent = round(c.votes * 100 / total_votes, 1) if total_votes > 0 else 0
            choice_stats.append({
                'choice': c,
                'votes': c.votes,
                'percent': percent,
            })

        questions_stats.append({
            'question': q,
            'choices': choice_stats,
            'total_votes': total_votes,
        })

    return render(request, 'surveys/stats_user_passed_detail.html', {
        'survey': survey,
        'questions_stats': questions_stats,
    })
