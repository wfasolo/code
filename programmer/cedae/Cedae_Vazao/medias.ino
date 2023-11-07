//** Calcula a vazao Media  **//
void vazao_media() {

  // vazao dia
  i_d++;
  vz_dia += vazao;

  if (millis() - cont_s >= 10000) {
    vz_dia = (vz_dia / i_d);

    if (millis() - cont_d >= 86400000) {
      thing.stream(thing["Banco"]);
      i_d = 0;
      vz_dia = 0;
      cont_d = millis();
    }
  }

  // vazao hora
  i_h++;
  vz_hor += vazao;

  if (millis() - cont_s >= 10000) {
    vz_hor = (vz_hor / i_h);

    if (millis() - cont_h >= 3600000) {
      thing.stream(thing["Banco"]);
      i_h = 0;
      vz_hor = 0;
      cont_h = millis();
      ntp.forceUpdate();
    }
  }

  // vazao minuto
  i_m++;
  vz_min += vazao;

  if (millis() - cont_s >= 10000) {
    vz_min = (vz_min / i_m);

    if (millis() - cont_m >= 60000) {
      thing.stream(thing["Banco"]);
      i_m = 0;
      vz_min = 0;
      cont_m = millis();
    }
  }

  // vazao 10 segundos
  i_s++;
  vz_seg += vazao;

  if (millis() - cont_s >= 10000) {
    vz_seg = (vz_seg / i_s);

    thing.stream(thing["Vz_media"]);
    i_s = 0;
    vz_seg = 0;
    cont_s = millis();
  }
}
