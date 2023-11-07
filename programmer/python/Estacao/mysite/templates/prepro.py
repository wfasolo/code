from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def dados(corrigir, chuva):
    previsao = corrigir['corrigido']
    previsao = previsao.drop(['hora'], axis=1)

    X = chuva.drop(['Chuv'], axis=1)
    y = chuva['Chuv']


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.01,shuffle=True)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    prev_trans = scaler.transform(previsao)

    return {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test, 'prev_trans': prev_trans}
