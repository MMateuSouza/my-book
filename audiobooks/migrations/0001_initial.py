# Generated by Django 3.2.5 on 2021-10-22 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('publishing_company', models.CharField(max_length=64, verbose_name='Editora')),
                ('edition', models.PositiveIntegerField(verbose_name='Edição')),
                ('isbn_10', models.CharField(max_length=10, verbose_name='ISBN 10')),
                ('isbn_13', models.CharField(max_length=13, verbose_name='ISBN 13')),
                ('front_cover', models.ImageField(upload_to='front_cover', verbose_name='Foto de Capa')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiobooks.book', verbose_name='Livro')),
                ('subchapters', models.ManyToManyField(blank=True, related_name='_audiobooks_chapter_subchapters_+', to='audiobooks.Chapter', verbose_name='Subcapítulos')),
            ],
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Autor')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiobooks.book', verbose_name='Livro')),
            ],
        ),
    ]
