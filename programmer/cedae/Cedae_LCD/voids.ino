//**** verificar conexão ****//
void conectar() {
  WiFi.disconnect();
  digitalWrite(LED_BUILTIN, LOW);
  OLED.clearDisplay();
  OLED.setTextColor(WHITE, BLACK);
  OLED.setTextSize(2);
  OLED.print("off line !");
  OLED.display();
  delay(100);
  WiFi.reconnect();
  iniciar = false;
}

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