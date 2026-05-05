import json
import time
from awscrt import mqtt, io
from awsiot import mqtt_connection_builder

# =========================
# AWS IoT CONFIG
# =========================
ENDPOINT = "atpkehqrmu534-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "ems-device"
PATH_TO_CERT = "Certificates/certificate.pem.crt"
PATH_TO_KEY = "Certificates/private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"
TOPIC = "ems/data"

# =========================
# MQTT CONNECTION SETUP
# =========================
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

# =========================
# CONNECT
# =========================
print("Connecting to AWS IoT...")
mqtt_connection.connect().result()
print("Connected!")

# =========================
# TEST DATA (CHANGE HERE)
# =========================

# NORMAL
# test_data = [100,105,110,115,120,118,122,125,128,130]

# ALERT (HIGH SPIKE)
# test_data = [100,105,110,115,120,118,122,125,128,300]

# OPTIMAL (LOW DROP)
test_data = [
    5.2, 4.8, 4.5, 4.3, 4.1, 4.6, 5.5, 6.8, 7.5, 8.2,
    9.0, 10.5, 11.8, 12.5, 13.0, 12.2, 11.5, 10.8, 11.2, 12.0,
    13.5, 14.2, 12.8, 11.0,
    
    5.1, 4.7, 4.4, 4.2, 4.0, 4.5, 5.6, 6.9, 7.8, 8.5,
    9.3, 10.8, 12.0, 12.8, 13.3, 12.4, 11.7, 10.9, 11.4, 12.2,
    13.8, 14.5, 13.0, 11.3,

    # anomalies (only 8)
    22.0, 21.5, 23.0, 24.5, 25.0, 26.2, 24.8, 27.0,

    # back to normal
    13.2, 11.5
]
# =========================
# PUBLISH LOOP
# =========================
for val in test_data:
    payload = {
        "power": float(val),
        "timestamp": int(time.time())
    }

    try:
        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        print("Published:", payload)

    except Exception as e:
        print("Publish failed:", str(e))

    time.sleep(1)  # simulate real-time

# =========================
# DISCONNECT
# =========================
mqtt_connection.disconnect().result()
print("Disconnected")