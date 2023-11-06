/*----------------------------------------------------------------------------------------------------------------------------------------
                        †                                Ver:1.0.0
                   †††††††††††                           Projeto: I9pool
                        †                                Autor: Theo Menezes
                        †                                Descrição: Ionizador inteligente com conexão WiFi.
                        †                                Status: Em desenvolvimento
                        †                                †João 14:6 - Eu sou o caminho, a verdade e a vida†
  ----------------------------------------------------------------------------------------------------------------------------------------*/
String VERSION = "1.2.6"; //IMPORTANTE



/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   EEPROM
  ----------------------------------------------------------------------------------------------------------------------------------------*/
/*-------------------------
          ADDRESS
  -------------------------
  -/ 0 (volume da piscina)
  -/ 1 (zona de tempo)
  -/ 2 (valor do padrao)
  -/ 3 (Hora de acionamento)
*/

#include <EEPROM.h>


void write_eeprom(int endereco, int  valor) {
  EEPROM.write(endereco, valor);
  EEPROM.commit();//Salva o dado na EEPROM.
  // Serial.println(EEPROM.read(endereco));

}



/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END EEPROM
  ------------------------------------------------------------------------------------------------------------------------*/


/*----------------------------------------------------------------------------------------------------------------------------------------
                                                MAP OF HARDWARE AND LYBRARES OVERALL
  ----------------------------------------------------------------------------------------------------------------------------------------*/

#define eletrodo 12
#define ponte_h 0
#define botao 13
#define amperimetro A0
#define bomba 3//16
int hora, minuto, dia;
int hora_acionamento;
bool controleBomba = false;
bool controleAc = false;
bool forceTrat = false;
bool forceupdate = false;
bool eletrodoStatus = true;
bool eletrodoErroMaster = true;
bool statusModoOp = false;
bool conect;
String mensagem;
float kp = 0.5,
      ki = 0.05,
      kd = 0.005,
      p = 0,
      i = 0,
      d = 0,
      pid = 0,
      erro = 0,
      tempo = 1,
      dt = 0,
      amp = 0;

int setpoint = 50;
int pwm = 0;
int amp_final = 0;


int startingHour = 0 ; // Definir hora inicial aqui
int seconds = 0;
int minutes = 0;
int hours = startingHour;
int days = 0;

unsigned long bot1 = 0;
unsigned long bot2 = 0;
unsigned long tempoCorrido = 0; // variavel pertence ao acionamento

unsigned long tempoOp; // variavel tempo de acionamento
unsigned long tempoPh; //variavel inicio  ponte h(limpeza)
int vol2 ;
bool verifbot = false;
int contbut = 0;


// --- Protótipo da Função ---
long moving_average();       //Função para filtro de média móvel

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   LYBRARES WIFI MANAGER
  ----------------------------------------------------------------------------------------------------------------------------------------*/
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <ESP8266Ping.h>
WiFiManager wifiManager;



#include <LiquidCrystal_I2C.h> // responsável pela comunicação com o display LCD

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   WIFI
  ----------------------------------------------------------------------------------------------------------------------------------------*/
const char* remote_host = "i9pool.ddns.net";
void statusConect() {
  //Serial.print("Status");
  //Serial.println(WiFi.status());


  if (WiFi.status() == WL_CONNECTED && Ping.ping(remote_host)) {
    conect = true;
  } else {
    conect = false;
  }


}

unsigned long tempoInicio;

void wifiConfig() {

  tempoInicio = millis();
  while (millis() - tempoInicio < 10000) {

    if (!digitalRead(botao) == HIGH) {
      wifiManager.resetSettings();
      lcd.clear();
      lcd.setCursor(2, 0);
      lcd.print("CONFIGURE O");
      lcd.setCursor(5, 1);
      lcd.print("WI-FI");
      wifiManager.setConfigPortalTimeout ( 120 );
      wifiManager.autoConnect("I9_CONFIG");
    }
    yield();
  }
}



/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   THINGER IO
  ----------------------------------------------------------------------------------------------------------------------------------------*/
//#define _DEBUG_
#define RECONNECTION_TIMEOUT 1
#define THINGER_SERVER "i9pool.ddns.net"
#define THINGER_OUTPUT_BUFFER_GROWING_SIZE 24
#include <ThingerESP8266.h>
String ids = String(ESP.getChipId());
char id[9];
#define USERNAME "i9poolDevices"
//#define DEVICE_ID ids
#define DEVICE_CREDENTIAL "i9pool&100%"

//version do código deve ser inserido aqui

ThingerESP8266 thing(USERNAME, id, DEVICE_CREDENTIAL);

String ss =  wifiManager.getSSID();
String ps =  wifiManager.getPassword();
const char* sc = const_cast<char*>(ss.c_str());
const char* pc = const_cast<char*>(ps.c_str());

void thingerio() {

  ids.toCharArray(id, 9);





  thing.add_wifi(sc, pc);

  thing["Informacoes"] >> [](pson & out) {
    out["Versao"] = VERSION;
    out["hora"] = hours;
    out["minuto"] = minutes;
    out["EletrodoStatus"] = eletrodoStatus;
    out["eletrodoErroMaster"] = eletrodoErroMaster;
  };

  thing["Mensagem"] >> [](pson & out) {

    out = mensagem;
  };

  thing["Atualização"] << [](pson & in) {

    if (in.is_empty()) {
      in = forceupdate;
    }
    else {
      forceupdate = in ? true : false;
    }
  };

  thing["utc"] = [](pson & in , pson & out) {
    out = EEPROM.read(1);
    if (in.is_empty()) {
      in = EEPROM.read(1);
    }
    else {
      EEPROM.begin(5);
      write_eeprom(1, in);
    }
  };

  thing["Volume"] = [](pson & in , pson & out) {
    out = EEPROM.read(0);
    if (in.is_empty()) {
      in = EEPROM.read(0);
    }
    else {
      EEPROM.begin(5);
      write_eeprom(0, in);
      calcTempo();
      setpoint = (3024000000 * EEPROM.read(0) * 0.01) / tempoOp;

    }
  };

  thing["Hora_acionamento"] = [](pson & in , pson & out) {
    out = EEPROM.read(3);
    if (in.is_empty()) {
      in = EEPROM.read(3);
    }
    else {
      EEPROM.begin(5);
      write_eeprom(3, in);
      hora_acionamento = EEPROM.read(3);
    }
  };



  thing["bomba"] = [](pson & in, pson & out ) {
    out = (bool)controleBomba;
    if (in.is_empty()) {
      in = (bool)controleBomba;
    }
    else {
      if (controleAc) {

      } else {
        controleBomba = in ? true : false;
      }
    }
  };

  thing["LimpezaEletrodo"] = [](pson & in, pson & out ) {
    out = (bool) digitalRead(ponte_h);
    if (in.is_empty()) {
      in = (bool) digitalRead(ponte_h);
    }
    else {
      digitalWrite(ponte_h, in ? HIGH : LOW);
    }
  };

  thing["TratamentoForcado"] = [](pson & in, pson & out ) {
    out = forceTrat;
    if (in.is_empty()) {
      in = forceTrat;
    }
    else {
      forceTrat = in ? true : false;
    }
  };

  thing["DadosOperacao"] >> [](pson & out) {
    out["Corrente"] =  amp_final;
    out["Correção"] = pid;
    out["PWM"] = pwm;
    out["Setpoint"] = setpoint;
    out["Mensagem"] = mensagem ;


  };

}
void tHandle() {
  if (conect) {
    thing.handle();

  }
}
void send_msg( String msgm) {
  if (conect) {
    String diathing = dds(days);
    String mt = diathing + "-" + hours + ":" + minutes + " " + msgm;
    mensagem = mt;
    thing.write_bucket(id, "Mensagem");
  }
}

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   LCD
  ----------------------------------------------------------------------------------------------------------------------------------------*/

void lcd_corrente() {
  lcd.clear();
  lcd.setCursor(4, 0);
  lcd.print("CORRENTE");
  lcd.setCursor(5, 1);
  lcd.print(amp_final);
  lcd.setCursor(8, 1);
  lcd.print("mAh");

}

void lcd_temperatura() {
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("I9POOL");
  lcd.setCursor(6, 1);
}

void lcd_status_op() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("STATUS OPERACAO");
  if (digitalRead(bomba) == HIGH) {
    lcd.setCursor(4, 1);
    lcd.print("LIGADO");
  } else {
    lcd.setCursor(3, 1);
    lcd.print("DESLIGADO");
  }
}

void lcd_data_hora() {
  lcd.clear();
  lcd.setCursor(6, 0);
  diadasemana(days);
  lcd.setCursor(5, 1);
  print2digitos(hours);
  lcd.setCursor(7, 1);
  lcd.print(":");
  lcd.setCursor(8, 1);
  print2digitos(minutes);
}

void lcd_ip() {
  if (WiFi.status() == WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(WiFi.SSID());
    lcd.setCursor(12, 0);
    int x1 = constrain(WiFi.RSSI(), -90, -40);
    int x2 = map(x1, -90, -40, 0, 100);
    lcd.print(x2);
    lcd.setCursor(15, 0);
    lcd.print("%");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
  } else {
    lcd.clear();
    lcd.setCursor(3, 0);
    lcd.print("REDE WI-FI");
    lcd.setCursor(2, 1);
    lcd.print("DESCONECTADA");
  }
}
void lcd_erro_parametros() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("APLIQUE ELEVADOR");
  lcd.setCursor(0, 1);
  lcd.print("DE CONDUTIVIDADE");
}
void lcd_erro() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ERRO!  VERIFIQUE");
  lcd.setCursor(0, 1);
  lcd.print("  O ELETRODO");
}

void lcd_default() {
  lcd.clear();
  lcd.setCursor(4, 0);
  lcd.print("RESTAURAR");
  lcd.setCursor(2, 1);
  lcd.print("CONFIGURACOES");
}


int contTela = 0;
unsigned long lcd_tempo = 0;
bool lcd_force = false;
void exibe_lcd() {
  if ((millis() - lcd_tempo > 10000 ) or (lcd_force == true) ) {
    lcd_tempo = millis();
    lcd_force = false;
    switch (contTela) {
      case 0:
        lcd_temperatura();
        break;
      case 1:
        lcd_corrente();
        break;
      case 2:
        lcd_data_hora();
        break;
      case 3:
        lcd_status_op();
        break;
      case 4:
        lcd_ip();
        break;
      case 5:
        lcd_default();
        break;
      case 6:
        lcd_erro_parametros();
        break;
      case 7:
        lcd_erro();
        break;
    }

  }
}


unsigned long tempo_lcd = 0;
bool lcd_ac = false;
void lcd_led() {
  if (millis() - tempo_lcd > 10000) {
    lcd.setBacklight(LOW);
    lcd_ac = false;
  }
}

void lcd_on() {
  lcd.setBacklight(HIGH);
  tempo_lcd = millis();
  lcd_ac = true;
}

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   START SETUP
  ----------------------------------------------------------------------------------------------------------------------------------------*/
void startSetup() {
  int tamanho = 1;
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("CONFIGURACAO");
  lcd.setCursor(4, 1);
  lcd.print("INICIAL");
  delay(3000);
  lcd.setCursor(1, 0);
  lcd.print("VAMOS COMECAR?");
  lcd.setCursor(2, 1);
  lcd.print("SERA RAPIDO!");
  delay(3000);

  //CONFIGURACAO DE HORA
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("TAMANHO PISCINA");
  lcd.setCursor(8, 1);
  lcd.print("m3");
  lcd.setCursor(6, 1);
  lcd.print(tamanho);
  bool verif_while = true;

  while (verif_while) {
    yield();
    if (!digitalRead(botao) == HIGH && contbut == 0) {
      bot1 = millis();
      contbut = 1;
    } else if (!digitalRead(botao) == HIGH && contbut == 1) {
      bot2 = millis();
      verifbot = true;
    }

    if (!digitalRead(botao) == LOW && verifbot == true or bot2 - bot1 > 5000 && verifbot == true) {
      verifbot = false;
      contbut = 0;
      if ( bot2 - bot1 > 5000) {
        verif_while = false;
      }
      else
      {
        tamanho++;
        if (tamanho > 60) {
          tamanho = 1;
        } else if (tamanho < 1) {
          tamanho = 60;
        }

        lcd.setCursor(6, 1);
        lcd.print(tamanho);
        delay(500);
      }
      //retardo(10);
    }

  }
  write_eeprom(0, tamanho);

  //CONFIGURACAO DE HORA
  int fuso = -3;
  lcd.clear();
  lcd.setCursor(1, 0);
  lcd.print("AJUSTE HORARIO");
  lcd.setCursor(8, 1);
  lcd.print("UTC");
  lcd.setCursor(6, 1);
  lcd.print(fuso);
  verif_while = true;
  delay(500);
  while (verif_while) {
    yield();


    if (!digitalRead(botao) == HIGH && contbut == 0) {
      bot1 = millis();
      contbut = 1;
    } else if (!digitalRead(botao) == HIGH && contbut == 1) {
      bot2 = millis();
      verifbot = true;
    }

    if (!digitalRead(botao) == LOW && verifbot == true or bot2 - bot1 > 5000 && verifbot == true) {
      verifbot = false;
      contbut = 0;
      if ( bot2 - bot1 > 5000) {
        verif_while = false;
      }
      else
      {
        fuso--;
        if (fuso < -5) {
          fuso = -2;
        }
        lcd.setCursor(6, 1);
        lcd.print(fuso);
        delay(500);
      }
      // retardo(10);
    }
  }
  write_eeprom(1, abs(fuso));
  write_eeprom(2, 0);
  write_eeprom(3, 6);
  write_eeprom(4, 25);
  EEPROM.end();

}//END void


void defaultConf() {
  EEPROM.begin(4);
  write_eeprom(0, 0);
  write_eeprom(1, 0);
  write_eeprom(2, 1);
  EEPROM.end();
  wifiManager.resetSettings();
  delay(3000);
  yield();
  ESP.reset();
}

bool initConf() {
  if (EEPROM.read(2) != 0) {
    return true;
  } else {
    return false;
  }
}

/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END START SETUP
  ------------------------------------------------------------------------------------------------------------------------*/


/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   UPDATE HTTP
  ----------------------------------------------------------------------------------------------------------------------------------------*/
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>
extern "C" {
#include "user_interface.h"
}
ESP8266WiFiMulti WiFiMulti;
HTTPClient http;

bool forceUp = false;

/*
   FUNCAO DO OTA
*/
void checkUpdate(void) {
  http.begin("i9poolatt.ddns.net", 8080, "/version.html");

  // inicio da conexao HTTP e envio do header
  int httpCode = http.GET();
  if (httpCode) {
    if (httpCode == 200) {
      String payload = http.getString();
      payload.replace(".", "");
      VERSION.replace(".", "");
      lcd.clear();
      if (VERSION.toInt() < payload.toInt()) {
        lcd.setCursor(1, 0);
        lcd.print("PARA ATUALIZAR");
        lcd.setCursor(0, 1);
        lcd.print("PRIMA  O  BOTAO");

        unsigned long tempoAtt = millis();
        while (millis() - tempoAtt < 10000) {
          yield();
          if (!digitalRead(botao) == HIGH or forceUp == true ) {
            forceUp = false;
            //tempoAtt += 10000;
            lcd.clear();
            lcd.setCursor(1, 0);
            lcd.print("ATUALIZANDO...");
            lcd.setCursor(4, 1);
            lcd.print("AGUARDE");
            payload = "";
            t_httpUpdate_return ret = ESPhttpUpdate.update("http://i9poolatt.ddns.net:8080/fw.bin");
            lcd.clear();
            lcd.setCursor(1, 0);
            lcd.print(ret);
            delay(3000);
            lcd.clear();
            switch (ret) {
              case HTTP_UPDATE_FAILED:
                lcd.setCursor(1, 0);
                lcd.print("FALHA");
                delay(3000);
                break;

              case HTTP_UPDATE_NO_UPDATES:
                lcd.setCursor(1, 0);
                lcd.print("SEM ARQUIVO");
                delay(3000);
                break;

              case HTTP_UPDATE_OK:
                lcd.setCursor(1, 0);
                lcd.print("SUCESSO");
                delay(3000);
                break;
            }
          }
        }
      }
    }
  }
  lcd.clear();
}

/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END UPDATE HTTP
  ------------------------------------------------------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   NTP
  ----------------------------------------------------------------------------------------------------------------------------------------*/
#include <NTPClient.h>//Biblioteca do timeClient.
#include <WiFiUdp.h>//Biblioteca do UDP.
int utc; //UTC -3:00 Brazil
WiFiUDP udp;//Cria um objeto "ntpUDP".

/*
  FUNCAO AUXILIAR PARA EXIBIR DIA DA SEMANA DO DISPLAY
*/
void diadasemana(int diasemana) { // FUNCAO DE TROCAR O NUMERO PELO DIA EM STRING E EXIBIR NO INICIO
  switch (diasemana) {
    case 0:
      lcd.print("DOM");
      break;
    case 1:
      lcd.print("SEG");
      break;
    case 2:
      lcd.print("TER");
      break;
    case 3:
      lcd.print("QUA");
      break;
    case 4:
      lcd.print("QUI");
      break;
    case 5:
      lcd.print("SEX");
      break;
    case 6:
      lcd.print("SAB");
      break;

  }

}

String dds(int diasemana) { // FUNCAO DE TROCAR O NUMERO PELO DIA EM STRING E EXIBIR NO INICIO
  switch (diasemana) {
    case 0:
      return"DOM";
      break;
    case 1:
      return"SEG";
      break;
    case 2:
      return"TER";
      break;
    case 3:
      return"QUA";
      break;
    case 4:
      return"QUI";
      break;
    case 5:
      return"SEX";
      break;
    case 6:
      return"SAB";
      break;

  }

}


void print2digitos(int number) {
  if (number >= 0 && number < 10) {
    lcd.print('0');
  }
  lcd.print(number);
}


/*
   FUNÇAO pegar hora
*/

void get_time() {
  if (conect) {
    retardo(500);

    if ( EEPROM.read(1) == 2) {
      NTPClient timeClient(udp, "i9poolntp.ddns.net", -2 * 3600, 60000);
      timeClient.begin();
      while (!timeClient.update()) {
        timeClient.forceUpdate();
        yield();
      }
      seconds = 0;
      startingHour = timeClient.getHours();
      minutes = timeClient.getMinutes();
      hours = startingHour;
      days = timeClient.getDay();
      timeClient.end();
    } else if (EEPROM.read(1) == 3) {
      NTPClient timeClient(udp, "i9poolntp.ddns.net", -3 * 3600, 60000);
      timeClient.begin();
      while (!timeClient.update()) {
        timeClient.forceUpdate();
        yield();
      }
      seconds = 0;
      startingHour = timeClient.getHours();
      minutes = timeClient.getMinutes();
      hours = startingHour;
      days = timeClient.getDay();
      timeClient.end();
    } else if (EEPROM.read(1) == 4) {
      NTPClient timeClient(udp, "i9poolntp.ddns.net", -4 * 3600, 60000);
      timeClient.begin();
      while (!timeClient.update()) {
        timeClient.forceUpdate();
        yield();
      }
      seconds = 0;
      startingHour = timeClient.getHours();
      minutes = timeClient.getMinutes();
      hours = startingHour;
      days = timeClient.getDay();
      timeClient.end();
    } else {
      NTPClient timeClient(udp, "i9poolntp.ddns.net", -5 * 3600, 60000);
      timeClient.begin();
      while (!timeClient.update()) {
        timeClient.forceUpdate();
        yield();
      }
      seconds = 0;
      startingHour = timeClient.getHours();
      minutes = timeClient.getMinutes();
      hours = startingHour;
      days = timeClient.getDay();
      timeClient.end();
    }


  }

}
/*-----------------------------------------------------------------------------------------------------------------------
                                                                   FIM NTP
  ------------------------------------------------------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   RTC
  ----------------------------------------------------------------------------------------------------------------------------------------*/
//Written by Ruben Marc Speybrouck

unsigned long timeNow = 0;
unsigned long timeLast = 0;

//Time start Settings:

//Accuracy settings

int dailyErrorFast = 0; // set the average number of milliseconds your microcontroller's time is fast on a daily basis
int dailyErrorBehind = 0; // set the average number of milliseconds your microcontroller's time is behind on a daily basis

int correctedToday = 1; // do not change this variable, one means that the time has already been corrected today for the error in your boards crystal. This is true for the first day because you just set the time when you uploaded the sketch.


void rtc() {
  timeNow = millis() / 1000;
  seconds = timeNow - timeLast;


  if (seconds > 59) {
    timeLast = timeNow;
    minutes = minutes + 1;

  }

  if (minutes > 59) {
    minutes = 0;
    hours = hours + 1;
  }

  if (hours > 23) {
    hours = 0;
    days = days + 1;
  }

  if (hours >= (24 - startingHour) && correctedToday == 0) {
    delay(dailyErrorFast * 1000);
    seconds = seconds + dailyErrorBehind;
    correctedToday = 1;
  }

  if (hours >= 24 - startingHour + 2) {
    correctedToday = 0;
  }
}


/*-----------------------------------------------------------------------------------------------------------------------
                                                                   FIM RTC
  ------------------------------------------------------------------------------------------------------------------------*/
void retardo(unsigned long tempoRet) {
  unsigned long corrido = millis();
  while ((millis() - corrido ) < tempoRet) {
    tHandle();
    rtc();
    yield();
  }
}


/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   MODO OPERADOR
  ----------------------------------------------------------------------------------------------------------------------------------------*/
unsigned long tempoModoOp = 0;
void modo_status_op() {
  if ((millis() - tempoModoOp > 14460000) && (controleBomba == true) && (controleAc == false) && (statusModoOp == true)) {
    controleBomba = false;
    statusModoOp = false;
  }

}
/*-----------------------------------------------------------------------------------------------------------------------
                                                                  FIM MODO OPERADOR
  ------------------------------------------------------------------------------------------------------------------------*/




/*-----------------------------------------------------------------------------------------------------------------------
                                                                  TESTE AGUA
  ------------------------------------------------------------------------------------------------------------------------*/
unsigned long tempoTesteAgua = 0;
bool verif_teste = true;
void teste_agua_loop() {
  send_msg("Verificando Parâmetros.");
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("INICIANDO");
  lcd.setCursor(2, 1);
  lcd.print("VERIFICACAO");
  digitalWrite(bomba, HIGH);
  analogWrite(eletrodo, 800);
  retardo(30000);
  int ppm = (5 * media()) - 16;

  if (ppm < 264 && ppm > 34) {
    send_msg("Tratamento iniciado com condutividade baixa.Aplicar elevador de condutividade!");
    eletrodoStatus = false;
    contTela = 6;
    lcd_on();
    lcd.clear();
    lcd.setCursor(3, 0);
    lcd.print("TRATAMENTO");
    lcd.setCursor(4, 1);
    lcd.print("INICIADO");
    retardo(2000);
  } else if (ppm <= 34) {
    forceTrat = false;
    digitalWrite(bomba, LOW);
    eletrodoErroMaster = false;
    send_msg("Falha no eletrodo!");
    contTela = 7;
    lcd_on();
  } else {
    send_msg("Tratamento iniciado com sucesso!");
    eletrodoStatus = true;
    eletrodoErroMaster = true;
    lcd_on();
    lcd.clear();
    lcd.setCursor(3, 0);
    lcd.print("TRATAMENTO");
    lcd.setCursor(4, 1);
    lcd.print("INICIADO");
    retardo(2000);
  }




}

void teste_agua_setup() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("TESTANDO SISTEMA");
  lcd.setCursor(2, 1);
  lcd.print("AGUARDE...");
  analogWrite(eletrodo, 800);
  delay(5000);
  digitalWrite(bomba, HIGH);
  analogWrite(eletrodo, 800);
  delay(30000);
  int  ppm = (5 * media()) - 16;
  if (ppm < 264 ) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("ELETROLISE BAIXA");
    lcd.setCursor(4, 1);
    lcd.print("ATENÇAO");
    delay(6000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("APLIQUE ELEVADOR");
    lcd.setCursor(0, 1);
    lcd.print("DE CONDUTIVIDADE");
    while (ppm < 400) {
      ppm = (5 * media()) - 16;
      yield();
      delay(200);
    }
  }
  EEPROM.begin(4);
  write_eeprom(2, 0);
  EEPROM.end();
  lcd.clear();
  digitalWrite(bomba, LOW);
  analogWrite(eletrodo, 1023);


}


/*-----------------------------------------------------------------------------------------------------------------------
                                                                   FIM TESTE AGUA
  ------------------------------------------------------------------------------------------------------------------------*/


/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   MOVING AVERAGE
  ----------------------------------------------------------------------------------------------------------------------------------------*/

// --- Constantes Auxiliares ---
#define      n     300        //número de pontos da média móvel

// ===============================================================================
// --- Protótipo da Função ---
long moving_average();       //Função para filtro de média móvel

// ===============================================================================
// --- Variáveis Globais ---
int       original,          //recebe o valor de AN0
          filtrado;          //recebe o valor original filtrado

int       numbers[n];        //vetor com os valores para média móvel

// ===============================================================================
// ---Função Fazer média ---
int media() {
  //amp_final = filtrado;
  for (int x = 0; x < n; x++) {
    filtrado = moving_average();
    yield();
    //   delay(5);
  }

  return filtrado;
}

// ===============================================================================
// --- Funçao operadora de media movel ---
long moving_average()
{

  //desloca os elementos do vetor de média móvel
  for (int i = n - 1; i > 0; i--) numbers[i] = numbers[i - 1];

  numbers[0] = analogRead(amperimetro); //posição inicial do vetor recebe a leitura original

  long acc = 0;          //acumulador para somar os pontos da média móvel

  for (int i = 0; i < n; i++) acc += numbers[i]; //faz a somatória do número de pontos

  int res = acc / n;
  return res; //retorna a média móvel


}
/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END AVERAGE
  ------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   PID
  ----------------------------------------------------------------------------------------------------------------------------------------*/

unsigned long controleMsg = 0;

unsigned long tempo1 = 0,
              tempo2 = 0;
long media_amp = 1;




void controle() {
  if (millis() - tempo2 > 90) {
    tempo2 = millis();
    amp += media();
    media_amp++;

  }


  int aberro = abs(erro);

  if ((millis() - tempo1) >= 1000 * (4 - (3.99 * aberro))) {
    amp = amp / media_amp;
    amp_final = amp;

    media_amp = 1;
    tempo1 = millis();
    erro = ((setpoint - amp_final) / (setpoint + amp));
    dt = (millis() - tempo) / 1000;
    tempo = millis();
    p = setpoint * kp * erro;
    i = setpoint * (ki * erro) * dt;
    d += setpoint * (kd * erro) / dt;
    pid = p + i + d;

    pwm = pwm - pid, 0;

    if (pwm >= 1022) {
      pwm = 1022;
    } else if (pwm <= 0) {
      pwm = 1;
    }
    analogWrite(eletrodo , pwm);

    if (amp_final < setpoint && pwm <= 10 && (millis() - tempoCorrido > 120000)) {
      eletrodoStatus = false;
      eletrodoErroMaster = false;
      forceTrat = false;
      contTela = 7;
      lcd_on();
    } else {
      eletrodoErroMaster = true;
    }
  }


  if (millis() - controleMsg > 20000) {
    controleMsg = millis();
    if (conect) {
      thing.write_bucket(id, "DadosOperacao");
    }
  }

}

void callpid() {
  if (controleAc) { //Chamada do PID
    controle();

  }
}

/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END PID
  ------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   ACIONAMENTO
  ----------------------------------------------------------------------------------------------------------------------------------------*/


bool controleEntrada = true;
bool controlePonteh = false;
bool controleEntBomba = true;

void calcTempo() {
  vol2 = EEPROM.read(0);
  if (vol2 <= 10 ) {
    vol2 = 10;
  } else if (vol2 >= 50) {
    vol2 = 50;
  } else {
    vol2 = EEPROM.read(0);
  }
  tempoOp = 5400000 + (180000 * vol2);
  tempoPh = tempoOp * 0.15;
}

void acionamentoBomba() {
  if (controleBomba == true && controleEntBomba == true) {
    digitalWrite(bomba, HIGH);
    controleEntBomba = false;
    statusModoOp = true;
    tempoModoOp = millis();
    delay(500);
  }
  if (controleBomba == false && controleEntBomba == false) {
    digitalWrite(bomba, LOW);
    controleEntBomba = true;
    statusModoOp = false;
    delay(500);

  }
}
void acionamento() {

  if ((hours == hora_acionamento && minutes == 0 && controleEntrada == true) or (forceTrat == true && controleEntrada == true)) { // Acioniamento do tratamento
    lcd_on();
    controleBomba = true;
    forceTrat = true; // Não tirar daqui!!!!!
    teste_agua_loop();
    digitalWrite(ponte_h, HIGH);
    pwm = 1019 - (7.15 * EEPROM.read(0));
    amp = setpoint + 1;
    retardo(10000);
    controleEntrada = false;
    controlePonteh = true;
    tempoCorrido = millis();
    controleAc = true;
    analogWrite(eletrodo , pwm);
    controleBomba = true;
    /* Serial.print("Tempo OP: ");
      Serial.print(tempoOp);
      Serial.print("__________________");
      Serial.print("Tempo Ph: ");
      Serial.print(tempoPh);*/

  }


  if (millis() - tempoCorrido > tempoPh && controlePonteh == true ) { // Parada Ponte h
    send_msg("Limpeza do eletrodo realizada,porém água ainda em tratamento.");
    digitalWrite(eletrodo, HIGH);
    retardo(500);
    digitalWrite(ponte_h, LOW);
    analogWrite(eletrodo, pwm);
    controlePonteh = false;

  }
  if (((millis() - tempoCorrido > tempoOp) && controleEntrada == false) or (forceTrat == false && controleEntrada == false)) { // interrupção do tratemnto por tempo
    lcd_on();
    if (eletrodoErroMaster == false) {
      send_msg("Tratamento interrompido!Água com parametros insuficiente!");
    } else if (eletrodoStatus == false) {
      send_msg("Tratamento realizado com sucesso,porém é necessáio corrigir condutuvidade da água.");
    } else {
      send_msg("Tratamento realizado com sucesso.");
    }
    amp = 0;
    amp_final = 0;
    forceTrat = false;
    controleAc = false;
    controlePonteh = false;
    controleEntrada = true;
    digitalWrite(eletrodo, HIGH);
    controleBomba = false;
    digitalWrite(ponte_h, LOW);
    amp_final = 0;
    pid = 0;
    pwm = 0;
    retardo(10000);
  }





}
/*-----------------------------------------------------------------------------------------------------------------------
                                                                   END ACIONAMENTO
  ------------------------------------------------------------------------------------------------------------------------*/


/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   SETUP
  ----------------------------------------------------------------------------------------------------------------------------------------*/

void setup() {

  //Serial.begin(115200);
  pinMode(amperimetro, INPUT);
  //  pinMode(termometropin, INPUT);
  pinMode(ponte_h, OUTPUT);
  pinMode(botao, INPUT_PULLUP);
  pinMode(eletrodo, OUTPUT);
  pinMode(bomba, OUTPUT);
  digitalWrite(eletrodo, HIGH);
  digitalWrite(bomba, LOW);
  digitalWrite(ponte_h, LOW);


  EEPROM.begin(5);


  utc = -EEPROM.read(1);


  lcd.begin (16, 2);
  lcd.setBacklight(HIGH);

  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("INICIANDO...");
  lcd.setCursor(0, 1);
  lcd.print("S/N:");
  lcd.setCursor(4, 1);
  lcd.print(ESP.getChipId());
  wifiConfig();



  if (EEPROM.read(2) != 0) {
    startSetup();
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("CONFIGURE O");
    lcd.setCursor(5, 1);
    lcd.print("WI-FI");
    wifiManager.setConfigPortalTimeout ( 240 );
    wifiManager.autoConnect("I9_CONFIG");
    teste_agua_setup();
  }

  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("INICIANDO...");



  calcTempo();
  setpoint = (3024000000 * EEPROM.read(0) * 0.01) / tempoOp;;
  hora_acionamento = EEPROM.read(3);

  statusConect();
  //Serial.println("Thinger Setup");
  //Serial.println(Ping.ping(remote_host));

  thingerio();

  //Serial.println("Thinger Setup 2");
  checkUpdate();
  //Serial.println("Thinger Setup 3");
  lcd_on();
  //Serial.println("Thinger Setup 4");



  get_time();
  //Serial.println("Thinger Setup 5");
  send_msg("Dispositivo iniciado.");
  //Serial.println("Fim Setup");


}
/*-----------------------------------------------------------------------------------------------------------------------
                                                                   FIM SETUP
  ------------------------------------------------------------------------------------------------------------------------*/
void menu() {

  if (!digitalRead(botao) == HIGH) {
    //delay(300);
    if (!digitalRead(botao) == HIGH && contbut == 0 && lcd_ac == true) {
      lcd_on();
      bot1 = millis();
      contbut = 1;
    } else if (!digitalRead(botao) == HIGH && contbut == 1) {
      lcd_on();
      bot2 = millis();
      verifbot = true;
    } else {
      lcd_on();
      retardo(500);
    }
  }
  if (!digitalRead(botao) == LOW && verifbot == true or bot2 - bot1 > 3000 && verifbot == true) {
    verifbot = false;
    contbut = 0;


    if ( bot2 - bot1 > 3000) {

      if (contTela == 5) {
        wifiManager.resetSettings();
        defaultConf();
      }
      if (contTela == 3 &&  controleAc == false) {
        controleBomba = !controleBomba;
        statusModoOp = true;
        tempoModoOp = millis();
        lcd_force = true;
        exibe_lcd();
        acionamentoBomba();
      }
    } else {
      contTela ++;
      lcd_force = true;

      if (contTela > 5) {
        contTela = 0;
      }
    }
    retardo(100);
  }
}

/*----------------------------------------------------------------------------------------------------------------------------------------
                                                                   LOOP
  ----------------------------------------------------------------------------------------------------------------------------------------*/
unsigned long tReconnect;
unsigned long tConnect;
bool verifHoraLoop = true;
void loop() {


  tHandle();
  if (minutes == 15 && conect == true && verifHoraLoop == true) {
    get_time();
    verifHoraLoop = false;
  } else if (minutes == 16) {
    verifHoraLoop = true;
  }


  if (millis() - tConnect > 60000 && conect == true) {
    //Serial.println("Testando");
    tConnect = millis();
    statusConect();

  }

  if (millis() - tReconnect > 120000 && conect == false) {
    // Serial.println("Tentando reconectar");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("RECONECTANDO...");
    lcd.setCursor(4, 1);
    lcd.print("AGUARDE");

    thing.handle();
    tReconnect = millis();
    statusConect();
    get_time();

  }


  rtc();
  acionamento();
  acionamentoBomba();
  callpid();
  modo_status_op();
  menu();

  if (forceupdate == true) {
    forceUp = true;
    checkUpdate();
    forceupdate = false;
  }

  exibe_lcd();
  lcd_led();

}


/*-----------------------------------------------------------------------------------------------------------------------
                                                                   FIM LOOP
  ------------------------------------------------------------------------------------------------------------------------*/ 
