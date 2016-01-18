from django.conf.urls import url

from theapp import views
urlpatterns = [

    url(r'^notif$', views.omnitest, name='omnibus'),

    url(r'^signup$', views.signup, name='signup'),

    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),

    url(r'^send-confirmation$', views.generate_confirmation,
        name='send-confirmation-email'),

    url(r'^approve/(?P<user_id>\d+)$',
        views.approve_user, name='approve-user'),
    url(r'^approvals$',
        views.approvals, name='approvals'),

    url(r'^email-confirm/(?P<token>[a-zA-Z0-9]+)$',
        views.confirm_email, name='email-confirm'),

    url(r'', views.user_home, name='user-home'),

    # url(r'^signup$', admin.site.urls),
]
