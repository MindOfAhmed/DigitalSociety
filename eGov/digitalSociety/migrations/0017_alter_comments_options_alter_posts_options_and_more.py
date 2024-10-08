# Generated by Django 4.2.13 on 2024-08-22 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalSociety', '0016_posts_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-likes_count', '-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-likes_count', '-timestamp']},
        ),
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='digitalSociety.citizens'),
        ),
        migrations.AddField(
            model_name='comments',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
