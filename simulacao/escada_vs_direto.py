"""
Por que o "direto no superior" chega mais aos R$ 18 mil aos 28 do que a escada?
Mostra as horas acumuladas para o superior e estende a simulação até os 31 anos.
    python3 simulacao/escada_vs_direto.py
"""
import numpy as np
import simulacao as S
from meu_caso import CEN, com

I1 = CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"]
I3 = CEN["I3) Integral direto no superior"]
CASOS = {
    "Escada (16h/sem depois da posse no médio)": I1,
    "Escada (22h/sem depois da posse no médio)": com(I1, h_sem_trabalhando=22),
    "Direto no superior": I3,
}

def rodar(meses):
    S.MESES = meses
    out = {}
    for nome, c in CASOS.items():
        r = S.simular(c, adesao=0.65, n=8000)
        out[nome] = r
    return out

if __name__ == "__main__":
    r28, r31 = rodar(73), rodar(73 + 36)
    print(f"{'Caminho':46s} {'≥8k até 25':>10s} {'≥18k aos 28':>11s} {'≥18k aos 31':>11s} "
          f"{'renda até 28':>12s} {'renda até 31':>12s}")
    for nome in CASOS:
        a, b = r28[nome], r31[nome]
        print(f"{nome:46s} {a['estavel8k_25'].mean():10.0%} {a['top18k_28'].mean():11.0%} "
              f"{b['top18k_28'].mean():11.0%} {np.median(a['renda_acum'])/1000:10.0f}k "
              f"{np.median(b['renda_acum'])/1000:10.0f}k")
