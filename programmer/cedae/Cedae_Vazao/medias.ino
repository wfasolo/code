//** Calcula a vazao Media  **//
void vazao_media() {
  i_m++;
  i_h++;
  i_d++;
  vz_dia += vazao;
  vz_hor += vazao;
  vz_min += vazao;

  thing.stream(thing["Vz_media"]);

  vz_min2 = (vz_min / (i_m + 1));
  thing.stream(thing["Vz_min"]);


  vz_hor = (vz_hor / (i_h + 1));
  thing.stream(thing["Vz_hor"]);
  vz_hor = (vz_hor * (i_h + 1));

  vz_dia = (vz_dia / (i_d + 1));
  thing.stream(thing["Vz_dia"]);
  vz_dia = (vz_dia * (i_d + 1));


  if (segundo < 15) {  // vazao minuto
    vz_min = (vz_min / (i_m + 1));
    i_m = 0;
    if (minuto == 0) {  // vazao hora
      vz_hor = (vz_hor / (i_h + 1));
      thing.write_bucket("dados_vazaobji", "Vz_hor");
      i_h = 0;
      if (hora == 0) {  // vazao dia

        delay(100);
        ESP.restart();
      }
    }
  }
}
