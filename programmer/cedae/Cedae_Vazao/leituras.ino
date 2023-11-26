//**** Leituras dos Dados ****//
void ler_vazao() {
  if (abs(altura2 - altura) >= 4) {
    cont = cont - 50;
  }

  if (millis() - cont >= 20000) {
    digitalWrite(LED_BUILTIN, LOW);
    inicio();
    cont = millis();

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    float distance = duration * pulso / 2;
    altura2 = dist - distance;
    if (altura2 < 0) {
      altura2 = md_ler[0];
    }
    md_ler[2] = md_ler[1];
    md_ler[1] = md_ler[0];
    md_ler[0] = altura;

    altura = (altura2 + md_ler[0] + md_ler[1] + md_ler[2]) / 4;

    vazao = 0.69 * pow(altura, 1.522);

    vazao_media();
    digitalWrite(LED_BUILTIN, HIGH);
  }
}
