import traceback

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from theapp.models import EmailVerification
from theapp.models import User
from theapp.models import Approval
from theapp.tasks import post_signup_processing, send_email_confirmation
from theapp.forms import UserForm
from theapp.predefined import ADMIN_TYPE_ONE
from theapp.predefined import ADMIN_TYPE_TWO


def omnitest(request):
    return render(request, 'theapp/omni_frontend.html')


def signup(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, "theapp/signup.html",
                      {'form': form})
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            user.set_password(form.data['password'])
            user.save()
            post_signup_processing.delay(user, request.get_host())
            return render(request, 'theapp/signup.html', {'ok': user})
        else:
            return render(request, "theapp/signup.html",
                          {'form': form})


@require_http_methods(["GET"])
def approvals(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    is_admin = Q(name=ADMIN_TYPE_ONE) | Q(name=ADMIN_TYPE_TWO)
    if not request.user.groups.filter(is_admin).exists():
        return HttpResponse("You are not an admin", status_code=403)

    approvals = Approval.objects.filter(by_admin=request.user)
    return render(request, 'theapp/admin_approvals.html',
                  dict(approvals=approvals))


@require_http_methods(["GET"])
def approve_user(request, user_id):
    is_admin = Q(name=ADMIN_TYPE_ONE) | Q(name=ADMIN_TYPE_TWO)
    message = ''
    if request.user.groups.filter(is_admin).exists():
        try:
            user = User.objects.get(pk=user_id)
        except:
            return HttpResponse("User does not exist")
        else:
            approval = user.approvals.filter(by_admin=request.user).first()
            if approval is None:
                message = "You are not authorized to approve this user."
            else:
                if approval and approval.can_be_approved_by(request.user):
                    approval.mark_approved()
                    message = "Approved %s !" % user.username
                else:
                    message = "You are not authorized to approve this user."
    else:
        message = "Only admins can approve."

    return HttpResponse(message)


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """
    Logout user.
    """
    logout(request)
    return redirect(reverse('login'))


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    View a user sees when they login,
    or after clicking an email confirmation
    link.
    """
    if request.user and request.user.is_authenticated():
        return redirect(reverse('user-home'))
    data = request.POST
    # user_id can be either via username or email
    user_id = data.get('username', None)
    password = data.get('password', None)

    # Try to authenticate a user with given creds
    user = authenticate(username=user_id, password=password)
    if not user:
        error = "Incorrect password or username."
        print(error)
        return render(request,
                      'theapp/login.html',
                      dict(error=error))

    try:
        # Login user
        login(request, user)
    except:
        traceback.print_exc()
        return render(request,
                      'theapp/login.html',
                      error='Something went wrong. Sorry.')
    else:
        return redirect(reverse('user-home'))


@require_http_methods(["GET"])
def user_home(request):
    """
    View a user sees if they are logged in,
    or after clicking an email confirmation
    link.
    """

    if not request.user.is_authenticated():
        return redirect(reverse('login'))

    errors = []

    # Check if user has confirmed their email
    email_address = EmailVerification.objects.filter(
        user=request.user).first()

    # A message, in case they haven't.
    if not email_address or not email_address.verified:
        errors.append('Your email is not verified yet. ')
        errors.append('Please click the activation link in your email.')
        return render(request, 'theapp/user_home.html',
                      {'not_verified': True, 'errors': errors})

    approvals = Approval.objects.filter(for_user=request.user)
    # A successful logged in user will see this
    return render(request,
                  'theapp/user_home.html',
                  {'approvals': approvals})


@require_http_methods(["GET"])
def generate_confirmation(request):
    if request.user.is_authenticated():
        send_email_confirmation(request.user)
    return redirect(reverse('login'))


@require_http_methods(["GET"])
def confirm_email(request, token):
    message = ''
    if EmailVerification.objects.filter(token=token).exists():
        email = EmailVerification.objects.filter(token=token).first()
        if not email.verified:
            email.verified = True
            email.user.is_active = True
            email.save()
            email.user.save()
            message = "Thank you for verifying your email.\
                        You now need to wait for your approval."
        else:
            message = "You've already confirmed your email."

    else:
        message = "Invalid confirmation token. Please contact site admin."

    return render(request, "theapp/verified.html", dict(message=message))
