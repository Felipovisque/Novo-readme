"""
E se eu passar logo num nível médio de ~R$ 8 mil+? Compara as vidas simuladas
pelo momento em que você ficou estável (≥ R$ 8 mil).
    python3 simulacao/passar_cedo.py
"""
import numpy as np
from simulacao import simular
from meu_caso import CEN, com

I1 = com(CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"],
         eficiencia=1.2, h_sem_trabalhando=22)

GRUPOS = [("Passa até o fim de 2027 (~23 anos)", 22.9, 24.0),
          ("Passa em 2028 (~24 anos)", 24.0, 25.0),
          ("Passa em 2029 (~25 anos)", 25.0, 26.0),
          ("Só depois / pelo superior direto", 26.0, 99)]

if __name__ == "__main__":
    for a in (0.65, 0.85):
        r = simular(I1, adesao=a, n=20000)
        ie = np.nan_to_num(r["idade_estavel"], nan=99)
        print(f"\nCumprindo {a:.0%} (escada + IA + 22h após posse)")
        print(f"  {'Quando fica estável (≥8k)':38s} {'% das vidas':>11s} {'≥18k aos 28':>11s} {'renda até 28':>12s}")
        for nome, lo, hi in GRUPOS:
            m = (ie >= lo) & (ie < hi)
            print(f"  {nome:38s} {m.mean():11.0%} {r['top18k_28'][m].mean():11.0%} "
                  f"{np.median(r['renda_acum'][m])/1000:10.0f}k")
