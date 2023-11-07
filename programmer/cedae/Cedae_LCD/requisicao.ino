// Realizar requisição HTTP e retornar a resposta como uma string
String fazerRequisicaoHTTP(String url) {
  String resposta;
  clienteHTTP.begin(clienteWiFi, url);
  int codigoHTTP = clienteHTTP.GET();

  if (codigoHTTP > 0) {
    if (codigoHTTP == HTTP_CODE_OK) {
      resposta = clienteHTTP.getString();
    } else {
      Serial.print("Erro na Requisição HTTP, Código: ");
      Serial.println(codigoHTTP);
    }
  } else {
    Serial.println("Falha ao fazer a Requisição HTTP");
  }

  clienteHTTP.end();
  return resposta;
}
