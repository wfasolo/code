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

unsigned long cont = 0, cont1 = 0, c_con = 0, cont_BD = 0;

float     pres = 1015.0f, temp = 25.0f, umid = 50.0f,
          pres1 = 1015.0f, temp1 = 25.0f, umid1 = 50.0f,
          pres2 = 1015.0f, temp2 = 25.0f, umid2 = 50.0f,
          pres3 = 1015.0f, temp3 = 25.0f, umid3 = 50.0f,
          presBD = 0.0f, tempBD = 0.0f, umidBD = 0.0f;

int chuv = 0, id = 1, inicio = 0,
    hora = 61, minuto = 61, segundo = 61;

const int pinoSensor = D5;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  WiFi.mode(WIFI_STA);
  multiWiFi.addAP("FASOLO", "@@lucas@@");
  //multiWiFi.addAP("BGF", "@giagra@");
  multiWiFi.addAP("LAB", "@@lucas@@");
  multiWiFi.addAP("a1", "@1234567@");
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
  pres = bme.readPressure() / 99.0f;
  temp = bme.readTemperature();
  umid = bme.readHumidity();
  pres3 = pres2 = pres1 = pres;
  temp3 = temp2 = temp1 = temp;
  umid3 = umid2 = umid1 = umid;
}

void loop()
{
  //verifica a conexao WiFi
  if (multiWiFi.run() != WL_CONNECTED)
  {
    conectar();
  }
  else
  {
    thing.handle();
    digitalWrite(LED_BUILTIN, HIGH);
    c_con = 0;

    if ((millis() / 1000) - cont >= 20)
    {
      digitalWrite(LED_BUILTIN, LOW);
      ler_clima();
      ler_chuva();
      chuva_real();
      at_hora();
      banco_20();

      cont = (millis() / 1000);
    }
  }
}

//**** verificar conexão ****//
void conectar()
{
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
  yield();
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  //WiFi.reconnect();
  yield();

  c_con++;

  if (c_con >= 5000) {
    ESP.restart();
  }
}

//**** ler chuva ****//
void ler_chuva()
{
  int sens_chuv = 0, i = 0, cc = 0;

  for (i = 0; i <= 15; i++) {
    if (digitalRead(pinoSensor) == HIGH) {
      cc = 0;
    }
    else {
      cc = 1;
    }

    sens_chuv = sens_chuv + cc;
    delay(15);
    yield();
  }

  sens_chuv = sens_chuv / i;

  if ( sens_chuv < 1)
  {
    chuv = 0;
    id = 0;
  }
  else
  {
    chuv = 1;
  }
}

//**** chuva tempo real ****//
void chuva_real()
{
  if (id == 0 && chuv == 1) {
    thing.stream(thing["parametros"]);
    delay(100);
    yield();

    ler_chuva();

    if (chuv == 1) {
      pres = presBD / cont1,
      temp = tempBD / cont1,
      umid = umidBD / cont1;

      thing.write_bucket("dados_estacao1", "parametros");
    }
    id = 1;
  }
}

//**** gravacao no banco de dados a cada 20 minutos ****//
void banco_20()
{
  if (minuto == 0 || minuto == 20 || minuto == 40)
  {
    if ( cont_BD == 0)
    {
      cont_BD = 1;
      pres = presBD / cont1,
      temp = tempBD / cont1,
      umid = umidBD / cont1;
      ler_chuva();

      thing.write_bucket("dados_estacao1", "parametros");

      presBD = 0;
      tempBD = 0;
      umidBD = 0;
      cont1 = 0;
    }
  }
  else
    cont_BD = 0;
}

//**** Atualizacao da hora ****//
void  at_hora()
{
  ntp.forceUpdate();
  hora = ntp.getHours();
  minuto = ntp.getMinutes();
  segundo = ntp.getSeconds();
}

//**** ler parametros do clima ****//
void ler_clima()
{
  int ii = 0;
  pres3 = pres2; pres2 = pres1; pres1 = pres;
  temp3 = temp2; temp2 = temp1; temp1 = temp;
  umid3 = umid2; umid2 = umid1; umid1 = umid;

  for (ii = 0; ii <= 15; ii++)
  {
    pres += bme.readPressure() / 99.0f;
    temp += bme.readTemperature();
    umid += bme.readHumidity();
    delay(5);
  }
  yield();
  pres = (pres / (ii + 1));
  temp = (temp / (ii + 1));
  umid = (umid / (ii + 1));

  pres = (pres + pres1 + pres2 + pres3) / 4.0;
  temp = (temp + temp1 + temp2 + temp3) / 4.0;
  umid = (umid + umid1 + umid2 + umid3) / 4.0;

  presBD += pres;
  tempBD += temp;
  umidBD += umid;
  cont1++;
}
