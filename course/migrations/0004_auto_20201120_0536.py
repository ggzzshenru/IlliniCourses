# Generated by Django 3.1.3 on 2020-11-20 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20201120_0535'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='course',
            table='Course',
        ),
        migrations.AlterModelTable(
            name='genedsatisfaction',
            table='GenedSatisfaction',
        ),
        migrations.AlterModelTable(
            name='generaleducation',
            table='GeneralEducation',
        ),
        migrations.AlterModelTable(
            name='grade',
            table='Grade',
        ),
    ]
