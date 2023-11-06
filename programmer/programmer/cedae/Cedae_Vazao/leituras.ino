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
  md_ler[1] = md_ler[0];
  md_ler[2] = md_ler[1];
  md_ler[3] = md_ler[2];
  altura = (altura + md_ler[0] + md_ler[1] + md_ler[2] + md_ler[3]) / 5;
  md_ler[0] = altura;
  vazao = 0.69 * pow(altura, 1.522);
}
