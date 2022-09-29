from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from termcolor import colored
from django.middleware import csrf

from modules import (
    createUrlListFromFile,
    customLogInfo,
    getMyPrivateFileContent,
    isSpecialUser,
    makeSendMailRequest,
    convertUrlsBase
)


# ------------------- VIEWS --------------------
def index(request):
    context = {
        "img_url_list": convertUrlsBase(
            createUrlListFromFile('static/images/gallery/img_url_list.txt'),
            use_statically_url=True),
        "is_page_need_header": True,
    }

    return render(request, "root_app/home_page.html", context)

def requestLog(request):
    if request.user.is_superuser:
        return render(request, "root_app/request_log_page.html")
    else:
        pass

def letter(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(f'/login/?direct_to=letter')

    else:
        file_content = 'no content displayed for this user'
        intro_file_content = 'no content displayed for this user'
        is_special_user = False

        # set permission
        if isSpecialUser(request.user) or request.user.is_superuser:
            is_special_user = True
            try:
                file_content = getMyPrivateFileContent(
                    repo_name=settings.ENV_GITHUB_PRIVATE_REPO,
                    file_path=settings.ENV_GITHUB_LETTER_PATH,
                    token=settings.ENV_GITHUB_TOKEN
                )
                intro_file_content = getMyPrivateFileContent(
                    repo_name=settings.ENV_GITHUB_PRIVATE_REPO,
                    file_path=settings.ENV_GITHUB_LETTER_INTRO_PATH,
                    token=settings.ENV_GITHUB_TOKEN
                )
            except:
                file_content = "Error while getting file content."
                print(file_content)

            print(f'{request.user} is special user or superuser')

        return render(
            request,
            "root_app/letter_page.html",
            {
                'file_content': file_content,
                'intro_file_content': intro_file_content,
                'is_special_user': is_special_user
            }
        )

def memo(request):
    return render(request, "root_app/memo_page.html")

def gallery(request):
    return render(
        request,
        "root_app/gallery_page.html"
    )

def log(request):
    return render(
        request,
        "root_app/log_page.html"
    )

def login_view(request):
    queries = {
        "direct_to": f"{request.GET.get('direct_to')}"
    }

    #-----------------------------------------------
    def default_login_view(message, infoStatus, direct_to=None):
        """ return login default view """

        context = {
            "message": message,
            "infoStatus": infoStatus,
            "direct_to": direct_to
        }
        return render(request, "root_app/login_page.html", context)

    def login_success(message, infoStatus, direct_to='None'):
        # notify (send mail)
        if isSpecialUser(request.user):
            makeSendMailRequest(
                csrftoken = csrf.get_token(request),
                req_endpoint = request.build_absolute_uri('/api/send-mail'),
                subject = "your crush login",
                message = "Hi, your crush is logged in into your website. \ndon't forget to check the server log!.",
            )

        # redirect handler
        if direct_to == 'None' or direct_to == "":
            return HttpResponseRedirect(reverse('root_app:index'))
        else:
            # is direct_to valid
            try:
                return HttpResponseRedirect(reverse(f'root_app:{direct_to}'))
            except:
                return HttpResponseRedirect(reverse("root_app:index"))

    def try_login():
        # form
        username = request.POST.get('username')
        password = request.POST.get('password')
        direct_to = request.POST.get('direct_to')
        # parameter that we got from query params of GET before and passed to hidden input field and then POST it via login button

        if username != "" or password != "":
            user = authenticate(request, username=username, password=password)

            if user is not None: # success
                request.session.set_expiry(1209600)
                login(request, user)

                print(colored(f"=> [login success] = @{request.user.username}", 'blue', attrs=['reverse']))
                return login_success("Login berhasil!", "success", direct_to)

            else: # failed
                print(colored(f"=> [login failed] = @{username} (something was wrong)", 'blue', attrs=['reverse']))
                return default_login_view("User tidak ditemukan, coba tanyakan pada admin (zakky)", 'fail', direct_to)

        else:
            return default_login_view("Form tidak boleh kosong", "fail", direct_to)

    #-----------------------------------------------
    if not request.user.is_authenticated: # user is not signed in
        if request.method == "POST":
            return try_login()

        if queries["direct_to"] == "letter":
            message = "Hanya user khusus yang boleh masuk!"
        else:
            message = "Selamat datang!. Login untuk mendapatkan akses khusus!"

        return default_login_view(message, "", queries["direct_to"])

    else: # user already signed in
        return login_success(
            "Anda telah login!",
            "success", queries["direct_to"]
        )

def logout_view(request):
    logout(request)

    return render(
        request,
        "root_app/login_page.html",
        {
            "message": "Anda telah Logout!",
            "direct_to": "index"
        }
    )

def externalHit(request):
    url = request.GET.get('url', "")

    if "imgix.net" in url:
        # remove imgix.net query such 'w' (width) to get actual size of image
        try:
            query_index = url.index('?')
            url = url[:query_index]
        except:
            pass

    return HttpResponseRedirect(url)

def googleSiteVerification(request):
    return render(request, 'root_app/google_site_verification.html')

def siteMap(request):
    return render(request, 'root_app/sitemap.xml', content_type='text/xml')

def robots(request):
    return render(request, 'root_app/robots.txt', content_type="text/plain")

def ads(request):
    return render(request, 'root_app/ads.txt', content_type="text/plain")