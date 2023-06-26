#include <WiFi.h>
#include <PubSubClient.h>
#include "esp_camera.h"
#include <base64.h>
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

//WIFI config
const char* ssid = "NOTEVITORIA";
const char* password = "123vba456";

//MQTT config
bool useMQTT = true;
const char* mqttServer = "192.168.1.171";
const char* HostName = "mqtt.vitoria.pc";
const char* mqttUser = "";
const char* mqttPassword = "";
const char* topic_PHOTO = "MOTION/DETECTION";
const char* topic_PUBLISH = "PICTURE";
const int MAX_PAYLOAD = 60000;

WiFiClient espClient;
PubSubClient client(espClient);

void startCameraServer();

void take_picture() {
  camera_fb_t * fb = NULL;
  Serial.println("Taking picture");
  fb = esp_camera_fb_get(); 
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  Serial.println("Picture taken");
  sendMQTT(fb->buf, fb->len); // Envia a imagem capturada via MQTT (mem.dados, mem.comp)
  esp_camera_fb_return(fb); // Libera a memoria do framebuffer
  
}

void sendMQTT(const uint8_t * buf, uint32_t len) {
  Serial.println("Enviando imagem...");
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get(); // Captura imagem
  if (!fb) { // Verifica se a captura da imagem foi bem-sucedida
    Serial.println("Falha na captura da imagem da câmera");
    return;
  }
  String encrypt = base64::encode(fb->buf, fb->len); //formato Base64
  if (client.publish(topic_PUBLISH, encrypt.c_str())) {
    Serial.println("Imagem enviada com sucesso");
  } else {
    Serial.println("Falha ao enviar imagem");
  }
  esp_camera_fb_return(fb);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(HostName, mqttUser, mqttPassword)) {
      Serial.println("connected");
      client.subscribe(topic_PHOTO);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(String topic, byte* message, unsigned int length) {
  String messageTemp;
  Serial.println(topic);
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  if (topic == topic_PHOTO) {
    if(messageTemp == "on"){
      take_picture();
    }
  }
}

void setup() {
  // Initialise the Serial Communication
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // Config Camera Settings
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  sensor_t * s = esp_camera_sensor_get();
  //sensores iniciais estão invertidos verticalmente e as cores estão um pouco saturadas.
  if (s->id.PID == OV3660_PID) { //verifica se o ID do sensor é compatível com o sensor OV3660
    s->set_vflip(s, 1); // vira de volta
    s->set_brightness(s, 1); // aumenta um pouco o brilho
    s->set_saturation(s, -2); // diminui a saturação
  }
  s->set_framesize(s, FRAMESIZE_QVGA); //captura de imagem da câmera, tamanho QVGA (320x240 pixels)

  // Configuração da conexão Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Inicialização do servidor da câmera
  startCameraServer();

  // IP local para conexão
  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");

  // Set MQTT Connection
  client.setServer(mqttServer, 1883);
  client.setBufferSize (MAX_PAYLOAD); //This is the maximum payload length
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
