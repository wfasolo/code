import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import sklearn.metrics as metrics


def valor(prepara):
    X_train = prepara['X_train']
    X_test = prepara['X_test']
    y_train = prepara['y_train']
    y_test = prepara['y_test']
    prev_trans = prepara['prev_trans']

    # Tainan model
    model = KNeighborsClassifier(n_neighbors=(1))
    model.fit(X_train, y_train)

    # Fazer previsoes
    y_pred = model.predict(X_test)

    acur = metrics.accuracy_score(y_test, y_pred)

    previsao = pd.DataFrame(model.predict_proba(prev_trans))

    return {'acuracia': acur, 'previsao': previsao}
