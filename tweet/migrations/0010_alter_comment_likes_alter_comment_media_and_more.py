# Generated by Django 4.2.5 on 2023-10-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0009_comment_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(to='tweet.like'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='media',
            field=models.ManyToManyField(to='tweet.tweeetfile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='replies',
            field=models.ManyToManyField(to='tweet.comment'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='comments',
            field=models.ManyToManyField(to='tweet.comment'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='likes',
            field=models.ManyToManyField(to='tweet.like'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='media',
            field=models.ManyToManyField(to='tweet.tweeetfile'),
        ),
    ]
