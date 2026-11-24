"""
Simulação Monte Carlo — Felipe, dos 22 aos 28 anos (dez/2026 a dez/2032).

Cada "vida" simulada anda mês a mês. Em cada mês:
  - você planeja X horas/semana de estudo e cumpre uma fração aleatória
    (média 65%, com meses ruins de vez em quando);
  - podem aparecer concursos; a chance de passar em cada um depende das
    horas EFETIVAS acumuladas naquele tipo de prova;
  - cargos de nível superior e o CACD só contam se você tiver diploma
    a tempo da posse.

Os parâmetros são ESTIMATIVAS (marcadas como tal). Mude-os e rode de novo:
    python3 simulacao/simulacao.py
"""
import numpy as np

N = 20000                     # vidas simuladas por cenário
MESES = 73                    # dez/2026 (mês 0) até dez/2032 (mês 72)
rng = np.random.default_rng(42)

def mes(ano, m):              # índice do mês
    return (ano - 2026) * 12 + (m - 12)

FIM_25 = mes(2029, 12)        # fim dos seus 25 anos
FIM_28 = mes(2032, 12)        # fim dos seus 28 anos
TCE_GO = mes(2027, 1)

# ---------- Parâmetros (estimativas) ----------
ADESAO_MEDIA = 0.65           # você cumpre ~65% do que planeja
P_MES_RUIM = 0.08             # mês de crise (doença, namoro novo, desânimo...)
ADESAO_MES_RUIM = 0.25
SEMANAS_MES = 4.3

# tipo de prova: (concursos/ano ao seu alcance, horas p/ 50% do teto,
#                 dispersão, teto de chance por prova, salário R$/mês)
PROVAS = {
    "medio_top":  (4.0, 1100, 300, 0.22, 10000),  # TCEs, assembleias, câmaras
    "medio_banco": (1.2,  500, 150, 0.45,  5000),  # BB, Caixa, estatais nível médio
    "sup_top":    (5.0, 2800, 600, 0.14, 20000),  # auditor/analista controle, fiscal, Bacen
    "cacd":       (1.0, 5000, 900, 0.20, 22000),  # diplomata (inglês+francês do zero pesam)
}
SALARIO_ESTAGIO = 1800
SALARIO_POS_FORMADO = 3000    # sem cargo e já formado: acabou o estágio, emprego comum
H_SEM_POS_FORMADO = 18        # ...e sobra menos tempo para estudar

def chance(tipo, horas):
    _, h50, s, teto, _ = PROVAS[tipo]
    return teto / (1 + np.exp(-(horas - h50) / s))


def simular(c):
    """c: dicionário com as regras do cenário."""
    res = {k: np.zeros(N) for k in
           ("estavel8k_25", "top18k_28", "diplomata_28", "jubilado", "renda_acum",
            "idade_estavel", "diploma_idade", "fora_28")}
    for i in range(N):
        # --- diploma ---
        jubilado = False
        if c["diploma"] == "cederj":
            if rng.random() > c["p_passar_estat"]:
                jubilado = True
                grad = mes(2027, 7) + int(rng.normal(30, 6))   # recomeça em EaD privada
            else:
                grad = mes(2030, 1) + int(rng.normal(0, 5))
                if rng.random() < 0.20:
                    grad += 6                                   # mais um atraso
        else:  # EaD privada com aproveitamento de disciplinas
            grad = mes(2029, 1) + int(rng.normal(0, 4))
        grad = max(grad, 3)

        h = {"medio": c.get("horas_iniciais", 0.0), "sup": 0.0, "cacd": 0.0}
        cargo, salario, renda = None, SALARIO_ESTAGIO, 0.0
        t_estavel = None
        mercado_trainee = False

        for t in range(MESES):
            # ---------- mercado ----------
            if c["trilha"] == "mercado":
                if t == grad:
                    mercado_trainee = rng.random() < 0.20
                    salario = 9000 if mercado_trainee else 5500
                elif t > grad and (t - grad) % 12 == 0:
                    salario *= 1.18 if mercado_trainee else 1.12
                if t >= grad and salario >= 8000 and t_estavel is None:
                    t_estavel = t
                renda += salario
                continue

            # ---------- estudo do mês ----------
            ades = ADESAO_MES_RUIM if rng.random() < P_MES_RUIM else \
                rng.beta(ADESAO_MEDIA * 10, (1 - ADESAO_MEDIA) * 10)
            if cargo:
                planejado = c["h_sem_trabalhando"]
            elif t >= grad:
                planejado = min(c["h_sem"], H_SEM_POS_FORMADO)
                salario = SALARIO_POS_FORMADO
            else:
                planejado = c["h_sem"]
            efetivo = planejado * ades * SEMANAS_MES

            foco = c["foco"](cargo, t, grad)
            h[foco] += efetivo
            if foco == "medio":
                h["sup"] += c.get("sobreposicao", 0.5) * efetivo      # parte do conteúdo serve depois
            if foco == "sup":
                h["cacd"] += 0.3 * efetivo

            # ---------- provas do mês ----------
            tipos = []
            if t == TCE_GO:
                tipos.append(("medio_top", 1))
            elif t > TCE_GO:
                for tipo in c["provas"](cargo):
                    n = rng.poisson(PROVAS[tipo][0] / 12)
                    if n:
                        tipos.append((tipo, n))
            for tipo, n in tipos:
                exige_diploma = tipo in ("sup_top", "cacd")
                if exige_diploma and grad > t + 9:
                    continue                    # não teria diploma na posse
                horas = {"medio_top": h["medio"], "medio_banco": h["medio"],
                         "sup_top": h["sup"], "cacd": h["cacd"]}[tipo]
                for _ in range(n):
                    if rng.random() < chance(tipo, horas):
                        novo = PROVAS[tipo][4]
                        if novo > (salario if cargo else 0):
                            cargo, posse = tipo, t + (3 if tipo != "cacd" else 6)
                            salario_futuro = novo
                        break

            if cargo and t >= posse:
                salario = salario_futuro
                if t_estavel is None and salario >= 8000:
                    t_estavel = t
            renda += salario

        res["estavel8k_25"][i] = t_estavel is not None and t_estavel <= FIM_25
        res["top18k_28"][i] = salario >= 18000 or (cargo in ("sup_top", "cacd"))
        res["diplomata_28"][i] = cargo == "cacd"
        res["jubilado"][i] = jubilado
        res["renda_acum"][i] = renda
        res["idade_estavel"][i] = 22.9 + t_estavel / 12 if t_estavel is not None else np.nan
        res["diploma_idade"][i] = 22.9 + grad / 12
        res["fora_28"][i] = (c["trilha"] == "mercado" and
                             rng.random() < (0.10 if mercado_trainee else 0.02))
    return res


# ---------- Cenários ----------
def foco_escada(cargo, t, grad):
    return "medio" if cargo is None else "sup"

def provas_escada(cargo):
    return ["medio_top", "medio_banco", "sup_top"] if cargo is None else ["sup_top"]

def foco_hibrido(cargo, t, grad):
    # nível médio só até 12 meses antes do diploma; depois, tudo no superior
    return "medio" if (cargo is None and t < grad - 12) else "sup"

def provas_hibrido(cargo):
    return ["medio_top", "medio_banco", "sup_top"] if cargo is None else ["sup_top"]

CENARIOS = {
    "A*) Escada híbrida (recomendada)": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.88,
        h_sem=25, h_sem_trabalhando=16, horas_iniciais=170, sobreposicao=0.65,
        foco=foco_hibrido, provas=provas_hibrido),
    "B*) Escada híbrida + diploma acelerado": dict(
        trilha="concurso", diploma="privada", p_passar_estat=1.0,
        h_sem=25, h_sem_trabalhando=16, horas_iniciais=170, sobreposicao=0.65,
        foco=foco_hibrido, provas=provas_hibrido),
    "A) Escada: nível médio -> superior (CEDERJ)": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.88,
        h_sem=25, h_sem_trabalhando=14, horas_iniciais=170,
        foco=foco_escada, provas=provas_escada),
    "B) Escada + diploma acelerado (EaD privada)": dict(
        trilha="concurso", diploma="privada", p_passar_estat=1.0,
        h_sem=25, h_sem_trabalhando=14, horas_iniciais=170,
        foco=foco_escada, provas=provas_escada),
    "C) Direto no nível superior (sem médio)": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.88,
        h_sem=25, h_sem_trabalhando=14, horas_iniciais=170,
        foco=lambda cargo, t, grad: "sup",
        provas=lambda cargo: ["sup_top"]),
    "D) CACD puro desde 2027": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.80,
        h_sem=25, h_sem_trabalhando=14, horas_iniciais=170,
        foco=lambda cargo, t, grad: "cacd",
        provas=lambda cargo: ["cacd"]),
    "E) Escada + Direito Ibmec junto": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.80,
        h_sem=15, h_sem_trabalhando=8, horas_iniciais=170,
        foco=foco_escada, provas=provas_escada),
    "F) Mercado (estágio -> trainee/analista)": dict(
        trilha="mercado", diploma="cederj", p_passar_estat=0.85,
        h_sem=0, h_sem_trabalhando=0,
        foco=None, provas=None),
    "G) Escada, mas sem levar Estatística a sério": dict(
        trilha="concurso", diploma="cederj", p_passar_estat=0.65,
        h_sem=25, h_sem_trabalhando=14, horas_iniciais=170,
        foco=foco_escada, provas=provas_escada),
}

if __name__ == "__main__":
    print(f"{'Cenário':48s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} "
          f"{'Diplomata':>9s} {'Jubilado':>8s} {'Idade estável (mediana)':>23s} "
          f"{'Diploma (mediana)':>17s} {'Renda acum. R$ mil':>18s}")
    for nome, c in CENARIOS.items():
        r = simular(c)
        ida = np.nanmedian(r["idade_estavel"]) if np.any(~np.isnan(r["idade_estavel"])) else float("nan")
        sem = np.mean(np.isnan(r["idade_estavel"]))
        print(f"{nome:48s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
              f"{r['diplomata_28'].mean():9.1%} {r['jubilado'].mean():8.0%} "
              f"{ida:16.1f} ({sem:.0%} nunca) {np.median(r['diploma_idade']):17.1f} "
              f"{np.median(r['renda_acum'])/1000:18.0f}")
