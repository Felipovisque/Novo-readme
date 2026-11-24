"""
E se você largar o trabalho e estudar em tempo integral?
    python3 simulacao/integral.py

Rotina integral (a partir de fev/2027, quando você já sairia do cartório):
  seg-sex ~7-8h de estudo + academia todo dia; sáb e dom surf cedo e estudo depois.
  ~43h/semana no total: ~35h de concurso + ~8h de faculdade (CEDERJ/Estatística).
Compara com o caminho recomendado (estágio, 25h/semana de concurso).
"""
import numpy as np
from simulacao import CENARIOS, simular, mes, chance

N_INT = 10000
A = CENARIOS["A*) Escada híbrida (recomendada)"]
C = CENARIOS["C) Direto no nível superior (sem médio)"]
FEV27 = mes(2027, 2)

def com(base, **kw):
    c = dict(base); c.update(kw); return c

CEN = {
    "Base: estágio + 25h/sem (escada híbrida)": A,
    "T1) Integral 35h até o diploma, depois emprego": com(
        A, integral_desde=FEV27, h_sem=35, h_sem_estagio=25),
    "T2) Integral 35h até passar (família banca)": com(
        A, integral_desde=FEV27, h_sem=35, h_sem_estagio=25, apoio_pos_diploma=True),
    "T3) Integral PESADO 45h até passar (família banca)": com(
        A, integral_desde=FEV27, h_sem=45, h_sem_estagio=25, apoio_pos_diploma=True,
        p_mes_ruim=0.12),                       # mais risco de esgotamento
    "T4) Integral 35h direto no SUPERIOR (família banca)": com(
        C, integral_desde=FEV27, h_sem=35, h_sem_estagio=25, apoio_pos_diploma=True),
}

ADESOES = {"55% (sem estrutura)": 0.55, "65%": 0.65, "75%": 0.75, "85%": 0.85}

if __name__ == "__main__":
    print("TCE-GO se largar o cartório JÁ (dez/26) em vez de usar o recesso:")
    for nome, a in ADESOES.items():
        com_rec, sem = 260 * a, 330 * a
        print(f"  {nome:22s} {chance('medio_top', com_rec):.1%} (recesso) vs "
              f"{chance('medio_top', sem):.1%} (largando já)")
    print()
    for nome, c in CEN.items():
        print(nome)
        print(f"  {'adesão':22s} {'≥8k até 25':>10s} {'≥18k até 28':>11s} {'idade estável':>13s} "
              f"{'idade top':>9s} {'jubilado':>8s} {'renda acum. R$ mil':>18s}")
        for na, a in ADESOES.items():
            r = simular(c, adesao=a, n=N_INT)
            ie = np.nanmedian(r["idade_estavel"]) if np.mean(~np.isnan(r["idade_estavel"])) >= .5 else np.nan
            it = np.nanmedian(r["idade_top"]) if np.mean(~np.isnan(r["idade_top"])) >= .5 else np.nan
            print(f"  {na:22s} {r['estavel8k_25'].mean():10.0%} {r['top18k_28'].mean():11.0%} "
                  f"{ie:13.1f} {it:9.1f} {r['jubilado'].mean():8.0%} "
                  f"{np.median(r['renda_acum'])/1000:18.0f}")
        print()
