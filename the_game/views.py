from django.views import View
from django.shortcuts import render, redirect
from random import randint
from django.http.response import HttpResponse
from the_game.models import Question, Category, GRADE
from the_game.forms import AnswerForm, StageOneForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
qqnt =len(Question.objects.all()) # number of all records in questions table
already_asked = list()

def ask():
    id = randint(1, qqnt)
    print(qqnt)
    print(already_asked)
    if id not in already_asked:
        to_ask = Question.objects.get(pk=id)
        #print(to_ask)
        already_asked.append(id)
        print("w funkcji asked" + str(already_asked))
        print(" w funkcji - to ask:   " + str(to_ask))
        qta= {'question': to_ask.query, 'category': to_ask.category, 'answer': to_ask.answer, 'comment': to_ask.comment }
        #print(ctx)
        return qta
    else:
        if len(already_asked) == qqnt:
            out = '''<html>
            <body>
                <h1>Out of questions</h1>
            </body>
        </html>
    '''
            return HttpResponse(out)
        else:
            ask()

count = 0

# @csrf_exempt
class Stage_One(View):
    count = 0
    def get(self, request):
        form = AnswerForm()
        will_ask = ask()
        print("wynik funkcji ask() w StageOne" + str(will_ask))
        q = will_ask['question']
        c = will_ask['comment']
        a = will_ask['answer']
        b = will_ask['category']
        # trzeba przekazać odpowiedz 'a' metoda post
        print("zapytam o " + str(will_ask))
        ctx = {'form': form, 'qqq': q, 'ccc':c, 'aaa':a, 'bbb':b}
        print(ctx)

        return render(request, "game_templates/stage_one.html", ctx)

    def post(self, request):
        form = AnswerForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player_answer']
            print(form.data['asked_question_answer'])
            prev_answer = form.data['asked_question_answer']

            if player == prev_answer:
                print("doszlo")
                #count += 1
                form = AnswerForm()
                will_ask = ask()
                q = will_ask['question']
                c = will_ask['comment']
                a = will_ask['answer']
                b = will_ask['category']
                # trzeba przekazać odpowiedz 'a' metoda post
                # print(will_ask)
                ctx = {'form': form, 'qqq': q, 'ccc': c, 'aaa': a, 'bbb': b}
                print("post ctx " + str(ctx))
                return render(request, "game_templates/stage_one.html", ctx)

            else:
                return HttpResponse("wrong")

def askMF():
    id = randint(1, qqnt)
    print(qqnt)
    print(already_asked)
    if id not in already_asked:
        to_askMF = Question.objects.get(pk=id)
        #print(to_ask)
        return to_askMF

class StageOneMF(View):

    def get(self, request):

        form = StageOneForm(instance=askMF())
        return render(request, "game_templates/stage_one_MF.html", {'form':form})
    def post(self, request):
        pass

# class EditEmployee(View):
#
#     def get(self, request, employee_id):
#         emp = Employee.objects.get(pk=employee_id)
#         form = EmployeeEditForm(instance=emp)
#         return render(request, "exercises/employee_form.html", {'form':form})
#
#     def post(self, request, employee_id):
#         emp = Employee.objects.get(pk=employee_id)
#         form = EmployeeEditForm(request.POST, instance=emp)
#         if form.is_valid():
#             form.save()
#         return render(request, "exercises/employee_form.html", {'form': form})