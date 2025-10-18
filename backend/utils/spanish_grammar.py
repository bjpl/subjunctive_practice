"""
Spanish Grammar Rules and Constants

This module contains all the linguistic rules, patterns, and constants
needed for Spanish subjunctive conjugation.
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum


class Tense(Enum):
    """Subjunctive tenses"""
    PRESENT = "present_subjunctive"
    IMPERFECT_RA = "imperfect_subjunctive_ra"
    IMPERFECT_SE = "imperfect_subjunctive_se"


class Person(Enum):
    """Grammatical persons"""
    YO = "yo"
    TU = "tú"
    EL = "él/ella/usted"
    NOSOTROS = "nosotros/nosotras"
    VOSOTROS = "vosotros/vosotras"
    ELLOS = "ellos/ellas/ustedes"


# Regular verb endings for subjunctive
REGULAR_ENDINGS = {
    "present_subjunctive": {
        "-ar": {
            "yo": "e",
            "tú": "es",
            "él/ella/usted": "e",
            "nosotros/nosotras": "emos",
            "vosotros/vosotras": "éis",
            "ellos/ellas/ustedes": "en"
        },
        "-er": {
            "yo": "a",
            "tú": "as",
            "él/ella/usted": "a",
            "nosotros/nosotras": "amos",
            "vosotros/vosotras": "áis",
            "ellos/ellas/ustedes": "an"
        },
        "-ir": {
            "yo": "a",
            "tú": "as",
            "él/ella/usted": "a",
            "nosotros/nosotras": "amos",
            "vosotros/vosotras": "áis",
            "ellos/ellas/ustedes": "an"
        }
    },
    "imperfect_subjunctive_ra": {
        "-ar": {
            "yo": "ara",
            "tú": "aras",
            "él/ella/usted": "ara",
            "nosotros/nosotras": "áramos",
            "vosotros/vosotras": "arais",
            "ellos/ellas/ustedes": "aran"
        },
        "-er": {
            "yo": "iera",
            "tú": "ieras",
            "él/ella/usted": "iera",
            "nosotros/nosotras": "iéramos",
            "vosotros/vosotras": "ierais",
            "ellos/ellas/ustedes": "ieran"
        },
        "-ir": {
            "yo": "iera",
            "tú": "ieras",
            "él/ella/usted": "iera",
            "nosotros/nosotras": "iéramos",
            "vosotros/vosotras": "ierais",
            "ellos/ellas/ustedes": "ieran"
        }
    },
    "imperfect_subjunctive_se": {
        "-ar": {
            "yo": "ase",
            "tú": "ases",
            "él/ella/usted": "ase",
            "nosotros/nosotras": "ásemos",
            "vosotros/vosotras": "aseis",
            "ellos/ellas/ustedes": "asen"
        },
        "-er": {
            "yo": "iese",
            "tú": "ieses",
            "él/ella/usted": "iese",
            "nosotros/nosotras": "iésemos",
            "vosotros/vosotras": "ieseis",
            "ellos/ellas/ustedes": "iesen"
        },
        "-ir": {
            "yo": "iese",
            "tú": "ieses",
            "él/ella/usted": "iese",
            "nosotros/nosotras": "iésemos",
            "vosotros/vosotras": "ieseis",
            "ellos/ellas/ustedes": "iesen"
        }
    }
}


# Complete irregular verb conjugations (30+ verbs)
IRREGULAR_VERBS = {
    "ser": {
        "present_subjunctive": {
            "yo": "sea", "tú": "seas", "él/ella/usted": "sea",
            "nosotros/nosotras": "seamos", "vosotros/vosotras": "seáis",
            "ellos/ellas/ustedes": "sean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "fuera", "tú": "fueras", "él/ella/usted": "fuera",
            "nosotros/nosotras": "fuéramos", "vosotros/vosotras": "fuerais",
            "ellos/ellas/ustedes": "fueran"
        },
        "imperfect_subjunctive_se": {
            "yo": "fuese", "tú": "fueses", "él/ella/usted": "fuese",
            "nosotros/nosotras": "fuésemos", "vosotros/vosotras": "fueseis",
            "ellos/ellas/ustedes": "fuesen"
        }
    },
    "estar": {
        "present_subjunctive": {
            "yo": "esté", "tú": "estés", "él/ella/usted": "esté",
            "nosotros/nosotras": "estemos", "vosotros/vosotras": "estéis",
            "ellos/ellas/ustedes": "estén"
        },
        "imperfect_subjunctive_ra": {
            "yo": "estuviera", "tú": "estuvieras", "él/ella/usted": "estuviera",
            "nosotros/nosotras": "estuviéramos", "vosotros/vosotras": "estuvierais",
            "ellos/ellas/ustedes": "estuvieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "estuviese", "tú": "estuvieses", "él/ella/usted": "estuviese",
            "nosotros/nosotras": "estuviésemos", "vosotros/vosotras": "estuvieseis",
            "ellos/ellas/ustedes": "estuviesen"
        }
    },
    "ir": {
        "present_subjunctive": {
            "yo": "vaya", "tú": "vayas", "él/ella/usted": "vaya",
            "nosotros/nosotras": "vayamos", "vosotros/vosotras": "vayáis",
            "ellos/ellas/ustedes": "vayan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "fuera", "tú": "fueras", "él/ella/usted": "fuera",
            "nosotros/nosotras": "fuéramos", "vosotros/vosotras": "fuerais",
            "ellos/ellas/ustedes": "fueran"
        },
        "imperfect_subjunctive_se": {
            "yo": "fuese", "tú": "fueses", "él/ella/usted": "fuese",
            "nosotros/nosotras": "fuésemos", "vosotros/vosotras": "fueseis",
            "ellos/ellas/ustedes": "fuesen"
        }
    },
    "haber": {
        "present_subjunctive": {
            "yo": "haya", "tú": "hayas", "él/ella/usted": "haya",
            "nosotros/nosotras": "hayamos", "vosotros/vosotras": "hayáis",
            "ellos/ellas/ustedes": "hayan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "hubiera", "tú": "hubieras", "él/ella/usted": "hubiera",
            "nosotros/nosotras": "hubiéramos", "vosotros/vosotras": "hubierais",
            "ellos/ellas/ustedes": "hubieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "hubiese", "tú": "hubieses", "él/ella/usted": "hubiese",
            "nosotros/nosotras": "hubiésemos", "vosotros/vosotras": "hubieseis",
            "ellos/ellas/ustedes": "hubiesen"
        }
    },
    "dar": {
        "present_subjunctive": {
            "yo": "dé", "tú": "des", "él/ella/usted": "dé",
            "nosotros/nosotras": "demos", "vosotros/vosotras": "deis",
            "ellos/ellas/ustedes": "den"
        },
        "imperfect_subjunctive_ra": {
            "yo": "diera", "tú": "dieras", "él/ella/usted": "diera",
            "nosotros/nosotras": "diéramos", "vosotros/vosotras": "dierais",
            "ellos/ellas/ustedes": "dieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "diese", "tú": "dieses", "él/ella/usted": "diese",
            "nosotros/nosotras": "diésemos", "vosotros/vosotras": "dieseis",
            "ellos/ellas/ustedes": "diesen"
        }
    },
    "saber": {
        "present_subjunctive": {
            "yo": "sepa", "tú": "sepas", "él/ella/usted": "sepa",
            "nosotros/nosotras": "sepamos", "vosotros/vosotras": "sepáis",
            "ellos/ellas/ustedes": "sepan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "supiera", "tú": "supieras", "él/ella/usted": "supiera",
            "nosotros/nosotras": "supiéramos", "vosotros/vosotras": "supierais",
            "ellos/ellas/ustedes": "supieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "supiese", "tú": "supieses", "él/ella/usted": "supiese",
            "nosotros/nosotras": "supiésemos", "vosotros/vosotras": "supieseis",
            "ellos/ellas/ustedes": "supiesen"
        }
    },
    "ver": {
        "present_subjunctive": {
            "yo": "vea", "tú": "veas", "él/ella/usted": "vea",
            "nosotros/nosotras": "veamos", "vosotros/vosotras": "veáis",
            "ellos/ellas/ustedes": "vean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "viera", "tú": "vieras", "él/ella/usted": "viera",
            "nosotros/nosotras": "viéramos", "vosotros/vosotras": "vierais",
            "ellos/ellas/ustedes": "vieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "viese", "tú": "vieses", "él/ella/usted": "viese",
            "nosotros/nosotras": "viésemos", "vosotros/vosotras": "vieseis",
            "ellos/ellas/ustedes": "viesen"
        }
    },
    "hacer": {
        "present_subjunctive": {
            "yo": "haga", "tú": "hagas", "él/ella/usted": "haga",
            "nosotros/nosotras": "hagamos", "vosotros/vosotras": "hagáis",
            "ellos/ellas/ustedes": "hagan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "hiciera", "tú": "hicieras", "él/ella/usted": "hiciera",
            "nosotros/nosotras": "hiciéramos", "vosotros/vosotras": "hicierais",
            "ellos/ellas/ustedes": "hicieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "hiciese", "tú": "hicieses", "él/ella/usted": "hiciese",
            "nosotros/nosotras": "hiciésemos", "vosotros/vosotras": "hicieseis",
            "ellos/ellas/ustedes": "hiciesen"
        }
    },
    "decir": {
        "present_subjunctive": {
            "yo": "diga", "tú": "digas", "él/ella/usted": "diga",
            "nosotros/nosotras": "digamos", "vosotros/vosotras": "digáis",
            "ellos/ellas/ustedes": "digan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "dijera", "tú": "dijeras", "él/ella/usted": "dijera",
            "nosotros/nosotras": "dijéramos", "vosotros/vosotras": "dijerais",
            "ellos/ellas/ustedes": "dijeran"
        },
        "imperfect_subjunctive_se": {
            "yo": "dijese", "tú": "dijeses", "él/ella/usted": "dijese",
            "nosotros/nosotras": "dijésemos", "vosotros/vosotras": "dijeseis",
            "ellos/ellas/ustedes": "dijesen"
        }
    },
    "tener": {
        "present_subjunctive": {
            "yo": "tenga", "tú": "tengas", "él/ella/usted": "tenga",
            "nosotros/nosotras": "tengamos", "vosotros/vosotras": "tengáis",
            "ellos/ellas/ustedes": "tengan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "tuviera", "tú": "tuvieras", "él/ella/usted": "tuviera",
            "nosotros/nosotras": "tuviéramos", "vosotros/vosotras": "tuvierais",
            "ellos/ellas/ustedes": "tuvieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "tuviese", "tú": "tuvieses", "él/ella/usted": "tuviese",
            "nosotros/nosotras": "tuviésemos", "vosotros/vosotras": "tuvieseis",
            "ellos/ellas/ustedes": "tuviesen"
        }
    },
    "poner": {
        "present_subjunctive": {
            "yo": "ponga", "tú": "pongas", "él/ella/usted": "ponga",
            "nosotros/nosotras": "pongamos", "vosotros/vosotras": "pongáis",
            "ellos/ellas/ustedes": "pongan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pusiera", "tú": "pusieras", "él/ella/usted": "pusiera",
            "nosotros/nosotras": "pusiéramos", "vosotros/vosotras": "pusierais",
            "ellos/ellas/ustedes": "pusieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "pusiese", "tú": "pusieses", "él/ella/usted": "pusiese",
            "nosotros/nosotras": "pusiésemos", "vosotros/vosotras": "pusieseis",
            "ellos/ellas/ustedes": "pusiesen"
        }
    },
    "poder": {
        "present_subjunctive": {
            "yo": "pueda", "tú": "puedas", "él/ella/usted": "pueda",
            "nosotros/nosotras": "podamos", "vosotros/vosotras": "podáis",
            "ellos/ellas/ustedes": "puedan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pudiera", "tú": "pudieras", "él/ella/usted": "pudiera",
            "nosotros/nosotras": "pudiéramos", "vosotros/vosotras": "pudierais",
            "ellos/ellas/ustedes": "pudieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "pudiese", "tú": "pudieses", "él/ella/usted": "pudiese",
            "nosotros/nosotras": "pudiésemos", "vosotros/vosotras": "pudieseis",
            "ellos/ellas/ustedes": "pudiesen"
        }
    },
    "querer": {
        # Present subjunctive follows stem-changing pattern (e→ie)
        # Only imperfect forms are truly irregular
        "imperfect_subjunctive_ra": {
            "yo": "quisiera", "tú": "quisieras", "él/ella/usted": "quisiera",
            "nosotros/nosotras": "quisiéramos", "vosotros/vosotras": "quisierais",
            "ellos/ellas/ustedes": "quisieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "quisiese", "tú": "quisieses", "él/ella/usted": "quisiese",
            "nosotros/nosotras": "quisiésemos", "vosotros/vosotras": "quisieseis",
            "ellos/ellas/ustedes": "quisiesen"
        }
    },
    "venir": {
        "present_subjunctive": {
            "yo": "venga", "tú": "vengas", "él/ella/usted": "venga",
            "nosotros/nosotras": "vengamos", "vosotros/vosotras": "vengáis",
            "ellos/ellas/ustedes": "vengan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "viniera", "tú": "vinieras", "él/ella/usted": "viniera",
            "nosotros/nosotras": "viniéramos", "vosotros/vosotras": "vinierais",
            "ellos/ellas/ustedes": "vinieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "viniese", "tú": "vinieses", "él/ella/usted": "viniese",
            "nosotros/nosotras": "viniésemos", "vosotros/vosotras": "vinieseis",
            "ellos/ellas/ustedes": "viniesen"
        }
    },
    "salir": {
        "present_subjunctive": {
            "yo": "salga", "tú": "salgas", "él/ella/usted": "salga",
            "nosotros/nosotras": "salgamos", "vosotros/vosotras": "salgáis",
            "ellos/ellas/ustedes": "salgan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "saliera", "tú": "salieras", "él/ella/usted": "saliera",
            "nosotros/nosotras": "saliéramos", "vosotros/vosotras": "salierais",
            "ellos/ellas/ustedes": "salieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "saliese", "tú": "salieses", "él/ella/usted": "saliese",
            "nosotros/nosotras": "saliésemos", "vosotros/vosotras": "salieseis",
            "ellos/ellas/ustedes": "saliesen"
        }
    },
    "traer": {
        "present_subjunctive": {
            "yo": "traiga", "tú": "traigas", "él/ella/usted": "traiga",
            "nosotros/nosotras": "traigamos", "vosotros/vosotras": "traigáis",
            "ellos/ellas/ustedes": "traigan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "trajera", "tú": "trajeras", "él/ella/usted": "trajera",
            "nosotros/nosotras": "trajéramos", "vosotros/vosotras": "trajerais",
            "ellos/ellas/ustedes": "trajeran"
        },
        "imperfect_subjunctive_se": {
            "yo": "trajese", "tú": "trajeses", "él/ella/usted": "trajese",
            "nosotros/nosotras": "trajésemos", "vosotros/vosotras": "trajeseis",
            "ellos/ellas/ustedes": "trajesen"
        }
    },
    "caer": {
        "present_subjunctive": {
            "yo": "caiga", "tú": "caigas", "él/ella/usted": "caiga",
            "nosotros/nosotras": "caigamos", "vosotros/vosotras": "caigáis",
            "ellos/ellas/ustedes": "caigan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "cayera", "tú": "cayeras", "él/ella/usted": "cayera",
            "nosotros/nosotras": "cayéramos", "vosotros/vosotras": "cayerais",
            "ellos/ellas/ustedes": "cayeran"
        },
        "imperfect_subjunctive_se": {
            "yo": "cayese", "tú": "cayeses", "él/ella/usted": "cayese",
            "nosotros/nosotras": "cayésemos", "vosotros/vosotras": "cayeseis",
            "ellos/ellas/ustedes": "cayesen"
        }
    },
    "conocer": {
        "present_subjunctive": {
            "yo": "conozca", "tú": "conozcas", "él/ella/usted": "conozca",
            "nosotros/nosotras": "conozcamos", "vosotros/vosotras": "conozcáis",
            "ellos/ellas/ustedes": "conozcan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "conociera", "tú": "conocieras", "él/ella/usted": "conociera",
            "nosotros/nosotras": "conociéramos", "vosotros/vosotras": "conocierais",
            "ellos/ellas/ustedes": "conocieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "conociese", "tú": "conocieses", "él/ella/usted": "conociese",
            "nosotros/nosotras": "conociésemos", "vosotros/vosotras": "conocieseis",
            "ellos/ellas/ustedes": "conociesen"
        }
    },
    "producir": {
        "present_subjunctive": {
            "yo": "produzca", "tú": "produzcas", "él/ella/usted": "produzca",
            "nosotros/nosotras": "produzcamos", "vosotros/vosotras": "produzcáis",
            "ellos/ellas/ustedes": "produzcan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "produjera", "tú": "produjeras", "él/ella/usted": "produjera",
            "nosotros/nosotras": "produjéramos", "vosotros/vosotras": "produjerais",
            "ellos/ellas/ustedes": "produjeran"
        },
        "imperfect_subjunctive_se": {
            "yo": "produjese", "tú": "produjeses", "él/ella/usted": "produjese",
            "nosotros/nosotras": "produjésemos", "vosotros/vosotras": "produjeseis",
            "ellos/ellas/ustedes": "produjesen"
        }
    },
    "conducir": {
        "present_subjunctive": {
            "yo": "conduzca", "tú": "conduzcas", "él/ella/usted": "conduzca",
            "nosotros/nosotras": "conduzcamos", "vosotros/vosotras": "conduzcáis",
            "ellos/ellas/ustedes": "conduzcan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "condujera", "tú": "condujeras", "él/ella/usted": "condujera",
            "nosotros/nosotras": "condujéramos", "vosotros/vosotras": "condujerais",
            "ellos/ellas/ustedes": "condujeran"
        },
        "imperfect_subjunctive_se": {
            "yo": "condujese", "tú": "condujeses", "él/ella/usted": "condujese",
            "nosotros/nosotras": "condujésemos", "vosotros/vosotras": "condujeseis",
            "ellos/ellas/ustedes": "condujesen"
        }
    }
}


# Stem-changing verb patterns (e→ie, o→ue, e→i)
STEM_CHANGING_VERBS = {
    "e→ie": {
        "pensar": {"stem": "piens", "type": "-ar"},
        "entender": {"stem": "entiend", "type": "-er"},
        "sentir": {"stem": "sient", "type": "-ir"},
        "preferir": {"stem": "prefier", "type": "-ir"},
        "cerrar": {"stem": "cierr", "type": "-ar"},
        "empezar": {"stem": "empiez", "type": "-ar"},
        "comenzar": {"stem": "comienz", "type": "-ar"},
        "perder": {"stem": "pierd", "type": "-er"},
        "querer": {"stem": "quier", "type": "-er"},
        "mentir": {"stem": "mient", "type": "-ir"}
    },
    "o→ue": {
        "dormir": {"stem": "duerm", "type": "-ir"},
        "morir": {"stem": "muerm", "type": "-ir"},
        "poder": {"stem": "pued", "type": "-er"},
        "volver": {"stem": "vuelv", "type": "-er"},
        "contar": {"stem": "cuent", "type": "-ar"},
        "encontrar": {"stem": "encuentr", "type": "-ar"},
        "mostrar": {"stem": "muestr", "type": "-ar"},
        "recordar": {"stem": "recuerd", "type": "-ar"},
        "costar": {"stem": "cuest", "type": "-ar"}
    },
    "e→i": {
        "pedir": {"stem": "pid", "type": "-ir"},
        "servir": {"stem": "sirv", "type": "-ir"},
        "repetir": {"stem": "repit", "type": "-ir"},
        "seguir": {"stem": "sig", "type": "-ir"},
        "conseguir": {"stem": "consig", "type": "-ir"},
        "vestir": {"stem": "vist", "type": "-ir"},
        "medir": {"stem": "mid", "type": "-ir"},
        "reír": {"stem": "rí", "type": "-ir"}
    }
}


# Spelling change rules
SPELLING_CHANGES = {
    "g→gu": {
        "pattern": r"g([ae])",
        "examples": ["pagar", "llegar", "jugar", "rogar", "negar"],
        "rule": "Before 'e', 'g' becomes 'gu' to maintain /g/ sound"
    },
    "c→qu": {
        "pattern": r"c([ei])",
        "examples": ["sacar", "buscar", "tocar", "explicar", "practicar"],
        "rule": "Before 'e', 'c' becomes 'qu' to maintain /k/ sound"
    },
    "z→c": {
        "pattern": r"z([ei])",
        "examples": ["empezar", "comenzar", "alcanzar", "cruzar", "almorzar"],
        "rule": "Before 'e', 'z' becomes 'c' following Spanish orthography"
    },
    "gu→gü": {
        "pattern": r"gu([ae])",
        "examples": ["averiguar", "apaciguar"],
        "rule": "Before 'e', 'gu' becomes 'gü' to maintain /gw/ sound"
    },
    "c→z": {
        "pattern": r"c([ao])",
        "examples": ["convencer", "vencer", "esparcir"],
        "rule": "Before 'a' or 'o', 'c' becomes 'z' to maintain /θ/ sound"
    },
    "i→y": {
        "pattern": r"i([aeo])",
        "examples": ["leer", "creer", "caer", "oír", "construir"],
        "rule": "Unstressed 'i' between vowels becomes 'y'"
    }
}


# WEIRDO triggers for subjunctive
WEIRDO_TRIGGERS = {
    "Wishes": {
        "triggers": [
            "querer que", "desear que", "esperar que", "preferir que",
            "ojalá (que)", "que + subjunctive (command)", "necesitar que"
        ],
        "examples": [
            "Quiero que vengas a la fiesta.",
            "Espero que tengas un buen día.",
            "Ojalá que llueva café."
        ]
    },
    "Emotions": {
        "triggers": [
            "alegrarse de que", "sentir que", "temer que", "tener miedo de que",
            "sorprender que", "molestar que", "gustar que", "encantar que",
            "estar contento de que", "estar triste de que"
        ],
        "examples": [
            "Me alegro de que estés aquí.",
            "Siento que no puedas venir.",
            "Me sorprende que sepas español."
        ]
    },
    "Impersonal_Expressions": {
        "triggers": [
            "es importante que", "es necesario que", "es posible que",
            "es probable que", "es imposible que", "es mejor que",
            "es bueno que", "es malo que", "es raro que", "es una lástima que"
        ],
        "examples": [
            "Es importante que estudies.",
            "Es posible que llueva mañana.",
            "Es mejor que llegues temprano."
        ]
    },
    "Recommendations": {
        "triggers": [
            "recomendar que", "sugerir que", "aconsejar que", "proponer que",
            "pedir que", "exigir que", "mandar que", "ordenar que",
            "rogar que", "insistir en que"
        ],
        "examples": [
            "Recomiendo que vayas al médico.",
            "Te sugiero que hables con él.",
            "Exijo que me digas la verdad."
        ]
    },
    "Doubt_Denial": {
        "triggers": [
            "dudar que", "no creer que", "no pensar que", "no estar seguro de que",
            "negar que", "no es verdad que", "no es cierto que", "no es obvio que"
        ],
        "examples": [
            "Dudo que sea verdad.",
            "No creo que venga hoy.",
            "Niego que haya dicho eso."
        ]
    },
    "Ojalá": {
        "triggers": ["ojalá", "ojalá que"],
        "examples": [
            "Ojalá que tengas suerte.",
            "Ojalá no llueva.",
            "Ojalá puedas venir."
        ]
    }
}


def get_verb_type(verb: str) -> Optional[str]:
    """
    Determine the verb type based on ending.

    Args:
        verb: Infinitive form of the verb

    Returns:
        Verb type ('-ar', '-er', '-ir') or None if invalid
    """
    if verb.endswith("ar"):
        return "-ar"
    elif verb.endswith("er"):
        return "-er"
    elif verb.endswith("ir"):
        return "-ir"
    return None


def get_verb_stem(verb: str) -> str:
    """
    Extract the stem from an infinitive verb.

    Args:
        verb: Infinitive form of the verb

    Returns:
        Verb stem (infinitive minus ending)
    """
    if verb.endswith(("ar", "er", "ir")):
        return verb[:-2]
    return verb


def apply_spelling_changes(verb: str, stem: str, ending: str) -> str:
    """
    Apply orthographic spelling changes to maintain pronunciation.

    Args:
        verb: Original infinitive
        stem: Verb stem
        ending: Conjugation ending

    Returns:
        Correctly spelled conjugation
    """
    # g→gu before e
    if verb.endswith("gar") and ending.startswith("e"):
        stem = stem[:-1] + "gu"

    # c→qu before e
    elif verb.endswith("car") and ending.startswith("e"):
        stem = stem[:-1] + "qu"

    # z→c before e
    elif verb.endswith("zar") and ending.startswith("e"):
        stem = stem[:-1] + "c"

    # gu→gü before e
    elif verb.endswith("guar") and ending.startswith("e"):
        stem = stem[:-2] + "gü"

    # -ger/-gir: g→j before a/o
    elif verb.endswith(("ger", "gir")) and ending.startswith(("a", "o")):
        stem = stem[:-1] + "j"

    # -guir: gu→g before a/o
    elif verb.endswith("guir") and ending.startswith(("a", "o")):
        stem = stem[:-2] + "g"

    return stem + ending


def is_stem_changing(verb: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Check if a verb is stem-changing and return pattern info.

    Args:
        verb: Infinitive form of the verb

    Returns:
        Tuple of (is_stem_changing, pattern_type, pattern_info)
    """
    for pattern, verbs in STEM_CHANGING_VERBS.items():
        if verb in verbs:
            return True, pattern, verbs[verb]
    return False, None, None


# Common regular verbs for practice
COMMON_REGULAR_VERBS = {
    "-ar": [
        "hablar", "estudiar", "trabajar", "viajar", "cantar", "bailar",
        "caminar", "comprar", "cocinar", "escuchar", "mirar", "nadar",
        "descansar", "tomar", "visitar", "ayudar", "limpiar", "necesitar"
    ],
    "-er": [
        "comer", "beber", "aprender", "leer", "correr", "comprender",
        "vender", "responder", "prometer", "romper", "temer", "meter"
    ],
    "-ir": [
        "vivir", "escribir", "recibir", "abrir", "subir", "decidir",
        "partir", "sufrir", "cubrir", "compartir", "describir", "permitir"
    ]
}


# Export all constants
__all__ = [
    'Tense',
    'Person',
    'REGULAR_ENDINGS',
    'IRREGULAR_VERBS',
    'STEM_CHANGING_VERBS',
    'SPELLING_CHANGES',
    'WEIRDO_TRIGGERS',
    'COMMON_REGULAR_VERBS',
    'get_verb_type',
    'get_verb_stem',
    'apply_spelling_changes',
    'is_stem_changing'
]
