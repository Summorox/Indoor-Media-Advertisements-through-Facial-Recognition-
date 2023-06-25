#include <WiFi.h>
#include <PubSubClient.h>

//MQTT module
const char *ssid = "NOTEVITORIA";//"Rede";//"IoT";
const char *password = "123vba456";//"12345678";//"iot#123.";
const char* mqtt_server = "192.168.137.1"; //195-mqtt server IP address
const char* mqtt_topic = "MOTION/DETECTION";
WiFiClient espClient;
PubSubClient client(espClient);
//this variable will indicate if the MQTT message was already sent
bool lastState = LOW;

//PIR sensor module
const int MOTION_PIN = 13; // Pin connected to motion detector
const int LED_PIN = LED_BUILTIN; // LED pin - active-high
int sensor_output;

void wifi_initialization(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqtt_server, 1883);
}

void pir_sensor_initialization(){
  Serial.println("Waiting For Power On Warm Up\n");
  delay(20000); /* Power On Warm Up Delay */
  Serial.println("Ready!\n");
}

void connect_MQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client_pub")) {
      Serial.println("connected");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

 
//===========================================================
void setup(){
  Serial.begin(9600);
  pinMode(MOTION_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
  wifi_initialization();
  pir_sensor_initialization();
  
 }
 
//===========================================================

void loop(){
  if (!client.connected()) {
    connect_MQTT();
  }
  
  client.loop();
  sensor_output = digitalRead(MOTION_PIN);
  
  if (sensor_output == HIGH){
    Serial.println("Motion detected!\n");
    client.publish(mqtt_topic, "on");
    //digitalWrite(LED_PIN,HIGH);
    delay(15000);
  
  }
  else{
    Serial.println("No motion detected!\n");
    client.publish(mqtt_topic, "off");
    //digitalWrite(LED_PIN,LOW);
    delay(2000);
  }
}
