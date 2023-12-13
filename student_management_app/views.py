import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from student_management_app.forms import LoginForm
from student_management_app.models import CustomUser


def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    try:
        if request.user is not None:
            return HttpResponse("User : " + request.user.username + " usertype : " + str(request.user.user_type))
    except:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "YOUR_API_KEY",' \
           '        authDomain: "FIREBASE_AUTH_URL",' \
           '        databaseURL: "FIREBASE_DATABASE_URL",' \
           '        projectId: "FIREBASE_PROJECT_ID",' \
           '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
           '        messagingSenderId: "FIREBASE_SENDER_ID",' \
           '        appId: "FIREBASE_APP_ID",' \
           '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")


def signup_student(request):
    return render(request, "signup_student_page.html")


def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    sex = request.POST.get("sex")

    # try:
    user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                          first_name=first_name, last_name=last_name,
                                          user_type=3)
    user.students.gender = sex
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    # except:
    #   messages.error(request, "Failed to Add Student")
