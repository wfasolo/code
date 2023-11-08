// Exibir valores na tela OLED
void telavazao(float taxaVazao) {

  int vazao = 0.69 * pow(taxaVazao, 1.522);
  int hora = ntp.getHours();
  int minuto = ntp.getMinutes();
  OLED.clearDisplay();
  OLED.setTextColor(WHITE, BLACK);
  //valor da vazao
  OLED.setTextSize(1);
  OLED.setCursor(2, 0);
  OLED.println("Vazao");
  OLED.setTextSize(4);
  OLED.setCursor(5, 30);
  OLED.print(vazao);
  OLED.setTextSize(1);
  OLED.print(" L/s");

  //Relogio
  OLED.setTextSize(1);
  OLED.setCursor(90, 0);
  if (hora < 10) {
    OLED.print("0");
  }
  OLED.print(hora);
  OLED.print(":");
  if (minuto < 10) {
    OLED.print("0");
  }
  OLED.print(minuto);

  OLED.display();
}

// Exibir valores na tela OLED
void telareserv(float alturaReser) {
  int porc = (alturaReser / 2.2) * 100;
  float altura = (55 * alturaReser / 2.3);

  int hora = ntp.getHours();
  int minuto = ntp.getMinutes();
  OLED.clearDisplay();
  OLED.setTextColor(WHITE, BLACK);

  //valor do nivel do reservatorio
  OLED.setTextSize(1);
  OLED.setCursor(2, 0);
  OLED.println("Reservatorio");
  OLED.setTextSize(4);
  OLED.setCursor(5, 30);
  OLED.print(porc);
  OLED.setTextSize(1);
  OLED.print(" %");

  //Relogio
  OLED.setTextSize(1);
  OLED.setCursor(90, 0);
  if (hora < 10) {
    OLED.print("0");
  }
  OLED.print(hora);
  OLED.print(":");
  if (minuto < 10) {
    OLED.print("0");
  }
  OLED.print(minuto);

  //Desenha nivel reservatorio
  OLED.drawLine(85, 8, 85, 63, WHITE);
  OLED.drawLine(125, 8, 125, 63, WHITE);
  OLED.drawLine(85, 63, 125, 63, WHITE);
  OLED.fillRect(85, (64 - altura), 40, altura, WHITE);

  OLED.display();
}

// Piscar tela
void piscarTela(float taxaVazao, float alturaReser) {
  if (taxaVazao < 50 || alturaReser >= 2.1) {
    OLED.clearDisplay();
    OLED.setTextColor(WHITE, BLACK);
    OLED.setTextSize(3);
    OLED.println("Atencao");
    OLED.display();
    digitalWrite(4, LOW);
  } else {
    digitalWrite(4, HIGH);
  }
}
