# Generated manually for MediLogic project
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sintomas', models.TextField()),
                ('resultado', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
