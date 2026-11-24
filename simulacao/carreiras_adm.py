"""
Mapa de carreiras para quem faz ADMINISTRAÇÃO, com o SEU perfil:
CEDERJ EaD, CR baixo, networking zero, inglês intermediário, família banca estudo,
diploma por volta de jan/2030. Inclui concursos, mercado (vendas, dados, comex...),
Relações Internacionais e o efeito de cada pós-graduação.
    python3 simulacao/carreiras_adm.py
Todos os números são ESTIMATIVAS para comparar caminhos, não previsão.
"""
import numpy as np
from simulacao import CENARIOS, simular, mes, FIM_25, FIM_28

N_C = 8000
rng = np.random.default_rng(2027)
MAI27 = mes(2027, 5)

# ----------------------------------------------------------------- concursos (motor principal)
A, C, D = (CENARIOS[k] for k in ("A*) Escada híbrida (recomendada)",
                                 "C) Direto no nível superior (sem médio)",
                                 "D) CACD puro desde 2027"))
INTEGRAL = dict(integral_desde=MAI27, h_sem=35, h_sem_estagio=25, apoio_pos_diploma=True,
                p_passar_estat=0.93)

def com(base, **kw):
    c = dict(base); c.update(kw); return c

def so(tipos):
    # antes de passar: só o concurso-alvo; depois da posse: continua subindo para o superior top
    return dict(foco=lambda cargo, t, grad: "sup",
                provas=lambda cargo, tipos=tipos: tipos if cargo is None else ["sup_top"])

ALVO = {"estatais": 5, "Administrador": 6, "Chancelaria": 7, "CACD": 4}

CONCURSOS = {
    "Concurso: escada médio -> superior (integral)": com(A, **INTEGRAL),
    "Concurso: direto no superior top (integral)": com(C, **INTEGRAL),
    "Concurso: estatais nível sup. (Petrobras, BB, Caixa, BNDES)": com(C, **INTEGRAL, **so(["estatal_sup"])),
    "Concurso: Administrador federal (univ./órgãos) + sobe depois": com(C, **INTEGRAL, **so(["adm_federal"])),
    "Concurso: Oficial de Chancelaria (Itamaraty)": com(C, **INTEGRAL, **so(["ofchan"])),
    "Concurso: CACD (diplomata)": com(D, **INTEGRAL),
}

# ----------------------------------------------------------------- mercado (modelo próprio)
# prep_h: horas efetivas de preparo antes de procurar vaga | diploma: exige diploma para entrar
# p_ent: chance/mês de entrar depois de pronto (já com penalidade do seu perfil)
# sal0: salário de entrada | g, gsd: crescimento anual médio e incerteza | teto: limite aos 28
# falha: chance/ano de a carreira "travar" e você ir para outra coisa (~R$ 3,5 mil)
# fora: chance de trabalhar fora/remoto em moeda forte até 28, se entrou (com inglês C1)
MERCADO = {
    "Vendas B2B/SaaS (SDR -> executivo de contas)": dict(prep_h=150, diploma=False, p_ent=0.22, sal0=3500, g=0.28, gsd=0.22, teto=30000, falha=0.10, fora=0.18),
    "Assessor de investimentos (vendas + finanças)": dict(prep_h=220, diploma=False, p_ent=0.15, sal0=2500, g=0.30, gsd=0.40, teto=45000, falha=0.18, fora=0.03),
    "Banco privado: gerente comercial/PJ": dict(prep_h=150, diploma=False, p_ent=0.06, sal0=4000, g=0.15, gsd=0.10, teto=18000, falha=0.06, fora=0.02),
    "Dados/BI (Excel, SQL, Power BI)": dict(prep_h=450, diploma=False, p_ent=0.12, sal0=4000, g=0.20, gsd=0.12, teto=22000, falha=0.05, fora=0.15),
    "Comércio exterior / logística internacional": dict(prep_h=220, diploma=False, p_ent=0.12, sal0=3200, g=0.14, gsd=0.08, teto=15000, falha=0.05, fora=0.10),
    "Marketing digital / tráfego / growth": dict(prep_h=250, diploma=False, p_ent=0.15, sal0=3000, g=0.18, gsd=0.20, teto=16000, falha=0.10, fora=0.08),
    "RH / gestão de pessoas": dict(prep_h=100, diploma=False, p_ent=0.12, sal0=3200, g=0.10, gsd=0.06, teto=11000, falha=0.04, fora=0.02),
    "Gestão de projetos / PMO": dict(prep_h=200, diploma=True, p_ent=0.08, sal0=4500, g=0.14, gsd=0.08, teto=16000, falha=0.04, fora=0.05),
    "Trainee de multinacional": dict(prep_h=150, diploma=True, p_ent=0.006, sal0=8500, g=0.18, gsd=0.10, teto=25000, falha=0.03, fora=0.15),
    "Mercado financeiro (banco de investimento, gestora)": dict(prep_h=500, diploma=True, p_ent=0.004, sal0=8000, g=0.25, gsd=0.20, teto=40000, falha=0.08, fora=0.10),
    "RI: ONGs / organismos internacionais / consulados": dict(prep_h=200, diploma=True, p_ent=0.02, sal0=3800, g=0.10, gsd=0.08, teto=14000, falha=0.05, fora=0.20),
    "Academia: mestrado -> doutorado (bolsa CAPES)": dict(prep_h=300, diploma=True, p_ent=0.05, sal0=2100, g=0.10, gsd=0.0, teto=3100, falha=0.02, fora=0.25),
}

# pós-graduação / formação extra: efeito na entrada (x), no salário (x) e no crescimento (+)
POS = {
    "Nenhuma": dict(ent=1.0, sal=1.0, g=0.0, custo=0),
    "Especialização/MBA EaD barata (~R$ 4 mil)": dict(ent=1.05, sal=1.04, g=0.0, custo=4000),
    "MBA presencial de marca (FGV/COPPEAD/Ibmec, ~R$ 50 mil)": dict(ent=1.6, sal=1.10, g=0.02, custo=50000),
    "Certificação da área (CPA-20/CEA, Power BI, PMP, Google Ads...)": dict(ent=1.35, sal=1.05, g=0.01, custo=1500),
    "Curso + prática forte de VENDAS (~100h)": dict(ent=1.25, sal=1.05, g=0.03, custo=1000),
    "Inglês C1 certificado": dict(ent=1.30, sal=1.10, g=0.02, custo=1500, fora=2.0),
    "Pós/mestrado em Relações Internacionais": dict(ent=1.10, sal=1.03, g=0.0, custo=8000),
}
SINERGIA_VENDAS = {"Vendas B2B/SaaS (SDR -> executivo de contas)", "Assessor de investimentos (vendas + finanças)",
                   "Banco privado: gerente comercial/PJ", "Marketing digital / tráfego / growth"}
SINERGIA_RI = {"RI: ONGs / organismos internacionais / consulados", "Comércio exterior / logística internacional"}


def mercado(p, ades, pos=POS["Nenhuma"], nome="", n=N_C):
    ok25, ok28, sal28, fora = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    gm = 1 + (ades - 0.65)                       # disciplina acelera aprendizado e promoções
    ent = pos["ent"]
    if pos is POS["Curso + prática forte de VENDAS (~100h)"] and nome not in SINERGIA_VENDAS:
        ent = 1.05
    if pos is POS["Pós/mestrado em Relações Internacionais"] and nome in SINERGIA_RI:
        ent = 1.6
    for i in range(n):
        grad = mes(2030, 1) + int(rng.normal(0, 5)) + (6 if rng.random() < 0.2 else 0)
        pronto = int(p["prep_h"] / (20 * ades * 4.3))       # ~20h/sem de preparo na área
        inicio = max(pronto, grad if p["diploma"] else 0)
        entrou, sal, t_ent = False, 1800, None
        for t in range(FIM_28 + 1):
            if not entrou:
                if t >= grad:
                    sal = 3000                               # emprego genérico depois do diploma
                if t >= inicio and rng.random() < min(0.9, p["p_ent"] * ent):
                    entrou, t_ent = True, t
                    sal = p["sal0"] * pos["sal"] * np.exp(rng.normal(0, 0.15))
                    fora[i] = rng.random() < min(0.9, p["fora"] * pos.get("fora", 1.0))
            elif (t - t_ent) % 12 == 0 and t > t_ent:
                if rng.random() < p["falha"]:
                    entrou, sal = False, 3500; inicio = 10**9   # carreira travou
                else:
                    sal = min(p["teto"], sal * np.exp(rng.normal(np.log(1 + (p["g"] + pos["g"]) * gm),
                                                                 p["gsd"])))
            if sal >= 8000 and t <= FIM_25:
                ok25[i] = 1
        ok28[i], sal28[i] = sal >= 18000, sal
    return ok25.mean(), ok28.mean(), np.median(sal28), np.percentile(sal28, 90), fora.mean()


if __name__ == "__main__":
    for na, a in {"65%": 0.65, "85%": 0.85}.items():
        print(f"\n=== TODOS OS CAMINHOS (cumprindo {na}) ===")
        print(f"{'Caminho':64s} {'≥8k até 25':>10s} {'≥18k aos 28':>11s} {'salário 28 (med.)':>17s} "
              f"{'top 10% aos 28':>14s} {'fora até 28':>11s}")
        linhas = []
        for nome, c in CONCURSOS.items():
            r = simular(c, adesao=a, n=N_C)
            s28 = r["salario_28"]
            fora = 0.0
            for chave, cod in ALVO.items():
                if chave in nome:
                    print(f"   [{nome}: passou no concurso-alvo até 28 = {np.mean(r['primeiro'] == cod):.0%}]")
            if "Chancelaria" in nome:
                fora = 0.35 * np.mean(r["primeiro"] == 7)   # remoção para o exterior até 28
            linhas.append((nome, r["estavel8k_25"].mean(), np.mean(s28 >= 18000), np.median(s28),
                           np.percentile(s28, 90), fora))
        for nome, p in MERCADO.items():
            linhas.append((nome, *mercado(p, a, nome=nome)))
        for l in sorted(linhas, key=lambda x: -(x[1] + x[2])):
            print(f"{l[0]:64s} {l[1]:10.0%} {l[2]:11.0%} {l[3]:17,.0f} {l[4]:14,.0f} {l[5]:11.0%}")

    print("\n=== EFEITO DAS PÓS-GRADUAÇÕES / FORMAÇÕES EXTRAS (65%) — ≥18k aos 28 | salário mediano ===")
    alvo = ["Vendas B2B/SaaS (SDR -> executivo de contas)", "Dados/BI (Excel, SQL, Power BI)",
            "Comércio exterior / logística internacional", "Trainee de multinacional",
            "RI: ONGs / organismos internacionais / consulados", "Assessor de investimentos (vendas + finanças)"]
    print(f"{'Pós / formação':62s} " + " ".join(f"{x[:14]:>20s}" for x in alvo))
    for np_, pos in POS.items():
        cel = []
        for nome in alvo:
            _, o28, med, _, _ = mercado(MERCADO[nome], 0.65, pos, nome, n=4000)
            cel.append(f"{o28:5.0%} | {med/1000:5.1f}k")
        print(f"{np_:62s} " + " ".join(f"{x:>20s}" for x in cel))
