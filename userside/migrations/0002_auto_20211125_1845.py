# Generated by Django 3.2.6 on 2021-11-25 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='agent_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('user_name', models.CharField(max_length=200)),
                ('user_email', models.CharField(max_length=200)),
                ('user_contact', models.IntegerField()),
                ('user_image', models.CharField(max_length=200)),
                ('user_city', models.CharField(max_length=200)),
                ('user_state', models.CharField(max_length=200)),
                ('user_facebook', models.CharField(max_length=200)),
                ('user_twitter', models.CharField(max_length=200)),
                ('user_instagram', models.CharField(max_length=200)),
                ('user_linkedin', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='user_details',
            old_name='user_instagram',
            new_name='user_google',
        ),
    ]