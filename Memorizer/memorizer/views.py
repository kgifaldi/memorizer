from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.template import loader
from .forms import userForm, factForm, learnForm, radioForm
import math
# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext

username = "def"
password = ""
currentUser = User()
loggedIn = False
toMemorize = {}
flip = False

def add(request):
    global loggedIn
    loggedIn = True
    prompt = ""
    answer = ""
    template = loader.get_template('memorizer/add.html')
    if request.method == 'POST':
        form = factForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['htmlprompt']
            answer = form.cleaned_data['htmlanswer']
            print "prompt = ", prompt
            print "answer = ", answer
        else:
            print "notvalid"
        print "yes"
    else:
        print "no"
        print "method:", request.method
    username = request.session.get('username')
    userList = User.objects.all()
    numMemorized = -1
    streak = -1
    toMemorize = {}
    for user in userList:
        if username == user.username:
            user.toMemorize[prompt] = answer
            user.nextReview[prompt] = 1
            numMemorized = user.numMemorized
            streak = user.streak
            toMemorize = user.toMemorize
            user.save()
            print "factsaved"
            break
    context = {
        "username": username,
        "numMemorized": numMemorized,
        "streak": streak,
        "toMemorize": toMemorize,
    }
    return HttpResponse(template.render(context, request))


def login(request):
    global loggedIn
    loggedIn = False
    template = loader.get_template('memorizer/login.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def main(request):
    global loggedIn
    template = loader.get_template('memorizer/main.html')
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['htmlusername']
            request.session['username'] = username
            password = form.cleaned_data['htmlpassword']
            print "username = ", username
            print "password = ", password
        else:
            username = ""
            password = ""
    else:
        print "not POST"
        username = request.session.get('username')
    userList = User.objects.all()
    userFound = False
    for user in userList:
        if loggedIn or username == user.username and password == user.password:
            userFound = True
            loggedIn = True
            password = user.password
            numMemorized = user.numMemorized
            streak = user.streak
            toMemorize = user.toMemorize
            currentUser = user
            break
    if not userFound:
        numMemorized = 0
        streak = 0
        toMemorize = {}
        query = User()
        query.username = username
        query.password = password
        query.numMemorized = numMemorized
        query.streak = streak
        query.toMemorize = toMemorize
        currentUser = query
        query.save()

    context = {
        "username":username,
        "numMemorized":numMemorized,
        "streak":streak,
        "toMemorize":toMemorize,
        "numToReview":len(toMemorize),
    }
    return HttpResponse(template.render(context, request))


def learn(request):
    global loggedIn
    global flip
    nextSeen = 0
    loggedIn = True
    template = loader.get_template('memorizer/learn.html')
    tempUser = User()
    username = request.session.get('username')
    userList = User.objects.all()
    for user in userList:
        if username == user.username:
            numMemorized = user.numMemorized
            streak = user.streak
            toMemorize = user.toMemorize
            tempUser = user
            break
    response = ""
    if request.method == 'POST':
        print "FLIP:", flip
        if not flip:
            form = learnForm(request.POST)
            if form.is_valid():
                response = form.cleaned_data['htmlresponse']
                for key, value in tempUser.toMemorize.iteritems():
                    if value == response or value == "":
                        del tempUser.toMemorize[key]
                        tempUser.nextReview[key] = math.ceil(1.5*tempUser.nextReview[key])
                        nextSeen = tempUser.nextReview[key]
                        flip = False
                    else:
                        flip = True
                    break
        else:
            flip = False
            form = radioForm(request.POST)
            if form.is_valid():
                response = form.cleaned_data['htmlradio']
                if "yes_confirm" in response:
                    for key, value in tempUser.toMemorize.iteritems():
                        del tempUser.toMemorize[key]
                        tempUser.nextReview[key] = math.ceil(1.5*tempUser.nextReview[key])
                        nextSeen = tempUser.nextReview[key]
                        break
                    print "yes"
                elif "no_confirm" in response:
                    print "no, keeping fact"
                else:
                    print "RADIONOTWORKING"
            else:
                print "here"
    else:
        print "not POST"
    prompt = ""
    answer = ""
    for key, value in tempUser.toMemorize.iteritems():
        prompt = key
        answer = value
        break
    if not tempUser.toMemorize:
        finished = True
    else:
        finished = False
    context = {
        "username": username,
        "prompt": prompt,
        "answer": answer,
        "finished": finished,
        "flip": flip,
        "response": response,
        "nextSeen": nextSeen,
    }
    return HttpResponse(template.render(context, request))
# ad  logged in == true to beginning of about
