# Generated by Django 5.0.6 on 2024-05-16 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('image', models.ImageField(upload_to='gate_pass_images/')),
                ('contact_no', models.CharField(max_length=15)),
                ('department', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('EE', 'Electrical Engineering')], max_length=3)),
                ('reason_to_meet', models.TextField()),
            ],
        ),
    ]
