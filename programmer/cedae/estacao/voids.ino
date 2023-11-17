// parametros de iniciação //
void inicio() {
  if (iniciar == false) {
    if (multiWiFi.run() == WL_CONNECTED) {
      ntp.forceUpdate();

      if (i_inic > 2) {
        iniciar = true;
        i_inic = 0;
      }
      i_inic++;
    }
  }
}

//**** verificar conexão ****//
void conectar() {
  if (multiWiFi.run() != WL_CONNECTED) {
    WiFi.disconnect();
    digitalWrite(LED_BUILTIN, LOW);
    iniciar = false;
    delay(100);
    WiFi.reconnect();
  }
}

//**** Reiniciar NodeMCU ****//
void reb_esp() {
  if (forcereboot == true) {
    ESP.restart();
  }
}

//**** Atualizacao da hora ****//
void at_hora() {
  //dia = ntp.getDay();
  hora = ntp.getHours();
  minuto = ntp.getMinutes();
  segundo = ntp.getSeconds();
}

//**** ler chuva ****//
void ler_chuva() {
  int sens_chuv = 0, i = 0, cc = 0;

  for (i = 1; i <= 10; i++) {
    if (digitalRead(pinoSensor) == HIGH) {
      cc = 0;
    } else {
      cc = 1;
    }

    sens_chuv = sens_chuv + cc;
    delay(15);
    yield();
  }

  sens_chuv = sens_chuv / i;

  if (sens_chuv < 1) {
    chuv = 0;
    id = 0;
  } else {
    chuv = 1;
  }
}

//**** chuva tempo real ****//
void chuva_real() {
  if (id == 0 && chuv == 1) {
    thing.stream(thing["parametros"]);
    delay(10);
    yield();

    ler_chuva();

    if (chuv == 1) {
      pres0 = presBD / cont1,
      temp0 = tempBD / cont1,
      umid0 = umidBD / cont1;

      thing.write_bucket("dados_estacao1", "parametros");
    }
    id = 1;
  }
}

//**** gravacao no banco de dados a cada 20 minutos ****//
void banco_1h() {
  if (segundo <= 10) {
    if (minuto == 0) {
      if (cont_BD == 0) {
        cont_BD = 1;
        pres0 = presBD / cont1,
        temp0 = tempBD / cont1,
        umid0 = umidBD / cont1;
        ler_chuva();

        thing.write_bucket("dados_estacao1", "parametros");

        presBD = 0;
        tempBD = 0;
        umidBD = 0;
        cont1 = 0;
      }
      if (hora == 0) {

        delay(100);
        ESP.restart();
      }
    }
  } else
    cont_BD = 0;
}

//**** ler parametros do clima ****//
void ler_clima() {
  int ii = 0;

  pres2 = pres1;
  pres1 = pres0;

  temp2 = temp1;
  temp1 = temp0;

  umid2 = umid1;
  umid1 = umid0;

  float tp = 0, pr = 0, um = 0;

  for (ii = 0; ii < 5; ii++) {
    sensors_event_t humidity, temp;
    aht.getEvent(&humidity, &temp);
    pr += bmp.readPressure();
    tp += (bmp.readTemperature() + temp.temperature) / 2;
    um += humidity.relative_humidity;
    delay(20);
    yield();

  }

  float tp1 = tp / ii;
  float um1 = um / ii;
  float pr1 = pr / (ii * 100);
  float pr2 = (1 - ((0.0065 * 95) / (tp1 + (0.0065 * 95) + 273.15)));
  float pr3 = pr1 * pow(pr2, (-5.257));

  pres0 = (pr3 + pres0 + pres1 + pres2) / 4;
  temp0 = (tp1 + temp0 + temp1 + temp2) / 4;
  umid0 = (um1 + umid0 + umid1 + umid2) / 4;
  thing.stream(thing["parametros"]);

  presBD += pres0;
  tempBD += temp0;
  umidBD += umid0;
  cont1++;
}
