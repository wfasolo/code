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

unsigned long cont = 0, cont_s = 0, cont_m = 0, cont_h = 0, cont_d = 0, cont_ler = 0;
bool forcereboot = false, iniciar = false;
float altura = 0, pulso = 0, dist = 0;
float md_ler[4] = { 25, 25, 25, 25 };
float vz_seg = 0, vz_min = 0, vz_hor = 0, vz_dia = 0, vazao = 0;
int dia = 0, hora = 0, minuto = 0, segundo = 30;
int i = 0, i_s = 0, i_m = 0, i_h = 0, i_d = 0, i_ler = 0, i_inic = 0;

#define USERNAME "w_fasolo"
#define DEVICE_ID "vazao_BJI"
#define DEVICE_CREDENTIAL "cedaebji"
ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup() {
  // Serial.begin(115200);
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

  thing["Banco"] >> [](pson& out) {
    out["Vz_min"] = int(vz_min);
    out["Vz_hora"] = int(vz_hor);
    out["Vz_dia"] = int(vz_dia);
  };
  thing["Vz_media"] >> [](pson& out) {
    out = int(vz_seg);
  };
  thing["Altura"] >> [](pson& out) {
    out = altura;
  };
  thing["Reiniciar"] << [](pson& in) {
    if (in.is_empty()) {
      in = forcereboot;
    } else {
      forcereboot = in ? true : false;
    }
  };
}

void loop() {
  thing.handle();
  conectar();
  at_hora();
  banco_1h();
  reb_esp();
  vazao_media();
  digitalWrite(LED_BUILTIN, HIGH);

  if (millis() - cont > 5000) {
    inicio();
    ler_vazao();
    cont = millis();
  }
}
