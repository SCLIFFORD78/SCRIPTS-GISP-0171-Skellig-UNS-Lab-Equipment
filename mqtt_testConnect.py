# test_connect.py 
import paho.mqtt.client as mqtt 

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("Connected success")
    elif rc == 1:
        print("connection failed - incorrect protocol version")
    elif rc == 2:
        print("connection failed - invalid client identifier")
    elif rc == 3:
        print("connection failed - the broker is not available")
    elif rc == 4:
        print("connection failed - wrong username or password")
    elif rc == 5:
        print("connection failed - unauthorized")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client() 

client.username_pw_set(username="admin", password="public")
client.on_connect = on_connect 
#client.connect("40.118.124.87", 1883, 60)
client.connect("192.168.1.23", 1883, 60)

client.loop_forever()
