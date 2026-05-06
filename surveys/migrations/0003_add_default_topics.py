from django.db import migrations


def create_default_topics(apps, schema_editor):
    Topic = apps.get_model('surveys', 'Topic')
    default_topics = [
        ("Игры", "games.jpg"),
        ("Фильмы", "movies.png"),
        ("Кулинария", "cooking.jpg"),
        ("Спорт", "sport.jpg"),
        ("Искусство", "art.jpg"),
        ("Учёба", "study.jpg"),
        ("Психология", "psychology.png"),
        ("Другое", "other.jpg"),
    ]

    for name, image in default_topics:
        Topic.objects.get_or_create(name=name, defaults={"image": image})


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_topic_survey_question_choice_answer'),
    ]

    operations = [
        migrations.RunPython(create_default_topics),
    ]
