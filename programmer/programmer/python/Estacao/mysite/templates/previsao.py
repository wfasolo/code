import templates.leitura as lei
import templates.correcao as corr
import templates.prepro as pre
#import templates.KNeighbors as KNe
#import templates.Florest as Fl
import templates.SVC as svc
import templates.graficos as gra

def prev():

    leit = lei.ler()

    corrige = corr.corrigir(leit)

    prepara = pre.dados(corrige, leit['estacao'])

    #dados_KN = KNe.valor(prepara)

    #dados_FL = Florest.valor(prepara)

    dados_SVC = svc.valor(prepara)

    gra.graf(corrige['corrigido'],dados_SVC)
