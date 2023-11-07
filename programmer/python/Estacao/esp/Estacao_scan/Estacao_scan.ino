#include <Time.h>
#include <ThingerESP8266.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define SSID_ "FASOLO"
#define SSID_PASSWORD "@@lucas@@"

#define USERNAME "wfasolo"
#define DEVICE_ID "Estacao"
#define DEVICE_CREDENTIAL "@#lucas"

WiFiUDP udp; //Cria um objeto "UDP"
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);

Adafruit_BME280 bme;

unsigned long cont = -55000,
              cont2 = 0;

float pres = 0,
      temp = 0,
      umid = 0;

int chuv = 0;

const int pinoSensor = D5;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  WiFiManager wifiManager;
  wifiManager.resetSettings();
  //wifiManager.setConfigPortalTimeout(120);
  wifiManager.setTimeout(60);
  wifiManager.autoConnect("TEST");

  if (WiFi.status() != WL_CONNECTED)
  {
    WiFi.begin(SSID_, SSID_PASSWORD);
  }

  pinMode(pinoSensor, INPUT);
  ntp.begin();
  bme.begin(0x76);

  // resource output example (i.e. reading a sensor value)
  thing["parametros"] >> [](pson & out) {
    out["Chuv"] = chuv;
    out["Pres"] = pres;
    out["Temp"] = temp;
    out["Umid"] = umid;
  };
  //thing["Alt"] >> outputValue(bme.readAltitude(PressaoaNivelDoMar_HPA));
}

void loop()
{
  if (millis() - cont >= 60000)
  {
    //verifica a conexao WiFi
    if (WiFi.status() != WL_CONNECTED)
    {
      WiFi.reconnect();
      cont = millis() - 59000;
    }
    else
    {
      // Atualizacao da hora
      ntp.forceUpdate();
      int hora = ntp.getHours();
      int minuto = ntp.getMinutes();
      //

      // chuva
      if (digitalRead(pinoSensor) == HIGH)
      {
        chuv = 0;
      }
      else
      {
        chuv = 1;
      }
      //

      // medicao da temperatura
      pres = 0;
      temp = 0;
      umid = 0;

      for (int i = 0; i <= 99; i++)
      {
        pres = pres + bme.readPressure();
        temp = temp + bme.readTemperature();
        umid = umid + bme.readHumidity();
        delay(10);
      }

      pres = pres / (10000 * 0.99),
      temp = temp / 100,
      umid = umid / (100 * 0.9);
      //

      // gravacao no banco de dados a cada 15 minutos
      if (minuto == 00 || minuto == 15 || minuto == 30 || minuto == 45)
      {
        thing.write_bucket("dados_estacao1", "parametros");
      }
      //
      // reiniciar o esp
      if (hora == 13 && minuto == 02)
      {
        delay(30000);
        yield();
        ESP.restart();
      }
      //
    }
    // enviar dados
    thing.stream(thing["parametros"]);
    //thing.stream(thing["Alt"]);

    cont = millis();
    yield();
  }

  if (millis() - cont2 >= 15000)
  {
    thing.handle();
    cont2 = millis();
    yield();
  }
}
