from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from accounts import views as accounts_views
from book import views as book_view

CACHE_TIME_SHORT = int(getattr(settings, "CACHE_TIME_SHORT", 0))
CACHE_TIME_MEDIUM = int(getattr(settings, "CACHE_TIME_MEDIUM", 0))
CACHE_TIME_LONG = int(getattr(settings, "CACHE_TIME_LONG", 0))
SB_URL_BASE = getattr(settings, "SB_URL_BASE", "")

urlpatterns = [
    path('{}'.format(SB_URL_BASE), book_view.HomeListView.as_view(), name='home'),
    path('{}search/'.format(SB_URL_BASE), book_view.SearchListView.as_view(), name='search'),
    path('{}nodes/'.format(SB_URL_BASE), book_view.NodesListView.as_view(), name='nodes'),
    path('{}networks/'.format(SB_URL_BASE), book_view.NetworksListView.as_view(), name='networks'),
    path('{}recent_changes/'.format(SB_URL_BASE), book_view.RecentChangesListView.as_view(), name='recent_changes'),
    path('{}links/'.format(SB_URL_BASE), book_view.LinksListView.as_view(), name='links'),
    re_path(r'^{}nodes/(?P<node_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.NodeDetailsListView.as_view(), name='node_details'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.NetworkDetailsListView.as_view(), name='network_details'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.StationDetailsListView.as_view(), name='station_details'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/gallery/$'.format(SB_URL_BASE),
        book_view.StationGalleryListView.as_view(), name='station_gallery'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_basic/$'.format(SB_URL_BASE),
        book_view.ExtBasicDataUpdateView.as_view(), name='station_edit_basic'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_owner/$'.format(SB_URL_BASE),
        book_view.ExtOwnerDataUpdateView.as_view(), name='station_edit_owner'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_morphology/$'.format(SB_URL_BASE),
        book_view.ExtMorphologyDataUpdateView.as_view(), name='station_edit_morphology'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_housing/$'.format(SB_URL_BASE),
        book_view.ExtHousingDataUpdateView.as_view(), name='station_edit_housing'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_borehole/$'.format(SB_URL_BASE),
        book_view.ExtBoreholeDataUpdateView.as_view(), name='station_edit_borehole'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/add_borehole_layer/$'.format(SB_URL_BASE),
        book_view.station_borehole_layer_add, name='station_borehole_layer_add'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_borehole_layer/(?P<layer_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.station_borehole_layer_edit, name='station_borehole_layer_edit'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/remove_borehole_layer/(?P<layer_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.station_borehole_layer_remove, name='station_borehole_layer_remove'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/upload_photo/$'.format(SB_URL_BASE),
        book_view.station_photo_upload, name='station_photo_upload'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/edit_photo/(?P<photo_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.station_photo_edit, name='station_photo_edit'),
    re_path(r'^{}networks/(?P<network_pk>\w+)/station/(?P<station_pk>\w+)/remove_photo/(?P<photo_pk>\w+)/$'.format(SB_URL_BASE),
        book_view.station_photo_remove, name='station_photo_remove'),
    re_path(r'^{}user/(?P<username>\w+)/$'.format(SB_URL_BASE),
        book_view.UserDetailsListView.as_view(), name='user_details'),
    path('{}signup/'.format(SB_URL_BASE), accounts_views.signup, name='signup'),
    path('{}login/'.format(SB_URL_BASE), auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('{}logout/'.format(SB_URL_BASE), auth_views.LogoutView.as_view(), name='logout'),
    path('{}admin/'.format(SB_URL_BASE), admin.site.urls),
    re_path(r'^{}settings/account/$'.format(SB_URL_BASE), book_view.update_profile, name='my_account'),
    path('{}reset/'.format(SB_URL_BASE),
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ), name='password_reset'),
    path('{}reset/done/'.format(SB_URL_BASE),
        auth_views.PasswordResetDoneView
        .as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^' + SB_URL_BASE + r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView
        .as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('{}reset/complete/'.format(SB_URL_BASE),
        auth_views.PasswordResetCompleteView
        .as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path('{}settings/password/'.format(SB_URL_BASE), auth_views.PasswordChangeView
        .as_view(template_name='password_change.html'),
        name='password_change'),
    path('{}settings/password/done/'.format(SB_URL_BASE), auth_views.PasswordChangeDoneView
        .as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    path('{}refresh_fdsn/'.format(SB_URL_BASE), book_view.refresh_fdsn, name='refresh_fdsn'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add custom handlers for the HTTP error codes
handler404 = 'book.views.custom_404'
handler500 = 'book.views.custom_500'