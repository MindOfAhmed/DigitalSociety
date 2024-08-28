from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export.admin import ImportExportModelAdmin # to load data in bulk

'''This class is used to customize the User model in the admin panel to allow import-export functionality'''
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')  # filter options for the sidebar

class CitizensAdmin(ImportExportModelAdmin):
    list_display = ('national_id', 'first_name', 'last_name', 'date_of_birth', 'sex', 'blood_type')

class AddressesAdmin(ImportExportModelAdmin):
    list_display = ('citizen', 'country', 'city', 'street', 'building_number', 'floor_number', 'apartment_number', 'state')

class PassportsAdmin(ImportExportModelAdmin):
    list_display = ('citizen', 'passport_number', 'issue_date', 'expiry_date', 'picture')

class DrivingLicensesAdmin(ImportExportModelAdmin):
    list_display = ('license_number', 'citizen', 'picture', 'issue_date', 'expiry_date', 'nationality', 'emergency_contact', 'license_class')

class PropertiesAdmin(ImportExportModelAdmin):
    list_display = ('property_id', 'citizen', 'location', 'size', 'property_type', 'description', 'picture', 'is_under_transfer')

class VehiclesAdmin(ImportExportModelAdmin):
    list_display = ('serial_number', 'citizen', 'model', 'year', 'manufacturer', 'vehicle_type', 'plate_number', 'picture', 'is_under_transfer')

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'message')

class RenewalRequestsAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'request_type', 'reason', 'proof_document', 'status', 'picture', 'submitted_at', 'reviewed_at', 'rejection_reason')

class RegistrationRequestsAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'request_type', 'proof_document', 'previous_owner_id', 'status', 'submitted_at', 'reviewed_at', 'rejection_reason')

class ForumsAdmin(admin.ModelAdmin):
    list_display = ('region', 'title')

class PostsAdmin(admin.ModelAdmin):
    list_display = ('forum', 'author', 'title', 'content', 'timestamp', 'likes_count')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'timestamp')

admin.site.unregister(User) # unregister the default User model to allow the custom User model to be registered
admin.site.register(User, CustomUserAdmin) 
admin.site.register(Citizens, CitizensAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Passports, PassportsAdmin)
admin.site.register(DrivingLicenses, DrivingLicensesAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Vehicles, VehiclesAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(RenewalRequests, RenewalRequestsAdmin)
admin.site.register(RegistrationRequests, RegistrationRequestsAdmin)
admin.site.register(Forums, ForumsAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments, CommentsAdmin)