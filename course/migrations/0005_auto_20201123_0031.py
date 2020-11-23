# Generated by Django 3.1.3 on 2020-11-23 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20201120_0536'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=512)),
                ('workload', models.IntegerField(default=-1)),
                ('rating', models.IntegerField(default=-1)),
                ('subject_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
            ],
            options={
                'db_table': 'UserInput',
            },
        ),
        migrations.AddConstraint(
            model_name='userinput',
            constraint=models.UniqueConstraint(fields=('user_name', 'subject_number'), name='userinput_title_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='userinput',
            constraint=models.CheckConstraint(check=models.Q(workload__gte='-1'), name='userinput_workload_gte_zero_constraint'),
        ),
        migrations.AddConstraint(
            model_name='userinput',
            constraint=models.CheckConstraint(check=models.Q(workload__lte='5'), name='userinput_workload_lte_give_constraint'),
        ),
        migrations.AddConstraint(
            model_name='userinput',
            constraint=models.CheckConstraint(check=models.Q(rating__gte='-1'), name='userinput_rating_gte_zero_constraint'),
        ),
        migrations.AddConstraint(
            model_name='userinput',
            constraint=models.CheckConstraint(check=models.Q(rating__lte='5'), name='userinput_rating_lte_five_constraint'),
        ),
    ]
