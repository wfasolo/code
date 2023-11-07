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
  dia = ntp.getDay();
  hora = ntp.getHours();
  minuto = ntp.getMinutes();
  segundo = ntp.getSeconds();
}

//**** gravacao no banco de dados ****//
void banco_1h() {
  if (minuto == 0) {
    if (segundo < 10) {
      thing.write_bucket("dados_vazaobji", "Banco");
      if (hora == 0) {
        delay(100);
        ESP.restart();
      }
    }
  }
}

// parametros de iniciação //
void inicio() {
  if (iniciar == false) {
    if (multiWiFi.run() == WL_CONNECTED) {

      ntp.forceUpdate();
      cont_s = segundo * 1000;
      cont_m = cont_s;
      cont_h = (minuto * 60000) + cont_m;
      pson data;
      thing.get_property("parametro", data);
      dist = data["Distancia"];
      pulso = data["Pulso"];

      if (i_inic > 2) {
        iniciar = true;
        i_inic = 0;
      }
      i_inic++;
    }
  }
}
