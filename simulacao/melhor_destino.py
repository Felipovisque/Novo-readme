"""
Dá para mudar o destino? Empilha, uma por uma, as alavancas que funcionaram.
    python3 simulacao/melhor_destino.py
"""
import numpy as np
from simulacao import simular
from meu_caso import CEN, com, foco_virada

N_D = 8000
I1 = CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"]

PASSOS = [
    ("0. Hoje: escada integral, 65%, sem IA, relaxa após posse", I1, 0.65),
    ("1. + não relaxar depois da posse (22h/sem)", com(I1, h_sem_trabalhando=22), 0.65),
    ("2. + IA bem usada no estudo", com(I1, h_sem_trabalhando=22, eficiencia=1.2), 0.65),
    ("3. + método forte (questões, revisão espaçada)", com(I1, h_sem_trabalhando=22, eficiencia=1.3), 0.65),
    ("4. + disciplina subindo para 85%", com(I1, h_sem_trabalhando=22, eficiencia=1.3), 0.85),
    ("5. + diploma acelerado (EaD privada)", com(I1, h_sem_trabalhando=22, eficiencia=1.3,
                                                diploma="privada"), 0.85),
    ("6. + virar para o superior mais cedo (24m)", com(I1, h_sem_trabalhando=22, eficiencia=1.3,
                                                     diploma="privada", foco=foco_virada(24)), 0.85),
]

if __name__ == "__main__":
    print(f"{'Alavancas acumuladas':58s} {'≥8k até 25':>10s} {'≥18k aos 28':>11s} "
          f"{'idade cargo top':>15s} {'renda até 28':>12s}")
    for nome, c, a in PASSOS:
        r = simular(c, adesao=a, n=N_D)
        it = np.nanmedian(r["idade_top"])
        print(f"{nome:58s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
              f"{it:15.1f} {np.median(r['renda_acum'])/1000:10.0f}k")
