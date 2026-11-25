"""
E se você cumprir MAIS do que 65% do plano?
Roda os principais cenários para vários níveis de disciplina.
    python3 simulacao/disciplina.py
"""
import numpy as np
from simulacao import CENARIOS, simular, chance

N_GRADE = 10000

NIVEIS = {
    "50% (fase ruim)": 0.50,
    "65% (hoje)": 0.65,
    "75%": 0.75,
    "85%": 0.85,
    "95% (máquina)": 0.95,
    # mudança de mentalidade gradual: começa em 65% e chega a 85% em 12 meses
    "65%->85% em 1 ano": lambda t: 0.65 + 0.20 * min(t, 12) / 12,
    # empolga, depois cai: 90% por 3 meses e 60% depois
    "fogo de palha (90%->60%)": lambda t: 0.90 if t < 3 else 0.60,
}

CEN = ["A*) Escada híbrida (recomendada)",
       "B*) Escada híbrida + diploma acelerado",
       "C) Direto no nível superior (sem médio)",
       "D) CACD puro desde 2027"]

if __name__ == "__main__":
    print("Chance no TCE-GO (só pela preparação até 17/01):")
    for nome, a in NIVEIS.items():
        a0 = a(0) if callable(a) else a
        print(f"  {nome:26s} ~{260*a0:4.0f}h efetivas -> {chance('medio_top', 260*a0):.1%}")
    print()
    for cen in CEN:
        print(cen)
        print(f"  {'disciplina':26s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} {'diplomata':>9s} "
              f"{'jubilado':>8s} {'idade cargo top (mediana)':>26s} {'renda acum. R$ mil':>18s}")
        for nome, a in NIVEIS.items():
            r = simular(CENARIOS[cen], adesao=a, n=N_GRADE)
            top = r["idade_top"]
            med_top = f"{np.nanmedian(top):.1f}" if np.mean(~np.isnan(top)) >= 0.5 else "—  (<50% chega)"
            print(f"  {nome:26s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
                  f"{r['diplomata_28'].mean():9.0%} {r['jubilado'].mean():8.0%} "
                  f"{med_top:>26s} {np.median(r['renda_acum'])/1000:18.0f}")
        print()
