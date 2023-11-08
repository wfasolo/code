
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

ESP8266WiFiMulti multiWiFi;
WiFiClient clienteWiFi;
HTTPClient clienteHTTP;
WiFiUDP udp;
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);
Adafruit_SSD1306 OLED(128, 64, &Wire, -1);

unsigned long cont = 0, cont2 = 25000;
int i_inic = 0;
bool iniciar = false;
float taxaVazao, alturaReser;
String valorVazao, valorReser;
String urlVazao = "http://api.thinger.io/v2/users/w_fasolo/devices/vazao_BJI/Altura?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJ2YXphb19CSkkiLCJpYXQiOjE2OTc5MDQ1NDIsImp0aSI6IjY1MzNmNzllNDljMTM3ZDI2MTA3ZDdlYSIsInN2ciI6InVzLWVhc3QuYXdzLnRoaW5nZXIuaW8iLCJ1c3IiOiJ3X2Zhc29sbyJ9.Qs9lkU-YfBH8PVaq7UMK_xxR_fKGd8manC1eo7imIio";
String urlReser = "http://api.thinger.io/v2/users/w_fasolo/devices/reserv_BJI/Altura?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJyZXNlcnZfQkpJIiwiaWF0IjoxNjk3OTA0NDAzLCJqdGkiOiI2NTMzZjcxMzQ5YzEzN2QyNjEwN2Q3ZTkiLCJzdnIiOiJ1cy1lYXN0LmF3cy50aGluZ2VyLmlvIiwidXNyIjoid19mYXNvbG8ifQ.bm8kXw4JVOGlwUdCQReg4fQy368DNWSIYGK6Z4GhYDw";

void setup() {
  Serial.begin(115200);
  pinMode(4, OUTPUT);

  OLED.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  OLED.clearDisplay();
  OLED.setTextColor(WHITE, BLACK);
  OLED.setTextSize(2);
  OLED.println("conectando");
  OLED.display();


  WiFi.mode(WIFI_STA);
  multiWiFi.addAP("ITANET-FASOLO", "lucas123");
  multiWiFi.addAP("FASOLO", "@@lucas@@");
  multiWiFi.addAP("BGF", "@giagra@");
  multiWiFi.addAP("LAB", "@@lucas@@");
  multiWiFi.addAP("a1", "@1234567@");
  multiWiFi.addAP("a2", "@123456@");
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);
  ntp.begin();
  ntp.forceUpdate();
}

void loop() {
  if (multiWiFi.run() != WL_CONNECTED) {
    conectar();
  } else {
    if (millis() - cont > 30000) {
      piscarTela(taxaVazao, alturaReser);
      inicio();
      cont = millis();
      valorVazao = jsonDaResposta(fazerRequisicaoHTTP(urlVazao));
      valorReser = jsonDaResposta(fazerRequisicaoHTTP(urlReser));
      taxaVazao = valorVazao.toFloat();
      alturaReser = valorReser.toFloat();
    }
    if (millis() - cont2 >= 7500 & millis() - cont2 <= 8000) {
      digitalWrite(LED_BUILTIN, LOW);

      telavazao(taxaVazao);
    } else if (millis() - cont2 >= 15000) {
      telareserv(alturaReser);
      cont2 = millis();
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
}
