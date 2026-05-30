import json
import os

from src.config import REPORTS_DIR

REPORTS = [
    {
        "report_id": "GEN-2026-0001",
        "patient_name": "Ana Carolina Silva",
        "patient_id": "PAC-001",
        "birth_date": "1971-08-22",
        "exam_metadata": {
            "exam_type": "Painel Genomico Completo — Genera Premium",
            "exam_date": "2026-03-15",
            "collection_location": "Unidade Dasa — Av. Paulista, 2200 — Sao Paulo, SP",
            "laboratory_name": "Dasa Genomica",
            "laboratory_unit": "GeneOne — NTO Genomica SP",
            "protocol_number": "DAS-GEN-2026-001547",
            "responsible_physician": "Dr. Ricardo Mendes — CRM-SP 84.321",
            "technical_responsible": "Dra. Patricia Nogueira — CRBM 12.345"
        },
        "suggested_next_exam": {
            "date": "2027-03-15",
            "reason": "Reavaliacao anual do perfil genetico conforme protocolo Genera. Acompanhamento de marcadores de predisposicao metabolica e atualizacao de variantes farmacogeneticas.",
            "priority": "recomendado"
        },
        "complementary_exams": [
            {
                "name": "Hemoglobina Glicada (HbA1c)",
                "code": "TUSS 40302468",
                "reason": "Risco genetico aumentado para Diabetes Mellitus Tipo 2 (TCF7L2 rs7903146)",
                "frequency": "A cada 6 meses",
                "urgent": False
            },
            {
                "name": "Anti-Transglutaminase IgA (tTG-IgA)",
                "code": "TUSS 40304177",
                "reason": "Alelos HLA-DQ2 associados a maior predisposicao para Doenca Celiaca",
                "frequency": "Triagem inicial — repetir se sintomatico",
                "urgent": False
            },
            {
                "name": "Perfil Lipidico Completo",
                "code": "TUSS 40301470",
                "reason": "Monitoramento metabolico complementar — avaliacao cardiovascular",
                "frequency": "Anual",
                "urgent": False
            },
            {
                "name": "Dosagem de Vitamina D (25-OH)",
                "code": "TUSS 40304479",
                "reason": "Avaliacao de micronutrientes — bem-estar geral",
                "frequency": "Anual",
                "urgent": False
            }
        ],
        "sections": {
            "ancestralidade": {
                "title": "Composicao Ancestral",
                "description": "Estimativa da sua composicao ancestral com base em marcadores geneticos (AIMs — Ancestry Informative Markers) distribudos pelo genoma. Comparacao com paineis de referencia das 1000 Genomes e HapMap.",
                "data": {
                    "europeu": {"percentage": 68.2, "regioes": ["Iberica", "Norte da Europa", "Mediterranea"]},
                    "africano": {"percentage": 18.7, "regioes": ["Africa Ocidental", "Norte da Africa"]},
                    "indigena_americano": {"percentage": 9.4, "regioes": ["America do Sul — regiao Amazonica"]},
                    "asiatico": {"percentage": 3.1, "regioes": ["Leste Asiatico"]},
                    "judeu_ashkenazi": {"percentage": 0.6, "regioes": ["Europa Oriental"]}
                },
                "interpretation": "Sua ancestralidade e predominantemente europeia (68,2%), com contribuicoes significativas africanas (18,7%) e indigenas (9,4%). Esse perfil e tipico de populacoes do Sudeste brasileiro, refletindo a miscigenacao historica da regiao. A presenca de tracos judeus ashkenazi (0,6%) e um achado comum em brasileiros com ascendencia europeia.",
                "clinical_example": "A composicao ancestral e estimada comparando seu DNA com populacoes de referencia. Imagine que seu genoma e como um mosaico de pequenos trechos de DNA, cada um com 'assinaturas' tipicas de diferentes regioes do mundo. O algoritmo identifica a origem mais provavel de cada trecho e calcula as porcentagens. A margem de confianca e de aproximadamente 95%."
            },
            "predisposicao_doencas": {
                "title": "Predisposicao Genetica a Doencas",
                "description": "Analise de variantes geneticas (SNPs) associadas ao risco de desenvolvimento de condicoes de saude. ATENCAO: risco genetico nao e diagnostico — fatores ambientais, estilo de vida e historico familiar tambem sao determinantes.",
                "data": [
                    {
                        "condition": "Diabetes Mellitus Tipo 2",
                        "gene": "TCF7L2",
                        "variant": "rs7903146 (C/T)",
                        "risk_level": "risco aumentado",
                        "risk_score": 14,
                        "details": "Voce possui a variante no gene TCF7L2 associada a um risco 1,4x maior de desenvolver diabetes tipo 2 em comparacao com a populacao geral. O gene TCF7L2 regula a secrecao de insulina pelo pancreas. Pessoas com esta variante podem se beneficiar de monitoramento glicemico regular e habitos alimentares equilibrados.",
                        "clinical_example": "Pacientes com perfil genetico similar ao seu que adotaram dieta mediterranea e atividade fisica 3x/semana reduziram o risco em ate 30% segundo o Diabetes Prevention Program (DPP). Isso mostra que a genetica nao e destino — seus habitos fazem muita diferenca.",
                        "prevalence_general": "~10% da populacao brasileira",
                        "your_estimated_risk": "~14% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Doenca Celiaca",
                        "gene": "HLA-DQ2 / HLA-DQ8",
                        "variant": "HLA-DQ2.5",
                        "risk_level": "risco aumentado",
                        "risk_score": 3,
                        "details": "Voce e portadora dos alelos HLA-DQ2, associados a maior predisposicao para doenca celiaca. A presenca desses alelos nao significa que voce desenvolvera a condicao — apenas cerca de 3% das pessoas com esses marcadores a desenvolvem. O diagnostico requer exames clinicos e biopsia intestinal.",
                        "clinical_example": "Uma em cada 30 pessoas com alelos HLA-DQ2 desenvolve doenca celiaca. Os sintomas podem incluir desconforto abdominal, diarreia, perda de peso ou anemia. Se voce apresentar sintomas persistentes, converse com seu medico sobre a possibilidade de investigacao.",
                        "prevalence_general": "~1% da populacao",
                        "your_estimated_risk": "~3% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Cancer de Mama",
                        "gene": "BRCA1 / BRCA2",
                        "variant": "Nao detectada",
                        "risk_level": "risco tipico",
                        "risk_score": 12,
                        "details": "Nao foram detectadas variantes patogenicas nos genes BRCA1 e BRCA2. Seu risco genetico para cancer de mama e considerado tipico da populacao. Mantenha acompanhamento ginecologico regular conforme recomendacao medica (mamografia a partir dos 40 anos).",
                        "clinical_example": "A ausencia de variantes nos genes BRCA e uma boa noticia. A maioria dos casos de cancer de mama (cerca de 90%) nao esta relacionada a mutacoes hereditarias nesses genes, mas sim a fatores hormonais, ambientais e de estilo de vida.",
                        "prevalence_general": "~12% ao longo da vida",
                        "your_estimated_risk": "~12% (risco populacional tipico)"
                    },
                    {
                        "condition": "Hipertensao Arterial",
                        "gene": "AGT",
                        "variant": "rs699 (A/G)",
                        "risk_level": "risco tipico",
                        "risk_score": 25,
                        "details": "Voce nao possui as variantes de risco mais comuns no gene AGT. Seu perfil genetico sugere risco populacional tipico para hipertensao. Fatores como dieta rica em sodio, sedentarismo e estresse sao os principais contribuintes modificaveis.",
                        "clinical_example": "A hipertensao atinge 1 em cada 4 brasileiros adultos. A genetica contribui, mas os principais fatores sao o consumo excessivo de sal, sedentarismo, obesidade e estresse. Reduzir o sal para menos de 5g/dia (1 colher de cha) ja reduz significativamente o risco.",
                        "prevalence_general": "~25% da populacao adulta brasileira",
                        "your_estimated_risk": "~25% (risco populacional tipico)"
                    }
                ]
            },
            "bem_estar": {
                "title": "Bem-Estar e Caracteristicas Pessoais",
                "description": "Tracos geneticos que influenciam aspectos do seu dia a dia, metabolismo e resposta a nutrientes. Estas informacoes complementam sua jornada de autoconhecimento.",
                "data": [
                    {
                        "trait": "Intolerancia a Lactose",
                        "gene": "MCM6 / LCT",
                        "variant": "rs4988235 (G/G)",
                        "result": "Provavel intolerancia a lactose na idade adulta",
                        "details": "Seu genotipo G/G esta associado a reducao da producao de lactase na vida adulta, o que pode causar desconforto ao consumir leite e derivados. Aproximadamente 50% dos brasileiros tem essa caracteristica. Produtos sem lactose ou enzima lactase suplementar podem ajudar.",
                        "clinical_example": "Pense na lactase como uma 'tesoura' que quebra o acucar do leite (lactose). Na infancia, quase todo mundo produz essa tesoura. Na idade adulta, pessoas com seu perfil produzem menos. E como se a tesoura ficasse 'cega' com o tempo. Leites sem lactose ja vem com o acucar pre-quebrado."
                    },
                    {
                        "trait": "Metabolismo de Cafeina",
                        "gene": "CYP1A2",
                        "variant": "rs762551 (C/C)",
                        "result": "Metabolizador lento de cafeina",
                        "details": "Voce possui a variante associada ao metabolismo mais lento da cafeina. Isso significa que a cafeina permanece mais tempo no seu organismo, podendo aumentar a sensacao de alerta prolongada, mas tambem pode afetar a qualidade do sono se consumida a tarde ou noite.",
                        "clinical_example": "Para metabolizadores lentos, o efeito de uma xicara de cafe as 15h pode durar ate 8 horas. Se voce tem dificuldade para dormir, experimente tomar seu ultimo cafe ate as 13h. Cada pessoa e unica — observe como seu corpo reage."
                    },
                    {
                        "trait": "Tipo de Fibra Muscular",
                        "gene": "ACTN3",
                        "variant": "rs1815739 (C/T)",
                        "result": "Perfil misto de fibras musculares",
                        "details": "Voce possui uma copia funcional do gene ACTN3 (alfa-actinina-3), associado a fibras musculares de contracao rapida, e uma copia nao funcional. Esse perfil misto e comum (presente em ~40% da populacao) e sugere boa adaptabilidade tanto para exercicios de resistencia quanto de explosao.",
                        "clinical_example": "Fibras de contracao rapida ajudam em sprints e levantamento de peso. Fibras de contracao lenta favorecem corridas longas e natacao. Com seu perfil misto, voce tem versatilidade — pode se dar bem em diversos tipos de exercicio."
                    },
                    {
                        "trait": "Sensibilidade ao Sal",
                        "gene": "ACE",
                        "variant": "rs4343 (A/G)",
                        "result": "Sensibilidade moderada ao sodio",
                        "details": "Seu perfil genetico sugere sensibilidade moderada ao sal, o que significa que o consumo elevado de sodio pode ter um impacto maior na sua pressao arterial. A recomendacao geral de ate 5g de sal por dia e especialmente relevante para voce.",
                        "clinical_example": "O sodio age como uma 'esponja' que retem agua no corpo, aumentando o volume de sangue e a pressao nas arterias. Em pessoas sensiveis ao sal, esse efeito e mais pronunciado. Trocar parte do sal por temperos naturais (alho, cebola, ervas) e uma estrategia simples e eficaz."
                    }
                ]
            },
            "farmacogenetica": {
                "title": "Farmacogenetica — Resposta a Medicamentos",
                "description": "Analise de genes que influenciam como seu organismo processa (metaboliza) determinados medicamentos. Estas informacoes podem auxiliar seu medico na escolha de tratamentos mais adequados e na definicao de doses personalizadas. ATENCAO: nunca altere sua medicacao sem orientacao medica.",
                "data": [
                    {
                        "drug": "Varfarina (anticoagulante)",
                        "genes": "CYP2C9, VKORC1",
                        "result": "Metabolizadora normal — dose padrao esperada",
                        "details": "Seu perfil sugere resposta normal a varfarina. A dose padrao conforme protocolo clinico e provavelmente adequada, mas o monitoramento de INR (exame de coagulacao) e sempre necessario.",
                        "clinical_example": "A varfarina e um anticoagulante usado para prevenir tromboses. A dose correta varia muito entre pessoas. Seu perfil indica que voce provavelmente responde a dose padrao, mas apenas o exame de INR pode confirmar."
                    },
                    {
                        "drug": "Clopidogrel (antiagregante plaquetario)",
                        "gene": "CYP2C19",
                        "variant": "*1/*1 (metabolizador normal)",
                        "result": "Resposta normal esperada",
                        "details": "Voce possui alelos funcionais do gene CYP2C19, indicando metabolizacao normal do clopidogrel em seu metabolito ativo. A eficacia esperada do medicamento e a padrao.",
                        "clinical_example": "O clopidogrel e um 'protetor de vasos' usado apos infarto ou stent. Ele precisa ser ativado pelo figado para funcionar. Pessoas com seu perfil genetico fazem essa ativacao de forma eficiente."
                    },
                    {
                        "drug": "Estatinas (colesterol)",
                        "gene": "SLCO1B1",
                        "variant": "rs4149056 (T/T)",
                        "result": "Baixo risco de miopatia (dor muscular)",
                        "details": "Voce nao possui a variante associada ao aumento do risco de efeitos musculares adversos com estatinas. O risco de miopatia induzida por estatinas e considerado baixo.",
                        "clinical_example": "Algumas pessoas sentem dores musculares ao tomar estatinas. Isso pode ter causa genetica. Seu perfil indica baixo risco para esse efeito colateral, mas qualquer sintoma deve ser reportado ao medico."
                    },
                    {
                        "drug": "Omeprazol (refluxo gastrico)",
                        "gene": "CYP2C19",
                        "variant": "*1/*1 (metabolizador normal)",
                        "result": "Metabolizacao normal",
                        "details": "Seu organismo processa o omeprazol de forma eficiente. A dose padrao e provavelmente adequada para controle de sintomas de refluxo.",
                        "clinical_example": "O omeprazol reduz a producao de acido no estomago. Pessoas que metabolizam rapido podem precisar de doses maiores. Voce tem metabolizacao normal, entao a dose padrao deve funcionar bem."
                    }
                ]
            },
            "portador_condicoes_recessivas": {
                "title": "Status de Portador — Condicoes Recessivas",
                "description": "Analise de variantes associadas a doencas geneticas de heranca recessiva. Ser portador significa que voce possui uma copia da variante, mas NAO desenvolve a condicao. Se seu parceiro(a) tambem for portador(a) da MESMA condicao, ha 25% de chance de um filho(a) desenvolver a doenca.",
                "data": [
                    {
                        "condition": "Fibrose Cistica",
                        "gene": "CFTR",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas variantes patogenicas no gene CFTR. A fibrose cistica e uma doenca que afeta pulmoes e sistema digestivo.",
                        "clinical_example": "A fibrose cistica e uma das doencas geneticas recessivas mais comuns. Cerca de 1 em cada 25 pessoas de ascendencia europeia e portadora. Voce nao e portadora das variantes testadas."
                    },
                    {
                        "condition": "Anemia Falciforme",
                        "gene": "HBB",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas variantes associadas a anemia falciforme ou traco falciforme. Esta condicao e mais comum em populacoes de ascendencia africana.",
                        "clinical_example": "O traco falciforme confere protecao contra malaria, razao pela qual e mais comum em regioes onde a doenca e endemica. Voce nao possui essa variante."
                    },
                    {
                        "condition": "Atrofia Muscular Espinhal (AME)",
                        "gene": "SMN1",
                        "status": "Portadora",
                        "details": "Voce e portadora de uma delecao no gene SMN1. Isso nao afeta sua saude, mas e uma informacao relevante para planejamento familiar. Cerca de 1 em cada 50 pessoas e portadora. Recomenda-se que seu parceiro tambem realize o teste de portador para AME.",
                        "clinical_example": "Ser portador e como ter um 'manual de instrucoes' com uma pagina faltando, mas ainda ter outra copia completa do manual. Voce nao tem sintomas, mas pode passar a copia alterada para seus filhos. Se seu parceiro nao for portador, nao ha risco para os filhos."
                    },
                    {
                        "condition": "Hemocromatose Hereditaria",
                        "gene": "HFE",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas as variantes principais (C282Y, H63D) no gene HFE. Esta condicao causa acumulo excessivo de ferro no organismo e e mais comum em pessoas de ascendencia europeia.",
                        "clinical_example": "A hemocromatose e chamada de 'doenca do excesso de ferro'. O corpo absorve mais ferro do que precisa, o que pode danificar orgaos ao longo do tempo. Voce nao possui as variantes de risco."
                    }
                ]
            }
        }
    },
    {
        "report_id": "GEN-2026-0002",
        "patient_name": "Rafael dos Santos Oliveira",
        "patient_id": "PAC-002",
        "birth_date": "1984-03-11",
        "exam_metadata": {
            "exam_type": "Painel Genomico Completo — Genera Premium",
            "exam_date": "2026-03-20",
            "collection_location": "Unidade Dasa — Av. Brasil, 1500 — Rio de Janeiro, RJ",
            "laboratory_name": "Dasa Genomica",
            "laboratory_unit": "GeneOne — NTO Genomica RJ",
            "protocol_number": "DAS-GEN-2026-001598",
            "responsible_physician": "Dra. Claudia Andrade — CRM-RJ 52.789",
            "technical_responsible": "Dr. Marcos Teixeira — CRBM 15.678"
        },
        "suggested_next_exam": {
            "date": "2027-03-20",
            "reason": "Reavaliacao anual do perfil genetico. Atencao especial ao perfil de risco cardiovascular e funcao renal, considerando os achados de predisposicao a hipertensao e doenca renal cronica.",
            "priority": "recomendado"
        },
        "complementary_exams": [
            {
                "name": "Monitorizacao Ambulatorial da Pressao Arterial (MAPA 24h)",
                "code": "TUSS 40301969",
                "reason": "Risco genetico aumentado para hipertensao (AGT rs699 + CYP11B2 rs1799998)",
                "frequency": "Anual",
                "urgent": False
            },
            {
                "name": "Creatinina + Microalbuminuria",
                "code": "TUSS 40301144 + 40301187",
                "reason": "Genotipo APOL1 G1/G1 — risco aumentado de doenca renal cronica",
                "frequency": "A cada 6 meses",
                "urgent": False
            },
            {
                "name": "Hemoglobina Glicada (HbA1c)",
                "code": "TUSS 40302468",
                "reason": "Homozigoto TCF7L2 rs7903146 (T/T) — risco ~2x Diabetes Tipo 2",
                "frequency": "A cada 6 meses",
                "urgent": False
            },
            {
                "name": "PSA Total + Livre",
                "code": "TUSS 40303677",
                "reason": "Variante HOXB13 rs138213689 (G/A) — risco levemente aumentado de cancer de prostata. Considerar a partir dos 45 anos.",
                "frequency": "Anual (a partir dos 45 anos)",
                "urgent": False
            },
            {
                "name": "Perfil Lipidico Completo",
                "code": "TUSS 40301470",
                "reason": "Avaliacao de risco cardiovascular global",
                "frequency": "Anual",
                "urgent": False
            }
        ],
        "sections": {
            "ancestralidade": {
                "title": "Composicao Ancestral",
                "description": "Estimativa da sua composicao ancestral com base em marcadores geneticos (AIMs) distribudos pelo genoma.",
                "data": {
                    "africano": {"percentage": 54.3, "regioes": ["Africa Ocidental — Golfo da Guine", "Africa Central", "Africa Oriental — Bantu"]},
                    "europeu": {"percentage": 32.1, "regioes": ["Iberica", "Norte da Europa"]},
                    "indigena_americano": {"percentage": 10.8, "regioes": ["America do Sul — Tupi-Guarani"]},
                    "asiatico": {"percentage": 2.3, "regioes": ["Oriente Medio"]},
                    "leste_asiatico": {"percentage": 0.5, "regioes": ["Sudeste Asiatico"]}
                },
                "interpretation": "Sua ancestralidade reflete a rica miscigenacao afro-brasileira, com predominancia africana (54,3%) — especialmente da regiao do Golfo da Guine e Africa Central — combinada com contribuicao europeia (32,1%) e indigena (10,8%). Esse perfil e caracteristico de populacoes com forte heranca da diaspora africana no Brasil.",
                "clinical_example": "Seu genoma conta a historia das migracoes que formaram o Brasil. A alta porcentagem africana reflete a diaspora que trouxe pessoas de diversas regioes da Africa. O algoritmo compara trechos do seu DNA com bancos de referencia de populacoes atuais dessas regioes."
            },
            "predisposicao_doencas": {
                "title": "Predisposicao Genetica a Doencas",
                "description": "Analise de variantes geneticas (SNPs) associadas ao risco de desenvolvimento de condicoes de saude.",
                "data": [
                    {
                        "condition": "Hipertensao Arterial",
                        "gene": "AGT, CYP11B2",
                        "variant": "rs699 (C/T) + rs1799998 (T/T)",
                        "risk_level": "risco aumentado",
                        "risk_score": 38,
                        "details": "Voce possui variantes nos genes AGT e CYP11B2 associadas a predisposicao elevada para hipertensao arterial, especialmente em combinacao com dieta rica em sodio. O gene AGT regula a producao de angiotensinogenio, precursor da angiotensina que controla a pressao. O CYP11B2 influencia a producao de aldosterona, que regula sal e agua nos rins. Estudos indicam que individuos com esse perfil tem risco aproximadamente 1,7x maior. O monitoramento regular da pressao arterial e a reducao do consumo de sal sao fortemente recomendados.",
                        "clinical_example": "Pense no seu sistema de pressao arterial como um sistema de encanamento. Os genes AGT e CYP11B2 regulam o 'tamanho dos canos' e a 'quantidade de agua'. Suas variantes geneticas fazem com que seus 'canos' tendam a ser mais estreitos sob alta ingestao de sal. Reduzir o sal para menos de 5g/dia (1 colher de cha) e a medida mais eficaz para compensar essa tendencia genetica.",
                        "prevalence_general": "~25% da populacao adulta brasileira",
                        "your_estimated_risk": "~38% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Diabetes Mellitus Tipo 2",
                        "gene": "TCF7L2",
                        "variant": "rs7903146 (T/T)",
                        "risk_level": "risco aumentado",
                        "risk_score": 20,
                        "details": "Voce possui duas copias da variante de risco no gene TCF7L2, o que esta associado a um risco aproximadamente 2x maior de desenvolver diabetes tipo 2. O TCF7L2 controla a secrecao de insulina pelas celulas beta do pancreas. Com duas copias da variante, a producao de insulina pode ser menos eficiente. Este e um fator de risco significativo, mas nao determinante. Manter peso saudavel e praticar atividade fisica regular reduz substancialmente esse risco.",
                        "clinical_example": "Ter duas copias da variante TCF7L2 e como ter um 'motor' de producao de insulina que trabalha com eficiencia reduzida. mas a boa noticia e que exercicio fisico e alimentacao equilibrada sao como uma 'manutencao premium' que pode manter esse motor funcionando bem por muitos anos.",
                        "prevalence_general": "~10% da populacao brasileira",
                        "your_estimated_risk": "~20% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Doenca Renal Cronica",
                        "gene": "APOL1",
                        "variant": "G1/G1 (alto risco)",
                        "risk_level": "risco aumentado",
                        "risk_score": 8,
                        "details": "Voce possui duas copias da variante de alto risco no gene APOL1 (genotipo G1/G1). O gene APOL1 (Apolipoproteina L1) esta envolvido na imunidade inata e protecao contra tripanossomas (doenca do sono). Este perfil, mais comum em populacoes de ascendencia africana, esta associado a maior predisposicao a doenca renal cronica. Recomenda-se acompanhamento da funcao renal (creatinina, microalbuminuria) em check-ups regulares.",
                        "clinical_example": "As variantes G1/G1 no gene APOL1 sao como um 'escudo genetico' contra a doenca do sono que, infelizmente, tem um efeito colateral nos rins. Cerca de 15% das pessoas com esse genotipo desenvolvem algum grau de doenca renal. O monitoramento regular permite detectar alteracoes precocemente.",
                        "prevalence_general": "~3% da populacao",
                        "your_estimated_risk": "~8% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Cancer de Prostata",
                        "gene": "HOXB13, MSMB",
                        "variant": "rs138213689 (G/A)",
                        "risk_level": "risco levemente aumentado",
                        "risk_score": 17,
                        "details": "Voce possui uma variante no gene HOXB13 associada a um risco levemente aumentado de cancer de prostata (OR ~1,3). O gene HOXB13 e um fator de transcricao importante no desenvolvimento da prostata. A partir dos 45 anos, recomenda-se conversar com seu urologista sobre a inclusao do PSA no check-up anual, considerando este fator genetico.",
                        "clinical_example": "O cancer de prostata e o segundo mais comum em homens no Brasil. A presenca desta variante eleva levemente o risco, mas o rastreamento com PSA e toque retal a partir dos 45-50 anos permite detectar alteracoes em fases iniciais, quando o tratamento e mais eficaz.",
                        "prevalence_general": "~13% ao longo da vida",
                        "your_estimated_risk": "~17% (baseado apenas no fator genetico)"
                    }
                ]
            },
            "bem_estar": {
                "title": "Bem-Estar e Caracteristicas Pessoais",
                "description": "Tracos geneticos que influenciam aspectos do seu dia a dia, metabolismo e resposta a nutrientes.",
                "data": [
                    {
                        "trait": "Intolerancia a Lactose",
                        "gene": "MCM6 / LCT",
                        "variant": "rs4988235 (C/C)",
                        "result": "Provavel tolerancia a lactose na idade adulta",
                        "details": "Seu genotipo C/C esta associado a persistencia da producao de lactase, a enzima que digere o acucar do leite. Voce provavelmente tolera bem leite e derivados, caracteristica presente em cerca de 50% dos brasileiros.",
                        "clinical_example": "A persistencia da lactase e uma adaptacao evolutiva relativamente recente, que surgiu em populacoes que domesticavam gado leiteiro. Voce herdou essa caracteristica — seu corpo continua produzindo a enzima que digere o leite na vida adulta."
                    },
                    {
                        "trait": "Metabolismo de Alcool",
                        "gene": "ALDH2",
                        "variant": "rs671 (G/G — atividade normal)",
                        "result": "Metabolizacao normal de alcool",
                        "details": "Voce possui a versao ativa da enzima ALDH2, responsavel por processar o acetaldeido (subproduto toxico do alcool). Seu organismo processa o alcool de forma eficiente, sem os efeitos de rubor facial ou desconforto associados a variantes inativas.",
                        "clinical_example": "Quando voce bebe alcool, seu figado o transforma primeiro em acetaldeido (uma substancia toxica) e depois em acetato (inofensivo). A enzima ALDH2 faz essa segunda etapa. Sua versao ativa faz esse trabalho rapidamente, evitando o acumulo da substancia toxica."
                    },
                    {
                        "trait": "Predisposicao a Obesidade",
                        "gene": "FTO",
                        "variant": "rs9939609 (A/T)",
                        "result": "Risco moderado de obesidade",
                        "details": "Voce possui uma copia da variante no gene FTO associada a maior apetite e tendencia a ganho de peso. Individuos com esse perfil podem se beneficiar de atencao especial a dietas ricas em proteinas e fibras, que promovem maior saciedade.",
                        "clinical_example": "O gene FTO influencia a sensacao de fome e saciedade. Pessoas com a variante A tendem a sentir menos a sensacao de 'estou satisfeito'. Dietas ricas em proteinas (carnes magras, ovos, leguminosas) e fibras (vegetais, graos integrais) ajudam a compensar essa tendencia."
                    },
                    {
                        "trait": "Resposta ao Exercicio",
                        "gene": "PPARGC1A",
                        "variant": "rs8192678 (G/A)",
                        "result": "Boa resposta a exercicios aerobicos",
                        "details": "Seu perfil no gene PPARGC1A esta associado a boa capacidade de melhora do condicionamento cardiorrespiratorio com treinamento aerobico. Exercicios como corrida, natacao e ciclismo tendem a trazer bons resultados para voce.",
                        "clinical_example": "O gene PPARGC1A ajuda a regular como suas celulas produzem energia. Sua variante favorece a adaptacao ao exercicio aerobico. Isso significa que, com treino consistente, seu corpo responde bem — seu folego e resistencia tendem a melhorar significativamente."
                    }
                ]
            },
            "farmacogenetica": {
                "title": "Farmacogenetica — Resposta a Medicamentos",
                "description": "Analise de genes que influenciam como seu organismo processa determinados medicamentos. ATENCAO: nunca altere sua medicacao sem orientacao medica.",
                "data": [
                    {
                        "drug": "Varfarina (anticoagulante)",
                        "genes": "CYP2C9, VKORC1",
                        "result": "Metabolizador lento — dose reduzida recomendada",
                        "details": "Seu perfil nos genes CYP2C9 (*2/*3) e VKORC1 sugere metabolizacao mais lenta da varfarina, com maior sensibilidade ao medicamento. Caso precise usar este anticoagulante, doses iniciais mais baixas e monitoramento cuidadoso de INR sao recomendados.",
                        "clinical_example": "Para voce, a varfarina age como um 'freio mais sensivel'. Doses menores podem ser suficientes para o efeito desejado. Isso e uma informacao valiosa para o medico ajustar a dose inicial e reduzir o risco de sangramentos."
                    },
                    {
                        "drug": "Losartana (anti-hipertensivo)",
                        "gene": "CYP2C9",
                        "variant": "*2/*3 (metabolizador intermediario)",
                        "result": "Eficacia pode ser reduzida",
                        "details": "Voce possui variantes que reduzem a conversao da losartana em seu metabolito ativo. Converse com seu medico sobre a possibilidade de ajuste de dose ou medicamentos alternativos como IECA (enalapril, captopril) ou bloqueadores de canais de calcio (anlodipino).",
                        "clinical_example": "A losartana e um 'pro-farmaco' — ela precisa ser ativada pelo figado para funcionar. Com sua genetica, essa ativacao e parcial. E como ter uma chave que gira com mais dificuldade na fechadura. O medico pode considerar uma 'chave diferente' (outro medicamento) que funcione melhor para voce."
                    },
                    {
                        "drug": "Codeina (analgesico)",
                        "gene": "CYP2D6",
                        "variant": "*1/*4 (metabolizador intermediario)",
                        "result": "Eficacia parcialmente reduzida",
                        "details": "Seu organismo converte codeina em morfina (composto ativo) de forma parcialmente reduzida. O alivio da dor pode ser menor que o esperado com doses padrao. Alternativas como paracetamol, dipirona ou anti-inflamatorios podem ser consideradas sob orientacao medica.",
                        "clinical_example": "Codeina e como um 'remedio em duas etapas': voce toma codeina, e seu figado a transforma em morfina (que alivia a dor). Com seu perfil, essa transformacao e mais lenta, entao o alivio pode ser menor. Avise seu medico se sentir que remedios para dor nao estao fazendo efeito."
                    },
                    {
                        "drug": "Azatioprina (imunossupressor)",
                        "gene": "TPMT",
                        "variant": "*1/*3A (atividade intermediaria)",
                        "result": "Metabolizacao reduzida — risco de toxicidade",
                        "details": "Voce possui uma copia da variante de baixa atividade no gene TPMT. Caso necessite usar azatioprina, doses reduzidas (30-70% da dose padrao) sao recomendadas para evitar toxicidade medular (reducao das celulas do sangue).",
                        "clinical_example": "A azatioprina e como um 'freio' no sistema imune. O gene TPMT e a 'valvula de escape' que evita que o freio seja forte demais. Com uma copia menos ativa, a 'valvula' funciona mais devagar, entao doses menores sao necessarias. Esse teste de TPMT e obrigatorio antes de iniciar azatioprina em muitos paises."
                    }
                ]
            },
            "portador_condicoes_recessivas": {
                "title": "Status de Portador — Condicoes Recessivas",
                "description": "Analise de variantes associadas a doencas geneticas de heranca recessiva.",
                "data": [
                    {
                        "condition": "Anemia Falciforme",
                        "gene": "HBB",
                        "status": "Portador (traco falciforme)",
                        "details": "Voce e portador da variante HbS no gene HBB (traco falciforme). Voce nao desenvolve a doenca, mas pode transmitir a variante para seus filhos. Se seu parceiro(a) tambem for portador(a), ha 25% de chance de um filho ter anemia falciforme. O traco falciforme confere alguma protecao contra malaria, o que explica sua maior frequencia em populacoes de origem africana.",
                        "clinical_example": "O traco falciforme e como ter um manual de instrucoes com uma pagina levemente alterada. Voce nao tem sintomas no dia a dia, mas em situacoes extremas (desidratacao severa, altitudes elevadas) e bom saber. Em atividades fisicas intensas, mantenha-se bem hidratado."
                    },
                    {
                        "condition": "Fibrose Cistica",
                        "gene": "CFTR",
                        "status": "Nao portador",
                        "details": "Nao foram detectadas variantes patogenicas no gene CFTR."
                    },
                    {
                        "condition": "Deficiencia de G6PD",
                        "gene": "G6PD",
                        "status": "Portador (variante A-)",
                        "details": "Voce possui a variante A- no gene G6PD. A deficiencia de G6PD pode causar episodios de anemia hemolitica quando exposto a certos medicamentos (primaquina, dapsona, sulfas), alimentos (fava) ou infeccoes. E importante informar seu medico sobre este resultado antes de qualquer tratamento. Esta variante tambem confere protecao parcial contra malaria.",
                        "clinical_example": "A deficiencia de G6PD e como ter celulas vermelhas com 'blindagem reduzida' contra certas substancias. A maioria das pessoas com essa variante vive normalmente — o cuidado principal e evitar os gatilhos conhecidos. Leve esta informacao ao seu medico, especialmente antes de iniciar novos medicamentos."
                    },
                    {
                        "condition": "Hemoglobinopatia C",
                        "gene": "HBB",
                        "status": "Nao portador",
                        "details": "Nao foram detectadas variantes associadas a hemoglobina C."
                    }
                ]
            }
        }
    },
    {
        "report_id": "GEN-2026-0003",
        "patient_name": "Larissa Yumi Takahashi",
        "patient_id": "PAC-003",
        "birth_date": "1992-12-05",
        "exam_metadata": {
            "exam_type": "Painel Genomico Completo — Genera Premium",
            "exam_date": "2026-04-02",
            "collection_location": "Unidade Dasa — Rua Vergueiro, 1800 — Sao Paulo, SP",
            "laboratory_name": "Dasa Genomica",
            "laboratory_unit": "GeneOne — NTO Genomica SP",
            "protocol_number": "DAS-GEN-2026-001742",
            "responsible_physician": "Dr. Roberto Shimizu — CRM-SP 91.456",
            "technical_responsible": "Dra. Ana Beatriz Costa — CRBM 14.890"
        },
        "suggested_next_exam": {
            "date": "2027-04-02",
            "reason": "Reavaliacao anual do perfil genetico. Atencao especial ao perfil metabolico (risco diabetes em populacao asiatica) e cardiovascular. Revisao de variantes farmacogeneticas (HLA-B*1502 e HLA-B*5801 com alerta de seguranca).",
            "priority": "recomendado"
        },
        "complementary_exams": [
            {
                "name": "Hemoglobina Glicada (HbA1c)",
                "code": "TUSS 40302468",
                "reason": "Risco genetico aumentado para Diabetes Tipo 2 (KCNJ11 + TCF7L2). Populacoes asiaticas podem desenvolver diabetes com IMC mais baixo.",
                "frequency": "A cada 4 meses",
                "urgent": False
            },
            {
                "name": "Endoscopia Digestiva Alta",
                "code": "TUSS 40201010",
                "reason": "Variante IL1B rs1143627 (T/T) — risco aumentado de cancer gastrico, especialmente com H. pylori. Considerar pesquisa de H. pylori.",
                "frequency": "A cada 2 anos (a partir dos 40 anos, se H. pylori positivo)",
                "urgent": False
            },
            {
                "name": "Pesquisa de H. pylori (teste respiratorio ou antígeno fecal)",
                "code": "TUSS 40303537",
                "reason": "Rastreamento em paciente com perfil de risco para cancer gastrico",
                "frequency": "Triagem inicial",
                "urgent": False
            },
            {
                "name": "Perfil Lipidico Completo + Apolipoproteina B",
                "code": "TUSS 40301470 + 40301292",
                "reason": "Alelo APOE4 — risco cardiovascular + Alzheimer. Avaliacao de risco global.",
                "frequency": "Anual",
                "urgent": False
            },
            {
                "name": "Dosagem de Vitamina B12 e Acido Folico",
                "code": "TUSS 40304452 + 40302108",
                "reason": "Suporte neurologico — alelo APOE4 presente. Manter niveis otimos e fator protetor.",
                "frequency": "Anual",
                "urgent": False
            },
            {
                "name": "Densitometria Ossea (DEXA)",
                "code": "TUSS 40201053",
                "reason": "Perfil VDR rs1544410 — avaliacao basal de massa ossea. Complementar com dosagem de Vitamina D.",
                "frequency": "A cada 2 anos a partir dos 50 anos",
                "urgent": False
            }
        ],
        "sections": {
            "ancestralidade": {
                "title": "Composicao Ancestral",
                "description": "Estimativa da sua composicao ancestral com base em marcadores geneticos (AIMs) distribudos pelo genoma.",
                "data": {
                    "asiatico_leste": {"percentage": 56.8, "regioes": ["Japao", "Leste da China"]},
                    "europeu": {"percentage": 28.4, "regioes": ["Iberica", "Sul da Europa"]},
                    "indigena_americano": {"percentage": 8.9, "regioes": ["America do Sul"]},
                    "africano": {"percentage": 4.2, "regioes": ["Norte da Africa"]},
                    "sudeste_asiatico": {"percentage": 1.7, "regioes": ["Filipinas, Indonesia"]}
                },
                "interpretation": "Sua ancestralidade reflete a comunidade nipo-brasileira, com predominancia do Leste Asiatico (56,8% — majoritariamente Japao), combinada com significativa contribuicao europeia (28,4%) e indigena (8,9%). Este perfil e tipico de descendentes de imigrantes japoneses com miscigenacao ao longo das geracoes no Brasil.",
                "clinical_example": "A comunidade nipo-brasileira e uma das maiores do mundo fora do Japao. Seu DNA conta essa historia: a maior parte dos seus marcadores ancestrais aponta para o Japao, mas ha contribuicoes de outras origens que refletem a integracao da sua familia ao longo das geracoes no Brasil."
            },
            "predisposicao_doencas": {
                "title": "Predisposicao Genetica a Doencas",
                "description": "Analise de variantes geneticas (SNPs) associadas ao risco de desenvolvimento de condicoes de saude.",
                "data": [
                    {
                        "condition": "Diabetes Mellitus Tipo 2",
                        "gene": "KCNJ11, TCF7L2",
                        "variant": "rs5219 (C/T) + rs7903146 (C/T)",
                        "risk_level": "risco aumentado",
                        "risk_score": 18,
                        "details": "Voce possui variantes nos genes KCNJ11 e TCF7L2 associadas a risco elevado de diabetes tipo 2. O KCNJ11 controla a liberacao de insulina pelas celulas beta do pancreas. O TCF7L2 regula a secrecao de insulina. Este perfil e particularmente relevante para populacoes de ascendencia asiatica, que podem desenvolver diabetes com IMC mais baixo que outras populacoes. Monitoramento glicemico regular e manutencao de peso saudavel sao recomendados.",
                        "clinical_example": "Pessoas de ascendencia asiatica tem uma caracteristica metabolica particular: tendem a acumular gordura visceral (ao redor dos orgaos) com IMC mais baixo. Por isso, mesmo estando no peso considerado normal para outras populacoes, o risco metabolico pode ser maior. A circunferencia abdominal e um indicador importante — mantenha abaixo de 80cm (mulheres).",
                        "prevalence_general": "~10% da populacao brasileira",
                        "your_estimated_risk": "~18% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Cancer Gastrico",
                        "gene": "IL1B, IL1RN",
                        "variant": "rs1143627 (T/T)",
                        "risk_level": "risco levemente aumentado",
                        "risk_score": 2,
                        "details": "Voce possui variante no gene IL1B associada a risco levemente aumentado de cancer gastrico, especialmente em combinacao com infeccao por H. pylori. Este perfil e mais impactante em populacoes asiaticas. A erradicacao de H. pylori, se detectado, e a endoscopia de vigilancia podem ser consideradas a partir dos 40 anos.",
                        "clinical_example": "A bacteria H. pylori vive no estomago de cerca de 70% dos brasileiros. Na maioria das pessoas, nao causa problemas. Mas em pessoas com seu perfil genetico (variante IL1B) + ascendencia asiatica, a combinacao H. pylori + genetica pode aumentar o risco de alteracoes gastricas ao longo de decadas. A boa noticia: tratar o H. pylori reduz significativamente esse risco.",
                        "prevalence_general": "~1% ao longo da vida",
                        "your_estimated_risk": "~2% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Doenca de Alzheimer",
                        "gene": "APOE",
                        "variant": "e3/e4 (uma copia de APOE4)",
                        "risk_level": "risco aumentado",
                        "risk_score": 23,
                        "details": "Voce possui uma copia do alelo APOE4, associado a risco 2-3x maior de desenvolvimento de Alzheimer de inicio tardio (apos 65 anos). O gene APOE esta envolvido no transporte e metabolismo de lipideos no cerebro. Isso nao significa que voce desenvolvera a doenca — 25% da populacao tem pelo menos um alelo APOE4 e a maioria nunca desenvolve Alzheimer. Estilo de vida ativo, estimulacao cognitiva, dieta mediterranea, controle cardiovascular e sono de qualidade sao fatores protetores importantes.",
                        "clinical_example": "O alelo APOE4 e como um fator que deixa o cerebro um pouco mais 'sensivel' ao envelhecimento. Mas o cerebro tem uma capacidade incrivel de se adaptar (neuroplasticidade). Atividades que estimulam o cerebro — aprender coisas novas, socializar, ler, tocar instrumentos — funcionam como uma 'musculacao cerebral' que ajuda a manter a saude neurologica.",
                        "prevalence_general": "~10% apos 65 anos",
                        "your_estimated_risk": "~23% (baseado apenas no fator genetico)"
                    },
                    {
                        "condition": "Osteoporose",
                        "gene": "VDR, COL1A1",
                        "variant": "rs1544410 (A/G)",
                        "risk_level": "risco tipico",
                        "risk_score": 18,
                        "details": "Seu perfil nos genes associados ao metabolismo osseo (VDR — receptor de vitamina D e COL1A1 — colageno tipo 1) e considerado de risco tipico. Mantenha ingestao adequada de calcio (1000mg/dia) e vitamina D (800-1000 UI/dia), alem de exercicios com carga (musculacao, pilates) para a saude ossea.",
                        "clinical_example": "Seus ossos estao em constante renovacao — celulas chamadas osteoclastos 'removem' osso velho e osteoblastos 'constroem' osso novo. A partir dos 35-40 anos, a remocao naturalmente supera a construcao. Exercicios com impacto (caminhada, danca, musculacao) estimulam os osteoblastos a trabalharem mais, mantendo os ossos fortes."
                    }
                ]
            },
            "bem_estar": {
                "title": "Bem-Estar e Caracteristicas Pessoais",
                "description": "Tracos geneticos que influenciam aspectos do seu dia a dia, metabolismo e resposta a nutrientes.",
                "data": [
                    {
                        "trait": "Intolerancia a Lactose",
                        "gene": "MCM6 / LCT",
                        "variant": "rs4988235 (G/G)",
                        "result": "Provavel intolerancia a lactose na idade adulta",
                        "details": "Seu genotipo G/G esta associado a reducao da producao de lactase. Esta variante e muito comum em populacoes do Leste Asiatico (presente em mais de 90% dos individuos). Produtos sem lactose, leites vegetais fortificados ou suplementos de lactase podem ajudar.",
                        "clinical_example": "Na Asia, historicamente, o gado leiteiro nao era tao comum, entao a maioria das pessoas parava de produzir lactase apos a infancia. Voce herdou essa caracteristica. Leites vegetais (soja, amendoa, aveia) sao alternativas nutritivas, e muitos sao enriquecidos com calcio."
                    },
                    {
                        "trait": "Sensibilidade ao Alcool",
                        "gene": "ALDH2",
                        "variant": "rs671 (A/G — atividade reduzida)",
                        "result": "Metabolizacao reduzida de alcool — rubor facial",
                        "details": "Voce possui uma copia da variante inativa da enzima ALDH2, comum em populacoes do Leste Asiatico. Isso resulta em acumulo de acetaldeido apos o consumo de alcool, causando rubor facial, taquicardia e nausea. Alem do desconforto, este perfil esta associado a maior risco de cancer de esofago com consumo regular de alcool. A recomendacao e consumo muito moderado ou abstencao.",
                        "clinical_example": "Quando voce bebe alcool, seu corpo o converte em acetaldeido — uma substancia toxica e cancerigena. Depois, a enzima ALDH2 transforma o acetaldeido em algo inofensivo. Sua enzima ALDH2 e 'preguicosa' (so funciona pela metade), entao o acetaldeido se acumula. O rubor facial que voce sente e o sinal visivel desse acumulo."
                    },
                    {
                        "trait": "Metabolismo de Vitamina D",
                        "gene": "GC",
                        "variant": "rs2282679 (T/G)",
                        "result": "Niveis naturalmente mais baixos de vitamina D circulante",
                        "details": "Seu perfil no gene GC esta associado a niveis circulantes naturalmente mais baixos de vitamina D. Considerando que pessoas com ascendencia asiatica em regioes de alta insolacao tambem podem apresentar essa tendencia, a suplementacao preventiva pode ser discutida com seu medico.",
                        "clinical_example": "A vitamina D e produzida na pele quando exposta ao sol. Mas seu corpo tambem depende da proteina transportadora (codificada pelo gene GC) para mante-la circulando. Com sua variante, essa proteina transportadora e menos eficiente, entao mesmo tomando sol, seus niveis podem ser mais baixos. Exames de sangue podem verificar seus niveis."
                    },
                    {
                        "trait": "Resposta ao Estresse",
                        "gene": "COMT",
                        "variant": "rs4680 (A/A — Met/Met)",
                        "result": "Baixa atividade da COMT — maior sensibilidade ao estresse, boa cognicao em ambientes calmos",
                        "details": "Voce possui a variante de baixa atividade da enzima COMT, responsavel por degradar dopamina e noradrenalina no cortex pre-frontal (area do cerebro responsavel por planejamento, atencao e tomada de decisoes). Isso resulta em maior sensibilidade ao estresse, mas tambem em melhor desempenho cognitivo em ambientes calmos e estruturados. Tecnicas de mindfulness, meditacao e boa higiene do sono podem ser particularmente beneficas.",
                        "clinical_example": "Sua variante COMT e como ter um 'filtro' cerebral mais sensivel. Em ambientes tranquilos, isso e uma vantagem — voce processa informacoes com mais profundidade. Em ambientes estressantes, o excesso de estimulos pode sobrecarregar. Criar rotinas previsiveis e reservar momentos de silencio no seu dia pode fazer grande diferenca."
                    }
                ]
            },
            "farmacogenetica": {
                "title": "Farmacogenetica — Resposta a Medicamentos",
                "description": "Analise de genes que influenciam como seu organismo processa determinados medicamentos. ALERTA — algumas variantes encontradas exigem atencao especial. ATENCAO: nunca altere sua medicacao sem orientacao medica.",
                "data": [
                    {
                        "drug": "Carbamazepina (anticonvulsivante / estabilizador de humor)",
                        "gene": "HLA-B",
                        "variant": "HLA-B*1502 — POSITIVO",
                        "result": "ALERTA DE SEGURANCA — Risco de reacao cutanea grave (Sindrome de Stevens-Johnson / NET)",
                        "details": "ALERTA IMPORTANTE: Voce possui o alelo HLA-B*1502, fortemente associado ao risco de reacoes cutaneas graves com o uso de carbamazepina. A Sindrome de Stevens-Johnson e uma reacao rara mas potencialmente fatal. Este medicamento e CONTRAINDICADO para voce. Esta variante e mais comum em populacoes do Leste Asiatico. Informe sempre este resultado a qualquer medico antes de prescricoes, especialmente neurologistas e psiquiatras.",
                        "clinical_example": "Este e o achado farmacogenetico mais impactante do seu relatorio. O alelo HLA-B*1502 e como ter um 'alarme de seguranca' no sistema imune que pode disparar de forma exagerada com a carbamazepina. A boa noticia: sabendo disso, e possivel evitar o risco completamente usando medicamentos alternativos. Leve esta informacao sempre que for atendida por um novo medico."
                    },
                    {
                        "drug": "Alopurinol (gota / acido urico elevado)",
                        "gene": "HLA-B",
                        "variant": "HLA-B*5801 — POSITIVO",
                        "result": "ALERTA DE SEGURANCA — Risco de reacao cutanea grave",
                        "details": "ALERTA IMPORTANTE: Voce possui o alelo HLA-B*5801, associado a risco elevado de reacoes cutaneas graves com alopurinol. Este medicamento e CONTRAINDICADO para voce. Alternativas como febuxostat podem ser consideradas sob orientacao medica.",
                        "clinical_example": "Assim como com a carbamazepina, seu sistema imune tem um 'alarme' que pode reagir de forma exagerada ao alopurinol. Isso nao significa que voce nao pode tratar gota ou acido urico elevado — existem outros medicamentos seguros para o seu perfil."
                    },
                    {
                        "drug": "Omeprazol (refluxo gastrico)",
                        "gene": "CYP2C19",
                        "variant": "*2/*2 (metabolizador lento)",
                        "result": "Metabolizacao lenta — maior eficacia",
                        "details": "Voce possui duas copias da variante de baixa atividade no gene CYP2C19. Isso resulta em metabolizacao mais lenta do omeprazol, o que pode aumentar sua eficacia no controle do refluxo. No entanto, em uso prolongado, pode exigir ajuste de dose para evitar supressao acida excessiva.",
                        "clinical_example": "Para voce, o omeprazol age como um 'freio mais duradouro' na producao de acido. Isso e bom para controlar sintomas, mas em uso cronico, seu medico pode considerar uma dose menor que a padrao."
                    },
                    {
                        "drug": "Antidepressivos ISRS (sertralina, fluoxetina, citalopram)",
                        "gene": "CYP2C19",
                        "variant": "*2/*2 (metabolizador lento)",
                        "result": "Metabolizacao lenta — considerar dose inicial reduzida (~50%)",
                        "details": "Seu perfil de metabolizador lento do CYP2C19 afeta diversos antidepressivos ISRS. Caso precise de tratamento, doses iniciais mais baixas podem ser mais adequadas, com ajuste gradual conforme resposta e tolerancia. Esta informacao pode ajudar a reduzir efeitos colaterais no inicio do tratamento.",
                        "clinical_example": "Iniciar um antidepressivo com a dose errada pode causar efeitos colaterais desconfortaveis que levam ao abandono do tratamento. Com seu perfil, o medico sabe que deve comecar com doses mais baixas e subir devagar — isso aumenta as chances de sucesso do tratamento com menos desconforto."
                    }
                ]
            },
            "portador_condicoes_recessivas": {
                "title": "Status de Portador — Condicoes Recessivas",
                "description": "Analise de variantes associadas a doencas geneticas de heranca recessiva.",
                "data": [
                    {
                        "condition": "Fibrose Cistica",
                        "gene": "CFTR",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas variantes patogenicas no gene CFTR."
                    },
                    {
                        "condition": "Anemia Falciforme",
                        "gene": "HBB",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas variantes associadas a anemia falciforme ou traco falciforme."
                    },
                    {
                        "condition": "Talasemia Alfa",
                        "gene": "HBA1, HBA2",
                        "variant": "Delecao -alpha3.7 heterozigota",
                        "status": "Portadora silenciosa",
                        "details": "Voce e portadora de uma delecao em um dos genes da alfa-globina (proteina que compoe a hemoglobina, responsavel por transportar oxigenio no sangue). Como portadora silenciosa, voce nao apresenta sintomas — seus exames de sangue podem mostrar hemacias levemente menores (microcitose), mas sem anemia. Voce pode transmitir a variante. Se seu parceiro(a) tambem for portador(a), ha risco de talassemia em filhos. Esta variante e mais comum em populacoes asiaticas e africanas.",
                        "clinical_example": "Ser portadora silenciosa de talasemia alfa e como ter uma pequena fabrica de hemoglobina com capacidade produtiva levemente reduzida. Como voce tem outras copias normais do gene, a producao total e suficiente e voce nao tem sintomas. Seu medico pode notar no hemograma que suas hemacias sao um pouco menores (VCM reduzido) — isso e esperado e nao requer tratamento."
                    },
                    {
                        "condition": "Atrofia Muscular Espinhal (AME)",
                        "gene": "SMN1",
                        "status": "Nao portadora",
                        "details": "Nao foram detectadas variantes patogenicas no gene SMN1."
                    }
                ]
            }
        }
    }
]


def generate_reports():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    paths = []
    for report in REPORTS:
        filepath = os.path.join(REPORTS_DIR, f"{report['report_id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        paths.append(filepath)
    return paths


def load_report(report_id):
    filepath = os.path.join(REPORTS_DIR, f"{report_id}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_reports():
    if not os.path.exists(REPORTS_DIR):
        return []
    return [f.replace(".json", "") for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]


def get_patient_by_id(patient_id):
    for report in REPORTS:
        if report.get("patient_id") == patient_id:
            return {
                "patient_id": report["patient_id"],
                "patient_name": report["patient_name"],
                "birth_date": report.get("birth_date", ""),
                "reports": [report["report_id"]],
                "last_exam": report["exam_metadata"]["exam_date"],
            }
    return None


def list_patients():
    patients = {}
    for report in REPORTS:
        pid = report["patient_id"]
        if pid not in patients:
            patients[pid] = {
                "patient_id": pid,
                "patient_name": report["patient_name"],
                "birth_date": report.get("birth_date", ""),
                "reports": [report["report_id"]],
                "last_exam": report["exam_metadata"]["exam_date"],
            }
        else:
            patients[pid]["reports"].append(report["report_id"])
            if report["exam_metadata"]["exam_date"] > patients[pid]["last_exam"]:
                patients[pid]["last_exam"] = report["exam_metadata"]["exam_date"]
    return list(patients.values())


if __name__ == "__main__":
    paths = generate_reports()
    for p in paths:
        print(f"Generated: {p}")
