
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

//**** Upload Codigo ****//
void upload() {
  if (uploads == true) {
    t_httpUpdate_return ret = ESPhttpUpdate.update(client, "http://estacao.wuaze.com/upload/reserv.bin");
    switch (ret) {
      case HTTP_UPDATE_FAILED:
        atualiza = "UP FAILED";
        break;
      case HTTP_UPDATE_NO_UPDATES:
        atualiza = "NO UPDATE";
        break;
      case HTTP_UPDATE_OK:
        atualiza = "UPDATE OK";
        break;
    }
     thing.stream(thing["Atualiza"]);
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
    if (segundo < 5) {
      pson data;
      data["altura"] = altura;
      data["volume"] = volume;
      thing.write_bucket("dados_reserv_BJI", data);
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
      pson data;
      thing.get_property("parametro", data);
      dist = data["Distancia"];
      pulso = data["Pulso"];
      larg = data["Largura"];
      comp = data["Comprimento"];
      if (i_inic >= 2) {
        iniciar = true;
        i_inic = 0;
      }
      i_inic++;
    }
  }
}