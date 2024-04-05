from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):

    def seed_data(apps,schema_editor):
        user=CustomUser(name="anila",
                          email="anila2001@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="9567337386",
                         )
        user.set_password("anila")
        user.save()

    

    dependencies = [
        
    ]

    operations = [
        migrations.RunPython(seed_data),
        ]