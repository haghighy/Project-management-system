from django.contrib import admin
from .models import *


admin.site.register(Board)
admin.site.register(BoardLabel)
admin.site.register(BoardMember)
admin.site.register(BoardAction)
