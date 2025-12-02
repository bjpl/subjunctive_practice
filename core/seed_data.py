"""
Seed data for initial database setup.
Contains common Spanish verbs and sample exercises.
"""

from models.exercise import VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel

# Common Spanish verbs with subjunctive conjugations
SEED_VERBS = [
    {
        "infinitive": "hablar",
        "english_translation": "to speak",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 10,
        "present_subjunctive": {
            "yo": "hable",
            "tú": "hables",
            "él/ella/usted": "hable",
            "nosotros": "hablemos",
            "vosotros": "habléis",
            "ellos/ellas/ustedes": "hablen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "hablara",
            "tú": "hablaras",
            "él/ella/usted": "hablara",
            "nosotros": "habláramos",
            "vosotros": "hablarais",
            "ellos/ellas/ustedes": "hablaran"
        },
        "imperfect_subjunctive_se": {
            "yo": "hablase",
            "tú": "hablases",
            "él/ella/usted": "hablase",
            "nosotros": "hablásemos",
            "vosotros": "hablaseis",
            "ellos/ellas/ustedes": "hablasen"
        }
    },
    {
        "infinitive": "ser",
        "english_translation": "to be",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 1,
        "irregularity_notes": "Highly irregular verb, completely changes stem",
        "present_subjunctive": {
            "yo": "sea",
            "tú": "seas",
            "él/ella/usted": "sea",
            "nosotros": "seamos",
            "vosotros": "seáis",
            "ellos/ellas/ustedes": "sean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "fuera",
            "tú": "fueras",
            "él/ella/usted": "fuera",
            "nosotros": "fuéramos",
            "vosotros": "fuerais",
            "ellos/ellas/ustedes": "fueran"
        },
        "imperfect_subjunctive_se": {
            "yo": "fuese",
            "tú": "fueses",
            "él/ella/usted": "fuese",
            "nosotros": "fuésemos",
            "vosotros": "fueseis",
            "ellos/ellas/ustedes": "fuesen"
        }
    },
    {
        "infinitive": "estar",
        "english_translation": "to be",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 2,
        "irregularity_notes": "Irregular in present subjunctive stem",
        "present_subjunctive": {
            "yo": "esté",
            "tú": "estés",
            "él/ella/usted": "esté",
            "nosotros": "estemos",
            "vosotros": "estéis",
            "ellos/ellas/ustedes": "estén"
        },
        "imperfect_subjunctive_ra": {
            "yo": "estuviera",
            "tú": "estuvieras",
            "él/ella/usted": "estuviera",
            "nosotros": "estuviéramos",
            "vosotros": "estuvierais",
            "ellos/ellas/ustedes": "estuvieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "estuviese",
            "tú": "estuvieses",
            "él/ella/usted": "estuviese",
            "nosotros": "estuviésemos",
            "vosotros": "estuvieseis",
            "ellos/ellas/ustedes": "estuviesen"
        }
    },
    {
        "infinitive": "tener",
        "english_translation": "to have",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 3,
        "irregularity_notes": "Stem-changing e>ie, irregular stem in subjunctive",
        "present_subjunctive": {
            "yo": "tenga",
            "tú": "tengas",
            "él/ella/usted": "tenga",
            "nosotros": "tengamos",
            "vosotros": "tengáis",
            "ellos/ellas/ustedes": "tengan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "tuviera",
            "tú": "tuvieras",
            "él/ella/usted": "tuviera",
            "nosotros": "tuviéramos",
            "vosotros": "tuvierais",
            "ellos/ellas/ustedes": "tuvieran"
        }
    },
    {
        "infinitive": "hacer",
        "english_translation": "to do/make",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 4,
        "present_subjunctive": {
            "yo": "haga",
            "tú": "hagas",
            "él/ella/usted": "haga",
            "nosotros": "hagamos",
            "vosotros": "hagáis",
            "ellos/ellas/ustedes": "hagan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "hiciera",
            "tú": "hicieras",
            "él/ella/usted": "hiciera",
            "nosotros": "hiciéramos",
            "vosotros": "hicierais",
            "ellos/ellas/ustedes": "hicieran"
        }
    },
    {
        "infinitive": "poder",
        "english_translation": "to be able to/can",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": True,
        "frequency_rank": 5,
        "irregularity_notes": "Stem-changing o>ue",
        "present_subjunctive": {
            "yo": "pueda",
            "tú": "puedas",
            "él/ella/usted": "pueda",
            "nosotros": "podamos",
            "vosotros": "podáis",
            "ellos/ellas/ustedes": "puedan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pudiera",
            "tú": "pudieras",
            "él/ella/usted": "pudiera",
            "nosotros": "pudiéramos",
            "vosotros": "pudierais",
            "ellos/ellas/ustedes": "pudieran"
        }
    },
    {
        "infinitive": "ir",
        "english_translation": "to go",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 6,
        "irregularity_notes": "Completely irregular",
        "present_subjunctive": {
            "yo": "vaya",
            "tú": "vayas",
            "él/ella/usted": "vaya",
            "nosotros": "vayamos",
            "vosotros": "vayáis",
            "ellos/ellas/ustedes": "vayan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "fuera",
            "tú": "fueras",
            "él/ella/usted": "fuera",
            "nosotros": "fuéramos",
            "vosotros": "fuerais",
            "ellos/ellas/ustedes": "fueran"
        }
    },
    {
        "infinitive": "ver",
        "english_translation": "to see",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 7,
        "present_subjunctive": {
            "yo": "vea",
            "tú": "veas",
            "él/ella/usted": "vea",
            "nosotros": "veamos",
            "vosotros": "veáis",
            "ellos/ellas/ustedes": "vean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "viera",
            "tú": "vieras",
            "él/ella/usted": "viera",
            "nosotros": "viéramos",
            "vosotros": "vierais",
            "ellos/ellas/ustedes": "vieran"
        }
    },
    {
        "infinitive": "dar",
        "english_translation": "to give",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 8,
        "present_subjunctive": {
            "yo": "dé",
            "tú": "des",
            "él/ella/usted": "dé",
            "nosotros": "demos",
            "vosotros": "deis",
            "ellos/ellas/ustedes": "den"
        },
        "imperfect_subjunctive_ra": {
            "yo": "diera",
            "tú": "dieras",
            "él/ella/usted": "diera",
            "nosotros": "diéramos",
            "vosotros": "dierais",
            "ellos/ellas/ustedes": "dieran"
        }
    },
    {
        "infinitive": "saber",
        "english_translation": "to know",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 9,
        "present_subjunctive": {
            "yo": "sepa",
            "tú": "sepas",
            "él/ella/usted": "sepa",
            "nosotros": "sepamos",
            "vosotros": "sepáis",
            "ellos/ellas/ustedes": "sepan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "supiera",
            "tú": "supieras",
            "él/ella/usted": "supiera",
            "nosotros": "supiéramos",
            "vosotros": "supierais",
            "ellos/ellas/ustedes": "supieran"
        }
    },
    {
        "infinitive": "querer",
        "english_translation": "to want/love",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": True,
        "frequency_rank": 11,
        "irregularity_notes": "Stem-changing e>ie",
        "present_subjunctive": {
            "yo": "quiera",
            "tú": "quieras",
            "él/ella/usted": "quiera",
            "nosotros": "queramos",
            "vosotros": "queráis",
            "ellos/ellas/ustedes": "quieran"
        },
        "imperfect_subjunctive_ra": {
            "yo": "quisiera",
            "tú": "quisieras",
            "él/ella/usted": "quisiera",
            "nosotros": "quisiéramos",
            "vosotros": "quisierais",
            "ellos/ellas/ustedes": "quisieran"
        }
    },
    {
        "infinitive": "pensar",
        "english_translation": "to think",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 12,
        "irregularity_notes": "Stem-changing e>ie",
        "present_subjunctive": {
            "yo": "piense",
            "tú": "pienses",
            "él/ella/usted": "piense",
            "nosotros": "pensemos",
            "vosotros": "penséis",
            "ellos/ellas/ustedes": "piensen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pensara",
            "tú": "pensaras",
            "él/ella/usted": "pensara",
            "nosotros": "pensáramos",
            "vosotros": "pensarais",
            "ellos/ellas/ustedes": "pensaran"
        }
    },
    {
        "infinitive": "venir",
        "english_translation": "to come",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 13,
        "irregularity_notes": "Stem-changing e>ie, irregular stem",
        "present_subjunctive": {
            "yo": "venga",
            "tú": "vengas",
            "él/ella/usted": "venga",
            "nosotros": "vengamos",
            "vosotros": "vengáis",
            "ellos/ellas/ustedes": "vengan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "viniera",
            "tú": "vinieras",
            "él/ella/usted": "viniera",
            "nosotros": "viniéramos",
            "vosotros": "vinierais",
            "ellos/ellas/ustedes": "vinieran"
        }
    },
    {
        "infinitive": "decir",
        "english_translation": "to say/tell",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 14,
        "irregularity_notes": "Stem-changing e>i, irregular stem",
        "present_subjunctive": {
            "yo": "diga",
            "tú": "digas",
            "él/ella/usted": "diga",
            "nosotros": "digamos",
            "vosotros": "digáis",
            "ellos/ellas/ustedes": "digan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "dijera",
            "tú": "dijeras",
            "él/ella/usted": "dijera",
            "nosotros": "dijéramos",
            "vosotros": "dijerais",
            "ellos/ellas/ustedes": "dijeran"
        }
    },
    {
        "infinitive": "encontrar",
        "english_translation": "to find",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 15,
        "irregularity_notes": "Stem-changing o>ue",
        "present_subjunctive": {
            "yo": "encuentre",
            "tú": "encuentres",
            "él/ella/usted": "encuentre",
            "nosotros": "encontremos",
            "vosotros": "encontréis",
            "ellos/ellas/ustedes": "encuentren"
        },
        "imperfect_subjunctive_ra": {
            "yo": "encontrara",
            "tú": "encontraras",
            "él/ella/usted": "encontrara",
            "nosotros": "encontráramos",
            "vosotros": "encontrarais",
            "ellos/ellas/ustedes": "encontraran"
        }
    },
    {
        "infinitive": "pedir",
        "english_translation": "to ask for/request",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 16,
        "irregularity_notes": "Stem-changing e>i",
        "present_subjunctive": {
            "yo": "pida",
            "tú": "pidas",
            "él/ella/usted": "pida",
            "nosotros": "pidamos",
            "vosotros": "pidáis",
            "ellos/ellas/ustedes": "pidan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pidiera",
            "tú": "pidieras",
            "él/ella/usted": "pidiera",
            "nosotros": "pidiéramos",
            "vosotros": "pidierais",
            "ellos/ellas/ustedes": "pidieran"
        }
    },
    {
        "infinitive": "sentir",
        "english_translation": "to feel",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 17,
        "irregularity_notes": "Stem-changing e>ie/i",
        "present_subjunctive": {
            "yo": "sienta",
            "tú": "sientas",
            "él/ella/usted": "sienta",
            "nosotros": "sintamos",
            "vosotros": "sintáis",
            "ellos/ellas/ustedes": "sientan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "sintiera",
            "tú": "sintieras",
            "él/ella/usted": "sintiera",
            "nosotros": "sintiéramos",
            "vosotros": "sintierais",
            "ellos/ellas/ustedes": "sintieran"
        }
    },
    {
        "infinitive": "dormir",
        "english_translation": "to sleep",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 18,
        "irregularity_notes": "Stem-changing o>ue/u",
        "present_subjunctive": {
            "yo": "duerma",
            "tú": "duermas",
            "él/ella/usted": "duerma",
            "nosotros": "durmamos",
            "vosotros": "durmáis",
            "ellos/ellas/ustedes": "duerman"
        },
        "imperfect_subjunctive_ra": {
            "yo": "durmiera",
            "tú": "durmieras",
            "él/ella/usted": "durmiera",
            "nosotros": "durmiéramos",
            "vosotros": "durmierais",
            "ellos/ellas/ustedes": "durmieran"
        }
    },
    {
        "infinitive": "vivir",
        "english_translation": "to live",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 19,
        "present_subjunctive": {
            "yo": "viva",
            "tú": "vivas",
            "él/ella/usted": "viva",
            "nosotros": "vivamos",
            "vosotros": "viváis",
            "ellos/ellas/ustedes": "vivan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "viviera",
            "tú": "vivieras",
            "él/ella/usted": "viviera",
            "nosotros": "viviéramos",
            "vosotros": "vivierais",
            "ellos/ellas/ustedes": "vivieran"
        }
    },
    {
        "infinitive": "creer",
        "english_translation": "to believe",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 20,
        "present_subjunctive": {
            "yo": "crea",
            "tú": "creas",
            "él/ella/usted": "crea",
            "nosotros": "creamos",
            "vosotros": "creáis",
            "ellos/ellas/ustedes": "crean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "creyera",
            "tú": "creyeras",
            "él/ella/usted": "creyera",
            "nosotros": "creyéramos",
            "vosotros": "creyerais",
            "ellos/ellas/ustedes": "creyeran"
        }
    },
    {
        "infinitive": "estudiar",
        "english_translation": "to study",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 21,
        "present_subjunctive": {
            "yo": "estudie",
            "tú": "estudies",
            "él/ella/usted": "estudie",
            "nosotros": "estudiemos",
            "vosotros": "estudiéis",
            "ellos/ellas/ustedes": "estudien"
        },
        "imperfect_subjunctive_ra": {
            "yo": "estudiara",
            "tú": "estudiaras",
            "él/ella/usted": "estudiara",
            "nosotros": "estudiáramos",
            "vosotros": "estudiarais",
            "ellos/ellas/ustedes": "estudiaran"
        }
    },
    {
        "infinitive": "trabajar",
        "english_translation": "to work",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 22,
        "present_subjunctive": {
            "yo": "trabaje",
            "tú": "trabajes",
            "él/ella/usted": "trabaje",
            "nosotros": "trabajemos",
            "vosotros": "trabajéis",
            "ellos/ellas/ustedes": "trabajen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "trabajara",
            "tú": "trabajaras",
            "él/ella/usted": "trabajara",
            "nosotros": "trabajáramos",
            "vosotros": "trabajarais",
            "ellos/ellas/ustedes": "trabajaran"
        }
    },
    {
        "infinitive": "cantar",
        "english_translation": "to sing",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 23,
        "present_subjunctive": {
            "yo": "cante",
            "tú": "cantes",
            "él/ella/usted": "cante",
            "nosotros": "cantemos",
            "vosotros": "cantéis",
            "ellos/ellas/ustedes": "canten"
        },
        "imperfect_subjunctive_ra": {
            "yo": "cantara",
            "tú": "cantaras",
            "él/ella/usted": "cantara",
            "nosotros": "cantáramos",
            "vosotros": "cantarais",
            "ellos/ellas/ustedes": "cantaran"
        }
    },
    {
        "infinitive": "llegar",
        "english_translation": "to arrive",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 24,
        "irregularity_notes": "Spelling change: g→gu before e",
        "present_subjunctive": {
            "yo": "llegue",
            "tú": "llegues",
            "él/ella/usted": "llegue",
            "nosotros": "lleguemos",
            "vosotros": "lleguéis",
            "ellos/ellas/ustedes": "lleguen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "llegara",
            "tú": "llegaras",
            "él/ella/usted": "llegara",
            "nosotros": "llegáramos",
            "vosotros": "llegarais",
            "ellos/ellas/ustedes": "llegaran"
        }
    },
    {
        "infinitive": "comer",
        "english_translation": "to eat",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 25,
        "present_subjunctive": {
            "yo": "coma",
            "tú": "comas",
            "él/ella/usted": "coma",
            "nosotros": "comamos",
            "vosotros": "comáis",
            "ellos/ellas/ustedes": "coman"
        },
        "imperfect_subjunctive_ra": {
            "yo": "comiera",
            "tú": "comieras",
            "él/ella/usted": "comiera",
            "nosotros": "comiéramos",
            "vosotros": "comierais",
            "ellos/ellas/ustedes": "comieran"
        }
    },
    {
        "infinitive": "beber",
        "english_translation": "to drink",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 26,
        "present_subjunctive": {
            "yo": "beba",
            "tú": "bebas",
            "él/ella/usted": "beba",
            "nosotros": "bebamos",
            "vosotros": "bebáis",
            "ellos/ellas/ustedes": "beban"
        },
        "imperfect_subjunctive_ra": {
            "yo": "bebiera",
            "tú": "bebieras",
            "él/ella/usted": "bebiera",
            "nosotros": "bebiéramos",
            "vosotros": "bebierais",
            "ellos/ellas/ustedes": "bebieran"
        }
    },
    {
        "infinitive": "abrir",
        "english_translation": "to open",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 27,
        "present_subjunctive": {
            "yo": "abra",
            "tú": "abras",
            "él/ella/usted": "abra",
            "nosotros": "abramos",
            "vosotros": "abráis",
            "ellos/ellas/ustedes": "abran"
        },
        "imperfect_subjunctive_ra": {
            "yo": "abriera",
            "tú": "abrieras",
            "él/ella/usted": "abriera",
            "nosotros": "abriéramos",
            "vosotros": "abrierais",
            "ellos/ellas/ustedes": "abrieran"
        }
    },
    {
        "infinitive": "escribir",
        "english_translation": "to write",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 28,
        "present_subjunctive": {
            "yo": "escriba",
            "tú": "escribas",
            "él/ella/usted": "escriba",
            "nosotros": "escribamos",
            "vosotros": "escribáis",
            "ellos/ellas/ustedes": "escriban"
        },
        "imperfect_subjunctive_ra": {
            "yo": "escribiera",
            "tú": "escribieras",
            "él/ella/usted": "escribiera",
            "nosotros": "escribiéramos",
            "vosotros": "escribierais",
            "ellos/ellas/ustedes": "escribieran"
        }
    },
    {
        "infinitive": "cerrar",
        "english_translation": "to close",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 29,
        "irregularity_notes": "Stem-changing e>ie",
        "present_subjunctive": {
            "yo": "cierre",
            "tú": "cierres",
            "él/ella/usted": "cierre",
            "nosotros": "cerremos",
            "vosotros": "cerréis",
            "ellos/ellas/ustedes": "cierren"
        },
        "imperfect_subjunctive_ra": {
            "yo": "cerrara",
            "tú": "cerraras",
            "él/ella/usted": "cerrara",
            "nosotros": "cerráramos",
            "vosotros": "cerrarais",
            "ellos/ellas/ustedes": "cerraran"
        }
    },
    {
        "infinitive": "entender",
        "english_translation": "to understand",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 30,
        "irregularity_notes": "Stem-changing e>ie",
        "present_subjunctive": {
            "yo": "entienda",
            "tú": "entiendas",
            "él/ella/usted": "entienda",
            "nosotros": "entendamos",
            "vosotros": "entendáis",
            "ellos/ellas/ustedes": "entiendan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "entendiera",
            "tú": "entendieras",
            "él/ella/usted": "entendiera",
            "nosotros": "entendiéramos",
            "vosotros": "entendierais",
            "ellos/ellas/ustedes": "entendieran"
        }
    },
    {
        "infinitive": "volver",
        "english_translation": "to return",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 31,
        "irregularity_notes": "Stem-changing o>ue",
        "present_subjunctive": {
            "yo": "vuelva",
            "tú": "vuelvas",
            "él/ella/usted": "vuelva",
            "nosotros": "volvamos",
            "vosotros": "volváis",
            "ellos/ellas/ustedes": "vuelvan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "volviera",
            "tú": "volvieras",
            "él/ella/usted": "volviera",
            "nosotros": "volviéramos",
            "vosotros": "volvierais",
            "ellos/ellas/ustedes": "volvieran"
        }
    },
    {
        "infinitive": "servir",
        "english_translation": "to serve",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 32,
        "irregularity_notes": "Stem-changing e>i",
        "present_subjunctive": {
            "yo": "sirva",
            "tú": "sirvas",
            "él/ella/usted": "sirva",
            "nosotros": "sirvamos",
            "vosotros": "sirváis",
            "ellos/ellas/ustedes": "sirvan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "sirviera",
            "tú": "sirvieras",
            "él/ella/usted": "sirviera",
            "nosotros": "sirviéramos",
            "vosotros": "sirvierais",
            "ellos/ellas/ustedes": "sirvieran"
        }
    },
    {
        "infinitive": "repetir",
        "english_translation": "to repeat",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 33,
        "irregularity_notes": "Stem-changing e>i",
        "present_subjunctive": {
            "yo": "repita",
            "tú": "repitas",
            "él/ella/usted": "repita",
            "nosotros": "repitamos",
            "vosotros": "repitáis",
            "ellos/ellas/ustedes": "repitan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "repitiera",
            "tú": "repitieras",
            "él/ella/usted": "repitiera",
            "nosotros": "repitiéramos",
            "vosotros": "repitierais",
            "ellos/ellas/ustedes": "repitieran"
        }
    },
    {
        "infinitive": "empezar",
        "english_translation": "to begin/start",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 34,
        "irregularity_notes": "Stem-changing e>ie, spelling change z→c before e",
        "present_subjunctive": {
            "yo": "empiece",
            "tú": "empieces",
            "él/ella/usted": "empiece",
            "nosotros": "empecemos",
            "vosotros": "empecéis",
            "ellos/ellas/ustedes": "empiecen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "empezara",
            "tú": "empezaras",
            "él/ella/usted": "empezara",
            "nosotros": "empezáramos",
            "vosotros": "empezarais",
            "ellos/ellas/ustedes": "empezaran"
        }
    },
    {
        "infinitive": "terminar",
        "english_translation": "to finish",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 35,
        "present_subjunctive": {
            "yo": "termine",
            "tú": "termines",
            "él/ella/usted": "termine",
            "nosotros": "terminemos",
            "vosotros": "terminéis",
            "ellos/ellas/ustedes": "terminen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "terminara",
            "tú": "terminaras",
            "él/ella/usted": "terminara",
            "nosotros": "termináramos",
            "vosotros": "terminarais",
            "ellos/ellas/ustedes": "terminaran"
        }
    },
    {
        "infinitive": "salir",
        "english_translation": "to leave/go out",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 36,
        "irregularity_notes": "Irregular yo form: salgo → salg-",
        "present_subjunctive": {
            "yo": "salga",
            "tú": "salgas",
            "él/ella/usted": "salga",
            "nosotros": "salgamos",
            "vosotros": "salgáis",
            "ellos/ellas/ustedes": "salgan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "saliera",
            "tú": "salieras",
            "él/ella/usted": "saliera",
            "nosotros": "saliéramos",
            "vosotros": "salierais",
            "ellos/ellas/ustedes": "salieran"
        }
    },
    {
        "infinitive": "haber",
        "english_translation": "to have (auxiliary)",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 37,
        "irregularity_notes": "Highly irregular, used as auxiliary and impersonal 'hay'",
        "present_subjunctive": {
            "yo": "haya",
            "tú": "hayas",
            "él/ella/usted": "haya",
            "nosotros": "hayamos",
            "vosotros": "hayáis",
            "ellos/ellas/ustedes": "hayan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "hubiera",
            "tú": "hubieras",
            "él/ella/usted": "hubiera",
            "nosotros": "hubiéramos",
            "vosotros": "hubierais",
            "ellos/ellas/ustedes": "hubieran"
        },
        "imperfect_subjunctive_se": {
            "yo": "hubiese",
            "tú": "hubieses",
            "él/ella/usted": "hubiese",
            "nosotros": "hubiésemos",
            "vosotros": "hubieseis",
            "ellos/ellas/ustedes": "hubiesen"
        }
    },
    {
        "infinitive": "poner",
        "english_translation": "to put/place",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 38,
        "irregularity_notes": "Irregular yo form: pongo → pong-",
        "present_subjunctive": {
            "yo": "ponga",
            "tú": "pongas",
            "él/ella/usted": "ponga",
            "nosotros": "pongamos",
            "vosotros": "pongáis",
            "ellos/ellas/ustedes": "pongan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pusiera",
            "tú": "pusieras",
            "él/ella/usted": "pusiera",
            "nosotros": "pusiéramos",
            "vosotros": "pusierais",
            "ellos/ellas/ustedes": "pusieran"
        }
    },
    {
        "infinitive": "traer",
        "english_translation": "to bring",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 39,
        "irregularity_notes": "Irregular yo form: traigo → traig-",
        "present_subjunctive": {
            "yo": "traiga",
            "tú": "traigas",
            "él/ella/usted": "traiga",
            "nosotros": "traigamos",
            "vosotros": "traigáis",
            "ellos/ellas/ustedes": "traigan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "trajera",
            "tú": "trajeras",
            "él/ella/usted": "trajera",
            "nosotros": "trajéramos",
            "vosotros": "trajerais",
            "ellos/ellas/ustedes": "trajeran"
        }
    },
    {
        "infinitive": "conocer",
        "english_translation": "to know (person/place)",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 40,
        "irregularity_notes": "Spelling change: c→zc before a/o",
        "present_subjunctive": {
            "yo": "conozca",
            "tú": "conozcas",
            "él/ella/usted": "conozca",
            "nosotros": "conozcamos",
            "vosotros": "conozcáis",
            "ellos/ellas/ustedes": "conozcan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "conociera",
            "tú": "conocieras",
            "él/ella/usted": "conociera",
            "nosotros": "conociéramos",
            "vosotros": "conocierais",
            "ellos/ellas/ustedes": "conocieran"
        }
    },
    {
        "infinitive": "parecer",
        "english_translation": "to seem/appear",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 41,
        "irregularity_notes": "Spelling change: c→zc before a/o",
        "present_subjunctive": {
            "yo": "parezca",
            "tú": "parezcas",
            "él/ella/usted": "parezca",
            "nosotros": "parezcamos",
            "vosotros": "parezcáis",
            "ellos/ellas/ustedes": "parezcan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pareciera",
            "tú": "parecieras",
            "él/ella/usted": "pareciera",
            "nosotros": "pareciéramos",
            "vosotros": "parecierais",
            "ellos/ellas/ustedes": "parecieran"
        }
    },
    {
        "infinitive": "seguir",
        "english_translation": "to follow/continue",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": True,
        "frequency_rank": 42,
        "irregularity_notes": "Stem-changing e>i, spelling change gu→g before a/o",
        "present_subjunctive": {
            "yo": "siga",
            "tú": "sigas",
            "él/ella/usted": "siga",
            "nosotros": "sigamos",
            "vosotros": "sigáis",
            "ellos/ellas/ustedes": "sigan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "siguiera",
            "tú": "siguieras",
            "él/ella/usted": "siguiera",
            "nosotros": "siguiéramos",
            "vosotros": "siguierais",
            "ellos/ellas/ustedes": "siguieran"
        }
    },
    {
        "infinitive": "morir",
        "english_translation": "to die",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 43,
        "irregularity_notes": "Stem-changing o>ue/u",
        "present_subjunctive": {
            "yo": "muera",
            "tú": "mueras",
            "él/ella/usted": "muera",
            "nosotros": "muramos",
            "vosotros": "muráis",
            "ellos/ellas/ustedes": "mueran"
        },
        "imperfect_subjunctive_ra": {
            "yo": "muriera",
            "tú": "murieras",
            "él/ella/usted": "muriera",
            "nosotros": "muriéramos",
            "vosotros": "murierais",
            "ellos/ellas/ustedes": "murieran"
        }
    },
    {
        "infinitive": "leer",
        "english_translation": "to read",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 44,
        "irregularity_notes": "Spelling change: i→y between vowels",
        "present_subjunctive": {
            "yo": "lea",
            "tú": "leas",
            "él/ella/usted": "lea",
            "nosotros": "leamos",
            "vosotros": "leáis",
            "ellos/ellas/ustedes": "lean"
        },
        "imperfect_subjunctive_ra": {
            "yo": "leyera",
            "tú": "leyeras",
            "él/ella/usted": "leyera",
            "nosotros": "leyéramos",
            "vosotros": "leyerais",
            "ellos/ellas/ustedes": "leyeran"
        }
    },
    {
        "infinitive": "oír",
        "english_translation": "to hear",
        "verb_type": VerbType.IRREGULAR,
        "is_irregular": True,
        "frequency_rank": 45,
        "irregularity_notes": "Irregular: y inserted, accent changes",
        "present_subjunctive": {
            "yo": "oiga",
            "tú": "oigas",
            "él/ella/usted": "oiga",
            "nosotros": "oigamos",
            "vosotros": "oigáis",
            "ellos/ellas/ustedes": "oigan"
        },
        "imperfect_subjunctive_ra": {
            "yo": "oyera",
            "tú": "oyeras",
            "él/ella/usted": "oyera",
            "nosotros": "oyéramos",
            "vosotros": "oyerais",
            "ellos/ellas/ustedes": "oyeran"
        }
    },
    {
        "infinitive": "buscar",
        "english_translation": "to search/look for",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 46,
        "irregularity_notes": "Spelling change: c→qu before e",
        "present_subjunctive": {
            "yo": "busque",
            "tú": "busques",
            "él/ella/usted": "busque",
            "nosotros": "busquemos",
            "vosotros": "busquéis",
            "ellos/ellas/ustedes": "busquen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "buscara",
            "tú": "buscaras",
            "él/ella/usted": "buscara",
            "nosotros": "buscáramos",
            "vosotros": "buscarais",
            "ellos/ellas/ustedes": "buscaran"
        }
    },
    {
        "infinitive": "pagar",
        "english_translation": "to pay",
        "verb_type": VerbType.REGULAR,
        "is_irregular": False,
        "frequency_rank": 47,
        "irregularity_notes": "Spelling change: g→gu before e",
        "present_subjunctive": {
            "yo": "pague",
            "tú": "pagues",
            "él/ella/usted": "pague",
            "nosotros": "paguemos",
            "vosotros": "paguéis",
            "ellos/ellas/ustedes": "paguen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "pagara",
            "tú": "pagaras",
            "él/ella/usted": "pagara",
            "nosotros": "pagáramos",
            "vosotros": "pagarais",
            "ellos/ellas/ustedes": "pagaran"
        }
    },
    {
        "infinitive": "jugar",
        "english_translation": "to play",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 48,
        "irregularity_notes": "Stem-changing u>ue, spelling change g→gu before e",
        "present_subjunctive": {
            "yo": "juegue",
            "tú": "juegues",
            "él/ella/usted": "juegue",
            "nosotros": "juguemos",
            "vosotros": "juguéis",
            "ellos/ellas/ustedes": "jueguen"
        },
        "imperfect_subjunctive_ra": {
            "yo": "jugara",
            "tú": "jugaras",
            "él/ella/usted": "jugara",
            "nosotros": "jugáramos",
            "vosotros": "jugarais",
            "ellos/ellas/ustedes": "jugaran"
        }
    },
    {
        "infinitive": "contar",
        "english_translation": "to count/tell",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 49,
        "irregularity_notes": "Stem-changing o>ue",
        "present_subjunctive": {
            "yo": "cuente",
            "tú": "cuentes",
            "él/ella/usted": "cuente",
            "nosotros": "contemos",
            "vosotros": "contéis",
            "ellos/ellas/ustedes": "cuenten"
        },
        "imperfect_subjunctive_ra": {
            "yo": "contara",
            "tú": "contaras",
            "él/ella/usted": "contara",
            "nosotros": "contáramos",
            "vosotros": "contarais",
            "ellos/ellas/ustedes": "contaran"
        }
    },
    {
        "infinitive": "recordar",
        "english_translation": "to remember",
        "verb_type": VerbType.STEM_CHANGING,
        "is_irregular": False,
        "frequency_rank": 50,
        "irregularity_notes": "Stem-changing o>ue",
        "present_subjunctive": {
            "yo": "recuerde",
            "tú": "recuerdes",
            "él/ella/usted": "recuerde",
            "nosotros": "recordemos",
            "vosotros": "recordéis",
            "ellos/ellas/ustedes": "recuerden"
        },
        "imperfect_subjunctive_ra": {
            "yo": "recordara",
            "tú": "recordaras",
            "él/ella/usted": "recordara",
            "nosotros": "recordáramos",
            "vosotros": "recordarais",
            "ellos/ellas/ustedes": "recordaran"
        }
    },
]

# Sample achievements
SEED_ACHIEVEMENTS = [
    {
        "name": "First Steps",
        "description": "Complete your first exercise",
        "category": "milestone",
        "points": 10,
        "criteria": {"exercises_completed": 1}
    },
    {
        "name": "Week Warrior",
        "description": "Maintain a 7-day streak",
        "category": "streak",
        "points": 50,
        "criteria": {"streak_days": 7}
    },
    {
        "name": "Century Club",
        "description": "Answer 100 questions correctly",
        "category": "mastery",
        "points": 100,
        "criteria": {"correct_answers": 100}
    },
    {
        "name": "Perfect Session",
        "description": "Get 100% in a session with 10+ exercises",
        "category": "practice",
        "points": 25,
        "criteria": {"perfect_session": True, "min_exercises": 10}
    },
    {
        "name": "Subjunctive Master",
        "description": "Master 20 different verbs",
        "category": "mastery",
        "points": 200,
        "criteria": {"verbs_mastered": 20}
    },
]
