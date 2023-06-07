from .models import DeviceConfiguration,DeviceData

def check_if_data_exists(func):
    def wrapper(*args, **kwargs):
    	if kwargs['data'].get('timestamp') and kwargs['data'].get('device_id'):
	    	try:
	    		query = DeviceData.objects.get(device_id=kwargs['data'].get('device_id'),timestamp=kwargs['data'].get('timestamp'))
	    	except:
	    		query = None
	    	if not query:
	    		DeviceData.objects.create(type=kwargs['data'].get('type'),data=kwargs['data'],
	    			timestamp=kwargs['data'].get('timestamp'),device_id=kwargs['data'].get('device_id'))
    return wrapper


@check_if_data_exists
def realdata(data={'timestamp':'123456'}):
	print("real data")