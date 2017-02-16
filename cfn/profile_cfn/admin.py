from django.contrib import admin
from .models import ProfileCfn

admin.site.register(ProfileCfn)

# @admin.register(ProfileCfn)
# class AlbumAdmin(admin.ModelAdmin):
#     exclude = ('follows',)
