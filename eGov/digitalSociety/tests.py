from django.test import TestCase, override_settings # to override the settings for testing
import tempfile # to create temporary files that store the uploaded files
from rest_framework.test import APIClient # to test the API views
from django.db import IntegrityError # to catch the IntegrityError when creating a duplicate object
import factory # to create factories for the models
from django.contrib.auth.models import Group # to create a group for the user
from django.urls import reverse # to make requests to the views
from datetime import datetime, timedelta # to create dates for the models
from rest_framework_simplejwt.tokens import RefreshToken # to create JWT tokens for the users
from django.core.files.uploadedfile import SimpleUploadedFile # to create a SimpleUploadedFile for the uploaded files
from django.core.files.storage import default_storage # to access the media folder
import os # to access the file system
import shutil # to copy files
from django.conf import settings # to access the media root path from settings
from .models import *
from .modelFactory import *
from .views import *

'''This helper function is used to copy the test files to the temp media folder'''
def setup_test_files(temp_media_root, files):
    for file in files:
        src_path = os.path.join(settings.BASE_DIR, 'media', file)
        dest_path = os.path.join(temp_media_root, file)
        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)
        else:
            raise FileNotFoundError(f"Source file {src_path} does not exist")
# copilot ^_^
'''
This class sets up the temp media folder for the tests and cleans it up after the tests are done. 
Other test classes can inherit from this class to use the temp media folder
'''
class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = cls.temp_media_root
        setup_test_files(cls.temp_media_root, ['valid.jpeg', 'invalid.jpeg'])  

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_media_root)
        super().tearDownClass()
# copilot ^_^

'''VIEWS TESTS'''
class UserGroupViewTest(TestCase):
    '''Agenda: test that the view returns the list of groups the authenticated user is in correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create users to test with
        self.user_in_group = UserFactory(username='user_in_group')
        self.user_not_in_group = UserFactory(username='user_not_in_group')
        # create a group and the user to it
        self.group = Group.objects.create(name='test_group')
        self.user_in_group.groups.add(self.group)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    # copilot ^_^
    
    def test_user_in_group(self):
        # get the JWT token for the user in the group and pass it in the request header
        token = self.get_jwt_token(self.user_in_group)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # copilot ^_^
        # call the view and assert that the user is in the group
        response = self.client.get(reverse('user_groups'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['groups'], ['test_group'])
    
    def test_user_not_in_group(self):
        # get the JWT token for the user not in the group and pass it in the request header
        token = self.get_jwt_token(self.user_not_in_group)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # call the view and assert that the user is not in the group
        response = self.client.get(reverse('user_groups'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['groups'], [])

    def test_unauthenticated_user(self):
        # call the view without an authorization header
        response = self.client.get(reverse('user_groups'))
        self.assertEqual(response.status_code, 401)

class CitizenInfoValidationTest(TestCase):
    '''Agenda: test the view validates the citizen data for an authenticated user in the Citizens group correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')
        # define the json data to be sent in the request
        self.json_data = {
            'national_id': self.citizen.national_id,
            'first_name': self.citizen.first_name,
            'last_name': self.citizen.last_name,
            'date_of_birth': self.citizen.date_of_birth,
            'sex': self.citizen.sex,
            'blood_type': self.citizen.blood_type
        }
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_citizen_info_validation(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')        
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('citizen_info_validation'), self.json_data, format='json')
        # copilot ^_^
        self.assertEqual(response.status_code, 200)

    def test_unauthorised_citizen_info_validation(self):        
        # ensure a valid request from an unauthorised user in the Citizens group returns a 401 error
        response = self.client.post(reverse('citizen_info_validation'), self.json_data, format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_wrong_citizen_info_validation(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the json data to be sent in the request
        wrong_json_data = {
            'national_id': 1234,
            'first_name': self.citizen.first_name,
            'last_name': self.citizen.last_name,
            'date_of_birth': self.citizen.date_of_birth,
            'sex': self.citizen.sex,
            'blood_type': self.citizen.blood_type
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('citizen_info_validation'), wrong_json_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_citizen_not_in_group(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('citizen_info_validation'), self.json_data, format='json')
        self.assertEqual(response.status_code, 403)

class UserDocumentsTest(TestCase):
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='testuser')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create associated documents for the citizen
        self.passport = PassportsFactory(citizen=self.citizen)
        self.license = DrivingLicensesFactory(citizen=self.citizen)
        self.property = PropertiesFactory(citizen=self.citizen)
        self.vehicle = VehiclesFactory(citizen=self.citizen)
        self.address = AddressesFactory(citizen=self.citizen)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_user_documents_retrieval(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # make a request to the view
        response = self.client.get(reverse('user_documents'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # define the valid data that will be sent
        valid_data = {
            'citizen': CitizensSerializer(self.citizen).data,
            'passport': PassportsSerializer(self.passport).data,
            'license': DrivingLicenseSerializer(self.license).data,
            'properties': PropertiesSerializer([self.property], many=True).data,
            'vehicles': VehiclesSerializer([self.vehicle], many=True).data,
            'addresses': AddressesSerializer([self.address], many=True).data,
        }
        # check that the picture URLs are correctly updated
        base_url = 'http://127.0.0.1:8080'
        valid_data['citizen']['picture'] = base_url + valid_data['citizen']['picture']
        valid_data['passport']['picture'] = base_url + valid_data['passport']['picture']
        valid_data['license']['picture'] = base_url + valid_data['license']['picture']
        valid_data['properties'][0]['picture'] = base_url + valid_data['properties'][0]['picture']
        valid_data['vehicles'][0]['picture'] = base_url + valid_data['vehicles'][0]['picture']
        self.assertEqual(response.data, valid_data)
    # copilot ^_^

class UserProfileTest(BaseTestCase):
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='testuser')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_valid_username_change(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid username change is successful
        response = self.client.post(reverse('user_profile'), {'username': 'newuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ensure that the username was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newuser')
        # ensure that a notification was created
        notification = Notifications.objects.get(citizen=self.citizen)
        self.assertIn('Your username has been changed to newuser', notification.message)
    
    def test_duplicate_username_error(self):
        # create another user to test duplicate username
        UserFactory(username='existinguser')
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure changing to a username that already exists produces error
        response = self.client.post(reverse('user_profile'), {'username': 'existinguser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This username is already taken.', response.data['username'])

    def test_profile_picture_upload(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # create a dummy image file
        image = SimpleUploadedFile('test_image.jpg', b'test_image_content', content_type='image/jpeg')
        # ensure uploading a profile picture is successful
        response = self.client.post(reverse('user_profile'), {'profile_picture': image})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure that the picture was saved and a notification was created
        self.citizen.refresh_from_db()
        self.assertTrue(self.citizen.picture.name.endswith('test_image.jpg'))
        notification = Notifications.objects.get(citizen=self.citizen)
        self.assertIn('Your profile picture has been updated.', notification.message)
    # copilot ^_^

class ChangePasswordTest(TestCase):
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='testuser', password="123London")
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_change_password_success(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure changing password with correct current password is successfull
        response = self.client.post(reverse('change_password'), {
            'current_password': '123London',
            'new_password': 'newpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('The password has been changed successfully.', response.data['message'])
        # ensure that the password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))
        # ensure that a notification was created
        notification = Notifications.objects.get(citizen=self.citizen)
        self.assertIn('Your password has been changed.', notification.message)
    
    def test_incorrect_current_password(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure changing password with incorrect current password produces error
        response = self.client.post(reverse('change_password'), {
            'current_password': 'wrongpassword',
            'new_password': 'newpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The current password is incorrect.', response.data['current_password'])

class AddressInfoValidationTest(TestCase):
    '''Agenda: test the view validates the address data for an authenticated user in the Citizens group correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')
        # create an address for the user
        self.address = AddressesFactory(citizen=self.citizen)
        # define the json data to be sent in the request
        self.json_data = {
            'country': self.address.country,
            'city': self.address.city,
            'street': self.address.street,
            'building_number': self.address.building_number,
            'floor_number': self.address.floor_number,
            'apartment_number': self.address.apartment_number
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_address_info_validation(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('address_info_validation'), self.json_data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_unauthorised_address_info_validation(self):
        # ensure a valid request from an unauthorised user in the Citizens group returns a 401 error
        response = self.client.post(reverse('address_info_validation'), self.json_data, format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_wrong_address_validation(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the json data to be sent in the request
        wrong_json_data = {
            'country': self.address.country,
            'city': self.address.city,
            'street': self.address.street,
            'building_number': self.address.building_number,
            'floor_number': self.address.floor_number,
            'apartment_number': 'wrong'
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('address_info_validation'), wrong_json_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_citizen_not_in_group(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('address_info_validation'), self.json_data, format='json')
        self.assertEqual(response.status_code, 403)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class PassportInfoValidationTest(BaseTestCase):
    '''Agenda: test the view allows the authenticated user in the citizens group to create a passport renewal request correctly.'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a passport for the user with issue date not within the last 3 years
        self.passport = PassportsFactory(citizen=self.citizen, passport_number='P0123456', issue_date='2020-01-01', expiry_date='2025-01-01')
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')

        # open the media folder and create a SimpleUploadedFile for the valid picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')

        # define the valid multipart data to be sent in the requests
        self.data = {
            'passport_number': self.passport.passport_number,
            'issue_date': self.passport.issue_date,
            'expiry_date': self.passport.expiry_date,
            'picture': picture,
        }
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        )
        # copilot ^_^

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_passport_info_validation(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('passport_info_validation'), self.data, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_passport_info(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'passport_number': 'invalid',
            'issue_date': '2020-01-01',
            'expiry_date': '2025-01-01',
            'picture': self.data['picture'],
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('passport_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_unauthenticated_passport_info_validation(self):
        # ensure a valid request from an unauthenticated user returns a 401 error
        response = self.client.post(reverse('passport_info_validation'), self.data, format='multipart')
        self.assertEqual(response.status_code, 401)
    
    def test_not_citizen(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('passport_info_validation'), self.data, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_early_renewal_without_proof(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'passport_number': self.passport.passport_number,
            'issue_date': '2023-01-01', # within 3 years
            'expiry_date': '2028-01-01',
            'picture': self.data['picture'],
        }
        # ensure that if the issue date is within the last 3 years and no reason and proof document are provided, the request is rejected
        response = self.client.post(reverse('passport_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_early_renewal_with_proof(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the valid multipart data to be sent in the request
        valid_data = {
            'passport_number': self.passport.passport_number,
            'issue_date': self.passport.issue_date, 
            'expiry_date': self.passport.expiry_date,
            'picture': self.data['picture'],
            'reason': factory.Faker('text'),
            'proof_document': self.proof_document,
        }
        # ensure that the request is created if the issue date is within the last 3 years and a reason and proof document are provided
        response = self.client.post(reverse('passport_info_validation'), valid_data, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_picture(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # open the media folder and create a SimpleUploadedFile for the invalid picture
        with default_storage.open('invalid.jpeg', 'rb') as image_file:
            invalid_picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'passport_number': self.passport.passport_number,
            'issue_date': self.passport.issue_date, 
            'expiry_date': self.passport.expiry_date,
            'picture': invalid_picture,
        }
        # ensure that the invalid picture is rejected
        response = self.client.post(reverse('passport_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class DrivingLicensesValidationTest(BaseTestCase):
    '''Agenda: test the view allows the authenticated user in the citizens group to create a driver's license renewal request correctly.'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a license for the user with issue date not within the last 3 years
        self.driving_license = DrivingLicensesFactory(issue_date='2020-01-01', expiry_date='2030-01-01', citizen=self.citizen, license_number='P0123456')
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')

        # open the media folder and create a SimpleUploadedFile for the valid picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')

        # define the valid multipart data to be sent in the requests
        self.data = {
            'license_number': self.driving_license.license_number,
            'issue_date': self.driving_license.issue_date,
            'expiry_date': self.driving_license.expiry_date,
            'nationality': self.driving_license.nationality,
            'license_class': self.driving_license.license_class,
            'emergency_contact': self.driving_license.emergency_contact,
            'picture': picture,
        }
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_invalid_license_info(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'license_number': 'invalid',
            'issue_date': self.driving_license.issue_date,
            'expiry_date': self.driving_license.expiry_date,
            'nationality': self.driving_license.nationality,
            'license_class': self.driving_license.license_class,
            'emergency_contact': self.driving_license.emergency_contact,
            'picture': self.data['picture'],
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('license_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_unauthenticated_license_info(self):
        # ensure a valid request from an unauthenticated user returns a 401 error
        response = self.client.post(reverse('license_info_validation'), self.data, format='multipart')
        self.assertEqual(response.status_code, 401)
    
    def test_not_citizen(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('license_info_validation'), self.data, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_early_renewal_without_proof(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'license_number': self.driving_license.license_number,
            'issue_date': '2023-01-01', # within 3 years
            'expiry_date': '2033-01-01',
            'nationality': self.driving_license.nationality,
            'license_class': self.driving_license.license_class,
            'emergency_contact': self.driving_license.emergency_contact,
            'picture': self.data['picture'],
        }
        # ensure that if the issue date is within the last 3 years and no reason and proof document are provided, the request is rejected
        response = self.client.post(reverse('license_info_validation'), invalid_data, format='multipart')   
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_picture(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # open the media folder and create a SimpleUploadedFile for the invalid picture
        with default_storage.open('invalid.jpeg', 'rb') as image_file:
            invalid_picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'license_number': self.driving_license.license_number,
            'issue_date': self.driving_license.issue_date,
            'expiry_date': self.driving_license.expiry_date,
            'nationality': self.driving_license.nationality,
            'license_class': self.driving_license.license_class,
            'emergency_contact': self.driving_license.emergency_contact,
            'picture': invalid_picture,
        }
        # ensure that the invalid picture is rejected
        response = self.client.post(reverse('license_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_data(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid multipart data to be sent in the request
        invalid_data = {
            'license_number': self.driving_license.license_number,
            'issue_date': self.driving_license.issue_date,
            'expiry_date': self.driving_license.expiry_date,
            'nationality': self.driving_license.nationality,
            'license_class': self.driving_license.license_class,
            'emergency_contact': self.driving_license.emergency_contact,
            'picture': 'invalid',
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('license_info_validation'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
class AddressRegistrationTest(BaseTestCase):
    '''Agenda: test the view allows the authenticated user in the citizens group to register an address correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')
        # create an address for the user
        self.address = AddressesFactory(citizen=self.citizen)
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        )
        # define the current address to be sent in the test_address_already_registered function
        self.data = {
            'country': self.address.country,
            'city': self.address.city,
            'street': self.address.street,
            'building_number': self.address.building_number,
            'floor_number': self.address.floor_number,
            'apartment_number': self.address.apartment_number,
            'proof_document': self.proof_document,
        }
        # define the new address to be registered 
        self. new_address = {
            'country': 'Egypt',
            'city': 'Cairo',
            'street': 'El Haram',
            'building_number': 10,
            'floor_number': 3,
            'apartment_number': 5,
            'proof_document': self.proof_document,
        }
        
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_address_registration(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('register_address'), self.new_address, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_address_already_registered(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure that if the address is already registered for the user, the request is rejected
        response = self.client.post(reverse('register_address'), self.data, format='multipart')
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_address_registration(self):
        # ensure a valid request from an unauthenticated user returns a 401 error
        response = self.client.post(reverse('register_address'), self.new_address, format='multipart')
        self.assertEqual(response.status_code, 401)
    
    def test_not_citizen(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('register_address'), self.new_address, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_invalid_data(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid data to be sent in the request
        invalid_data = {
            'country': 'Egypt',
            'city': 'Cairo',
            'street': 'El Haram',
            'building_number': 'invalid',
            'floor_number': 3,
            'apartment_number': 5,
            'proof_document': self.proof_document,
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('register_address'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder       
class PropertyRegistrationTest(BaseTestCase):
    '''Agenda: test the view allows the authenticated user in the citizens group to register a property correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')
        # create a property for the user
        self.property = PropertiesFactory(citizen=self.citizen)
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # open the media folder and create a SimpleUploadedFile for the test picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')

        # define the data for the existing property that will be sent in the test_property_already_registered function
        self.data = {
            'property_id': self.property.property_id,
            'location': self.property.location,
            'property_type': self.property.property_type,
            'description': self.property.description,
            'size': self.property.size,
            'picture': picture,
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }
        # define the data for the new property to be registered
        self.new_property = {
            'property_id': '12345',
            'location': 'New York',
            'property_type': 'Residential',
            'description': 'Near central park',
            'size': '200 sqm',
            'picture': picture,
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_property_registration(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('register_property'), self.new_property, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_property_already_registered(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure that if the property is already registered for the user, the request is rejected
        response = self.client.post(reverse('register_property'), self.data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_not_citizen(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('register_property'), self.new_property, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_unauthenticated_citizen(self):
        # ensure a valid request from an unauthenticated user returns a 401 error
        response = self.client.post(reverse('register_property'), self.new_property, format='multipart')
        self.assertEqual(response.status_code, 401)
    
    def test_invalid_data(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid data to be sent in the request
        invalid_data = {
            'property_id': '12345',
            'location': 'New York',
            'property_type': 'Residential',
            'description': 'Near central park',
            'size': '200 sqm',
            'picture': 'invalid', # invalid 
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('register_property'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder    
class VehicleRegistrationTest(BaseTestCase):
    '''Agenda: test the view allows the authenticated user in the citizens group to register a vehicle correctly'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user and a citizen for the user
        self.user = UserFactory(username='user')
        self.citizen = CitizensFactory(user=self.user)
        # create the Citizens group and add the user to it
        citizen_group = Group.objects.create(name='Citizens')
        self.user.groups.add(citizen_group)
        # create a user not in the Citizens group
        self.user_not_citizen = UserFactory(username='user_not_citizen')
        # create a vehicle for the user
        self.vehicle = VehiclesFactory(citizen=self.citizen)
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # open the media folder and create a SimpleUploadedFile for the test picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        
        # define the data for the existing vehicle that will be sent in the test_vehicle_already_registered function
        self.data = {
            'serial_number': self.vehicle.serial_number,
            'plate_number': self.vehicle.plate_number,
            'model': self.vehicle.model,
            'year': self.vehicle.year,
            'manufacturer': self.vehicle.manufacturer,
            'vehicle_type': self.vehicle.vehicle_type,
            'picture': picture,
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }
        # define the data for the new vehicle to be registered
        self.new_vehicle = {
            'serial_number': '12345',
            'plate_number': 'ABC123',
            'model': 'Toyota',
            'year': '2021',
            'manufacturer': 'Toyota',
            'vehicle_type': 'Sedan',
            'picture': picture,
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_vehicle_registration(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user in the Citizens group returns a success message
        response = self.client.post(reverse('register_vehicle'), self.new_vehicle, format='multipart')
        self.assertEqual(response.status_code, 200)
    
    def test_vehicle_already_registered(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure that if the vehicle is already registered for the user, the request is rejected
        response = self.client.post(reverse('register_vehicle'), self.data, format='multipart')
        self.assertEqual(response.status_code, 400)
    
    def test_unauthenticated_citizen(self):
        # ensure a valid request from an unauthenticated user returns a 401 error
        response = self.client.post(reverse('register_vehicle'), self.new_vehicle, format='multipart')
        self.assertEqual(response.status_code, 401)
    
    def test_not_citizen(self):
        # get the JWT token for the user not in the Citizens group and pass it in the request header
        token = self.get_jwt_token(self.user_not_citizen)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure a valid request from a user not in the Citizens group results in a forbidden response
        response = self.client.post(reverse('register_vehicle'), self.new_vehicle, format='multipart')
        self.assertEqual(response.status_code, 403)
    
    def test_invalid_data(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # define the invalid data to be sent in the request
        invalid_data = {
            'serial_number': '12-3-45', # invalid type
            'plate_number': 'ABC123',
            'model': 'Toyota',
            'year': '2021',
            'manufacturer': 'Toyota',
            'vehicle_type': 'Sedan',
            'picture': 'invalid', # invalid 
            'previous_owner_id': '1',
            'proof_document': self.proof_document,
        }
        # ensure an invalid request from a user in the Citizens group returns a bad request message
        response = self.client.post(reverse('register_vehicle'), invalid_data, format='multipart')
        self.assertEqual(response.status_code, 400)    

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class RenewalRequestsAPIViewTest(BaseTestCase):
    '''Agenda: test the view allows the inspector to view the pending requests'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create renewal requests to test the view
        self.renewal_request_1 = RenewalRequestsFactory(status='Pending')
        self.renewal_request_2 = RenewalRequestsFactory(status='Pending')
        self.rejected_renewal_request = RenewalRequestsFactory(status='Rejected')
        self.approved_renewal_request = RenewalRequestsFactory(status='Approved')

    def test_renewal_requests_view(self):
        # ensure that the view returns all the pending renewal requests
        response = self.client.get(reverse('renewal_requests'))
        self.assertEqual(response.status_code, 200)
        # ensure that the response returns the 2 pending requests
        response_data = response.json()
        self.assertEqual(len(response_data), 2) # copilot ^_^
        
    def test_view_only_returns_pending_requests(self):
        # ensure that the view doesn't return the rejected nor the approved renewal request
        response = self.client.get(reverse('renewal_requests'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        for request in response_data:
            self.assertNotEqual(request['status'], 'Rejected')
            self.assertNotEqual(request['status'], 'Approved')   

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class AcceptRenewalRequestTest(BaseTestCase):
    '''Agenda: test the view allows inspectors to accept the renewal requests'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user 
        self.user = UserFactory(username='user')
        # create the Inspectors group and add the user to it
        inspectors_group = Group.objects.create(name='Inspectors')
        self.user.groups.add(inspectors_group)
        # create a citizen and at them to the citzens group
        self.citizen_user = UserFactory(username='citizen')
        self.citizen = CitizensFactory(user=self.citizen_user)
        # create documents to renew
        self.passport = PassportsFactory(citizen=self.citizen)
        self.license = DrivingLicensesFactory(citizen=self.citizen)
        # create renewal requests for the documents
        self.passport_request = RenewalRequestsFactory(request_type="Passport", citizen=self.citizen)
        self.license_request = RenewalRequestsFactory(request_type="Driver's License", citizen=self.citizen)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_accept_passport_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the view accepts the passport renewal request
        response = self.client.post(reverse('accept_renewal_request', args=[self.passport_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure that the request status is Approved
        self.assertEqual(RenewalRequests.objects.get(id=self.passport_request.id).status, 'Approved')
        # ensure the issue date is today and the expiry date is today + 5 years
        self.assertEqual(Passports.objects.get(passport_number=self.passport.passport_number).issue_date, datetime.now().date())
        self.assertEqual(Passports.objects.get(passport_number=self.passport.passport_number).expiry_date, datetime.now().date() + timedelta(days=5*365))
        
    def test_accept_license_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the view accepts the license renewal request
        response = self.client.post(reverse('accept_renewal_request', args=[self.license_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure that the request status is Approved
        self.assertEqual(RenewalRequests.objects.get(id=self.license_request.id).status, 'Approved')
        # ensure the issue date is today and the expiry date is today + 10
        self.assertEqual(DrivingLicenses.objects.get(license_number=self.license.license_number).issue_date, datetime.now().date())
        self.assertEqual(DrivingLicenses.objects.get(license_number=self.license.license_number).expiry_date, datetime.now().date() + timedelta(days=10*365))
    
    def test_request_doesnt_exist(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure that if the request is not found, the view returns an error
        response = self.client.post(reverse('accept_renewal_request', args=[50]))
        self.assertEqual(response.status_code, 400)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class RejectRenewalRequestTest(BaseTestCase):
    '''Agenda: test the view allows inspectors to reject the renewal requests'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user 
        self.user = UserFactory(username='user')
        # create the Inspectors group and add the user to it
        inspectors_group = Group.objects.create(name='Inspectors')
        self.user.groups.add(inspectors_group)
        # create a citizen and add them to the citizens group
        self.citizen_user = UserFactory(username='citizen')
        self.citizen = CitizensFactory(user=self.citizen_user)
        # create documents to renew
        self.passport = PassportsFactory(citizen=self.citizen)
        self.license = DrivingLicensesFactory(citizen=self.citizen)
        # create renewal requests for the documents
        self.passport_request = RenewalRequestsFactory(request_type="Passport", citizen=self.citizen)
        self.license_request = RenewalRequestsFactory(request_type="Driver's License", citizen=self.citizen)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_reject_passport_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure the request is rejected
        response = self.client.post(reverse('reject_renewal_request', args=[self.passport_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure the request status is Rejected
        self.assertEqual(RenewalRequests.objects.get(id=self.passport_request.id).status, 'Rejected')
        # ensure that there is a rejection reason submitted in the request
        self.assertIsNotNone(RenewalRequests.objects.get(id=self.passport_request.id).rejection_reason)
        # ensure that the request is reviewed today
        self.assertEqual(RenewalRequests.objects.get(id=self.passport_request.id).reviewed_at.date(), datetime.now().date())

    def test_reject_license_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure the request is rejected
        response = self.client.post(reverse('reject_renewal_request', args=[self.license_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure the request status is Rejected
        self.assertEqual(RenewalRequests.objects.get(id=self.license_request.id).status, 'Rejected')
        # ensure that there is a rejection reason submitted in the request
        self.assertIsNotNone(RenewalRequests.objects.get(id=self.license_request.id).rejection_reason)
        # ensure that the request is reviewed today
        self.assertEqual(RenewalRequests.objects.get(id=self.license_request.id).reviewed_at.date(), datetime.now().date())

class RegistrationRequestsAPIViewTest(TestCase):
    '''Agenda: test the view allows the inspector to view the pending requests'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create registration requests to test the view
        self.registration_request_1 = RegistrationRequestsFactory(status='Pending')
        self.registration_request_2 = RegistrationRequestsFactory(status='Pending')
        self.rejected_registration_request = RegistrationRequestsFactory(status='Rejected')
        self.approved_registration_request = RegistrationRequestsFactory(status='Approved')

    def test_registration_requests_view(self):
        # ensure that the view returns all the pending registration requests
        response = self.client.get(reverse('registration_requests'))
        self.assertEqual(response.status_code, 200)
        # ensure that the response returns the 2 pending requests
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
        
    def test_view_only_returns_pending_requests(self):
        # ensure that the view doesn't return the rejected nor the approved renewal request
        response = self.client.get(reverse('registration_requests'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        for request in response_data:
            self.assertNotEqual(request['status'], 'Rejected')
            self.assertNotEqual(request['status'], 'Approved')

@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class AcceptRegistrationRequestTest(BaseTestCase):
    '''Agenda: test the view allows inspectors to accept the registration requests'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user 
        self.user = UserFactory(username='user')
        # create the Inspectors group and add the user to it
        inspectors_group = Group.objects.create(name='Inspectors')
        self.user.groups.add(inspectors_group)
        # create a citizen and at them to the citzens group
        self.citizen_user = UserFactory(username='citizen')
        self.citizen = CitizensFactory(user=self.citizen_user)
        # create entities to register
        self.address = AddressesFactory(citizen=self.citizen, state="Pending Request")
        self.property = PropertiesFactory(citizen=self.citizen, is_under_transfer=True)
        self.vehicle = VehiclesFactory(citizen=self.citizen, is_under_transfer=True)
        # create registration requests for the entities
        self.address_request = RegistrationRequestsFactory(request_type="Address Registration", citizen=self.citizen)
        self.property_request = RegistrationRequestsFactory(request_type="Property Registration", citizen=self.citizen)
        self.vehicle_request = RegistrationRequestsFactory(request_type="Vehicle Registration", citizen=self.citizen)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_accept_address_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the view accepts the address registration request
        response = self.client.post(reverse('accept_registration_request', args=[self.address_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure that the request status is Approved
        self.assertEqual(RegistrationRequests.objects.get(id=self.address_request.id).status, 'Approved')
        # ensure that the address state is changed to Active
        self.assertEqual(Addresses.objects.get(id=self.address.id).state, 'Active')
        
    def test_accept_property_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the view accepts the property registration request
        response = self.client.post(reverse('accept_registration_request', args=[self.property_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure that the request status is Approved
        self.assertEqual(RegistrationRequests.objects.get(id=self.property_request.id).status, 'Approved')
        # ensure that the propery is not under transfer anymore
        self.assertEqual(Properties.objects.get(id=self.property.id).is_under_transfer, False)
        # ensure that the property has been deleted from the record as owned by previous owner
        self.assertEqual(Properties.objects.filter(property_id=self.property.property_id).count(), 1)

    def test_accept_vehicle_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the view accepts the vehicle registration request
        response = self.client.post(reverse('accept_registration_request', args=[self.vehicle_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure that the request status is Approved
        self.assertEqual(RegistrationRequests.objects.get(id=self.vehicle_request.id).status, 'Approved')
        # ensure that the vehicle is not under transfer anymore
        self.assertEqual(Vehicles.objects.get(id=self.vehicle.id).is_under_transfer, False)
        # ensure that the vehicle has been deleted from the record as owned by previous owner
        self.assertEqual(Vehicles.objects.filter(plate_number=self.vehicle.plate_number).count(), 1)

    def test_request_doesnt_exist(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure that if the request is not found, the view returns an error
        response = self.client.post(reverse('accept_registration_request', args=[50]))
        self.assertEqual(response.status_code, 400)
    
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class RejectRegistrationRequestTest(BaseTestCase):
    '''Agenda: test the view allows inspectors to reject the registration requests'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user 
        self.user = UserFactory(username='user')
        # create the Inspectors group and add the user to it
        inspectors_group = Group.objects.create(name='Inspectors')
        self.user.groups.add(inspectors_group)
        # create a citizen and add them to the citizens group
        self.citizen_user = UserFactory(username='citizen')
        self.citizen = CitizensFactory(user=self.citizen_user)
        # create entities to register
        self.address = AddressesFactory(citizen=self.citizen, state="Pending Request")
        self.property = PropertiesFactory(citizen=self.citizen, is_under_transfer=True)
        self.vehicle = VehiclesFactory(citizen=self.citizen, is_under_transfer=True)
        # create registration requests for the documents
        self.address_request = RegistrationRequestsFactory(request_type="Address Registration", citizen=self.citizen)
        self.property_request = RegistrationRequestsFactory(request_type="Property Registration", citizen=self.citizen)
        self.vehicle_request = RegistrationRequestsFactory(request_type="Vehicle Registration", citizen=self.citizen)
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_reject_address_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure the request is rejected
        response = self.client.post(reverse('reject_registration_request', args=[self.address_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure the request status is Rejected
        self.assertEqual(RegistrationRequests.objects.get(id=self.address_request.id).status, 'Rejected')
        # ensure that there is a rejection reason submitted in the request
        self.assertIsNotNone(RegistrationRequests.objects.get(id=self.address_request.id).rejection_reason)
        # ensure that the request is reviewed today
        self.assertEqual(RegistrationRequests.objects.get(id=self.address_request.id).reviewed_at.date(), datetime.now().date())
        # ensure the placeholder address is deleted
        self.assertEqual(Addresses.objects.filter(id=self.address.id).count(), 0)
    
    def test_reject_property_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure the request is rejected
        response = self.client.post(reverse('reject_registration_request', args=[self.property_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure the request status is Rejected
        self.assertEqual(RegistrationRequests.objects.get(id=self.property_request.id).status, 'Rejected')
        # ensure that there is a rejection reason submitted in the request
        self.assertIsNotNone(RegistrationRequests.objects.get(id=self.property_request.id).rejection_reason)
        # ensure that the request is reviewed today
        self.assertEqual(RegistrationRequests.objects.get(id=self.property_request.id).reviewed_at.date(), datetime.now().date())
        # ensure the placeholder address is deleted
        self.assertEqual(Properties.objects.filter(id=self.property.id).count(), 0)

    def test_reject_vehicle_request(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # count notifications before the request
        initial_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure the request is rejected
        response = self.client.post(reverse('reject_registration_request', args=[self.vehicle_request.id]))
        self.assertEqual(response.status_code, 200)
        # count notifications after the request
        final_notification_count = Notifications.objects.filter(citizen=self.citizen).count()
        # ensure that the citizen receives a new notification
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        # ensure the request status is Rejected
        self.assertEqual(RegistrationRequests.objects.get(id=self.vehicle_request.id).status, 'Rejected')
        # ensure that there is a rejection reason submitted in the request
        self.assertIsNotNone(RegistrationRequests.objects.get(id=self.vehicle_request.id).rejection_reason)
        # ensure that the request is reviewed today
        self.assertEqual(RegistrationRequests.objects.get(id=self.vehicle_request.id).reviewed_at.date(), datetime.now().date())
        # ensure the placeholder address is deleted
        self.assertEqual(Vehicles.objects.filter(id=self.vehicle.id).count(), 0)

class GetContentViewsTest(TestCase):
    '''Agenda: Test the get views for the townhall and ensure they work as expected'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create a user and a citizen for that user
        self.user = UserFactory()
        self.citizen = CitizensFactory(user=self.user)
        # create a notification object for the user
        self.notification = Notifications.objects.create(citizen=self.citizen, message='Test Notification')
        # create 2 forums and add the citizen to them
        self.forum = Forums.objects.create(region="nation", title="test forum")
        self.forum2 = Forums.objects.create(region="nation", title="forum 2")
        self.forum.members.add(self.citizen)
        self.forum2.members.add(self.citizen)
        # create 2 posts for the first forum
        self.post = Posts.objects.create(forum=self.forum, author=self.citizen, title="test post 1", content="test")
        self.post2 = Posts.objects.create(forum=self.forum, author=self.citizen, title="test post 2", content="test")
        # create a comment for the first post
        self.comment = Comments.objects.create(post=self.post, author=self.citizen, content="test")

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_get_notification(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the notification for the user
        response = self.client.get(reverse('get_notifications'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
    
    def test_get_forums(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the forums
        response = self.client.get(reverse('get_forums'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
    
    def test_get_forum_by_id(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the forum by id
        response = self.client.get(reverse('get_forum', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], 'test forum')
    
    def test_get_posts(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the posts of the forum
        response = self.client.get(reverse('get_posts', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
    
    def test_get_post_by_id(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the post by id
        response = self.client.get(reverse('get_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], 'test post 1')
    
    def test_get_comment(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view returns the comment
        response = self.client.get(reverse('get_comments', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

class CreateContentaViewsTest(TestCase):
    '''Agenda: Test the create views for the townhall and ensure they work as expected'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create a user and a citizen for that user
        self.user = UserFactory()
        self.citizen = CitizensFactory(user=self.user)
        # create a 'Reps' user group and add the citizen to it
        self.reps = Group.objects.create(name="Reps")
        self.user.groups.add(self.reps)
        # define a forum for the post to be created
        self.forum = Forums.objects.create(region="nation", title="test forum 2")
        # create another user and a citizen for them
        self.user2 = UserFactory()
        self.citizen2 = CitizensFactory(user=self.user2)
        # create a post for the comment to be created
        self.post = Posts.objects.create(forum=self.forum, author=self.citizen, title="test post", content="test")
        # define the request data that will be sent to the views
        self.forum_data = {
            "title": "test forum",
            "region": "nation"
        }
        self.post_data = {
            "title": "test post",
            "content": "test",
            "forum_id": self.forum.id
        }
        self.comment_data = {
            "post": self.post.id,
            "content": "test",
        }
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_create_forum(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view creates a forum
        response = self.client.post(reverse('create_forum'), self.forum_data, format='json')
        self.assertEqual(response.status_code, 200)
        # ensure that both users are in the forum since the region is nation
        self.assertEqual(Forums.objects.get(title='test forum').members.count(), 2)
    
    def test_create_post(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view creates a post
        response = self.client.post(reverse('create_post'), self.post_data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_create_comment(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view creates a comment
        response = self.client.post(reverse('create_comment', args=[self.post.id]), self.comment_data, format='json')
        self.assertEqual(response.status_code, 200)

class ContentLikeViewsTest(TestCase):
    '''Agenda: Test the like views for the townhall and ensure they work as expected'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create a user and a citizen for that user
        self.user = UserFactory()
        self.citizen = CitizensFactory(user=self.user)
        # create a forum and a post for it
        self.forum = Forums.objects.create(region="nation", title="test forum")
        self.post = Posts.objects.create(forum=self.forum, author=self.citizen, title="test post", content="test")
        # create a comment on the post
        self.comment = Comments.objects.create(post=self.post, author=self.citizen, content="test")
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_like_post(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view likes the post
        response = self.client.post(reverse('update_post_likes', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_like_comment(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view likes the comment
        response = self.client.post(reverse('update_comment_likes', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)

class DeleteContentViewsTest(TestCase):
    '''Agenda: Test the delete views for the townhall and ensure they work as expected'''
    def setUp(self):
        # set up the test client
        self.client = APIClient()
        # create a user and a citizen for that user
        self.user = UserFactory()
        self.citizen = CitizensFactory(user=self.user)
        # create a forum and a post for it
        self.forum = Forums.objects.create(region="nation", title="test forum")
        self.post = Posts.objects.create(forum=self.forum, author=self.citizen, title="test post", content="test")
        # create a comment on the post
        self.comment = Comments.objects.create(post=self.post, author=self.citizen, content="test")
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_delete_comment(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view deletes the comment
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        # get the JWT token for the user and pass it in the request header
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # ensure the view deletes the post
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

'''MODELS TESTS'''
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class ModelCreationTests(BaseTestCase):
    '''Agenda: test the creation of models, field constraints, and relationships work as expected'''
    def setUp(self):
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # open the media folder and create a SimpleUploadedFile for the test picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            self.picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        # create a user
        self.user = UserFactory()
        # create data for the user
        self.citizen = Citizens.objects.create(
            user=self.user,
            national_id='1234567890',
            date_of_birth='2000-01-01',
            first_name='John',
            last_name='Doe',
            blood_type='O+',
            sex='M',
            picture=self.picture
        )
        self.address = Addresses.objects.create(
            country='Egypt',
            city='Cairo',
            street='El-Merghany',
            building_number='123',
            floor_number='2',
            apartment_number='4',
            citizen=self.citizen,
            state='Pending Request'
        )
        self.passport = Passports.objects.create(
            passport_number='12345678',
            citizen=self.citizen,
            issue_date='2021-01-01',
            expiry_date='2026-01-01',
            picture=self.picture
        )
        self.license = DrivingLicenses.objects.create(
            license_number='12345678',
            citizen=self.citizen,
            issue_date='2021-01-01',
            expiry_date='2026-01-01',
            picture=self.picture
        )
        self.property = Properties.objects.create(
            property_id='PROP123',
            citizen=self.citizen,
            location='Downtown',
            property_type='Residential',
            description='A nice place to live.',
            size='1200 sqft',
            picture=self.picture,
        )
        self.vehicle = Vehicles.objects.create(
            serial_number=123456,
            citizen=self.citizen,
            model='Mustang',
            manufacturer='Ford',
            year=2020,
            vehicle_type='Sports Car',
            picture=self.picture,
            plate_number='XYZ123',
        )
        self.notification = Notifications.objects.create(
            citizen=self.citizen,
            message='Test Notification'
        )
        self.renewal_request = RenewalRequests.objects.create(
            citizen=self.citizen,
            request_type='Passport'
        )
        self.registration_request = RegistrationRequests.objects.create(
            citizen=self.citizen,
            request_type='Address Registration'
        )
        self.forum = Forums.objects.create(
            title='Test Forum',
            region='Cairo'
        )
        self.post = Posts.objects.create(
            forum=self.forum,
            title='Test Post',
            content='Test Content',
            author=self.citizen
        )
        self.comment = Comments.objects.create(
            post=self.post,
            content='Test Comment',
            author=self.citizen
        )
    
    # ensure the creation of the models works as expected
    def test_address_creation(self):
        address = Addresses.objects.get(id=self.address.id)
        self.assertEqual(address.country, 'Egypt')
        self.assertEqual(address.city, 'Cairo')
        self.assertEqual(address.street, 'El-Merghany')
        self.assertEqual(address.building_number, 123)
        self.assertEqual(address.floor_number, 2)
        self.assertEqual(address.apartment_number, 4)
        self.assertEqual(address.state, 'Pending Request')
    
    def test_citizen_creation(self):
        citizen = Citizens.objects.get(user=self.user)
        self.assertEqual(citizen.national_id, '1234567890')
        self.assertEqual(citizen.date_of_birth, datetime.strptime('2000-01-01', '%Y-%m-%d').date())
        self.assertEqual(citizen.first_name, 'John')
        self.assertEqual(citizen.last_name, 'Doe')
        self.assertEqual(citizen.blood_type, 'O+')
        self.assertEqual(citizen.sex, 'M')
    
    def test_passport_creation(self):
        passport = Passports.objects.get(passport_number=self.passport.passport_number)
        self.assertEqual(passport.passport_number, '12345678')
        self.assertEqual(passport.issue_date, datetime.strptime('2021-01-01', '%Y-%m-%d').date())
        self.assertEqual(passport.expiry_date, datetime.strptime('2026-01-01', '%Y-%m-%d').date())
    
    def test_license_creation(self):
        license = DrivingLicenses.objects.get(license_number=self.license.license_number)
        self.assertEqual(license.license_number, '12345678')
        self.assertEqual(license.issue_date, datetime.strptime('2021-01-01', '%Y-%m-%d').date())
        self.assertEqual(license.expiry_date, datetime.strptime('2026-01-01', '%Y-%m-%d').date())
    
    def test_property_creation(self):
        property = Properties.objects.get(property_id=self.property.property_id)
        self.assertEqual(property.property_id, 'PROP123')
        self.assertEqual(property.location, 'Downtown')
        self.assertEqual(property.property_type, 'Residential')
        self.assertEqual(property.description, 'A nice place to live.')
        self.assertEqual(property.size, '1200 sqft')
    
    def test_vehicle_creation(self):
        vehicle = Vehicles.objects.get(serial_number=self.vehicle.serial_number)
        self.assertEqual(vehicle.serial_number, 123456)
        self.assertEqual(vehicle.model, 'Mustang')
        self.assertEqual(vehicle.manufacturer, 'Ford')
        self.assertEqual(vehicle.year, 2020)
        self.assertEqual(vehicle.vehicle_type, 'Sports Car')
        self.assertEqual(vehicle.plate_number, 'XYZ123')
    
    def test_notification_creation(self):
        notification = Notifications.objects.get(id=self.notification.id)
        self.assertEqual(notification.message, 'Test Notification')
    
    def test_renewal_request_creation(self):
        renewal_request = RenewalRequests.objects.get(id=self.renewal_request.id)
        self.assertEqual(renewal_request.request_type, 'Passport')
    
    def test_registration_request_creation(self):
        registration_request = RegistrationRequests.objects.get(id=self.registration_request.id)
        self.assertEqual(registration_request.request_type, 'Address Registration')
    
    def test_forum_creation(self):
        forum = Forums.objects.get(id=self.forum.id)
        self.assertEqual(forum.title, 'Test Forum')
        self.assertEqual(forum.region, 'Cairo')
        # add the citizen as a member to the form
        forum.members.add(self.citizen)
        # ensure that the citizen is a member of the forum
        self.assertIn(self.citizen, forum.members.all())
    
    def test_post_creation(self):
        post = Posts.objects.get(id=self.post.id)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test Content')
        self.assertEqual(post.author, self.citizen)
    
    def test_comment_creation(self):
        comment = Comments.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.author, self.citizen)
    
    # ensure the unique constraints are enforced
    def test_national_id_uniqueness(self):
        # create 2 users with the same national id
        user1 = User.objects.create(username='user1', password='password')
        citizen1 = Citizens.objects.create(user=user1, national_id='12345', first_name='John', last_name='Doe', date_of_birth='1990-01-01')
        user2 = User.objects.create(username='user2', password='password')
        # ensure that the second user with the same national id cannot be created
        with self.assertRaises(IntegrityError):
            Citizens.objects.create(user=user2, national_id='12345', first_name='Jane', last_name='Smith', date_of_birth='1992-02-02')

    # ensure the default value for the state field is as expected
    def test_default_state_value(self):
        user = User.objects.create(username='user', password='password')
        citizen = Citizens.objects.create(user=user, national_id='12345', first_name='John', last_name='Doe', date_of_birth='1990-01-01')
        address = Addresses.objects.create(citizen=citizen, country='Country', city='City', street='Street', building_number=1, floor_number=2, apartment_number=3)
        self.assertEqual(address.state, 'Active')

    # ensure the one to one relationship between User and Citizens is as expected
    def test_user_citizen_relationship(self):
        user = User.objects.create(username='user', password='password')
        citizen = Citizens.objects.create(user=user, national_id='67890', first_name='Alice', last_name='Wonder', date_of_birth='1988-08-08')
        self.assertEqual(user.citizen, citizen)
        self.assertEqual(citizen.user, user)
    
    # ensure the one to many relationship between Citizens and Addresses is as expected
    def test_citizen_address_relationship(self):
        user = User.objects.create(username='user', password='password')
        citizen = Citizens.objects.create(user=user, national_id='67890', first_name='Alice', last_name='Wonder', date_of_birth='1988-08-08')
        address = Addresses.objects.create(citizen=citizen, country='Country', city='City', street='Street', building_number=1, floor_number=2, apartment_number=3)
        self.assertEqual(address.citizen, citizen)
        self.assertIn(address, citizen.addresses_set.all())
 
'''SERIALIZERS TESTS'''
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class ModelSerializersTest(BaseTestCase):
    '''Agenda: test the basic serialization-deserialization for the model serializers'''
    def setUp(self):
        # create model objects
        self.citizen = CitizensFactory()
        self.user = UserFactory()
        self.passport = PassportsFactory()
        self.license = DrivingLicensesFactory()
        self.address = AddressesFactory()
        self.property = PropertiesFactory()
        self.vehicle = VehiclesFactory()
        self.notification = NotificationsFactory()
        self.forum = Forums.objects.create(title="test", region="nation")
        self.post = Posts.objects.create(forum=self.forum, author=self.citizen, content="test", title="test")
        self.comment = Comments.objects.create(post=self.post, author=self.citizen, content="test")
        # create serializers instances
        self.citizen_serializer = CitizensSerializer(self.citizen)
        self.user_serializer = UserSerializer(self.user)
        self.passport_serializer = PassportsSerializer(self.passport)
        self.licnese_serializer = DrivingLicenseSerializer(self.license)
        self.address_serializer = AddressesSerializer(self.address)
        self.property_serializer = PropertiesSerializer(self.property)
        self.vehicle_serializer = VehiclesSerializer(self.vehicle)
        self.notification_serializer = NotificationsSerializer(self.notification)
        self.forum_serializer = ForumsSerializer(self.forum)
        self.post_serializer = PostsSerializer(self.post)
        self.comment_serializer = CommentsSerializer(self.comment)
    
    def test_citizen_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.citizen_serializer.data
        self.assertEqual(set(data.keys()), set(['picture', 'user', 'national_id', 'date_of_birth', 'first_name', 'last_name', 'blood_type', 'sex']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['picture'], self.citizen.picture.url)
        self.assertEqual(data['national_id'], self.citizen.national_id)
        self.assertEqual(datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(), self.citizen.date_of_birth)
        self.assertEqual(data['first_name'], self.citizen.first_name)
        self.assertEqual(data['last_name'], self.citizen.last_name)
        self.assertEqual(data['blood_type'], self.citizen.blood_type)
        self.assertEqual(data['sex'], self.citizen.sex)
    
    def test_user_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()), set(['username']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['username'], self.user.username)
    
    def test_passport_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.passport_serializer.data
        self.assertEqual(set(data.keys()), set(['passport_number', 'citizen', 'issue_date', 'expiry_date', 'picture']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['passport_number'], self.passport.passport_number)
        self.assertEqual(datetime.strptime(data['issue_date'], '%Y-%m-%d').date(), self.passport.issue_date)
        self.assertEqual(datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(), self.passport.expiry_date)
        self.assertEqual(data['picture'], self.passport.picture.url)

    def test_license_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.licnese_serializer.data
        self.assertEqual(set(data.keys()), set(['license_number', 'citizen', 'issue_date', 'expiry_date', 'picture', 'nationality', 'emergency_contact', 'license_class']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['license_number'], self.license.license_number)
        self.assertEqual(datetime.strptime(data['issue_date'], '%Y-%m-%d').date(), self.license.issue_date)
        self.assertEqual(datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(), self.license.expiry_date)
        self.assertEqual(data['picture'], self.license.picture.url)
        self.assertEqual(data['nationality'], self.license.nationality)
        self.assertEqual(data['emergency_contact'], self.license.emergency_contact)
        self.assertEqual(data['license_class'], self.license.license_class)

    def test_address_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.address_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'country', 'city', 'street', 'building_number', 'floor_number', 'apartment_number', 'citizen', 'state']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['country'], self.address.country)
        self.assertEqual(data['city'], self.address.city)
        self.assertEqual(data['street'], self.address.street)
        self.assertEqual(data['building_number'], self.address.building_number)
        self.assertEqual(data['floor_number'], self.address.floor_number)
        self.assertEqual(data['apartment_number'], self.address.apartment_number)
        self.assertEqual(data['state'], self.address.state)

    def test_property_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.property_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'property_id', 'location', 'property_type', 'citizen', 'picture', 'is_under_transfer', 'description', 'size']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['property_id'], self.property.property_id)
        self.assertEqual(data['location'], self.property.location)
        self.assertEqual(data['property_type'], self.property.property_type)
        self.assertEqual(data['description'], self.property.description)
        self.assertEqual(data['size'], self.property.size)
        
    def test_vehicle_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.vehicle_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'serial_number', 'plate_number', 'model', 'year', 'manufacturer', 'vehicle_type', 'citizen', 'picture', 'is_under_transfer']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['serial_number'], self.vehicle.serial_number)
        self.assertEqual(data['plate_number'], self.vehicle.plate_number)
        self.assertEqual(data['model'], self.vehicle.model)
        self.assertEqual(str(data['year']), self.vehicle.year)
        self.assertEqual(data['manufacturer'], self.vehicle.manufacturer)
        self.assertEqual(data['vehicle_type'], self.vehicle.vehicle_type)
        self.assertEqual(data['picture'], self.vehicle.picture.url)
    
    def test_notification_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.notification_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'citizen', 'message']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['message'], self.notification.message)
    
    def test_forum_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.forum_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'region', 'members']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['title'], self.forum.title)
        self.assertEqual(data['region'], self.forum.region)
    
    def test_post_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.post_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'content', 'author', 'forum', 'picture', 'timestamp', 'likes', 'likes_count']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['title'], self.post.title)
        self.assertEqual(data['content'], self.post.content)
        self.assertEqual(data['author'], self.post.author.user.username)
        self.assertEqual(data['forum'], self.post.forum.id)

    def test_comment_serializer_contains_expected_fields(self):
        # ensure the serializer contains the expected fields
        data = self.comment_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'content', 'author', 'post', 'picture', 'timestamp', 'likes', 'likes_count']))
        # ensure that the fields equal the model fields
        self.assertEqual(data['content'], self.comment.content)
        self.assertEqual(data['author'], self.comment.author.user.username)
        self.assertEqual(data['post'], self.comment.post.id)
                            
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder                         
class ValidationSerializersTest(BaseTestCase):
    '''Agenda: test the validation serilaizers are valid for correct data and invalid otherwise'''
    def setUp(self):
        # create factory instances 
        self.citizen = CitizensFactory()
        self.address = AddressesFactory()
        # open the media folder and create a SimpleUploadedFile for the test picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        self.passport = PassportsFactory(passport_number='12345678', picture=picture)
        self.license = DrivingLicensesFactory(license_number='12345678', picture=picture)
       
    def test_valid_citizen_validation_Serializer(self):
        # define the valid data
        data = {
            'national_id': self.citizen.national_id,
            'date_of_birth': str(self.citizen.date_of_birth),
            'first_name': self.citizen.first_name,
            'last_name': self.citizen.last_name,
            'blood_type': self.citizen.blood_type,
            'sex': self.citizen.sex,
        }
        # create a serialzier and pass the data
        serializer = CitizenValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        # copilot ^_^
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_citizen_validation_serializer(self):
        # define the invalid data
        data = {
            'national_id': '12345',
            'date_of_birth': '2021-01-01',
            'first_name': 'John',
            'last_name': 'Invalid',
            'blood_type': 'O+',
            'sex': "M"
        }
        # create a serialzier and pass the data
        serializer = CitizenValidationSerializer(data=data)
        # ensure that it's invalid
        self.assertFalse(serializer.is_valid())

    def test_address_validation_serializer(self):
        # define the valid data
        data = {
            'country': self.address.country,
            'city': self.address.city,
            'street': self.address.street,
            'building_number': self.address.building_number,
            'floor_number': self.address.floor_number,
            'apartment_number': self.address.apartment_number,
        }
        # create a serialzier and pass the data
        serializer = AddressValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        self.assertTrue(serializer.is_valid())
    
    def test_passport_validation_serializer_without_proof(self):
        # define the data without the reason of early renewal nor the proof document
        data = {
            'passport_number': self.passport.passport_number,
            'issue_date': str(self.passport.issue_date),
            'expiry_date': str(self.passport.expiry_date),
            'picture': self.passport.picture
        }
        # create a srialzier and pass the data
        serializer = PassportValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['reason'])
        self.assertIsNone(serializer.validated_data['proof_document'])

    def test_passport_validation_serializer_with_proof(self):
        # create a SimpleUploadedFile for the proof document
        proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # define the data with the reason of early renewal and the proof document
        data = {
            'passport_number': self.passport.passport_number,
            'issue_date': str(self.passport.issue_date),
            'expiry_date': str(self.passport.expiry_date),
            'picture': self.passport.picture,
            'reason': 'Lost',
            'proof_document': proof_document
        }
        # create a srialzier and pass the data
        serializer = PassportValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        self.assertTrue(serializer.is_valid())
    
    def test_license_validation_serializer_without_proof(self):
        # define the data without the reason of early renewal nor the proof document
        data = {
            'license_number': self.license.license_number,
            'issue_date': str(self.license.issue_date),
            'expiry_date': str(self.license.expiry_date),
            'nationality': self.license.nationality,
            'license_class': self.license.license_class,
            'emergency_contact': self.license.emergency_contact,
            'picture': self.license.picture
        }
        # create a srialzier and pass the data
        serializer = DrivingLicenseValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['reason'])
        self.assertIsNone(serializer.validated_data['proof_document'])

    def test_license_validation_serializer_with_proof(self):
        # create a SimpleUploadedFile for the proof document
        proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # define the data with the reason of early renewal and the proof document
        data = {
            'license_number': self.license.license_number,
            'issue_date': str(self.license.issue_date),
            'expiry_date': str(self.license.expiry_date),
            'nationality': self.license.nationality,
            'license_class': self.license.license_class,
            'emergency_contact': self.license.emergency_contact,
            'picture': self.license.picture,
            'reason': 'Lost',
            'proof_document': proof_document
        }
        # create a srialzier and pass the data
        serializer = DrivingLicenseValidationSerializer(data=data)
        # ensure that it's valid
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)  # Print the errors to debug
        self.assertNotIn('The data you entered does not match our records.', serializer.errors.get('non_field_errors', []))
        self.assertTrue(serializer.is_valid())
    
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class RenewalRequestsSerializerTest(BaseTestCase):    
    '''Agenda: test the representation based on the 'to_representation' method is correct according to request type'''
    def test_passport_request_representation(self):
        # define a citizen and create a passport for them
        citizen = CitizensFactory()
        passport = PassportsFactory(citizen=citizen)
        # create a renewal request for their passport
        renewal_request = RenewalRequestsFactory(citizen=citizen, request_type='Passport')
        # create a serializer instance and pass the request to it
        serializer = RenewalRequestsSerializer(renewal_request)
        data = serializer.data
        # esnure the representation includes the passport and not the license & that the citizen info is correct
        self.assertIn('passport_info', data)
        self.assertIn('citizen_info', data)
        self.assertNotIn('license_info', data)
        self.assertNotIn('citizen_license_info', data)
        self.assertNotIn('citizen_passport_info', data)
        # ensure the expected fields in the citizen_info are correct
        citizen_info = data['citizen_info']
        self.assertEqual(set(citizen_info.keys()), set(['national_id', 'first_name', 'last_name', 'date_of_birth', 'sex']))

    def test_license_request_representation(self):
        # define a citizen and create a license for them
        citizen = CitizensFactory()
        license = DrivingLicensesFactory(citizen=citizen)
        # create a renewal request for their license
        renewal_request = RenewalRequestsFactory(citizen=citizen, request_type="Driver's License")
        # create a serializer instance and pass the request to it
        serializer = RenewalRequestsSerializer(renewal_request)
        data = serializer.data
        # esnure the representation includes the license and not the passport & that the citizen info is correct
        self.assertIn('license_info', data)
        self.assertIn('citizen_info', data)
        self.assertNotIn('passport_info', data)
        self.assertNotIn('citizen_license_info', data)
        self.assertNotIn('citizen_passport_info', data)
        # ensure the expected fields in the citizen_info are correct
        citizen_info = data['citizen_info']
        self.assertEqual(set(citizen_info.keys()), set(['national_id', 'first_name', 'last_name', 'blood_type']))
    
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder    
class RegistrationRequestsSerializerTest(BaseTestCase):
    '''Agenda: test the representation based on the 'to_representation' method is correct according to request type'''
    def setUp(self):
        # set up a testing client
        self.client = APIClient()
        # create a user 
        self.user = UserFactory(username='user')
        # create a citizen for the user
        self.citizen = CitizensFactory(user=self.user)
        # create entities to register
        self.address = AddressesFactory(citizen=self.citizen, state="Pending Request")
        self.property = PropertiesFactory(citizen=self.citizen, is_under_transfer=True)
        self.vehicle = VehiclesFactory(citizen=self.citizen, is_under_transfer=True)
        # create registration requests for the entities
        self.address_request = RegistrationRequestsFactory(request_type="Address Registration", citizen=self.citizen)
        self.property_request = RegistrationRequestsFactory(request_type="Property Registration", citizen=self.citizen)
        self.vehicle_request = RegistrationRequestsFactory(request_type="Vehicle Registration", citizen=self.citizen)
    
    def test_address_request_representation(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.address_request)
        data = serializer.data
        # esnure the representation includes the address and not the property and vehicle 
        self.assertIn('address_info', data)
        self.assertIn('citizen_info', data)
        self.assertNotIn('property_info', data)
        self.assertNotIn('vehicle_info', data)

    def test_property_request_representation(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.property_request)
        data = serializer.data
        # esnure the representation includes the address and not the property and vehicle 
        self.assertIn('property_info', data)
        self.assertIn('citizen_info', data)
        self.assertNotIn('address_info', data)
        self.assertNotIn('vehicle_info', data)

    def test_vehicle_request_representation(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.vehicle_request)
        data = serializer.data
        # esnure the representation includes the address and not the property and vehicle 
        self.assertIn('vehicle_info', data)
        self.assertIn('citizen_info', data)
        self.assertNotIn('address_info', data)
        self.assertNotIn('property_info', data)
    
    def test_get_address_info_method(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.address_request)
        # retrieve the address information from the serializer data
        address_info = serializer.data['address_info']
        # check that the serializer returns the correct address info
        self.assertIsNotNone(address_info)
        self.assertEqual(address_info['id'], self.address.id)
        self.assertEqual(address_info['state'], 'Pending Request')
        # copilot ^_^
    
    def test_get_property_info_method(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.property_request)
        # retrieve the property information from the serializer data
        property_info = serializer.data['property_info']
        # check that the serializer returns the correct property info
        self.assertIsNotNone(property_info)
        self.assertEqual(property_info['id'], self.property.id)
        self.assertEqual(property_info['is_under_transfer'], True)

    def test_get_vehicle_info_method(self):
        # create a serializer instance and pass the request to it
        serializer = RegistrationRequestsSerializer(self.vehicle_request)
        # retrieve the vehicle information from the serializer data
        vehicle_info = serializer.data['vehicle_info']
        # check that the serializer returns the correct vehicle info
        self.assertIsNotNone(vehicle_info)
        self.assertEqual(vehicle_info['id'], self.vehicle.id)
        self.assertEqual(vehicle_info['is_under_transfer'], True)
    
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # this will store and clean up the uploaded files in a temporary folder
class RegistrationSerializersTest(BaseTestCase):
    '''Agenda: test the registration serializers'''
    def setUp(self):
        # create a SimpleUploadedFile for the proof document
        self.proof_document = SimpleUploadedFile(
            "proof_document.pdf",  
            b"Dummy file content",  
            content_type='application/pdf'
        ) 
        # open the media folder and create a SimpleUploadedFile for the test picture
        with default_storage.open('valid.jpeg', 'rb') as image_file:
            picture = SimpleUploadedFile("TestImage.jpg", image_file.read(), content_type='image/jpeg')
        # define the valid and invalid data
        self.valid_property_data = {
            'property_id': 'PROP123',
            'location': 'Downtown',
            'property_type': 'Residential',
            'description': 'A nice place to live.',
            'size': '1200 sqft',
            'picture': picture,
            'previous_owner_id': 'OWNER456',
            'proof_document': self.proof_document
        }
        self.invalid_property_data = {
            'property_id': '',
            'location': 'Downtown',
            'property_type': 'InvalidType', 
            'description': 'A nice place to live.',
            'size': '1200 sqft',
            'picture': '',  
            'previous_owner_id': 'OWNER456',
            'proof_document': '' 
        }
        self.valid_vehicle_data = {
            'serial_number': 123456,
            'model': 'Mustang',
            'manufacturer': 'Ford',
            'year': 2020,
            'vehicle_type': 'Sports Car',
            'picture': picture,
            'plate_number': 'XYZ123',
            'proof_document':self.proof_document,
            'previous_owner_id': 'OWNER789'
        }

        self.invalid_vehicle_data = {
            'serial_number': 'abc',  
            'model': 'Mustang',
            'manufacturer': 'Ford',
            'year': 2020,
            'vehicle_type': 'Flying Car', 
            'picture': '',  
            'plate_number': 'XYZ123',
            'proof_document': '', 
            'previous_owner_id': 'OWNER789'
        }

    def test_property_registration_valid_data(self):
        # create a serializer instance and place the data
        serializer = PropertyRegistrationSerializer(data=self.valid_property_data)
        # ensure the serializer is valid
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['property_id'], 'PROP123')
        self.assertEqual(serializer.validated_data['location'], 'Downtown')
        self.assertEqual(serializer.validated_data['property_type'], 'Residential')
        self.assertEqual(serializer.validated_data['size'], '1200 sqft')

    def test_property_registration_invalid_data(self):
        # create a serializer instance and place the data
        serializer = PropertyRegistrationSerializer(data=self.invalid_property_data)
        # ensure the serializer is not valid
        self.assertFalse(serializer.is_valid())
        self.assertIn('property_id', serializer.errors)
        self.assertIn('property_type', serializer.errors)
        self.assertIn('picture', serializer.errors)
        self.assertIn('proof_document', serializer.errors)
    
    def test_vehicle_registration_valid_data(self):
         # create a serializer instance and place the data
        serializer = VehicleRegistrationSerializer(data=self.valid_vehicle_data)
        # ensure the serializer is valid
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['serial_number'], 123456)
        self.assertEqual(serializer.validated_data['model'], 'Mustang')
        self.assertEqual(serializer.validated_data['manufacturer'], 'Ford')
        self.assertEqual(serializer.validated_data['year'], 2020)
        self.assertEqual(serializer.validated_data['vehicle_type'], 'Sports Car')

    def test_vehicle_registration_invalid_data(self):
        # create a serializer instance and place the data
        serializer = VehicleRegistrationSerializer(data=self.invalid_vehicle_data)
        # ensure the serializer is not valid
        self.assertFalse(serializer.is_valid())
        self.assertIn('serial_number', serializer.errors)
        self.assertIn('vehicle_type', serializer.errors)
        self.assertIn('picture', serializer.errors)
        self.assertIn('proof_document', serializer.errors)

