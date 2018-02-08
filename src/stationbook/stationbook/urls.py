from django.conf.urls import include
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts import views as accounts_views
from book import views as book_view

urlpatterns = [
    path('', book_view.HomeListView.as_view(), name='home'),
    path('search/', book_view.SearchListView.as_view(), name='search'),
    re_path(r'^network/(?P<network_code>\w+)/$',
    book_view.NetworkDetailsListView.as_view(), name='network_details'),
    # re_path(r'^station/(?P<pk>\d+)/$',
    # book_view.StationDetailsListView.as_view(), name='station_details'),
    re_path(r'^network/(?P<network_code>\w+)/station/(?P<station_code>\w+)/$',
    book_view.StationDetailsListView.as_view(), name='station_details'),
    re_path(r'^network/(?P<network_code>\w+)/station/(?P<station_code>\w+)/edit_basic$',
    book_view.ExtBasicDataUpdateView.as_view(), name='station_edit_basic'),
    re_path(r'^network/(?P<network_code>\w+)/station/(?P<station_code>\w+)/edit_owner$',
    book_view.ExtOwnerDataUpdateView.as_view(), name='station_edit_owner'),
    re_path(r'^network/(?P<network_code>\w+)/station/(?P<station_code>\w+)/edit_morphology$',
    book_view.ExtMorphologyDataUpdateView.as_view(), name='station_edit_morphology'),
    re_path(r'^network/(?P<network_code>\w+)/station/(?P<station_code>\w+)/edit_housing$',
    book_view.ExtHousingDataUpdateView.as_view(), name='station_edit_housing'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView
    .as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    re_path(r'^settings/account/$',
    accounts_views.UserUpdateView.as_view(), name='my_account'),
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ), name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView
        .as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView
        .as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView
        .as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView
        .as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView
        .as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    path('refresh_fdsn/', book_view.refresh_fdsn, name='refresh_fdsn'),
]

# Add custom handlers for the HTTP error codes
handler404 = 'book.views.custom_404'
handler500 = 'book.views.custom_500'