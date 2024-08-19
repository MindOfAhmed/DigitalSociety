import factory
from django.core.files.base import ContentFile
from .models import *
from django.contrib.auth.models import User
'''
In this file, factories for the models are defined. These factories are used to create instances 
of the models for testing purposes. Random data is generated for the fields of the models using
the factory's Faker class. 
'''
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class CitizensFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Citizens

    user = factory.SubFactory(UserFactory)
    national_id = factory.Faker('ssn')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth')
    sex = factory.Faker('random_element', elements=('M', 'F'))
    blood_type = factory.Faker('random_element', elements=('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))

class AddressesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Addresses
    
    citizen = factory.SubFactory(CitizensFactory)
    country = factory.Faker('country')
    city = factory.Faker('city')
    street = factory.Faker('street_name')
    building_number = factory.Faker('random_int')
    floor_number = factory.Faker('random_int')
    apartment_number = factory.Faker('random_int')
    state = factory.Faker('random_element', elements=('Active', 'Inactive', 'Pending Request'))

class PassportsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Passports

    citizen = factory.SubFactory(CitizensFactory)
    passport_number = factory.Faker('ssn')
    issue_date = factory.Faker('date_this_decade')
    expiry_date = factory.Faker('date_this_decade')
    picture = factory.django.ImageField(from_func=lambda: ContentFile(b'', 'test.jpg'))

class DrivingLicensesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DrivingLicenses

    citizen = factory.SubFactory(CitizensFactory)
    license_number = factory.Sequence(lambda n: f'L{1000000 + n}')
    issue_date = factory.Faker('date_this_decade')
    expiry_date = factory.Faker('date_this_decade')
    nationality = factory.Faker('country')
    emergency_contact = factory.Faker('phone_number')
    license_class = factory.Faker('random_element', elements=('A', 'B', 'C', 'D'))
    picture = factory.django.ImageField(from_func=lambda: ContentFile(b'', 'test.jpg'))

class PropertiesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Properties
    
    property_id = factory.Faker('ssn')
    citizen = factory.SubFactory(CitizensFactory)
    location = factory.Faker('address')
    property_type = factory.Faker('random_element', elements=('Residential', 'Commercial', 'Land', 'Industrial', 'Agricultural', 'Intellectual'))
    description = factory.Faker('text')
    size = factory.Faker('text')
    picture = factory.django.ImageField(from_func=lambda: ContentFile(b'', 'test.jpg'))
    is_under_transfer = factory.Faker('boolean')
    
class VehiclesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicles

    serial_number = factory.Sequence(lambda n: 10000 + n)
    citizen = factory.SubFactory(CitizensFactory)
    model = factory.Faker('word')
    manufacturer = factory.Faker('word')
    year = factory.Faker('year')
    vehicle_type = factory.Faker('random_element', elements=('SUV', 'Sedan', 'Truck', 'Bus', 'Van', 'Sports Car', 'Motorcycle'))
    picture = factory.django.ImageField(from_func=lambda: ContentFile(b'', 'test.jpg'))
    plate_number = factory.Faker('ssn')
    is_under_transfer = factory.Faker('boolean')

class NotificationsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notifications

    citizen = factory.SubFactory(CitizensFactory)
    message = factory.Faker('text')

class RenewalRequestsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RenewalRequests
    
    citizen = factory.SubFactory(CitizensFactory)
    request_type = factory.Faker('random_element', elements=("Passport", "Driver's License"))
    picture = factory.django.ImageField(from_func=lambda: ContentFile(b'', 'test.jpg'))
    reason = factory.Faker('text')
    proof_document = factory.django.FileField()
    status = factory.Faker('random_element', elements=('Pending', 'Approved', 'Rejected'))
    rejection_reason = factory.Faker('text')

class RegistrationRequestsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistrationRequests

    citizen = factory.SubFactory(CitizensFactory)
    request_type = factory.Faker('random_element', elements=("Address Registration", "Property Registration", "Vehicle Registration"))
    proof_document = factory.django.FileField()
    previous_owner_id = factory.Faker('ssn')
    status = factory.Faker('random_element', elements=('Pending', 'Approved', 'Rejected'))
    rejection_reason = factory.Faker('text')