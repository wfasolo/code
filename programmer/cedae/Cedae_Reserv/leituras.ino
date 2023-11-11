//**** Leituras dos Dados ****//
void ler_volume() {
  if (segundo <= 5 && cont == 0) {
    digitalWrite(LED_BUILTIN, LOW);
    inicio();
    cont = 1;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    float duration = pulseIn(echoPin, HIGH);
    float distance = duration * pulso / 2;
    altura = (dist - distance) / 100;
    if (altura < 0) {
      altura = md_ler[0];
    }

    md_ler[2] = md_ler[1];
    md_ler[1] = md_ler[0];
    md_ler[0] = altura;

    altura = (md_ler[0] + md_ler[1] + md_ler[2]) / 3;

    volume = altura * comp * larg;

    thing.stream(thing["Volume"]);
    thing.stream(thing["Altura"]);
   // Serial.println(distance);
  }
  if (segundo > 5) {
    cont = 0;
  }
}
