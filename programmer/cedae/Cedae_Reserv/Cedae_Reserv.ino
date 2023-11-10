//By WFasolo//
#include <ESP8266WiFiMulti.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP udp;
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);

ESP8266WiFiMulti multiWiFi;

#define trigPin D5
#define echoPin D6


bool forcereboot = false, iniciar = false;
float altura = 0, pulso = 0, dist = 0, volume = 0, comp = 1, larg = 1;
float md_ler[3] = { 1, 1, 1 };
int dia = 0, hora = 0, minuto = 0, segundo = 30;
int i_inic = 0, seg_ant = 0, cont = 0;

#define USERNAME "w_fasolo"
#define DEVICE_ID "reserv_BJI"
#define DEVICE_CREDENTIAL "cedaebji"
ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup() {
  //Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

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

  thing["Rede"] >> [](pson& out) {
    out["SSID"] = WiFi.SSID();
    out["Sinal"] = WiFi.RSSI();
  };

  thing["Altura"] >> [](pson& out) {
    out = altura;
  };

  thing["Volume"] >> [](pson& out) {
    out = volume;
  };

  thing["Reiniciar"] << [](pson& in) {
    if (in.is_empty()) {
      in = forcereboot;
    } else {
      forcereboot = in ? true : false;
    }
  };
  ntp.forceUpdate();
}

void loop() {
  thing.handle();
  conectar();
  at_hora();
  banco_1h();
  reb_esp();
  ler_volume();
  digitalWrite(LED_BUILTIN, HIGH);
}
