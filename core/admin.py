from django.contrib import admin
from .models import UserProfile,DeviceType,DeviceConfiguration,DevicePermission,LatestData,Events,Player,DeviceData
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(DeviceType)
admin.site.register(DeviceConfiguration)
admin.site.register(DevicePermission)
admin.site.register(LatestData)
admin.site.register(Events)
admin.site.register(Player)
admin.site.register(DeviceData)

