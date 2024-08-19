# Generated by Django 4.2.13 on 2024-07-14 11:27

import digitalSociety.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("digitalSociety", "0004_alter_citizens_user"),
    ]

    operations = [
        migrations.RemoveField(model_name="citizens", name="nationality",),
        migrations.AlterField(
            model_name="renewalrequests",
            name="request_type",
            field=models.CharField(
                choices=[
                    ("Passport", "Passport"),
                    ("Driver's License", "Driver's License"),
                ],
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name="DrivingLicenses",
            fields=[
                (
                    "license_number",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                (
                    "picture",
                    models.ImageField(upload_to=digitalSociety.models.license_path),
                ),
                ("profession", models.CharField(max_length=30)),
                ("issue_date", models.DateField()),
                ("expiry_date", models.DateField()),
                ("nationality", models.CharField(max_length=30)),
                ("emergency_contact", models.CharField(max_length=30)),
                (
                    "license_class",
                    models.CharField(
                        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
                        max_length=1,
                    ),
                ),
                (
                    "citizen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="digitalSociety.citizens",
                    ),
                ),
            ],
        ),
    ]