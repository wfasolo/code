#include <ThingerESP8266.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti multiWiFi;

#define USERNAME "wfasolo"
#define DEVICE_ID "Estufa"
#define DEVICE_CREDENTIAL "@#lucas"

ThingerESP8266 thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

void setup()
{
  WiFi.mode(WIFI_STA);
  multiWiFi.addAP("FASOLO", "@@lucas@@");
  multiWiFi.addAP("BGF", "@giagra@");

  // resource output example (i.e. reading a sensor value)
  thing["parametros"] >> [](pson &in, pson &out) {
    out["Temp"] = temp;
    out["PWM"] = pwm;
    setpoint = in["Setpoint"];
  };
}

void loop()
{
  //verifica a conexao WiFi
  if (multiWiFi.run() != WL_CONNECTED)
  {
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

    // enviar dados
    thing.stream(thing["parametros"]);
    thing.handle();
  }
}
