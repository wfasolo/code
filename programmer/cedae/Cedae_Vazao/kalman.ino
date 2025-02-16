// Variáveis globais para o filtro de Kalman
float x_est = 0.0;    // Estimativa atual do estado (altura da água)
float P_est = 1.0;    // Covariância do erro da estimativa
float Q = 0.0001;     // Covariância do ruído do processo (valor inicial)
float R = 0.1;        // Covariância do ruído da medição (valor inicial)

// Parâmetros para adaptação
const float ALPHA = 0.01;    // Fator de amortecimento para adaptação (entre 0 e 1)
const float MIN_R = 0.001;   // Limite inferior para R
const float MIN_Q = 0.00001; // Limite inferior para Q

// Variáveis para acumulação das estatísticas da inovação
// (neste exemplo, usamos o valor imediato com amortecimento para simplificar)
float innovationAvg = 0.0;

float kalmanFilterAdaptive(float measurement) {
    // Fase de Predição
    float x_pred = x_est;            // Modelo simples: estado inalterado entre medições
    float P_pred = P_est + Q;          // Atualiza a covariância com o ruído do processo

    // Cálculo da inovação (erro entre a medição e a predição)
    float innovation = measurement - x_pred;
    
    // Atualização do ganho de Kalman
    float K = P_pred / (P_pred + R);
    
    // Fase de Atualização
    x_est = x_pred + K * innovation;   // Corrige a estimativa do estado
    P_est = (1 - K) * P_pred;          // Atualiza a covariância do erro
    
    // Adaptação dos parâmetros R e Q com base na inovação
    // Atualiza a média amortecida das inovações ao quadrado
    innovationAvg = (1 - ALPHA) * innovationAvg + ALPHA * (innovation * innovation);
    
    // Ajuste adaptativo de R:
    // A ideia é que a variância da inovação teórica deve ser P_pred + R.
    // Assim, a parte atribuída à medição é estimada por innovationAvg - P_pred.
    float newR = innovationAvg - P_pred;
    if(newR < MIN_R) {
        newR = MIN_R;
    }
    // Atualiza R com um amortecimento adicional para evitar oscilações bruscas
    R = (1 - ALPHA) * R + ALPHA * newR;
    
    // Adaptação de Q (opcional):
    // A partir da correção aplicada, estima-se o ruído do processo.
    float processNoiseEst = (K * innovation) * (K * innovation);
    float newQ = processNoiseEst;
    if(newQ < MIN_Q) {
        newQ = MIN_Q;
    }
    Q = (1 - ALPHA) * Q + ALPHA * newQ;
    
    return x_est;
}

    

    
    
