"""
Seed data for initial database setup.
Contains common Spanish verbs and sample exercises.
"""

from backend.models.exercise import VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel

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
