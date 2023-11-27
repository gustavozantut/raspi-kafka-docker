import Adafruit_DHT
from kafka import KafkaProducer
import datetime
import time
from confluent_kafka.admin import AdminClient, NewTopic

dht_pin = 18
# Function to read DHT11 sensor data
def read_dht11_sensor():
    
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    while (humidity is None) or (temperature is None):
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    return humidity, temperature

print('Reaching for sensor.')

while not read_dht11_sensor():
    
    pass

# Define the broker(s) you want to connect to
bootstrap_servers = "100.108.104.205:9092,100.108.97.215:9092,100.108.97.215:9093"

# Create an AdminClient instance
admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})
# Define topic configuration
topic_config = {
    "topic": "sensors_dht11",
    "partitions": 1,
    "replication.factor": 3,  # Set the desired replication factor
    "config": {
        "min.insync.replicas": 2  # Set the desired minimum in-sync replicas
    }
}
# Create a NewTopic instance
new_topic = NewTopic(
    topic_config["topic"],
    num_partitions=topic_config["partitions"],
    replication_factor=topic_config["replication.factor"],
    config={
        "min.insync.replicas": str(topic_config["config"]["min.insync.replicas"])
    }
)
# Create the topic
admin_client.create_topics([new_topic])

try:
    
    # Create Kafka producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, acks='all')
    print("producer created")
    
    while True:
        
        # Read DHT11 sensor data
        humidity, temperature = read_dht11_sensor()
        
        if (humidity is not None) and (temperature is not None):
            
            payload = f'Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Timestamp: {datetime.datetime.now()}'
            
            try:
                
                # Publish the payload to the Kafka topic
                producer.send("sensors_dht11", value=payload.encode('utf-8')).get()
                print("Published:\n", payload)
            
            except:
                
                pass
        else:
            
            print('Failed to read DHT11 sensor data.')

        #time.sleep(0.5)  # Wait for 0.5 seconds before reading the sensor again
        
except KeyboardInterrupt:
    
    pass

finally:
    
    # Close the Kafka producer upon exiting the loop
    producer.close()