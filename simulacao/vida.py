"""
Estágio (sair, completar 1 ano, ser efetivado), vida social/namoro e empreendedorismo.
    python3 simulacao/vida.py
Todos os números são ESTIMATIVAS para comparar caminhos.
"""
import numpy as np
from simulacao import CENARIOS, simular, mes, FIM_25, FIM_28

N_V = 10000
rng = np.random.default_rng(11)
A = CENARIOS["A*) Escada híbrida (recomendada)"]
C = CENARIOS["C) Direto no nível superior (sem médio)"]
FEV27, MAI27 = mes(2027, 2), mes(2027, 5)

def com(base, **kw):
    c = dict(base); c.update(kw); return c

def linha(nome, r):
    print(f"  {nome:58s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
          f"{np.median(r['renda_acum'])/1000:12.0f}")

def cab():
    print(f"  {'':58s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} {'renda R$ mil':>12s}")

# ------------------------------------------------------------------ 1. estágio
ESTAGIO = {
    "E0) Sai em fev/27 -> estágio melhor (base)": A,
    "E1) Completa 1 ano no cartório (mai/27) -> estágio melhor": A,   # igual no modelo
    "E2) Efetivado CLT no cartório (R$ 3 mil, 8h/dia) até passar": com(
        A, clt_desde=MAI27, salario_clt=3000, h_sem_clt=16),
    "E2b) Efetivado com R$ 4,5 mil": com(
        A, clt_desde=MAI27, salario_clt=4500, h_sem_clt=16),
    "E3) Sai em fev/27 -> integral 35h": com(
        A, integral_desde=FEV27, h_sem=35, h_sem_estagio=25),
    "E4) Completa 1 ano (mai/27) -> integral 35h": com(
        A, integral_desde=MAI27, h_sem=35, h_sem_estagio=25),
}

# ------------------------------------------------------------------ 2. vida social
# monge: +5h/sem, mas cansaço/solidão tiram adesão e aumentam meses ruins
# festeiro: -5h/sem e ressaca tira adesão
SOCIAL = {
    "Monge até passar (quase não sai)": (com(A, h_extra_sem_cargo=5, ades_delta_sem_cargo=-0.07,
                                             p_mes_ruim=0.14), 0.25),
    "Equilibrado (sexta à noite + domingo à tarde livres)": (A, 1.0),
    "Festeiro (sai 3x ou mais por semana)": (com(A, h_extra_sem_cargo=-5,
                                                 ades_delta_sem_cargo=-0.08), 1.4),
}

def namoro(fator_social, idade_estavel, n):
    """Chance de, aos 28, estar num namoro firme há 2+ anos (pré-requisito para casar ~28)."""
    t_est = np.where(np.isnan(idade_estavel), 999, (idade_estavel - 22.9) * 12)
    firme = np.zeros(n, dtype=bool)
    for i in range(n):
        estado, dur = "solteiro", 0
        for t in range(FIM_28 + 1):
            f = 1.1 if t >= t_est[i] else fator_social   # com cargo, todo mundo relaxa um pouco
            if estado == "solteiro":
                if rng.random() < 0.045 * f:
                    estado, dur = ("serio" if rng.random() < 0.35 else "casual"), 0
            else:
                dur += 1
                fim = 0.015 if estado == "serio" else 0.20
                if rng.random() < fim:
                    estado = "solteiro"
        firme[i] = estado == "serio" and dur >= 24
    return firme.mean()

# ------------------------------------------------------------------ 3. empreender
def empreender_no_lugar(n=100000):
    """Abre negócio em 2027 (com ~R$ 15 mil) em vez de estudar para concurso."""
    renda25, renda28 = np.zeros(n), np.zeros(n)
    for i in range(n):
        r = rng.random()
        if r < 0.55:      # fecha em até 3 anos; volta ao mercado como analista júnior
            renda25[i], renda28[i] = 2500, 4500
        elif r < 0.85:    # sobrevive pequeno
            renda25[i], renda28[i] = rng.uniform(2000, 5000), rng.uniform(3000, 8000)
        elif r < 0.97:    # cresce
            renda25[i], renda28[i] = rng.uniform(5000, 12000), rng.uniform(8000, 25000)
        else:             # estoura
            renda25[i], renda28[i] = rng.uniform(10000, 30000), rng.uniform(25000, 80000)
    return (renda25 >= 8000).mean(), (renda28 >= 18000).mean(), (renda28 >= 40000).mean()

if __name__ == "__main__":
    print("=== 1. ESTÁGIO (adesão 65%) ===")
    cab()
    for nome, c in ESTAGIO.items():
        linha(nome, simular(c, adesao=0.65, n=N_V))
    print()

    print("=== 2. VIDA SOCIAL até passar no nível médio (adesão base 65%) ===")
    print(f"  {'':58s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} {'namoro firme 2+ anos aos 28':>28s}")
    for nome, (c, f) in SOCIAL.items():
        r = simular(c, adesao=0.65, n=N_V)
        p = namoro(f, r["idade_estavel"], 4000)
        print(f"  {nome:58s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} {p:28.0%}")
    print()

    print("=== 3. EMPREENDEDORISMO ===")
    a25, a28, a40 = empreender_no_lugar()
    print(f"  Empreender NO LUGAR do concurso (2027):  ≥8k até 25: {a25:.0%}   ≥18k até 28: {a28:.0%}"
          f"   ≥40k aos 28: {a40:.1%}")
    r = simular(com(A, h_sem_trabalhando=12), adesao=0.65, n=N_V)
    extra = (rng.random(N_V) < 0.30) * rng.uniform(1000, 3000, N_V)
    print(f"  Escada + negócio paralelo DEPOIS do cargo (4h/sem):  ≥8k até 25: "
          f"{r['estavel8k_25'].mean():.0%}   ≥18k até 28: {r['top18k_28'].mean():.0%}"
          f"   renda extra média aos 28: R$ {extra.mean():.0f}/mês")
