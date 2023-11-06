// Exibir valores na tela OLED
void mostrarValoresNaTela(float taxaVazao, float alturaReser) {
  float altura = (55 * alturaReser / 2.3);
  int vazao = 0.69 * pow(taxaVazao, 1.522);
  int hora = ntp.getHours();
  int minuto = ntp.getMinutes();
  OLED.clearDisplay();
  OLED.setTextColor(WHITE, BLACK);
  //valor da vazao
  OLED.setTextSize(1);
  OLED.setCursor(2, 0);
  OLED.println("Vazao");
  OLED.setTextSize(2);
  OLED.setCursor(5, 16);
  OLED.print(vazao);
  OLED.setTextSize(1);
  OLED.print(" L/s");

  //valor do nivel do reservatorio
  OLED.setCursor(2, 36);
  OLED.println("Reservatorio");
  OLED.setTextSize(2);
  OLED.setCursor(5, 50);
  OLED.print(alturaReser);
  OLED.setTextSize(1);
  OLED.print(" m");

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
  if (taxaVazao < 0 || alturaReser > 2) {
    OLED.clearDisplay();
    OLED.setTextColor(WHITE, BLACK);
    OLED.setTextSize(3);
    OLED.println("Atencao");
    OLED.display();
    delay(250);
    digitalWrite(4, LOW);
  }
}
