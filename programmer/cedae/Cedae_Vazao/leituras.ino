//**** Leituras dos Dados ****//
void ler_vazao() {
  digitalWrite(LED_BUILTIN, LOW);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  float duration = pulseIn(echoPin, HIGH);
  float distance = duration * pulso / 2;

  altura = dist - distance;
  if (altura < 0) {
    altura = md_ler[0];
  }
  md_ler[2] = md_ler[1];
  md_ler[1] = md_ler[0];
  md_ler[0] = altura;

  altura = (md_ler[0] + md_ler[1] + md_ler[2]) / 3;

  vazao = 0.69 * pow(altura, 1.522);
}
