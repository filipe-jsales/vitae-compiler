"""Rótulos de seção/enum por idioma, usados na renderização do template LaTeX.

Mantidos em Python (não em YAML) porque são texto de interface do próprio
tema, não dados do currículo do usuário.
"""

LABELS = {
    "pt": {
        "titulo_documento": "Currículo",
        "resumo": "Resumo",
        "palavras_chave": "Palavras-chave",
        "publicacoes": "Publicações",
        "projetos": "Projetos",
        "orientacoes": "Orientações",
        "ensino": "Ensino",
        "premios": "Prêmios e Distinções",
        "papel": "Papel",
        "financiamento": "Financiamento",
        "atual": "atual",
        "tipo_orientacao": {
            "iniciacao_cientifica": "Iniciação Científica",
            "tcc": "TCC",
            "mestrado": "Mestrado",
            "doutorado": "Doutorado",
            "pos_doutorado": "Pós-doutorado",
        },
        "situacao": {
            "em_andamento": "em andamento",
            "concluida": "concluída",
        },
        "nivel_ensino": {
            "graduacao": "Graduação",
            "pos_graduacao": "Pós-graduação",
            "extensao": "Extensão",
        },
    },
    "en": {
        "titulo_documento": "Curriculum Vitae",
        "resumo": "Summary",
        "palavras_chave": "Keywords",
        "publicacoes": "Publications",
        "projetos": "Projects",
        "orientacoes": "Advising",
        "ensino": "Teaching",
        "premios": "Awards and Honors",
        "papel": "Role",
        "financiamento": "Funding",
        "atual": "present",
        "tipo_orientacao": {
            "iniciacao_cientifica": "Undergraduate Research",
            "tcc": "Undergraduate Thesis",
            "mestrado": "Master's",
            "doutorado": "PhD",
            "pos_doutorado": "Postdoctoral",
        },
        "situacao": {
            "em_andamento": "in progress",
            "concluida": "completed",
        },
        "nivel_ensino": {
            "graduacao": "Undergraduate",
            "pos_graduacao": "Graduate",
            "extensao": "Extension",
        },
    },
}

SUPPORTED_LANGUAGES = tuple(LABELS.keys())
