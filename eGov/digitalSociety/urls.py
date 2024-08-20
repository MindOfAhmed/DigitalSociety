from django.urls import path
from . import views
from .views import RenewalRequestsAPIView, RegistrationRequestsAPIView, UserDocumentsAPIView, ForumsAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("api/citizen_info_validation/", views.citizen_info_validation, name="citizen_info_validation"),
    path("api/address_info_validation/", views.address_info_validation, name="address_info_validation"),
    path("api/passport_info_validation/", views.passport_info_validation, name="passport_info_validation"),
    path("api/license_info_validation/", views.license_info_validation, name="license_info_validation"),
    path("api/register_address/", views.register_address, name="register_address"),
    path("api/register_property/", views.register_property, name="register_property"),
    path("api/register_vehicle/", views.register_vehicle, name="register_vehicle"),
    path("api/renewal_requests/", RenewalRequestsAPIView.as_view(), name="renewal_requests"),
    path("api/accept_renewal_request/<int:id>/", views.accept_renewal_request, name="accept_renewal_request"),
    path("api/reject_renewal_request/<int:id>/", views.reject_renewal_request, name="reject_renewal_request"),
    path("api/registration_requests/", RegistrationRequestsAPIView.as_view(), name="registration_requests"),
    path("api/accept_registration_request/<int:id>/", views.accept_registration_request, name="accept_registration_request"),
    path("api/reject_registration_request/<int:id>/", views.reject_registration_request, name="reject_registration_request"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/get_notifications/", views.get_notifications, name="get_notifications"), 
    path("api/user_documents/", UserDocumentsAPIView.as_view(), name="user_documents"),
    path("api/user_profile/", views.user_profile, name="user_profile"),
    path("api/change_password/", views.change_password, name="change_password"),
    path("api/user_groups/", views.user_groups, name="user_groups"),
    path("api/create_forum/", views.create_forum, name="create_forum"),
    path("api/get_forums/", ForumsAPIView.as_view(), name="get_forums"),
    path("api/get_forum/<int:id>/", views.get_forum, name="get_forum"),
]
''' 
    When a POST request is made to /token/ with valid user credentials (username and password),
    the TokenObtainPairView will validate the credentials against the user model. If the credentials are valid,
    it will return a response containing an access token and a refresh token in JSON format. 
'''