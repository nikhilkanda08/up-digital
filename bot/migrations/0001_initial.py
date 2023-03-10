# Generated by Django 3.2.15 on 2022-10-31 21:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, verbose_name='username')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of User')),
                ('searches', models.IntegerField(default=2, verbose_name='Allowed Searches')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('title', models.CharField(max_length=256, verbose_name='Campaign Title')),
                ('search_type', models.CharField(choices=[('organic_search', 'Organic Search'), ('googlemap', 'Google Maps')], default='organic_search', max_length=100, verbose_name='Search Type')),
                ('website', models.CharField(max_length=256, verbose_name='Website Name')),
                ('mobile_Searches', models.IntegerField(default=30, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Mobile Searches')),
                ('bounce_rate', models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Bounce Rate')),
                ('pages_per_session', models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Pages Per Session')),
                ('avg_session_duration', models.IntegerField(default=120, validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(5)], verbose_name='Average Session Duration')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_related_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=256, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=256, verbose_name='State')),
                ('country', models.CharField(max_length=256, verbose_name='Country')),
                ('keyword', models.CharField(max_length=256, verbose_name='Keyword')),
                ('searches_per_day', models.FloatField(verbose_name='Pages Per Session')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_related_name', to='bot.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_title', models.CharField(max_length=256, verbose_name='Website Title')),
                ('rank', models.IntegerField(verbose_name='Website Rank in Search')),
                ('result', models.TextField(verbose_name='Search Results')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Keywords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Keywords_name', to='bot.keywords')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_name', to='bot.campaign')),
            ],
        ),
    ]