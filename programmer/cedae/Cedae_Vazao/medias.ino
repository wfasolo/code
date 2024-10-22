//** Calcula a vazao Media  **//
void vazao_media()
{
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
  vol_trat = vz_dia * ((hora * 3.6) + (minuto * 0.06));
  thing.stream(thing["Vol_trat"]);
  vz_dia = (vz_dia * (i_d + 1));
}

void media2()
{
  if (segundo < 10 && est2 == 1)
  { // vazao minuto
    est2 = 0;
    vz_min = (vz_min / (i_m + 1));
    i_m = 0;
    if (minuto == 0)
    { // vazao hora
      vz_hor = (vz_hor / (i_h + 1));
      pson data;
      data["Vaz_Hora"] = int(vz_hor);
      thing.write_bucket("dados_vazaobji", data);
      i_h = 0;
      if (hora == 0)
      {
        delay(100);
        ESP.restart();
      }
    }
  }
  if (segundo >= 10)
  {
    est2 = 1;
  }
}
