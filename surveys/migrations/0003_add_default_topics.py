from django.db import migrations


def create_default_topics(apps, schema_editor):
    Topic = apps.get_model('surveys', 'Topic')
    default_topics = [
        "Игры",
        "Фильмы",
        "Кулинария",
        "Спорт",
        "Искусство",
        "Учёба",
        "Психология",
        "Другое",
    ]

    for name in default_topics:
        Topic.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_topic_survey_question_choice_answer'),
    ]

    operations = [
        migrations.RunPython(create_default_topics),
    ]
