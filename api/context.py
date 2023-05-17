from .models import DevicePermission

def get_user_devices(request):
    user = request.user
    try:
        devices = DevicePermission.objects.select_related('device_config','device_config__device_type').filter(profile=user)
    except Exception as e:
        print("Exception in context.py",e)
        devices = None
    if devices:
        d = {}
        for i in devices:
            if i.device_config.device_type.device_type in d.keys():
                d[i.device_config.device_type.device_type].append({"id":i.device_config.id,"device_name":i.device_config.device_name,
                                                                   "device_id":i.device_config.device_id,"display":i.device_config.display})
            else:
                d[i.device_config.device_type.device_type] = []
                d[i.device_config.device_type.device_type].append({"id":i.device_config.id,"device_name":i.device_config.device_name,
                                                                   "device_id":i.device_config.device_id,"display":i.device_config.display})
        device_list = [{"name":i,"devices":d[i]} for i in d.keys()]
    else:
        device_list = []
    return {"device_list":device_list}