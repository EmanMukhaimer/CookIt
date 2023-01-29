# Generated by Django 4.1.5 on 2023-01-28 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookit_app', '0003_remove_category_category_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='instructions',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='cookit_app.recipe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(related_name='reciepes', to='cookit_app.category'),
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_text', models.TextField()),
                ('step_number', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to='cookit_app.recipe')),
            ],
        ),
    ]
