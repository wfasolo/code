#include <Time.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define USERNAME "wfasolo"
#define DEVICE_ID "Estacao"
#define DEVICE_CREDENTIAL "@#lucas"

#define SSID "FASOLO"
#define SSID_PASSWORD "@@lucas@@"

WiFiUDP udp; //Cria um objeto "UDP"
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);
Adafruit_BME280 bme;

unsigned long cont = -55,
              cont2 = 0;

float     pres = 0,
          temp = 0,
          umid = 0;
int chuv = 0;
const int pinoSensor = D8;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  pinMode(pinoSensor, INPUT);
  ntp.begin();
  bme.begin(0x76);
  thing.add_wifi(SSID, SSID_PASSWORD);

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
  if ((millis() / 1000) - cont >= 59.5)
  {
    //verifica a conexao WiFi
    if (WiFi.status() != WL_CONNECTED)
    {
      WiFi.reconnect();
      cont = (millis() / 1000) - 59;
      yield();
    }

    else

    {
      // Atualizacao da hora
      ntp.forceUpdate();
      int hora = ntp.getHours();
      int minuto = ntp.getMinutes();
      //

      // reiniciar o esp
      if (hora == 13 && minuto == 03)
      {
        delay(40000);
        yield();
        ESP.restart();
      }
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
      if (minuto == 00 || minuto == 20 || minuto == 40)
      {
        thing.write_bucket("dados_estacao1", "parametros");
      }
      //

      // enviar dados
      thing.stream(thing["parametros"]);
      //thing.stream(thing["Alt"]);

      cont = (millis() / 1000);
      yield();
    }
  }

  if ((millis() / 1000) - cont2 >= 15)
  {
    thing.handle();
    cont2 = (millis() / 1000);
    yield();
  }
}
