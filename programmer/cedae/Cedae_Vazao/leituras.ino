//**** Leituras dos Dados ****//
void ler_vazao() {
  if (abs(leitura2 - leitura) >3) {
    cont = cont-5000;
  }
}
if (millis() - cont >= 20000) {
  cont = millis();
  digitalWrite(LED_BUILTIN, LOW);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * pulso / 2;
  Serial.println(duration);
  altura2 = dist - distance;
  if (altura2 < 0) {
    altura2 = md_ler[0];
  }
  md_ler[2] = md_ler[1];
  md_ler[1] = md_ler[0];
  md_ler[0] = altura;

  altura = (altura2 + md_ler[0] + md_ler[1] + md_ler[2]) / 4;

  vazao = 0.69 * pow(altura, 1.522);

  inicio();
  vazao_media();
  digitalWrite(LED_BUILTIN, HIGH);
}
}
