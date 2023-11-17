// By WFasolo//
#include <ESP8266WiFiMulti.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP udp;
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);

ESP8266WiFiMulti multiWiFi;

#define trigPin D5
#define echoPin D6

unsigned long cont = 0;
bool forcereboot = false, iniciar = false;
float altura = 0, pulso = 0, dist = 0;
float md_ler[3] = { 25, 25, 25 };
float vz_min = 100, vz_hor = 100, vz_dia = 100, vazao = 100, vz_min2 = 100;
int dia = 0, hora = 0, minuto = 0, segundo = 30;
int i_d = 0, i_h = 0, i_m = 0, i_inic = 0;
int vol_trat;

#define USERNAME "w_fasolo"
#define DEVICE_ID "vazao_BJI"
#define DEVICE_CREDENTIAL "cedaebji"
ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup() {
  Serial.begin(115200);
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

  thing["Rede"] >> [](pson &out) {
    out["SSID"] = WiFi.SSID();
    out["Sinal"] = WiFi.RSSI();
  };

  thing["Vz_media"] >> [](pson &out) {
    out = int(vazao);
  };
  thing["Vz_min"] >> [](pson &out) {
    out = int(vz_min2);
  };
  thing["Vz_hor"] >> [](pson &out) {
    out = int(vz_hor);
  };
  thing["Vol_trat"] >> [](pson &out) {
    out = vol_trat;
  };
  thing["Altura"] >> [](pson &out) {
    out = altura;
  };

  thing["Reiniciar"] << [](pson &in) {
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
  ler_vazao();
  reb_esp();
}
