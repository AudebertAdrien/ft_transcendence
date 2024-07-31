# Generated by Django 5.0.7 on 2024-07-24 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='best_score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='m_duration',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='m_nbr_ball_touch',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='m_score_adv_match',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='m_score_match',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='num_participated_tournaments',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='num_won_tournaments',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='p_win',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='total_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='total_match',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_win',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
