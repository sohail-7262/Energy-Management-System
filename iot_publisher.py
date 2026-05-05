import json
import time
import pandas as pd
from awscrt import mqtt, io
from awsiot import mqtt_connection_builder

# Load dataset
df = pd.read_csv("data/household.txt", sep=';', na_values=['?'])

df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df['Global_active_power'] = pd.to_numeric(df['Global_active_power'], errors='coerce')
df = df[['datetime', 'Global_active_power']].dropna()

# AWS IoT config (YOU WILL FILL THESE)
ENDPOINT = "atpkehqrmu534-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "ems-device"
PATH_TO_CERT = "Certificates/certificate.pem.crt"
PATH_TO_KEY = "Certificates/private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"
TOPIC = "ems/data"

# MQTT connection
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=io.ClientBootstrap(io.EventLoopGroup(1), io.DefaultHostResolver(io.EventLoopGroup(1))),
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting to AWS IoT...")
mqtt_connection.connect().result()
print("Connected!")

# Publish data row by row
for _, row in df.head(100).iterrows():  # limit for testing
    payload = {
        "timestamp": str(row["datetime"]),
        "power": float(row["Global_active_power"])
    }

    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(payload),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print("Published:", payload)

    time.sleep(1)  # simulate real-time