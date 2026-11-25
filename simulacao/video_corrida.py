"""
Vídeo "Quem vai mais longe?": corrida de barras da renda acumulada (mediana)
de cada caminho, mês a mês, dos 22 aos 31 anos.
    python3 simulacao/video_corrida.py      -> simulacao/video/quem_vai_mais_longe.mp4
Precisa de matplotlib e ffmpeg. Números = estimativas do modelo, não previsão.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import simulacao as S
S.MESES = 109                                   # dez/2026 até dez/2035 (~31 anos)
from meu_caso import CEN, com
from carreiras_adm import MERCADO, mercado, CONCURSOS
from ia import PRINCIPAL, renda_ia

N = 4000
ADES = 0.65
H = S.MESES
rng = np.random.default_rng(5)

I1 = CEN["I1) Integral escada híbrida (vira p/ superior 12m antes do diploma)"]
I3 = CEN["I3) Integral direto no superior"]

def serie_concurso(c):
    return S.simular(c, adesao=ADES, n=N, serie=True)["serie"]

def serie_negocio_ia():
    fim = renda_ia(PRINCIPAL, N)                 # renda aos 28 (mês 72)
    t = np.arange(H)
    rampa = np.clip((t - 5) / (72 - 5), 0, None)[None, :] * fim[:, None]
    rampa *= (1.10 ** (np.clip(t - 72, 0, None) / 12))[None, :]
    rampa[:, :5] = 1800                          # estágio até mai/2027
    return rampa

print("Rodando simulações...")
CAMINHOS = [
    ("Escada + IA (22h/sem após a posse)", "#22c55e", serie_concurso(com(I1, eficiencia=1.2, h_sem_trabalhando=22))),
    ("Direto no nível superior + IA", "#3b82f6", serie_concurso(com(I3, eficiencia=1.2))),
    ("Escada sem IA, relaxa após posse", "#a3e635", serie_concurso(I1)),
    ("Plano antigo: estágio + 25h", "#94a3b8", serie_concurso(CEN["Estágio + 25h (plano antigo)"])),
    ("CACD direto (diplomata)", "#eab308", serie_concurso(CONCURSOS["Concurso: CACD (diplomata)"])),
    ("Vendas B2B / SaaS", "#f97316", mercado(MERCADO["Vendas B2B/SaaS (SDR -> executivo de contas)"], ADES, n=N, serie=True, horizonte=H - 1)),
    ("Dados / BI", "#a855f7", mercado(MERCADO["Dados/BI (Excel, SQL, Power BI)"], ADES, n=N, serie=True, horizonte=H - 1)),
    ("Negócio com IA no lugar do concurso", "#ec4899", serie_negocio_ia()),
]

# métricas mês a mês
nomes = [c[0] for c in CAMINHOS]
cores = [c[1] for c in CAMINHOS]
acum = np.array([np.median(np.cumsum(c[2], axis=1), axis=0) for c in CAMINHOS])   # (k, H)
top = np.array([np.mean(c[2] >= 18000, axis=0) for c in CAMINHOS])                 # (k, H)
salmed = np.array([np.median(c[2], axis=0) for c in CAMINHOS])

MESES_PT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
def data(t):
    m = (11 + t) % 12; a = 2026 + (11 + t) // 12
    return f"{MESES_PT[m]}/{a}"

EVENTOS = [(1, "17/jan/2027: prova do TCE-GO"), (5, "mai/2027: fim do estágio → estudo integral"),
           (6, "jul/2027: Estatística 1 aprovada (ou jubilamento)"), (25, "jan/2029: você faz 25 anos"),
           (37, "jan/2030: diploma → libera concursos de nível superior"),
           (61, "jan/2032: você faz 28 anos"), (97, "jan/2035: você faz 31 anos")]

def moeda(v):
    return f"R$ {v/1e6:.2f} mi".replace(".", ",") if v >= 1e6 else f"R$ {v/1e3:.0f} mil"

# ---------------------------------------------------------------- animação
FPS, POR_MES, HOLD = 30, 5, 5 * 30
frames = (H - 1) * POR_MES + HOLD
BG, FG, MUT = "#0b1020", "#e5e7eb", "#94a3b8"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.parse_math": False})
fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=BG)
ax = fig.add_axes([0.285, 0.12, 0.50, 0.68], facecolor=BG)
k = len(CAMINHOS)
ypos = np.argsort(np.argsort(-acum[:, 0])).astype(float)

os.makedirs(os.path.join(os.path.dirname(__file__), "video"), exist_ok=True)
saida = os.path.join(os.path.dirname(__file__), "video", "quem_vai_mais_longe.mp4")
writer = FFMpegWriter(fps=FPS, codec="libx264", bitrate=6000, extra_args=["-pix_fmt", "yuv420p"])

print(f"Renderizando {frames} quadros...")
with writer.saving(fig, saida, dpi=100):
    for f in range(frames):
        tf = min(f / POR_MES, H - 1)
        t0 = int(tf); t1 = min(t0 + 1, H - 1); w = tf - t0
        val = acum[:, t0] * (1 - w) + acum[:, t1] * w
        pt = top[:, t0] * (1 - w) + top[:, t1] * w
        sm = salmed[:, t0] * (1 - w) + salmed[:, t1] * w
        alvo = np.argsort(np.argsort(-val)).astype(float)
        ypos += (alvo - ypos) * 0.18

        ax.clear(); ax.set_facecolor(BG)
        xmax = max(val.max() * 1.08, 50000)
        ax.set_xlim(0, xmax); ax.set_ylim(k - 0.4, -0.6)
        ax.barh(ypos, val, color=cores, height=0.72, zorder=2)
        for i in range(k):
            ax.text(-xmax * 0.012, ypos[i], nomes[i], ha="right", va="center", color=FG,
                    fontsize=16, fontweight="bold")
            ax.text(val[i] + xmax * 0.01, ypos[i] - 0.13, moeda(val[i]), ha="left", va="center",
                    color=FG, fontsize=17, fontweight="bold")
            ax.text(val[i] + xmax * 0.01, ypos[i] + 0.2,
                    f"salário típico {moeda(sm[i])}/mês · {pt[i]:.0%} com ≥ R$ 18 mil",
                    ha="left", va="center", color=MUT, fontsize=12.5)
        ax.tick_params(colors=MUT, labelsize=12, left=False, labelleft=False)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: moeda(x) if x > 0 else "0"))
        ax.grid(axis="x", color="#1f2937", zorder=0)
        for sp in ax.spines.values():
            sp.set_visible(False)

        fig.texts.clear()
        fig.text(0.04, 0.93, "Quem vai mais longe?", color=FG, fontsize=40, fontweight="bold")
        n_txt = f"{N:,}".replace(",", ".")
        fig.text(0.04, 0.885, "Dinheiro acumulado por caminho, dos 22 aos 31 anos  ·  mediana de "
                 + n_txt + " vidas simuladas cada  ·  cumprindo 65% do plano",
                 color=MUT, fontsize=16)
        idade = 22.9 + tf / 12
        fig.text(0.955, 0.25, f"{int(idade)} anos", color=FG, fontsize=60, fontweight="bold",
                 ha="right", alpha=0.9)
        fig.text(0.955, 0.19, data(int(tf)), color=MUT, fontsize=26, ha="right")
        ev = [e for e in EVENTOS if e[0] <= tf]
        if ev:
            fig.text(0.04, 0.045, "▶ " + ev[-1][1], color="#fbbf24", fontsize=19, fontweight="bold")
        fig.text(0.955, 0.045, "Estimativas do modelo — não é previsão", color="#64748b",
                 fontsize=12, ha="right")
        if f >= (H - 1) * POR_MES:
            fig.text(0.5, 0.82, "Aos 31: a escada com IA e sem relaxar ganha mais dinheiro; "
                     "o direto chega primeiro ao salário top",
                     color="#fbbf24", fontsize=19, fontweight="bold", ha="center")
        writer.grab_frame(facecolor=BG)
        if f % 100 == 0:
            print(f"  {f}/{frames}")

print("Final aos 31 anos:")
for i in np.argsort(-acum[:, -1]):
    print(f"  {nomes[i]:46s} {moeda(acum[i, -1]):>14s}   ≥18k: {top[i, -1]:.0%}")
print("Vídeo salvo em", saida)
