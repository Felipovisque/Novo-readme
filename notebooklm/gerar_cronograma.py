"""Gera 03_CRONOGRAMA_DIARIO.md (26/11/2026 a 17/01/2027).
    python3 notebooklm/gerar_cronograma.py
"""
import datetime as dt
import os

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
Q = "QConcursos/TEC → banca **FCC**, escolaridade **nível médio**, assunto: "

def estudo(assunto, video, qassunto, n=20, extra=None):
    d = {
        "manha": [f"📖 **P1** (resumo) de **{assunto}** → leia e marque o que não entendeu",
                  f"🎬 Videoaula (YouTube): busque *\"{video}\"* → assista 1 aula (até 1h, em 1,5x)",
                  f"🎧 **P4** (áudio) de {assunto} → ouça no carro ou na academia"],
        "noite": [f"✍️ **{n} questões** — {Q}*{qassunto}*",
                  "❌ Errou? **P6** + uma linha no caderno de erros"],
    }
    if extra:
        d["extra"] = extra
    return d

C = {}
def dia(data, titulo, **kw):
    C[data] = dict(titulo=titulo, **kw)

d = dt.date
# ---------------- Semana 1
dia(d(2026, 11, 26), "Logística + Legislação Institucional (1ª leitura)",
    manha=["📋 Peça o **recesso de 05 a 16/01** no cartório; veja o local da prova da Transpetro (6/12)",
           "✈️ Pesquise e, se der, compre **passagem e hotel para Goiânia** (ida 16/01)"],
    noite=["📖 **P1** de *Lei Orgânica do TCE-GO*: título I (natureza, competência, jurisdição)",
           "🗂️ **P3** (flashcards) do mesmo trecho → importe no Anki"])
dia(d(2026, 11, 27), "Português FCC: crase e concordância",
    **estudo("crase e concordância verbal/nominal", "crase FCC aula", "Português > crase; concordância"))
dia(d(2026, 11, 28), "DIAGNÓSTICO: prova antiga da FCC",
    manha=["⏱️ Faça uma **prova FCC antiga de nível médio de TCE ou TRT** com tempo (4h), sem consultar nada",
           "📊 Corrija e anote **a nota por matéria**: isso define onde você mais precisa melhorar"],
    noite=["🔁 Tarde: buffer (o que atrasou na semana)"])
dia(d(2026, 11, 29), "RLM: porcentagem, razão e proporção + replanejamento",
    **estudo("porcentagem, razão e proporção", "porcentagem razão proporção FCC aula",
             "Matemática > porcentagem; razão e proporção", 25,
             extra=["17h: **P7** + replanejamento da semana (20 min)", "18h30: igreja ⛪"]))
# ---------------- Semana 2
lic1 = [("princípios e aplicação da Lei 14.133 (arts. 1º a 5º)", "Lei 14.133 princípios aula"),
        ("definições e agentes públicos (arts. 6º a 10)", "Lei 14.133 agentes de contratação aula"),
        ("fases do processo licitatório (art. 17) e fase preparatória", "Lei 14.133 fase preparatória aula"),
        ("modalidades de licitação (arts. 28 a 32)", "Lei 14.133 modalidades aula")]
for i, (a, v) in enumerate(lic1):
    dat = d(2026, 11, 30) + dt.timedelta(days=i)
    if dat == d(2026, 12, 3):
        dia(dat, "Prova antiga da Cesgranrio (treino para a Transpetro)",
            manha=[f"📖 **P1** de *{a}* (30 min)"],
            noite=["⏱️ **1 prova antiga da Cesgranrio de nível médio** (Português + Matemática), com tempo",
                   "❌ Erros → caderno"])
        continue
    dia(dat, f"Licitações I: {a}", **estudo(a, v, "Licitações (Lei 14.133) > " + a.split(" (")[0], 20,
        extra=["✍️ +10 questões de Português FCC (pontuação, regência)"]))
dia(d(2026, 12, 4), "Licitações I: critérios de julgamento + revisão",
    **estudo("critérios de julgamento (art. 33 e seguintes)", "Lei 14.133 critérios de julgamento aula",
             "Licitações > critérios de julgamento", 20))
dia(d(2026, 12, 5), "Véspera da Transpetro: dia leve",
    manha=["🔁 2h: revise o que errou na prova antiga da Cesgranrio"],
    noite=["🎒 Separe: **documento com foto**, caneta preta de tubo transparente, cartão de confirmação",
           "🗺️ Veja o caminho até o local. **Cama cedo, sem GTA**"])
dia(d(2026, 12, 6), "🎯 PROVA TRANSPETRO (treino)",
    manha=["Chegue 1h antes. Português e Matemática primeiro, **sem deixar nada em branco** (zerar um bloco elimina)",
           "Depois, os Conhecimentos Específicos"],
    noite=["📝 Anote o que mais te travou (vale para o TCE-GO)", "18h30: igreja ⛪, se der tempo"])
# ---------------- Semana 3
adm = [("planejamento (estratégico, tático, operacional) e SWOT", "planejamento estratégico FCC aula"),
       ("organização: estruturas organizacionais e departamentalização", "estruturas organizacionais FCC aula"),
       ("direção: liderança e motivação", "liderança motivação teorias FCC aula"),
       ("controle e PDCA", "controle administrativo PDCA FCC aula"),
       ("Gestão de Pessoas: recrutamento, seleção, treinamento e avaliação de desempenho",
        "gestão de pessoas recrutamento seleção FCC aula")]
for i, (a, v) in enumerate(adm):
    dia(d(2026, 12, 7) + dt.timedelta(days=i), f"Adm. Geral / Gestão de Pessoas: {a.split(':')[0]}",
        **estudo(a, v, "Administração Geral > " + a.split(" (")[0], 25,
                 extra=["✍️ +10 questões de Português FCC (orações, coesão)"]))
dia(d(2026, 12, 12), "Buffer + RLM",
    **estudo("raciocínio lógico: proposições e conectivos", "lógica proposicional FCC aula",
             "Raciocínio Lógico > proposições", 20, extra=["🔁 Tarde: buffer"]))
dia(d(2026, 12, 13), "1ª REDAÇÃO + Estatística + revisão",
    manha=["📝 **Redação 1** (tema geral, 20–30 linhas, 50 min cronometrados) → mande para o Claude corrigir",
           "📊 30 min de Estatística 1: média, mediana e moda (P1 com material do CEDERJ)"],
    noite=["17h: **P7** + replanejamento", "18h30: igreja ⛪"])
# ---------------- Semana 4
lic2 = [("contratos administrativos: formalização, duração e garantias", "Lei 14.133 contratos aula"),
        ("alteração, extinção e fiscalização de contratos", "Lei 14.133 alteração contratos aula"),
        ("contratação direta: dispensa e inexigibilidade + sanções", "Lei 14.133 dispensa inexigibilidade aula"),
        ("Contabilidade Pública: PCASP, regimes contábeis e princípios", "contabilidade pública PCASP aula"),
        ("Contabilidade Pública: receita e despesa (estágios)", "receita e despesa pública estágios aula")]
for i, (a, v) in enumerate(lic2):
    dia(d(2026, 12, 14) + dt.timedelta(days=i), a if "Contab" in a else f"Licitações II: {a.split(':')[0]}",
        **estudo(a, v, ("Contabilidade Pública > " if "Contab" in a else "Licitações > ") + a.split(":")[-1].strip(), 20,
                 extra=["✍️ +10 questões de RLM"]))
dia(d(2026, 12, 19), "⏱️ SIMULADO 1 (completo)",
    manha=["70 questões + redação, **4h30 cronometradas** (prova antiga da FCC ou simulado de cursinho)"],
    noite=["📊 Corrija, anote a nota por matéria e mande os erros para o **P6**"])
dia(d(2026, 12, 20), "2ª REDAÇÃO + Estatística",
    manha=["📝 **Redação 2** → Claude corrige", "📊 30 min de Estatística: variância e desvio-padrão"],
    noite=["17h: **P7** + replanejamento", "18h30: igreja ⛪"])
# ---------------- Semana 5 (Natal)
for i in range(3):
    dia(d(2026, 12, 21) + dt.timedelta(days=i), "Semana de Natal: só o bloco da manhã",
        manha=["🔁 1h30: revisão do **caderno de erros** + 20 questões mistas FCC (o que você mais errou no Simulado 1)"],
        noite=["Livre 🎄"])
dia(d(2026, 12, 24), "🎄 LIVRE", manha=["Família, praia, descanso"], noite=["—"])
dia(d(2026, 12, 25), "🎄 LIVRE", manha=["Família, praia, descanso"], noite=["—"])
dia(d(2026, 12, 26), "Buffer + demais específicas do edital",
    manha=["📖 **P1** da 1ª matéria específica que ainda não estudou (confira no edital)"],
    noite=["✍️ 20 questões FCC dessa matéria"])
dia(d(2026, 12, 27), "3ª REDAÇÃO", manha=["📝 **Redação 3** → Claude corrige"],
    noite=["17h: replanejamento", "18h30: igreja ⛪"])
# ---------------- Semana 6 (Réveillon)
for i, nome in enumerate(["demais específicas (matéria A do edital)", "demais específicas (matéria B do edital)",
                          "demais específicas (matéria C) + Legislação Institucional (2ª leitura)"]):
    dia(d(2026, 12, 28) + dt.timedelta(days=i), nome[0].upper() + nome[1:],
        manha=[f"📖 **P1** + 🎬 videoaula: {nome}"],
        noite=["✍️ 20 questões FCC do mesmo assunto + **P5** (pegadinhas)"])
dia(d(2026, 12, 31), "🎆 LIVRE", manha=["Réveillon sem culpa"], noite=["—"])
dia(d(2027, 1, 1), "🎆 LIVRE", manha=["Descanso"], noite=["—"])
dia(d(2027, 1, 2), "Revisão leve", manha=["🔁 1h: caderno de erros + flashcards do Anki"], noite=["Livre"])
dia(d(2027, 1, 3), "⏱️ SIMULADO 2", manha=["70 questões + redação, 4h30 cronometradas"],
    noite=["📊 Correção + **P6**", "18h30: igreja ⛪"])
# ---------------- Semana 7 (recesso)
dia(d(2027, 1, 4), "Último dia de trabalho antes do recesso",
    **estudo("a matéria de pior nota no Simulado 2", "(assunto da pior matéria) FCC aula", "pior matéria do Simulado 2", 25))
integral = [
    ("Ter", "Licitações (tudo) + Legislação Institucional", "Redação 4 à noite"),
    ("Qua", "Contabilidade Pública + Adm. Geral", None),
    ("Qui", "Gestão de Pessoas + demais específicas", "Redação 5 à noite"),
    ("Sex", "Português FCC (tudo) + RLM", None),
]
for i, (_, mat, red) in enumerate(integral):
    extra = ["📝 " + red + " → Claude corrige"] if red else []
    dia(d(2027, 1, 5) + dt.timedelta(days=i), f"RECESSO (integral): {mat}",
        manha=["6h30–9h30: **P1** + videoaula da matéria mais fraca do dia",
               "10h–12h: **40 questões FCC** da mesma matéria",
               "13h30–15h: **lei seca** (Lei 14.133 + Lei Orgânica) com **P5**"],
        noite=["15h–16h30: academia/natação 🏊", "17h–18h30: Português + RLM (20 questões)"] + extra)
dia(d(2027, 1, 9), "⏱️ SIMULADO 3", manha=["70 questões + redação, 4h30"], noite=["📊 Correção + **P6**"])
dia(d(2027, 1, 10), "Revisão geral",
    manha=["🔁 Caderno de erros inteiro + **P7** (teste de 15 questões)"],
    noite=["17h: replanejamento", "18h30: igreja ⛪"])
# ---------------- Semana 8
dia(d(2027, 1, 11), "Reta final: peso 2 + Redação 6",
    manha=["✍️ 50 questões das matérias de peso 2 (Licitações, Contabilidade, Adm., Gestão de Pessoas)"],
    noite=["📝 **Redação 6** → Claude corrige", "📖 Lei seca: Lei Orgânica (só os destaques)"])
dia(d(2027, 1, 12), "Reta final: lei seca + Português",
    manha=["📖 Lei 14.133: só os artigos que você mais errou + **P5**"], noite=["✍️ 30 questões de Português FCC"])
dia(d(2027, 1, 13), "⏱️ SIMULADO 4 (no horário real da prova)", manha=["70 questões + redação"],
    noite=["📊 Correção rápida: só entender os erros, sem estudar matéria nova"])
dia(d(2027, 1, 14), "Só revisão", manha=["🔁 Caderno de erros + resumos P1 + flashcards"],
    noite=["Nada novo. Descanse"])
dia(d(2027, 1, 15), "Dia leve", manha=["1h–2h: destaques do caderno de erros"],
    noite=["🎒 Separe documento, caneta, cartão informativo. Confira o endereço do local de prova"])
dia(d(2027, 1, 16), "✈️ Viagem para Goiânia",
    manha=["Viaje. À tarde, **visite o local da prova**"], noite=["Jantar leve, dormir cedo. Nada de estudo"])
dia(d(2027, 1, 17), "🎯 PROVA DO TCE-GO",
    manha=["Comece pelas **Específicas (peso 2)**", "Reserve **50 min para a redação**, com 5 min de rascunho"],
    noite=["Você fez. Agora descanse uns dias 🙌"])

INGLES = {0: "🇬🇧 Aula de inglês 7h45", 2: "🇬🇧 Aula de inglês 7h45",
          1: "🎧 Inglês no carro (podcast)", 3: "🎧 Inglês no carro (podcast)", 4: "🎧 Inglês no carro (podcast)"}

linhas = ["# Cronograma diário: TCE-GO (26/11/2026 → 17/01/2027)", "",
          "Para cada dia: **o que ler/assistir (manhã)**, **quais exercícios fazer (noite)** e qual prompt do",
          "NotebookLM usar (veja `02_PROMPTS_PRONTOS.md`). **Mínimo de todo dia, mesmo em dia ruim: 20",
          "questões + 15 min de revisão.** Nunca fique dois dias seguidos sem estudar.", "",
          "> Se o curso de inglês entrar em recesso, mantenha só o áudio no carro. Se tiver AP do CEDERJ",
          "> em algum dia, ela vem primeiro.", ""]
semana_atual = None
for data in sorted(C):
    item = C[data]
    sem = data.isocalendar()[1]
    if sem != semana_atual:
        semana_atual = sem
        ini = data - dt.timedelta(days=data.weekday())
        linhas += ["", f"## Semana de {ini:%d/%m} a {ini + dt.timedelta(days=6):%d/%m}", ""]
    wd = data.weekday()
    linhas.append(f"### {DIAS[wd]} {data:%d/%m}: {item['titulo']}")
    for chave, rot in (("manha", "Manhã"), ("noite", "Noite")):
        for x in item.get(chave, []):
            linhas.append(f"- [ ] **{rot}:** {x}")
    for x in item.get("extra", []):
        linhas.append(f"- [ ] {x}")
    if wd in INGLES and "LIVRE" not in item["titulo"] and data < d(2027, 1, 5):
        linhas.append(f"- [ ] {INGLES[wd]}")
    if wd < 5 and data < d(2027, 1, 5) and "LIVRE" not in item["titulo"] and data != d(2026, 12, 24):
        linhas.append("- [ ] 🏋️ Academia/natação 16h30")
    linhas.append("")

saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_CRONOGRAMA_DIARIO.md")
open(saida, "w").write("\n".join(linhas))
print("ok:", saida, len(C), "dias")
