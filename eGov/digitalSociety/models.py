from django.db import models
from django.contrib.auth.models import User

def profile_picture_path(instance, filename):
    return f'profile_pictures/{instance.national_id}/{filename}'

class Citizens(models.Model):
    # map the citizen to the User model provided by Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen', null=True) # null=True
    national_id = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    picture = models.ImageField(upload_to=profile_picture_path, default='default.png')
    # each one is written twice because the first one is the value and the second is what will appear in the dropdown menu
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)

    def __str__(self):
        return self.user.username

class Addresses(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    building_number = models.IntegerField()
    floor_number = models.IntegerField()
    apartment_number = models.IntegerField()
    STATE_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive'), ('Pending Request', 'Pending Request')]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Active')

    def __str__(self):
        return self.street + ', ' + self.city + ', ' + self.country

def passport_picture_path(instance, filename):
    return f'passport_pictures/{instance.citizen.national_id}/{filename}'

def request_picture_path(instance, filename):
    return f'requests_new_pictures/{instance.citizen.national_id}/{filename}'

def proof_document_path(instance, filename):
    return f'requests_doc_proof/{instance.citizen.national_id}/{filename}'

def license_path(instance, filename):
    return f'license_pictures/{instance.citizen.national_id}/{filename}'

def property_path(instance, filename):
    return f'property_pictures/{instance.property_id}/{filename}'

def vehicle_path(instance, filename):
    return f'vehicle_pictures/{instance.serial_number}/{filename}'

class Passports(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=30, primary_key=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    picture = models.ImageField(upload_to=passport_picture_path)

class DrivingLicenses(models.Model):
    license_number = models.CharField(max_length=30, primary_key=True)
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=license_path)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    nationality = models.CharField(max_length=30, default='X')
    emergency_contact = models.CharField(max_length=30)
    CLASS_TYPES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    license_class = models.CharField(max_length=1, choices=CLASS_TYPES)

class Properties(models.Model):
    property_id = models.CharField(max_length=30) # this isn't the pk beacuse during the transfer process, there will be 2 instances of the property
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    PROPERTY_TYPES = [
        ('Residential', 'Residential'), 
        ('Commercial', 'Commercial'), 
        ('Industrial', 'Industrial'), 
        ('Agricultural', 'Agricultural'),
        ('Land', 'Land'), 
        ('Intellectual', 'Intellectual')
    ]
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    description = models.TextField()
    size = models.CharField(max_length=30, blank=True, null=True)
    picture = models.ImageField(upload_to=property_path)
    is_under_transfer = models.BooleanField(default=False)

class Vehicles(models.Model):
    serial_number = models.IntegerField()
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    year = models.IntegerField()
    VEHICLE_TYPES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'), 
        ('Truck', 'Truck'), 
        ('Van', 'Van'), 
        ('Bus', 'Bus'),
        ('Sports Car', 'Sports Car'),
        ('Motorcycle', 'Motorcycle')
    ]
    vehicle_type = models.CharField(max_length=30, choices=VEHICLE_TYPES)
    picture = models.ImageField(upload_to=vehicle_path)
    plate_number = models.CharField(max_length=30, unique=True)
    is_under_transfer = models.BooleanField(default=False)

class Notifications(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    message = models.TextField()

class Forums(models.Model):
    title = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    members = models.ManyToManyField(Citizens, related_name='forums')

    def __str__(self):
        return self.title

class Posts(models.Model):
    forum = models.ForeignKey(Forums, on_delete=models.CASCADE)
    author = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0) 
    likes = models.ManyToManyField(Citizens, related_name='liked_posts', blank=True)

    # order by most recent
    class Meta:
        ordering = ['-timestamp'] 
        # copilot ^_^

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class RenewalRequests(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    REQUEST_TYPES = [('Passport', 'Passport'), ("Driver's License", "Driver's License")]
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES)
    picture = models.ImageField(upload_to=request_picture_path) # this is for the new doc
    reason = models.TextField()
    proof_document = models.FileField(upload_to=proof_document_path)
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')] 
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True, default="not rejected")

class RegistrationRequests(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    REQUEST_TYPES = [
        ('Address Registration', 'Address Registration'),
        ('Property Registration', 'Property Registration'),
        ('Vehicle Registration', 'Vehicle Registration'),
    ]
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES)
    proof_document = models.FileField(upload_to=proof_document_path)
    previous_owner_id = models.CharField(max_length=30, null=True, blank=True) # null and blank becasue of the address registration
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True, default="not rejected")
