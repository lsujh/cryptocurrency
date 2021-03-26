# Generated by Django 3.1.7 on 2021-03-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("first_name", models.CharField(max_length=50, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=50, verbose_name="Фамилия")),
                ("phone", models.CharField(max_length=15, verbose_name="Телефон")),
                ("message", models.TextField(verbose_name="Сообщение")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Обратная связь",
                "verbose_name_plural": "Обратная связь",
            },
        ),
    ]