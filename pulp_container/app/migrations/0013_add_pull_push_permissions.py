# Generated by Django 2.2.17 on 2021-01-20 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('container', '0012_add_container_namespace_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='containerdistribution',
            options={'default_related_name': '%(app_label)s_%(model_name)s', 'permissions': [('pull_containerdistribution', 'Can pull from a registry repo'), ('push_containerdistribution', 'Can push into the registry repo')]},
        ),
    ]
