"""
Quanto o networking (contatos) pesa em cada caminho?
    python3 simulacao/networking.py
Concurso é impessoal: networking não muda a aprovação. No mercado ele muda
a chance de trainee/vaga boa e o salário de entrada (estimativas).
"""
import numpy as np
from simulacao import CENARIOS, simular

N_NET = 10000
A = CENARIOS["A*) Escada híbrida (recomendada)"]
F = CENARIOS["F) Mercado (estágio -> trainee/analista)"]

def com(base, **kw):
    c = dict(base); c.update(kw); return c

MERCADO = {
    "Mercado, networking ZERO (você hoje)": com(F, p_trainee=0.10, salario_junior=4000),
    "Mercado, networking construído (estágio bom + LinkedIn)": com(F, p_trainee=0.20, salario_junior=5500),
    "Mercado, networking FORTE (pai/família com contatos)": com(F, p_trainee=0.40, salario_junior=7500),
}

if __name__ == "__main__":
    print(f"{'Caminho':60s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} {'renda R$ mil':>12s}")
    for nome, c in MERCADO.items():
        r = simular(c, adesao=0.65, n=N_NET)
        print(f"{nome:60s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
              f"{np.median(r['renda_acum'])/1000:12.0f}")
    r = simular(A, adesao=0.65, n=N_NET)
    print(f"{'Escada (concurso) — networking zero, médio ou forte: igual':60s} "
          f"{r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
          f"{np.median(r['renda_acum'])/1000:12.0f}")
