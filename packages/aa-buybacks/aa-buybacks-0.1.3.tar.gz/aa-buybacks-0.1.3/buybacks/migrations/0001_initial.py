# Generated by Django 3.1.4 on 2020-12-26 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eveuniverse', '0004_effect_longer_name'),
        ('authentication', '0017_remove_fleetup_permission'),
        ('eveonline', '0012_index_additions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buybacks',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    ),
                ),
            ],
            options={
                'permissions': (
                    ('basic_access', 'Can access this app'),
                    ('setup_retriever', 'Can setup information retriever'),
                    ('manage_programs', 'Can manage buyback programs'),
                ),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                (
                    'corporation',
                    models.OneToOneField(
                        primary_key=True,
                        on_delete=models.deletion.CASCADE,
                        related_name='+',
                        to='eveonline.evecorporationinfo',
                    ),
                ),
                (
                    'character',
                    models.ForeignKey(
                        help_text='Character used for retrieving info',
                        on_delete=models.deletion.PROTECT,
                        related_name='+',
                        to='authentication.characterownership',
                    ),
                ),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                (
                    'id',
                    models.PositiveBigIntegerField(
                        help_text='Eve Online location ID',
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='In-game name of this station or structure',
                        max_length=100,
                    ),
                ),
                (
                    'eve_solar_system',
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=models.deletion.SET_DEFAULT,
                        related_name='+',
                        to='eveuniverse.evesolarsystem',
                    ),
                ),
                (
                    'category_id',
                    models.IntegerField(
                        choices=[
                            (3, 'station'),
                            (65, 'structure'),
                            (0, '(unknown)'),
                        ],
                        default=0,
                    ),
                ),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                (
                    'id',
                    models.PositiveBigIntegerField(
                        help_text='Item ID of the office',
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'corporation',
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='+',
                        to='buybacks.corporation',
                    ),
                ),
                (
                    'location',
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='+',
                        to='buybacks.location',
                    ),
                ),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
