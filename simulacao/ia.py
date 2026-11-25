"""
E a IA? Duas coisas diferentes:
  1) IA para ESTUDAR: muda a qualidade da hora (eficiência), não a quantidade.
  2) IA para GANHAR DINHEIRO (produtos digitais, vendas, vídeos): renda extra
     incerta, que custa horas de estudo.
    python3 simulacao/ia.py
Estimativas para comparar caminhos.
"""
import numpy as np
from simulacao import simular, FIM_28
from meu_caso import CEN, com

N_IA = 8000
rng = np.random.default_rng(99)
I1 = CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"]

ESTUDO = {
    "Sem IA": 1.00,
    "IA usada ERRADO (lê resumo em vez de fazer questão)": 0.90,
    "IA bem usada (tutor, questões, correção de redação)": 1.20,
    "IA muito bem usada + método (revisão espaçada, simulados)": 1.30,
}

def renda_ia(dist, n):
    """Renda mensal do negócio com IA aos 28: sorteia uma faixa."""
    faixas, probs = zip(*dist)
    idx = rng.choice(len(faixas), p=probs, size=n)
    return np.array([rng.uniform(*faixas[k]) for k in idx])

# lado: 5h/semana; principal: 35h/semana (renda aos 28, R$/mês)
LADO = [((0, 300), 0.60), ((300, 1500), 0.25), ((1500, 5000), 0.12), ((5000, 20000), 0.03)]
PRINCIPAL = [((0, 1000), 0.45), ((1000, 4000), 0.30), ((4000, 10000), 0.18), ((10000, 40000), 0.07)]

if __name__ == "__main__":
    print("=== 1. IA PARA ESTUDAR (escada integral I1) ===")
    print(f"  {'Uso da IA':58s} {'adesão':>6s} {'≥8k até 25':>10s} {'≥18k aos 28':>11s}")
    for nome, ef in ESTUDO.items():
        for a in (0.65, 0.85):
            r = simular(com(I1, eficiencia=ef), adesao=a, n=N_IA)
            print(f"  {nome:58s} {a:6.0%} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%}")
    print()

    print("=== 2. IA PARA GANHAR DINHEIRO ===")
    base = simular(com(I1, eficiencia=1.2), adesao=0.65, n=N_IA)
    print(f"  Escada + IA no estudo, sem negócio:                 ≥8k até 25 {base['estavel8k_25'].mean():.0%}"
          f"  ≥18k aos 28 {base['top18k_28'].mean():.0%}")
    lado = simular(com(I1, eficiencia=1.2, h_extra_sem_cargo=-5, h_sem_trabalhando=11),
                   adesao=0.65, n=N_IA)
    ex = renda_ia(LADO, N_IA)
    print(f"  Escada + negócio com IA 5h/sem desde já:            ≥8k até 25 {lado['estavel8k_25'].mean():.0%}"
          f"  ≥18k aos 28 {lado['top18k_28'].mean():.0%}  | negócio aos 28: mediana R$ {np.median(ex):.0f},"
          f" ≥R$1,5 mil {np.mean(ex >= 1500):.0%}")
    pr = renda_ia(PRINCIPAL, 100000)
    print(f"  Negócio com IA NO LUGAR do concurso (35h/sem):      renda aos 28: mediana R$ {np.median(pr):.0f},"
          f" ≥R$8 mil {np.mean(pr >= 8000):.0%}, ≥R$18 mil {np.mean(pr >= 18000):.0%}")
