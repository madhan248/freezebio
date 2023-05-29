from django.contrib import admin
from .models import ServiceModel,UserProfile,DeviceType,DeviceConfiguration,DevicePermission,LatestData,Events,Player,DeviceData
from django.contrib.sessions.models import Session



# Register your models here.
admin.site.register(Session)
# admin.site.register(UserProfile)
admin.site.register(DeviceType)
admin.site.register(DeviceConfiguration)
admin.site.register(DevicePermission)
admin.site.register(LatestData)
admin.site.register(Events)
admin.site.register(Player)
admin.site.register(DeviceData)
admin.site.register(ServiceModel)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	 list_display = ('user','organization')
	 search_fields = ['user__username','user__email']