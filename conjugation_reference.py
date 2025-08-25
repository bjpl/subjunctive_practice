"""
Conjugation reference tables for Spanish subjunctive
"""

SUBJUNCTIVE_ENDINGS = {
    "Present Subjunctive": {
        "-ar": {
            "yo": "-e",
            "tú": "-es", 
            "él/ella/usted": "-e",
            "nosotros": "-emos",
            "vosotros": "-éis",
            "ellos/ellas/ustedes": "-en"
        },
        "-er/-ir": {
            "yo": "-a",
            "tú": "-as",
            "él/ella/usted": "-a", 
            "nosotros": "-amos",
            "vosotros": "-áis",
            "ellos/ellas/ustedes": "-an"
        }
    },
    "Imperfect Subjunctive (ra)": {
        "-ar": {
            "yo": "-ara",
            "tú": "-aras",
            "él/ella/usted": "-ara",
            "nosotros": "-áramos",
            "vosotros": "-arais", 
            "ellos/ellas/ustedes": "-aran"
        },
        "-er/-ir": {
            "yo": "-iera",
            "tú": "-ieras",
            "él/ella/usted": "-iera",
            "nosotros": "-iéramos",
            "vosotros": "-ierais",
            "ellos/ellas/ustedes": "-ieran"
        }
    },
    "Imperfect Subjunctive (se)": {
        "-ar": {
            "yo": "-ase",
            "tú": "-ases",
            "él/ella/usted": "-ase",
            "nosotros": "-ásemos",
            "vosotros": "-aseis",
            "ellos/ellas/ustedes": "-asen"
        },
        "-er/-ir": {
            "yo": "-iese",
            "tú": "-ieses", 
            "él/ella/usted": "-iese",
            "nosotros": "-iésemos",
            "vosotros": "-ieseis",
            "ellos/ellas/ustedes": "-iesen"
        }
    }
}

COMMON_IRREGULAR_VERBS = {
    "ser": {
        "Present Subjunctive": ["sea", "seas", "sea", "seamos", "seáis", "sean"],
        "Imperfect Subjunctive": ["fuera/fuese", "fueras/fueses", "fuera/fuese", "fuéramos/fuésemos", "fuerais/fueseis", "fueran/fuesen"]
    },
    "estar": {
        "Present Subjunctive": ["esté", "estés", "esté", "estemos", "estéis", "estén"],
        "Imperfect Subjunctive": ["estuviera/estuviese", "estuvieras/estuvieses", "estuviera/estuviese", "estuviéramos/estuviésemos", "estuvierais/estuvieseis", "estuvieran/estuviesen"]
    },
    "haber": {
        "Present Subjunctive": ["haya", "hayas", "haya", "hayamos", "hayáis", "hayan"],
        "Imperfect Subjunctive": ["hubiera/hubiese", "hubieras/hubieses", "hubiera/hubiese", "hubiéramos/hubiésemos", "hubierais/hubieseis", "hubieran/hubiesen"]
    },
    "tener": {
        "Present Subjunctive": ["tenga", "tengas", "tenga", "tengamos", "tengáis", "tengan"],
        "Imperfect Subjunctive": ["tuviera/tuviese", "tuvieras/tuvieses", "tuviera/tuviese", "tuviéramos/tuviésemos", "tuvierais/tuvieseis", "tuvieran/tuviesen"]
    },
    "hacer": {
        "Present Subjunctive": ["haga", "hagas", "haga", "hagamos", "hagáis", "hagan"],
        "Imperfect Subjunctive": ["hiciera/hiciese", "hicieras/hicieses", "hiciera/hiciese", "hiciéramos/hiciésemos", "hicierais/hicieseis", "hicieran/hiciesen"]
    },
    "ir": {
        "Present Subjunctive": ["vaya", "vayas", "vaya", "vayamos", "vayáis", "vayan"],
        "Imperfect Subjunctive": ["fuera/fuese", "fueras/fueses", "fuera/fuese", "fuéramos/fuésemos", "fuerais/fueseis", "fueran/fuesen"]
    },
    "saber": {
        "Present Subjunctive": ["sepa", "sepas", "sepa", "sepamos", "sepáis", "sepan"],
        "Imperfect Subjunctive": ["supiera/supiese", "supieras/supieses", "supiera/supiese", "supiéramos/supiésemos", "supierais/supieseis", "supieran/supiesen"]
    },
    "poder": {
        "Present Subjunctive": ["pueda", "puedas", "pueda", "podamos", "podáis", "puedan"],
        "Imperfect Subjunctive": ["pudiera/pudiese", "pudieras/pudieses", "pudiera/pudiese", "pudiéramos/pudiésemos", "pudierais/pudieseis", "pudieran/pudiesen"]
    }
}

STEM_CHANGING_PATTERNS = {
    "e->ie": ["pensar", "querer", "sentir", "preferir", "entender", "perder"],
    "o->ue": ["poder", "dormir", "volver", "contar", "mover", "morir"],
    "e->i": ["pedir", "servir", "repetir", "seguir", "vestir", "competir"],
    "u->ue": ["jugar"],
    "i->ie": ["adquirir", "inquirir"]
}

SEQUENCE_OF_TENSES = {
    "Present/Future Main": ["Present Subjunctive", "Present Perfect Subjunctive"],
    "Past Main": ["Imperfect Subjunctive", "Pluperfect Subjunctive"],
    "Conditional Main": ["Imperfect Subjunctive"]
}

COMMON_ERRORS = {
    "using_infinitive": "Remember to conjugate the verb, not use the infinitive",
    "wrong_mood": "This requires subjunctive, not indicative mood",
    "wrong_tense": "Check the sequence of tenses - past main clause needs past subjunctive",
    "missing_que": "Don't forget 'que' between the clauses",
    "stem_change_missing": "This verb has a stem change in subjunctive"
}

SUBJUNCTIVE_TRIGGERS = {
    "Wishes & Desires": [
        "querer que", "desear que", "esperar que", "preferir que", 
        "ojalá (que)", "pedir que", "rogar que", "suplicar que"
    ],
    "Emotions": [
        "alegrarse de que", "sentir que", "temer que", "gustar que",
        "molestar que", "sorprender que", "estar contento de que", "lamentar que"
    ],
    "Doubt & Denial": [
        "dudar que", "no creer que", "no pensar que", "negar que",
        "no estar seguro de que", "no es cierto que", "es posible que", "es probable que"
    ],
    "Impersonal Expressions": [
        "es necesario que", "es importante que", "es bueno que", "es malo que",
        "es mejor que", "es peor que", "es urgente que", "conviene que"
    ],
    "Conjunctions": [
        "para que", "antes de que", "después de que", "hasta que",
        "a menos que", "con tal de que", "sin que", "aunque", "cuando (future)"
    ],
    "Relative Clauses": [
        "busco a alguien que...", "no hay nadie que...", "¿conoces a alguien que...?",
        "necesito algo que...", "no existe nada que..."
    ]
}

def get_conjugation_table(verb: str, tense: str) -> dict:
    """Get conjugation table for a specific verb and tense"""
    if verb in COMMON_IRREGULAR_VERBS and tense in COMMON_IRREGULAR_VERBS[verb]:
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        return dict(zip(persons, COMMON_IRREGULAR_VERBS[verb][tense]))
    
    # For regular verbs, return the endings
    if tense in SUBJUNCTIVE_ENDINGS:
        if verb.endswith("ar"):
            return SUBJUNCTIVE_ENDINGS[tense]["-ar"]
        else:
            return SUBJUNCTIVE_ENDINGS[tense]["-er/-ir"]
    
    return {}