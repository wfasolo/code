from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier


def valor(prepara):
    X_train = prepara['X_train']
    X_test = prepara['X_test']
    y_train = prepara['y_train']
    y_test = prepara['y_test']
    prev_trans = prepara['prev_trans']

    # Tainar modelo
    model = RandomForestClassifier(n_estimators=1, n_jobs=-1)
    model.fit(X_train, y_train)

    # Fazer previsoes
    y_pred = model.predict(X_test)

    acur = metrics.accuracy_score(y_test, y_pred)

    previsao = model.predict_proba(prev_trans)
    
    return {'acuracia': acur, 'previsao': previsao}
