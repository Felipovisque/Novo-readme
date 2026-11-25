"""
A simulação com os SEUS dados reais (dez/2026):
  - sem cidadania europeia (bisavô do seu pai não dá direito pela lei italiana de 2025);
  - família banca tempo integral enquanto você estuda de verdade; CEDERJ é gratuito;
  - estágio no cartório até completar 1 ano (~mai/2027), depois integral;
  - repete disciplinas em 2027.1 -> no integral sobra tempo para a faculdade (+5 pts em Estatística);
  - R$ 1 mil guardados; inglês intermediário; PS5 + GTA 6 recém-comprados.
    python3 simulacao/meu_caso.py
"""
import numpy as np
from simulacao import CENARIOS, simular, mes, chance

N_M = 10000
A = CENARIOS["A*) Escada híbrida (recomendada)"]
C = CENARIOS["C) Direto no nível superior (sem médio)"]
MAI27 = mes(2027, 5)

def com(base, **kw):
    c = dict(base); c.update(kw); return c

def foco_virada(meses_antes):
    return lambda cargo, t, grad: "medio" if (cargo is None and t < grad - meses_antes) else "sup"

INTEGRAL = dict(integral_desde=MAI27, h_sem=35, h_sem_estagio=25, apoio_pos_diploma=True,
                p_passar_estat=0.93)

CEN = {
    "Estágio + 25h (plano antigo)": A,
    "I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)": com(A, **INTEGRAL),
    "I2) Integral escada, vira p/ superior 24m antes do diploma": com(
        A, **INTEGRAL, foco=foco_virada(24)),
    "I3) Integral direto no superior": com(C, **INTEGRAL),
}

GTA = {
    "sem GTA (65%)": 0.65,
    "GTA sem regra (55% nos 4 primeiros meses)": lambda t: 0.55 if t < 4 else 0.65,
}

if __name__ == "__main__":
    print("TCE-GO:")
    for nome, a in {"65%": 0.65, "GTA sem regra (55%)": 0.55, "75%": 0.75}.items():
        print(f"  {nome:22s} ~{260*a:.0f}h efetivas -> {chance('medio_top', 260*a):.1%}")
    print()
    print(f"{'Cenário':68s} {'adesão':>6s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} "
          f"{'idade top':>9s} {'jubilado':>8s}")
    for nome, c in CEN.items():
        for na, a in {"65%": 0.65, "75%": 0.75, "85%": 0.85}.items():
            r = simular(c, adesao=a, n=N_M)
            top = r["idade_top"]
            it = f"{np.nanmedian(top):.1f}" if np.mean(~np.isnan(top)) >= .5 else "—"
            print(f"{nome:68s} {na:>6s} {r['estavel8k_25'].mean():10.0%} "
                  f"{r['top18k_28'].mean():11.0%} {it:>9s} {r['jubilado'].mean():8.0%}")
        print()
    print("Efeito do GTA 6 no I1:")
    for nome, a in GTA.items():
        r = simular(CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"],
                    adesao=a, n=N_M)
        print(f"  {nome:44s} ≥8k até 25: {r['estavel8k_25'].mean():.0%}  "
              f"≥18k até 28: {r['top18k_28'].mean():.0%}")
