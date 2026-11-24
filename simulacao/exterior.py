"""
Simulações de ir para fora.
    python3 simulacao/exterior.py

Parte 1: caminhos que combinam exterior + carreira no Brasil (usa o motor de simulacao.py).
Parte 2: emigrar de vez em 2027 (modelo próprio, mais simples).
Todos os números são ESTIMATIVAS para comparar caminhos.
"""
import numpy as np
from simulacao import CENARIOS, simular, mes, FIM_25

N_EXT = 10000
rng = np.random.default_rng(7)
base = CENARIOS["A*) Escada híbrida (recomendada)"]

def com(**kw):
    c = dict(base); c.update(kw); return c

# chance de conseguir bolsa de mestrado (Chevening, Erasmus Mundus, DAAD...) em ~2 tentativas.
# CR 5,5 pesa contra; disciplina alta melhora inglês, carta e experiência.
p_bolsa = lambda a: 0.06 + 0.25 * (a - 0.5)          # 65% -> ~10%; 85% -> ~15%
# mestrado pago em Portugal (~R$ 40-60 mil no total) como alternativa
p_portugal = lambda a: 0.45                            # supõe que você decide ir se não passar cedo

CEN_EXT = {
    "A*) Escada híbrida, só viagens de férias": base,
    "X0) Escada + intercâmbio curto (jan-fev/2028, 8 semanas)": com(
        pausa=(mes(2028, 1), 2, 25000, False)),
    "X1) Gap year Irlanda/WH JÁ (ago/27-jul/28), tranca a faculdade": com(
        pausa=(mes(2027, 8), 12, 45000)),
    "X1b) Gap year/WH DEPOIS do diploma (fev/30-jan/31, ~27 anos)": com(
        pausa=(mes(2030, 2), 12, 45000, False)),
    "X2) Escada + mestrado com BOLSA fora (~26-27 anos)": com(
        mestrado=dict(p=p_bolsa, dur=15, custo=8000)),
    "X3) Escada + mestrado PAGO em Portugal (~26-27 anos)": com(
        mestrado=dict(p=p_portugal, dur=18, custo=60000)),
}

# inglês C1 até o fim dos 25 (estimativa): aulas + áudio no carro vs. 1 ano vivendo em inglês
def p_c1(cen, a):
    if cen.startswith("X1)"):
        return min(0.95, 0.80 + 0.2 * (a - 0.65))
    if cen.startswith("X0"):
        return min(0.90, 0.40 + 0.9 * (a - 0.65))
    return min(0.90, 0.30 + 0.9 * (a - 0.65))

if __name__ == "__main__":
    for nome_a, a in {"65% (hoje)": 0.65, "85%": 0.85}.items():
        print(f"=== Disciplina {nome_a} ===")
        print(f"{'Cenário':62s} {'temporada fora':>10s} {'C1 até 25':>9s} {'≥8k até 25':>10s} "
              f"{'≥18k até 28':>11s} {'diploma (med.)':>14s} {'renda acum. R$ mil':>18s}")
        for nome, c in CEN_EXT.items():
            r = simular(c, adesao=a, n=N_EXT)
            fora = r["morou_fora"].mean()
            print(f"{nome:62s} {fora:14.0%} {p_c1(nome, a):9.0%} {r['estavel8k_25'].mean():10.0%} "
                  f"{r['top18k_28'].mean():11.0%} {np.median(r['diploma_idade']):14.1f} "
                  f"{np.median(r['renda_acum'])/1000:18.0f}")
        print()

    # ---------------- Parte 2: emigrar de vez ----------------
    print("=== X5) Emigrar de vez em 2027 (sem cidadania europeia) ===")
    n = 100000
    ades = 0.65
    # 1) consegue ficar legalmente além de 2 anos? (troca de visto, estudo superior, empregador)
    fica = rng.random(n) < 0.35
    # 2) termina algum diploma até os 28 (EaD brasileira online ou faculdade lá)
    diploma = rng.random(n) < np.where(fica, 0.40, 0.55)
    # 3) carreira qualificada aos 28 (escritório, salário de classe média local)
    qualificada = fica & diploma & (rng.random(n) < 0.45)
    print(f"  Ainda morando fora legalmente aos 28:       {fica.mean():.0%}")
    print(f"  Com diploma até os 28:                      {diploma.mean():.0%}")
    print(f"  Carreira qualificada fora aos 28:           {qualificada.mean():.0%}")
    print(f"  Volta ao Brasil sem cargo nem diploma:      {((~fica) & (~diploma)).mean():.0%}")
    print()
    print("=== X5b) Emigrar de vez COM cidadania europeia ===")
    fica = rng.random(n) < 0.80
    diploma = rng.random(n) < 0.55
    qualificada = fica & (rng.random(n) < np.where(diploma, 0.55, 0.25))
    print(f"  Ainda morando fora aos 28:                  {fica.mean():.0%}")
    print(f"  Carreira qualificada fora aos 28:           {qualificada.mean():.0%}")
