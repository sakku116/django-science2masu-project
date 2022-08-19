from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
from django.conf import settings
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import connection as db_connection
from django.core.mail import send_mail
from django.middleware import csrf

#import json

from modules import (
    createUrlListFromFile, 
    customLogInfo, 
    makeSendMailRequest,
    convertUrlsBase,
    getGhBlobList
)

# Create your views here.
def index(request):
    ''' redirect to home '''

    return HttpResponseRedirect('/')

def dbInfo(request):
    '''  get db connection info ''' 

    if not request.user.is_superuser:
        message = 'information of database is only for super user' 
        db_info = None
    else:
        message = 'db_info for super user'
        db_info = db_connection.settings_dict

    return JsonResponse(
        {
            "message": message,
            "dib_info": db_info
        }
    )

def imgUrlList(request):
    ''' get list of img urls from assets server (github repository) '''

    base_prefix = "static/images/"
    prefix = request.GET.get('prefix', "")
    message = []
    is_data_over = False

    try:
        img_url_list = convertUrlsBase(
            getGhBlobList(
                github_token = settings.ENV_GITHUB_TOKEN,
                github_repo = 'sakku116/science2masu-static-files',
                prefix = base_prefix + prefix,
            ), 
            use_imgix_url=True
        )
        message.append('success getting url list from file')
    except:
        img_url_list = convertUrlsBase(
            getGhBlobList(
                github_token = settings.ENV_GITHUB_TOKEN,
                github_repo = 'sakku116/science2masu-static-files',
                prefix = base_prefix,
            ), 
            use_imgix_url=True
        )
        message.append(f'failed to execute prefix query')

    max_index = len(img_url_list)-1

    from_index = request.GET.get('from_index', '0') # QUERY
    to_index = request.GET.get('to_index', str(max_index)) # QUERY

    # set value to default if the query parameter value is not digit (number in string)
    if from_index.isdigit() == False:
        from_index = '0'
    if to_index.isdigit() == False:
        to_index = max_index

    from_index = int(from_index)
    to_index = int(to_index)
        
    # limit index if the value is greater than max index
    if to_index >= max_index:
        to_index = max_index
        message.append('to_index reached the maximum index')
    if from_index >= max_index:
        from_index = max_index - 1
        message.append('from_index reached the maximum index')

    if from_index >= max_index or to_index >= max_index:
        is_data_over = True

    # handle from_index if it value equal to or greater than to_index
    if from_index == to_index:
        from_index = from_index
        to_index = from_index+1
    elif from_index > to_index:
        message.append("invalid index ('from_index' can't be greater than to_index)")
        # reset value
        from_index = 0
        to_index = max_index

    img_url_list = img_url_list[from_index:to_index]

    data = {
        'message': message,
        'img_url_list': img_url_list,
        'list_length': len(img_url_list),
        'from_index': from_index,
        'to_index': to_index,
        'base_prefix': base_prefix,
        'prefix': prefix,
        'is_data_over': is_data_over,
    }

    # 'https://docs.djangoproject.com/en/4.0/ref/request-response/#jsonresponse-objects'
    return JsonResponse(data = data)

def user(request, username_path=None):

    if request.method == "GET":
        ''' get all user '''

        if username_path:
            users = User.objects.filter(username=username_path) # queryset
        else:
            users = User.objects.all() # queryset

        # get spesific column only
        users = users.values_list('username', 'email', 'first_name', 'last_name') # queryset 
        ''' if values_list has 2 fields it will return
        [
            [field1, field2], <-- user1
            [field1, field2], <-- user2
        ]
        (list of user element list)
        '''

        # convert queryset to list
        users = list(users) # list

        result = []
        for user in users:
            ''' create new structure (list of dictionary)
            [
                {'field1':field1, 'field2':field2}, <-- user1
                {'field1':field1, 'field2':field2}, <-- user2
            ]
            (list of dictionary)
            '''

            username_value = user[0]
            email_value = user[1]
            fn_value = user[2]
            ln_value = user[3]

            user = {
                'username': username_value,
                'email': email_value,
                'first_name': fn_value,
                'last_name': ln_value
            }

            result.append(user)

        users = result

        if len(users) != 0:
            status = "success"
            message = "user found"
        else:
            status = "failed"
            message = "user not found"

        return JsonResponse(
            data = {
                'status': status,
                'message': message,
                'users': users,
            }
        )
    
    elif request.method == "POST":
        ''' create new user with basic information (username, email, passworrd) '''

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and password: # required
            new_user = User.objects.create_user(
                username = username, 
                email = email, 
                password = password
            )
            new_user.save()
            
            status = "success"
            message = f"new user was created ({username} - {email})"
        else:
            status = "failed"
            message = "failed to create new user"

        return JsonResponse(
            data = {
                'status': status,
                'message': message,
            }
        )

def sendMail(request):
    mail_subject = request.POST.get('subject', 'subject-testing')
    mail_message = request.POST.get('message', 'message-testing')
    mail_recipient = request.POST.get('recipient', 'kycraftprivate@gmail.com')

    try:
        send_mail(
            subject = mail_subject,
            message = mail_message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [mail_recipient],
        )
        print('email-sent')

        status = 200
        message = f"sending a mail to {mail_recipient}"

    except:
        status = 400
        message = f"failed to sending a mail to {mail_recipient}"

    return JsonResponse(
        {
            "message": message,
            "mail_subject": mail_subject,
            "mail_message": mail_message,
        }
    )

def runTest(request):
    ''' make any response to run test '''
    
    message = f"no task"

    makeSendMailRequest(
        csrftoken=csrf.get_token(request),
        req_endpoint=request.build_absolute_uri('/api/send-mail'),
        subject="test test tets runtest"
    )

    return JsonResponse(
        {
            "message": message,
        }
    )