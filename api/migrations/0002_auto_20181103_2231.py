# Generated by Django 2.1.2 on 2018-11-03 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	dependencies = [
		('api', '0001_initial'),
	]

	operations = [
		migrations.CreateModel(
			name='GenericField',
			fields=[
				(
					'id',
					models.AutoField(
						auto_created=True,
						primary_key=True,
						serialize=False,
						verbose_name='ID'
					)
				),
				('name', models.TextField()),
			],
		),
		migrations.RemoveField(
			model_name='risktype',
			name='fields',
		),
		migrations.CreateModel(
			name='DateField',
			fields=[
				(
					'genericfield_ptr',
					models.OneToOneField(
						auto_created=True,
						on_delete=django.db.models.deletion.CASCADE,
						parent_link=True,
						primary_key=True,
						serialize=False,
						to='api.GenericField'
					)
				),
			],
			bases=('api.genericfield',),
		),
		migrations.CreateModel(
			name='EnumField',
			fields=[
				(
					'genericfield_ptr',
					models.OneToOneField(
						auto_created=True,
						on_delete=django.db.models.deletion.CASCADE,
						parent_link=True,
						primary_key=True,
						serialize=False,
						to='api.GenericField'
					)
				),
				('choices', models.TextField()),
			],
			bases=('api.genericfield',),
		),
		migrations.CreateModel(
			name='NumberField',
			fields=[
				(
					'genericfield_ptr',
					models.OneToOneField(
						auto_created=True,
						on_delete=django.db.models.deletion.CASCADE,
						parent_link=True,
						primary_key=True,
						serialize=False,
						to='api.GenericField'
					)
				),
			],
			bases=('api.genericfield',),
		),
		migrations.CreateModel(
			name='TextField',
			fields=[
				(
					'genericfield_ptr',
					models.OneToOneField(
						auto_created=True,
						on_delete=django.db.models.deletion.CASCADE,
						parent_link=True,
						primary_key=True,
						serialize=False,
						to='api.GenericField'
					)
				),
			],
			bases=('api.genericfield',),
		),
		migrations.AddField(
			model_name='genericfield',
			name='risktype',
			field=models.ForeignKey(
				on_delete=django.db.models.deletion.CASCADE,
				to='api.RiskType'
			),
		),
	]
