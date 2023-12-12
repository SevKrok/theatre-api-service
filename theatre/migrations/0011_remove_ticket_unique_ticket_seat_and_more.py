# Generated by Django 5.0 on 2023-12-12 19:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0010_alter_actor_unique_together_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="ticket",
            name="unique_ticket_seat",
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("performance", "row", "seat")},
        ),
    ]
