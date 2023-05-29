# cd project/freezebio

# cd ..
source venv/bin/activate
mqttasgi --host localhost --port 1883 freezebio.asgi:application