
// Função para fazer a requisição HTTP
function fazerRequisicao() {
    var urlVazao = 'http://api.thinger.io/v2/users/w_fasolo/devices/vazao_BJI/Vz_min?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJ2YXphb19CSkkiLCJpYXQiOjE2OTc5MDQ1NDIsImp0aSI6IjY1MzNmNzllNDljMTM3ZDI2MTA3ZDdlYSIsInN2ciI6InVzLWVhc3QuYXdzLnRoaW5nZXIuaW8iLCJ1c3IiOiJ3X2Zhc29sbyJ9.Qs9lkU-YfBH8PVaq7UMK_xxR_fKGd8manC1eo7imIio'; // Substitua pela URL desejada
    var urlReservatorio = 'http://api.thinger.io/v2/users/w_fasolo/devices/reserv_BJI/Altura?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJyZXNlcnZfQkpJIiwiaWF0IjoxNjk3OTA0NDAzLCJqdGkiOiI2NTMzZjcxMzQ5YzEzN2QyNjEwN2Q3ZTkiLCJzdnIiOiJ1cy1lYXN0LmF3cy50aGluZ2VyLmlvIiwidXNyIjoid19mYXNvbG8ifQ.bm8kXw4JVOGlwUdCQReg4fQy368DNWSIYGK6Z4GhYDw'; // Substitua pela URL desejada

    var xhrVazao = new XMLHttpRequest();
    xhrVazao.open('GET', urlVazao, true);
    xhrVazao.onload = function () {
        if (xhrVazao.status === 200) {
            var respostaVazao = xhrVazao.responseText;
            var respostaObjVazao = JSON.parse(respostaVazao);
            var valorNumericoVazao = respostaObjVazao.out;
            document.getElementById('vazaoResposta').textContent = 'Vazão: ' + valorNumericoVazao.toFixed(0) + ' L/s';
        } else {
            document.getElementById('vazaoResposta').textContent = 'Vazão: Erro na Requisição HTTP';
        }
    };
    xhrVazao.send();

    var xhrReservatorio = new XMLHttpRequest();
    xhrReservatorio.open('GET', urlReservatorio, true);
    xhrReservatorio.onload = function () {
        if (xhrReservatorio.status === 200) {
            var respostaReservatorio = xhrReservatorio.responseText;
            var respostaObjReservatorio = JSON.parse(respostaReservatorio);
            var valorNumericoReservatorio = respostaObjReservatorio.out;
            document.getElementById('reservatorioResposta').textContent = 'Reservatório: ' + valorNumericoReservatorio.toFixed(1) + ' m';
            plotarTanque(valorNumericoReservatorio);
        } else {
            document.getElementById('reservatorioResposta').textContent = 'Reservatório: Erro na Requisição HTTP';
        }
    };
    xhrReservatorio.send();
}

// Função para plotar o tanque com base nos dados recebidos
function plotarTanque(valorNumerico) {
    var nivelAgua = (valorNumerico / 2.4) * 100;
    var perc = nivelAgua * 1.09091;

    document.getElementById('agua').style.height = nivelAgua + '%';
    document.getElementById('agua').textContent = (perc.toFixed(1)) + '%';
}

fazerRequisicao();
setInterval(fazerRequisicao, 60000);
