import Adafruit_DHT
from kafka import KafkaProducer
import datetime
import time

dht_pin = 4
# Function to read DHT11 sensor data
def read_dht11_sensor():
    
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    while (humidity is None) or (temperature is None):
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
    
    return humidity, temperature

while not read_dht11_sensor():
    
    print('Reaching for sensor.')
    
    pass

# Define the broker(s) you want to connect to
bootstrap_servers = "192.168.0.210:9092,192.168.0.101:9092,192.168.14.2:9092"

try:
    
    # Create Kafka producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, acks='all')
    print("producer created")
    
    while True:
        
        # Read DHT11 sensor data
        humidity, temperature = read_dht11_sensor()
        
        print(humidity,temperature)
        
        if (humidity is not None) and (temperature is not None):
            
            timestamp = datetime.datetime.now()
            payload = {
                'Temperature': temperature,
                'Humidity': humidity,
                'Timestamp': timestamp
                }
            
            try:
                
                # Publish the payload to the Kafka topic
                producer.send("dht11", value=payload.encode('utf-8')).get()
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