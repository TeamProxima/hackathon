from django.shortcuts import redirect,render
from django.contrib.sessions import *
from django.template import RequestContext
from json import dumps, loads, JSONEncoder, JSONDecoder
import random
#import MySQLdb

from functions import *
from models import *

def session_handler(request, new=True):
    if new:
        request.session['country'] = request.GET['country']
        request.session['city'] = request.GET['city']
        print request.session['country'], request.session['city']
        request.session['page_index'] = 0
        request.session['answer'] = {}
    else:
        del request.session['country']
        del request.session['city']
        del request.session['answer']
        del request.session['page_index']
        return False
    return True


def home(request):
    '''Show country and city selection'''
    try:
        context =  {'message': ''}
        return render(request, 'index.html', context)
    except Exception as e:
        print e
        return redirect("/")


country = None
city = None

def run(request):
    '''Ask questions to calculate price'''
    '''
        Question Format
        ID: Unique question identifier to evaluate answers
        Type: Identifier to determine question format
            Radio Button: 0
            Text Input: 1
            Dropdown: 2
            Slider: 3
            Checkbox: 4
        Text: Question text
        Alternative: Radio button, checkbox, dropdown alternatives
        Range: Slider range

    '''

    global pictures
    questions = [{'id': 'mealQ1', 'type': 4, 'text': "Which meals do you eat?", 'alt':['Breakfast', 'Launch', 'Dinner']},
          {'id': 'mealQ2', 'type': 3, 'text': "What do you prefer in a meal?", 'range': range(101), 'alt':['Vegetable', 'Meat']},
          {'id': 'mealQ3', 'type': 1, 'text': "How often do you go out for a meal?", 'alt':['times a week.']},
          {'id': 'mealQ4', 'type': 3, 'text': "What do you prefer?", 'range': range(101), 'alt': ['Restaurant', 'Fast Food']}
          ]
    questions2 = [{'id': 'beer_cigQ1', 'type': 1, 'text': "How much beer do you drink?", 'alt':['bottles per week']},
          {'id': 'beer_cigQ2', 'type': 1, 'text': "How many cigarette do you smoke?", 'alt':['packets per week']}
          ]
    questions3 = [{'id': 'accoQ1', 'type': 0, 'text': "Where do you want to live?", 'alt':['In city centre', 'Outside of city centre']},
          {'id': 'accoQ2', 'type': 0, 'text': "How many bedrooms?", 'alt':['1', '2', '3']}
          ]
    questions4 = [{'id': 'miscQ1', 'type': 1, 'text': "How many pieces of outfit do you buy?", 'alt':['pieces per month.']},
          {'id': 'miscQ2', 'type': 1, 'text': "How often do you go to cinema?", 'alt':['times a month.']},
          {'id': 'miscQ2', 'type': 0, 'text': "Do you want to have gym membership?", 'alt':['Yes', 'No']}
          ]

    qlist = [questions, questions2, questions3, questions4]
    try:
        if request.META['HTTP_REFERER'].split('/')[-1] == '':
            '''For country and city selection after index'''

            session_handler(request)

        if request.POST:
            request.session['page_index'] += 1
            request.session['answer'].update((request.POST.iterlists()))
            print request.session['answer']

        return render(request, 'result.html',
            {'message': '',
             'piclink': "pics/" + str(random.randint(0, 6)) + ".jpg",
            'questions': qlist[request.session['page_index']],
             'page_headers': [request.session['country'], request.session['city']]
             })
    except IndexError:
        '''
        global country,city
        answers = request.session['answer']
        num_of_beer = int(str(answers['beer_cigQ1'][0]))
        num_of_cig = int(str(answers['beer_cigQ2'][0]))
        meal_list = answers['mealQ1']
        meals = []
        for each in meal_list:
            meals.append(str(each))
        print meals
        veg_ratio = 1-(int(str(answers['mealQ2'][0]))/100.0)
        num_of_out_meal = int(str(answers['mealQ3'][0]))
        restaurant_ratio = 1- (int(str(answers['mealQ4'][0]))/100.0)
        print veg_ratio, num_of_out_meal, restaurant_ratio

        print 'nums beer cig:', num_of_beer, num_of_cig

        for key,value in answers.iteritems():
            print key, value
        db = MySQLdb.connect("localhost","root","root","test")
        cursor = db.cursor()
        print "select * from info where country='"+country+"' and city='"+city+"';"
        cursor.execute("select * from info where country='"+country+"' and city='"+city+"';")
        data = cursor.fetchone()
        print data
        db.close()

        daily_cost = meal_cost(meals, veg_ratio, num_of_out_meal, restaurant_ratio, data[2:])
        print 'cost',daily_cost

            'answers' has answers as a dictionary.
            Finished, calculate.
        '''
        session_handler(request, False)
        #return redirect("/")
        return render(request, 'result.html')
    except Exception as e:
        print e
        return redirect("/")
