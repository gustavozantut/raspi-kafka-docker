import json
import datetime
import Adafruit_DHT
from kafka import KafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic

dht_pin = 18
# Define the broker(s) you want to connect to
bootstrap_servers = "192.168.0.101:9092,192.168.14.2:9092,192.168.0.210:9092"

# Function to read DHT11 sensor data
def read_dht11_sensor():
    
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    while (humidity is None) or (temperature is None):
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    return humidity, temperature

print('Reaching for sensor...')


def create_kafka_topic():
    
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

print('Creating topic...')
while not create_kafka_topic():
    
        pass
        
print('Topic created!')

print('Reaching for sensor...')
while not read_dht11_sensor():
    
    pass

try:
    
    print('Creating topic...')
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, acks='all')
    while not producer():

            producer = KafkaProducer(bootstrap_servers=bootstrap_servers, acks='all')
            pass
            
    print('Topic created!')
    # Create Kafka producer
    
    print("producer created")
    
    while True:
        
        print('Sensor OK!')
        
        # Read DHT11 sensor data
        humidity, temperature = read_dht11_sensor()
        
        if (humidity is not None) and (temperature is not None):
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            payload = {
                'Temperature': temperature,
                'Humidity': humidity,
                'Timestamp': timestamp
                }
            
            # try:
                
            # Publish the payload to the Kafka topic
            producer.send("dht11", value=json.dumps(payload).encode('utf-8')).get()
            print("Published:\n", payload)
            
            # except:
                
            #     pass
        else:
            
            print('Failed to read DHT11 sensor data.')

        #time.sleep(0.5)  # Wait for 0.5 seconds before reading the sensor again
        
except KeyboardInterrupt:
    
    pass

finally:
    
    # Close the Kafka producer upon exiting the loop
    producer.close()