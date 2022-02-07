from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    #입력인자
    page = request.GET.get('page', '1')

    #질문목록
    question_list = Question.objects.order_by('-create_date')

    #페이징처리
    paginator = Paginator(question_list, 10) #10 per page
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj}
    return render(request, 'djangoman/question_list.html', context)
    #return HttpResponse("Hello this is djangoman")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'djangoman/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('djangoman:detail', question_id = question.id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form': form}
    return render(request, 'djangoman/question_detail.html', context)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('djangoman:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'djangoman/question_form.html', context)