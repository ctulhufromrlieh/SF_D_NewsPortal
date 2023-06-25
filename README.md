# SF_D_NewsPortal
Skill factory D2+ task. Project - News Portal

D3.6 Task:
Use these shell commands for bad words initialization:

from news.models import * 
BadWord.objects.all().delete()
BadWord.objects.create(text='енот')
BadWord.objects.create(text='рубл')