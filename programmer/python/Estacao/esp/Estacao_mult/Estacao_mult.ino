#include <Time.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti multiWiFi;

#define USERNAME "wfasolo"
#define DEVICE_ID "Estacao"
#define DEVICE_CREDENTIAL "@#lucas"

WiFiUDP udp; //Cria um objeto "UDP"
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);
Adafruit_BME280 bme;

unsigned long cont = 0,
              cont2 = 0,
              cont3 = 0,
              c_con = 0;

float pres = 0,
      temp = 0,
      umid = 0,
      pres2 = 0,
      temp2 = 0,
      umid2 = 0;

int chuv = 0,
    id = 1;

const int pinoSensor = D5;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  WiFi.mode(WIFI_STA);
  multiWiFi.addAP("FASOLO", "@@lucas@@");
  multiWiFi.addAP("BGF", "@giagra@");

  pinMode(pinoSensor, INPUT);
  ntp.begin();
  bme.begin(0x76);
  //  thing.add_wifi(SSID, SSID_PASSWORD);

  // resource output example (i.e. reading a sensor value)
  thing["parametros"] >> [](pson &out)
  {
    out["Chuv"] = chuv;
    out["Pres"] = pres;
    out["Temp"] = temp;
    out["Umid"] = umid;
  };
  //thing["Alt"] >> outputValue(bme.readAltitude(PressaoaNivelDoMar_HPA));
}

void loop()
{
  //verifica a conexao WiFi
  if (multiWiFi.run() != WL_CONNECTED)
  {
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    //WiFi.reconnect();
    //yield();

    c_con++;

    if (c_con >= 100)
    {
      delay(2000);
      ESP.restart();
    }
  }

  else

  {
    c_con = 0;

    //leitura
    if ((millis() / 1000) - cont2 >= 5)
    {
      yield();

      // medicao da temperatura
      pres2 = pres2 + bme.readPressure();
      temp2 = temp2 + bme.readTemperature();
      umid2 = umid2 + bme.readHumidity();
      cont3++;
      //

      // chuva
      ler_chuva();
      //

      //chuva tempo real
      if (id == 0 && chuv == 1)
      {
        thing.stream(thing["parametros"]);
        delay(100);
        yield();

        ler_chuva();

        if (chuv == 1)
        {
          pres = pres2 / (cont3 * 100 * 0.99),
          temp = temp2 / cont3,
          umid = umid2 / (cont3 * 0.9);

          thing.write_bucket("dados_estacao1", "parametros");
        }
        id = 1;
      }
      //

      cont2 = (millis() / 1000);
    }
    //

    //verificação
    if ((millis() / 1000) - cont >= 59.5)
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

      // gravacao no banco de dados a cada 20 minutos
      if (minuto == 0 || minuto == 20 || minuto == 40)
      {
        pres = pres2 / (cont3 * 100 * 0.99),
        temp = temp2 / cont3,
        umid = umid2 / (cont3 * 0.9);
        ler_chuva();

        thing.write_bucket("dados_estacao1", "parametros");

        pres2 = 0;
        temp2 = 0;
        umid2 = 0;
        cont3 = 0;
      }
      //

      pres = bme.readPressure() / (100 * 0.99);
      temp = bme.readTemperature();
      umid = bme.readHumidity() / 0.9;

      // enviar dados
      thing.stream(thing["parametros"]);
      //thing.stream(thing["Alt"]);

      cont = (millis() / 1000);
    }
    //

    thing.handle();
  }
}

// funcao ler chuva
void ler_chuva()
{

  int sens_chuv = 0, i = 0, cc = 0;

  for (i = 0; i <= 15; i++)
  {
    if (digitalRead(pinoSensor) == HIGH)
    {
      cc = 0;
    }
    else
    {
      cc = 1;
    }

    sens_chuv = sens_chuv + cc;
    delay(15);
    yield();
  }

  sens_chuv = sens_chuv / i;

  if (sens_chuv < 1)
  {
    chuv = 0;
    id = 0;
  }
  else
  {
    chuv = 1;
  }
} //
