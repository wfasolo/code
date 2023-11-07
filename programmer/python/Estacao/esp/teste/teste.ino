#include <Time.h>
#include <ThingerESP8266.h>
#include <NTPClient.h>//Biblioteca do NTP.
#include <WiFiUdp.h>//Biblioteca do UDP.

#define USERNAME "i9pool"
#define DEVICE_ID "teste123"
#define DEVICE_CREDENTIAL "&Ee9tOgwmKb7wB"

#define SSID "a1"
#define SSID_PASSWORD "@123456@"

WiFiUDP udp;//Cria um objeto "UDP"
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);//Cria um objeto "NTP"

float cont = 0,
      cont2 = -1100000,
      pres = 1011,
      temp = 24,
      umid = 60;

int chuv = 0;

const int pinoSensor = D5;

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  Serial.begin(9600);

  pinMode(pinoSensor, INPUT); //DEFINE O PINO COMO ENTRADA

  ntp.begin();//Inicia o NTP.

  thing.add_wifi(SSID, SSID_PASSWORD);

  // resource output example (i.e. reading a sensor value)
  thing["parametros"] >> [](pson & out) {
    out["Chuv"] = chuv;
    out["Pres"] = random(1010, 1013);
    out["Temp"] = random(24, 25);
    out["Umid"] = random(60, 63);

  };
  thing["Alt"] >> outputValue(101);

}

void loop()
{
  if (digitalRead(pinoSensor) == HIGH) {
    chuv = 0;
  } else {
    chuv = 1;
  }

  if (millis() - cont > 60000) {
    ntp.forceUpdate();//Força o Update.

    String hora = ntp.getFormattedTime();//Armazena na váriavel HORA, o horario atual.
    String a = String(hora[3]);
    String b = String(hora[4]);
    String minu = a + b;
    Serial.println (minu);
    Serial.println (hora);

    if (minu.toInt() == 00 || minu.toInt() == 15 || minu.toInt() == 30 || minu.toInt() == 45)
    { Serial.print("hora: ");
      Serial.println(hora);
    }


  }

  thing.stream(thing["parametros"]);
  thing.stream(thing["Alt"]);
  thing.handle();
  delay(200);
  cont = millis();


}
