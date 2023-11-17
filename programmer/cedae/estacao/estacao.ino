#include <ESP8266WiFiMulti.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

ESP8266WiFiMulti multiWiFi;
WiFiUDP udp;
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);

extern void ler_clima(), ler_chuva(), chuva_real(),
  at_hora(), banco_20();


#define USERNAME "wfasolo"
#define DEVICE_ID "Estacao"
#define DEVICE_CREDENTIAL "@#lucas"


Adafruit_AHTX0 aht;
Adafruit_BMP280 bmp;

unsigned long cont = 0, cont1 = 0, cont_conec = 0,
              c_con = 0, cont_BD = 0, cont_ler = 0;
bool forcereboot = false, iniciar = false;
float pres0 = 0, temp0 = 0, umid0 = 0,
      pres1 = 0, temp1 = 0, umid1 = 0,
      pres2 = 0, temp2 = 0, umid2 = 0,
      presBD = 0, tempBD = 0, umidBD = 0;

int chuv = 0, id = 1, i_inic,
    hora = 61, minuto = 61, segundo = 61;

const int pinoSensor = D5;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup() {
  //Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  WiFi.mode(WIFI_STA);
  multiWiFi.addAP("ITANET-FASOLO", "lucas123");
  multiWiFi.addAP("FASOLO", "@@lucas@@");
  multiWiFi.addAP("LAB", "@@lucas@@");
  multiWiFi.addAP("a1", "@1234567@");
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);
  ntp.begin();
  pinMode(pinoSensor, INPUT);
  bmp.begin(0x77);
  aht.begin();

  {
    sensors_event_t humidity, temp;
    aht.getEvent(&humidity, &temp);
    pres0 = bmp.readPressure() * 0.0101;
    temp0 = (bmp.readTemperature() + temp.temperature) / 2;
    umid0 = humidity.relative_humidity;
    pres2 = pres1 = pres0;
    temp2 = temp1 = temp0;
    umid2 = umid1 = umid0;
  }

  thing["parametros"] >> [](pson& out) {
    out["Chuv"] = chuv;
    out["Pres"] = pres0;
    out["Temp"] = temp0;
    out["Umid"] = umid0;
  };

  thing["Rede"] >> [](pson& out) {
    out["SSID"] = WiFi.SSID();
    out["Sinal"] = WiFi.RSSI();
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
  reb_esp();
  at_hora();
  banco_1h();
  digitalWrite(LED_BUILTIN, HIGH);
  c_con = 0;

  if (millis() - cont >= 29500) {
    if (segundo == 0 || segundo == 30) {
      digitalWrite(LED_BUILTIN, LOW);
      inicio();
      ler_clima();
      ler_chuva();
      chuva_real();

      cont = (millis());
    }
  }
}
