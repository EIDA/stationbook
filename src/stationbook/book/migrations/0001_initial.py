# Generated by Django 2.1.7 on 2019-11-20 15:32

import book.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchFdsnStationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_code', models.CharField(blank=True, max_length=256)),
                ('station_code', models.CharField(blank=True, max_length=256)),
                ('site_name', models.CharField(blank=True, max_length=256)),
                ('network_class', models.CharField(blank=True, choices=[('all', 'All'), ('permanent', 'Permanent'), ('temporary', 'Temporary')], default='', max_length=256)),
                ('network_access', models.CharField(blank=True, choices=[('all', 'All'), ('unrestricted', 'Unrestricted'), ('restricted', 'Restricted')], default='', max_length=256)),
                ('station_status', models.CharField(blank=True, choices=[('all', 'All'), ('open', 'Open'), ('closed', 'Closed')], default='', max_length=256)),
                ('station_access', models.CharField(blank=True, choices=[('all', 'All'), ('unrestricted', 'Unrestricted'), ('restricted', 'Restricted')], default='', max_length=256)),
                ('sensor_unit', models.CharField(blank=True, choices=[('all', 'All'), ('m', 'M'), ('ms', 'M/S'), ('mss', 'M/S^2'), ('pa', 'PA'), ('c', 'C'), ('deg', 'DEG'), ('undefined', 'Undefined')], default='', max_length=256)),
                ('sensor_type', models.CharField(blank=True, choices=[('all', 'All'), ('vbb', 'VBB'), ('bb', 'BB'), ('sp', 'SP'), ('sm', 'SM'), ('obs', 'OBS'), ('undefined', 'Undefined')], default='', max_length=256)),
                ('latitude_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('latitude_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('longitude_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('longitude_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('start_year_from', models.IntegerField(blank=True)),
                ('start_year_to', models.IntegerField(blank=True)),
                ('end_year_from', models.IntegerField(blank=True)),
                ('end_year_to', models.IntegerField(blank=True)),
                ('geological_unit', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('alluvial_deposits', 'Alluvial deposits'), ('ancient_alluvialterraces', 'Ancient alluvial terraces'), ('argillite', 'Argillite'), ('breccias', 'Breccias'), ('clay', 'Clay'), ('conglomerate', 'Conglomerate'), ('debris', 'Debris'), ('diabase', 'Diabase'), ('dolomite', 'Dolomite'), ('fillade', 'Fillade'), ('fluvial_deposits', 'Fluvial deposits'), ('gneiss', 'Gneiss'), ('granite', 'Granite'), ('jasper', 'Jasper'), ('lacustrine_deposits', 'Lacustrine deposits'), ('limestone', 'Limestone'), ('marls', 'Marls'), ('metamorphic_rock', 'Metamorphic rock'), ('micaschist', 'Micaschist'), ('morainic_deposits', 'Morainic deposits'), ('ophiolite', 'Ophiolite'), ('rhyolitic_ignimbrite', 'Rhyolitic ignimbrite'), ('sand_deposits', 'Sand deposits'), ('sandstone', 'Sandstone'), ('schist', 'Schist'), ('torbidite', 'Torbidite'), ('volcanic_deposits', 'Volcanic deposits'), ('volcanic_rocks', 'Volcanic rocks')], default='', max_length=256)),
                ('morphology_class', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'), ('t4', 'T4')], default='', max_length=256)),
                ('ground_type_ec8', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('s1', 'S1'), ('s2', 'S2')], default='', max_length=256)),
                ('basin_flag', models.BooleanField(default=False)),
                ('vs30_from', models.DecimalField(blank=True, decimal_places=6, max_digits=12)),
                ('vs30_to', models.DecimalField(blank=True, decimal_places=6, max_digits=12)),
                ('f0_from', models.DecimalField(blank=True, decimal_places=6, max_digits=12)),
                ('f0_to', models.DecimalField(blank=True, decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExtEntityBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_network_code', models.TextField(blank=True, default='', max_length=16384)),
                ('ext_network_start_year', models.TextField(blank=True, default='', max_length=16384)),
                ('ext_station_code', models.TextField(blank=True, default='', max_length=16384)),
                ('ext_station_start_year', models.TextField(blank=True, default='', max_length=16384)),
                ('entity_removed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FdsnNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256)),
                ('description', models.CharField(blank=True, default='', max_length=256)),
                ('start_date', models.DateTimeField(blank=True, default='', max_length=256)),
                ('restricted_status', models.CharField(blank=True, default='', max_length=256)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='FdsnNode',
            fields=[
                ('code', models.CharField(max_length=256, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=256)),
                ('url_dataselect', models.CharField(blank=True, default='', max_length=1024)),
                ('url_station', models.CharField(blank=True, default='', max_length=1024)),
                ('url_routing', models.CharField(blank=True, default='', max_length=1024)),
                ('url_wfcatalog', models.CharField(blank=True, default='', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='FdsnStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256)),
                ('site_name', models.CharField(blank=True, max_length=256)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('elevation', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('restricted_status', models.CharField(blank=True, max_length=256)),
                ('start_date', models.DateTimeField(blank=True, max_length=256)),
                ('end_date', models.DateTimeField(blank=True, max_length=256, null=True)),
                ('creation_date', models.DateTimeField(blank=True, max_length=256)),
                ('fdsn_network', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fdsn_stations', to='book.FdsnNetwork')),
            ],
            options={
                'ordering': ['fdsn_network__fdsn_node__code', 'fdsn_network__code', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=1024, null=True)),
                ('category', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(blank=True, max_length=1024)),
                ('location', models.CharField(blank=True, max_length=1024)),
                ('agency', models.CharField(blank=True, max_length=1024)),
                ('department', models.CharField(blank=True, max_length=1024)),
                ('telephone', models.CharField(blank=True, max_length=1024)),
                ('skype', models.CharField(blank=True, max_length=1024)),
                ('fdsn_networks', models.ManyToManyField(blank=True, related_name='editors', to='book.FdsnNetwork')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtAccessData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('updated_at', models.DateTimeField(null=True)),
                ('description', models.CharField(blank=True, default='Change', max_length=256)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtBasicData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('description', models.TextField(blank=True, default='', max_length=16384)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('imported_from_fdsn', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_synced', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtBoreholeData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('depth', models.IntegerField(default=0)),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtBoreholeLayerData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('description', models.CharField(blank=True, default='', max_length=256)),
                ('depth_top', models.IntegerField(default=0)),
                ('depth_bottom', models.IntegerField(default=0)),
                ('borehole_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borehole_layers', to='book.ExtBoreholeData')),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtHousingData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('description', models.TextField(blank=True, default='', max_length=16384)),
                ('housing_class', models.CharField(blank=True, choices=[('borehole', 'Borehole'), ('bridge', 'Bridge'), ('building', 'Building'), ('cave', 'Cave'), ('dam', 'Dam'), ('free_field', 'Free field'), ('other_structure', 'Other structure'), ('tunnel', 'Tunnel'), ('underground_shelter', 'Underground shelter'), ('urban_free_field', 'Urban free field')], default='', max_length=256)),
                ('in_building', models.BooleanField(default=True)),
                ('numer_of_storeys', models.IntegerField(default=0)),
                ('distance_to_building', models.IntegerField(default=0)),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtMorphologyData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('description', models.TextField(blank=True, default='', max_length=16384)),
                ('geological_unit', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('alluvial_deposits', 'Alluvial deposits'), ('ancient_alluvialterraces', 'Ancient alluvial terraces'), ('argillite', 'Argillite'), ('breccias', 'Breccias'), ('clay', 'Clay'), ('conglomerate', 'Conglomerate'), ('debris', 'Debris'), ('diabase', 'Diabase'), ('dolomite', 'Dolomite'), ('fillade', 'Fillade'), ('fluvial_deposits', 'Fluvial deposits'), ('gneiss', 'Gneiss'), ('granite', 'Granite'), ('jasper', 'Jasper'), ('lacustrine_deposits', 'Lacustrine deposits'), ('limestone', 'Limestone'), ('marls', 'Marls'), ('metamorphic_rock', 'Metamorphic rock'), ('micaschist', 'Micaschist'), ('morainic_deposits', 'Morainic deposits'), ('ophiolite', 'Ophiolite'), ('rhyolitic_ignimbrite', 'Rhyolitic ignimbrite'), ('sand_deposits', 'Sand deposits'), ('sandstone', 'Sandstone'), ('schist', 'Schist'), ('torbidite', 'Torbidite'), ('volcanic_deposits', 'Volcanic deposits'), ('volcanic_rocks', 'Volcanic rocks')], default='', max_length=256)),
                ('morphology_class', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'), ('t4', 'T4')], default='', max_length=256)),
                ('ground_type_ec8', models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('s1', 'S1'), ('s2', 'S2')], default='', max_length=256)),
                ('groundwater_depth', models.IntegerField(default=0)),
                ('vs_30', models.IntegerField(default=0)),
                ('f0', models.IntegerField(default=0)),
                ('amp_f0', models.IntegerField(default=0)),
                ('basin_flag', models.BooleanField(default=False)),
                ('bedrock_depth', models.IntegerField(default=0)),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='ExtOwnerData',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('name_first', models.CharField(blank=True, default='n/a', max_length=256)),
                ('name_last', models.CharField(blank=True, default='n/a', max_length=256)),
                ('department', models.CharField(blank=True, default='n/a', max_length=256)),
                ('agency', models.CharField(blank=True, default='n/a', max_length=256)),
                ('city', models.CharField(blank=True, default='n/a', max_length=256)),
                ('street', models.CharField(blank=True, default='n/a', max_length=256)),
                ('country', models.CharField(blank=True, default='n/a', max_length=256)),
                ('phone', models.CharField(blank=True, default='n/a', max_length=256)),
                ('email', models.CharField(blank=True, default='n/a', max_length=256)),
            ],
            bases=('book.extentitybase',),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('extentitybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='book.ExtEntityBase')),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('image', models.ImageField(upload_to=book.models.Photo.path_file_name)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('fdsn_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to='book.FdsnStation')),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
            bases=('book.extentitybase',),
        ),
        migrations.AddField(
            model_name='fdsnnetwork',
            name='fdsn_node',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fdsn_networks', to='book.FdsnNode'),
        ),
        migrations.AddField(
            model_name='fdsnstation',
            name='ext_basic_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station', to='book.ExtBasicData'),
        ),
        migrations.AddField(
            model_name='fdsnstation',
            name='ext_borehole_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station', to='book.ExtBoreholeData'),
        ),
        migrations.AddField(
            model_name='fdsnstation',
            name='ext_housing_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station', to='book.ExtHousingData'),
        ),
        migrations.AddField(
            model_name='fdsnstation',
            name='ext_morphology_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station', to='book.ExtMorphologyData'),
        ),
        migrations.AddField(
            model_name='fdsnstation',
            name='ext_owner_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station', to='book.ExtOwnerData'),
        ),
        migrations.AlterUniqueTogether(
            name='fdsnnetwork',
            unique_together={('fdsn_node', 'code', 'start_date')},
        ),
        migrations.AddField(
            model_name='extaccessdata',
            name='fdsn_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='access_data', to='book.FdsnStation'),
        ),
        migrations.AddField(
            model_name='extaccessdata',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fdsnstation',
            unique_together={('fdsn_network', 'code', 'start_date')},
        ),
    ]
