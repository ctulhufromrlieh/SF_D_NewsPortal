# SF_D_NewsPortal
Skill factory D2+ task. Project - News Portal

D3.6 Task:
Use these shell commands for bad words initialization:

from news.models import * <br>
BadWord.objects.all().delete() <br>
BadWord.objects.create(text='енот')<br>
BadWord.objects.create(text='рубл')<br>

D4.7 Task:
Updated shell commands (for pagination check)

#D5_8 Task: 
#Use these commands for Group creation:

from django.contrib.auth.models import Group, Permission
Group.objects.all().delete()
group1 = Group.objects.create(name="readers")
group2 = Group.objects.create(name="authors")
group2.permissions.add(Permission.objects.get(codename="add_post"))
group2.permissions.add(Permission.objects.get(codename="change_post"))
group2.permissions.add(Permission.objects.get(codename="delete_post"))
