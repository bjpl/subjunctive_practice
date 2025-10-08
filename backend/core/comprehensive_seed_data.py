"""
Comprehensive seed data for Spanish subjunctive practice application.

This file contains pedagogically-sound exercise content organized by:
- Difficulty level (EASY → EXPERT)
- Subjunctive trigger types (emotion, doubt, wishes, impersonal, conjunctions)
- Verb types (regular, stem-changing, irregular)
- Authentic contexts and scenarios

Based on research of Spanish language pedagogy and CEFR levels.
"""

from models.exercise import ExerciseType, SubjunctiveTense, DifficultyLevel

# ==============================================================================
# SUBJUNCTIVE TRIGGER PHRASES
# ==============================================================================

TRIGGER_PHRASES = {
    "emotion": [
        "espero que",  # I hope that
        "me alegra que",  # I'm happy that
        "temo que",  # I fear that
        "me molesta que",  # it bothers me that
        "me gusta que",  # I like that
        "siento que",  # I'm sorry that
        "me sorprende que",  # it surprises me that
        "me preocupa que",  # it worries me that
    ],
    "doubt_negation": [
        "dudo que",  # I doubt that
        "no creo que",  # I don't believe that
        "no pienso que",  # I don't think that
        "no es cierto que",  # it's not certain that
        "no es verdad que",  # it's not true that
        "es imposible que",  # it's impossible that
    ],
    "wishes_requests": [
        "quiero que",  # I want that
        "prefiero que",  # I prefer that
        "sugiero que",  # I suggest that
        "recomiendo que",  # I recommend that
        "pido que",  # I ask that
        "necesito que",  # I need that
        "deseo que",  # I wish that
    ],
    "impersonal": [
        "es importante que",  # it's important that
        "es necesario que",  # it's necessary that
        "es posible que",  # it's possible that
        "es mejor que",  # it's better that
        "es bueno que",  # it's good that
        "es malo que",  # it's bad that
        "es raro que",  # it's strange that
    ],
    "conjunctions": [
        "cuando",  # when (future)
        "aunque",  # although
        "para que",  # so that
        "sin que",  # without
        "antes de que",  # before
        "después de que",  # after
        "hasta que",  # until
        "a menos que",  # unless
    ]
}

# ==============================================================================
# COMPREHENSIVE EXERCISE SEED DATA
# ==============================================================================

SEED_EXERCISES = [

    # ==========================================================================
    # EASY LEVEL: Regular -AR verbs with common emotional triggers
    # ==========================================================================

    {
        "verb_infinitive": "hablar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Espero que tú _____ con tu familia hoy. (hablar)",
        "correct_answer": "hables",
        "alternative_answers": [],
        "distractors": ["hablas", "hablabas", "hablarás"],
        "explanation": "After 'espero que' (I hope that), we use the present subjunctive. For 'hablar' with 'tú', the subjunctive form is 'hables'.",
        "trigger_phrase": "espero que",
        "hint": "Remember: -AR verbs in subjunctive use -e endings instead of -a.",
    },
    {
        "verb_infinitive": "estudiar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Es importante que ella _____ para el examen. (estudiar)",
        "correct_answer": "estudie",
        "alternative_answers": [],
        "distractors": ["estudia", "estudiaba", "estudiará"],
        "explanation": "'Es importante que' is an impersonal expression requiring subjunctive. Regular -AR verbs change the 'a' to 'e'.",
        "trigger_phrase": "es importante que",
        "hint": "Impersonal expressions like 'es importante que' always trigger the subjunctive.",
    },
    {
        "verb_infinitive": "trabajar",
        "exercise_type": ExerciseType.MULTIPLE_CHOICE,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Me alegra que nosotros _____ juntos. (trabajar)",
        "correct_answer": "trabajemos",
        "alternative_answers": [],
        "distractors": ["trabajamos", "trabajábamos", "trabajaremos"],
        "explanation": "'Me alegra que' (I'm happy that) expresses emotion and requires subjunctive. For 'nosotros', add -emos to the stem.",
        "trigger_phrase": "me alegra que",
        "hint": "Emotions trigger the subjunctive. What feeling is expressed here?",
    },
    {
        "verb_infinitive": "cantar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Quiero que ellos _____ en el coro. (cantar)",
        "correct_answer": "canten",
        "alternative_answers": [],
        "distractors": ["cantan", "cantaban", "cantarán"],
        "explanation": "'Quiero que' (I want that) expresses a wish and requires subjunctive. For 'ellos', the ending is -en.",
        "trigger_phrase": "quiero que",
        "hint": "When you want someone else to do something, use subjunctive!",
    },
    {
        "verb_infinitive": "llegar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Es necesario que yo _____ temprano mañana. (llegar)",
        "correct_answer": "llegue",
        "alternative_answers": [],
        "distractors": ["llego", "llegaba", "llegaré"],
        "explanation": "'Es necesario que' requires subjunctive. Note: -gar verbs add 'u' before 'e' (llegue, not llege).",
        "trigger_phrase": "es necesario que",
        "hint": "Watch out for spelling changes with -gar verbs!",
    },

    # ==========================================================================
    # EASY LEVEL: Regular -ER/-IR verbs
    # ==========================================================================

    {
        "verb_infinitive": "comer",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Prefiero que tú _____ más verduras. (comer)",
        "correct_answer": "comas",
        "alternative_answers": [],
        "distractors": ["comes", "comías", "comerás"],
        "explanation": "'Prefiero que' expresses preference and requires subjunctive. -ER verbs use -a endings.",
        "trigger_phrase": "prefiero que",
        "hint": "-ER and -IR verbs flip: they use -a endings in subjunctive.",
    },
    {
        "verb_infinitive": "vivir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Es bueno que ellos _____ cerca de la escuela. (vivir)",
        "correct_answer": "vivan",
        "alternative_answers": [],
        "distractors": ["viven", "vivían", "vivirán"],
        "explanation": "'Es bueno que' is an impersonal expression requiring subjunctive. -IR verbs in subjunctive end in -a.",
        "trigger_phrase": "es bueno que",
        "hint": "Think about what ending -IR verbs take in subjunctive.",
    },
    {
        "verb_infinitive": "escribir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Sugiero que ella _____ una carta. (escribir)",
        "correct_answer": "escriba",
        "alternative_answers": [],
        "distractors": ["escribe", "escribía", "escribirá"],
        "explanation": "'Sugiero que' (I suggest that) requires subjunctive. Regular -IR verbs take -a endings.",
        "trigger_phrase": "sugiero que",
        "hint": "Suggestions about what others should do use subjunctive.",
    },
    {
        "verb_infinitive": "beber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Es importante que nosotros _____ mucha agua. (beber)",
        "correct_answer": "bebamos",
        "alternative_answers": [],
        "distractors": ["bebemos", "bebíamos", "beberemos"],
        "explanation": "Health advice with 'es importante que' requires subjunctive. -ER verbs with nosotros end in -amos.",
        "trigger_phrase": "es importante que",
        "hint": "This is health advice—what mood expresses recommendations?",
    },
    {
        "verb_infinitive": "abrir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EASY,
        "prompt": "Recomiendo que tú _____ las ventanas. (abrir)",
        "correct_answer": "abras",
        "alternative_answers": [],
        "distractors": ["abres", "abrías", "abrirás"],
        "explanation": "'Recomiendo que' (I recommend that) triggers subjunctive. -IR verb with tú: -as ending.",
        "trigger_phrase": "recomiendo que",
        "hint": "Recommendations use subjunctive to express what someone should do.",
    },

    # ==========================================================================
    # MEDIUM LEVEL: Stem-changing verbs (e>ie)
    # ==========================================================================

    {
        "verb_infinitive": "pensar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "No creo que él _____ en eso. (pensar)",
        "correct_answer": "piense",
        "alternative_answers": [],
        "distractors": ["piensa", "pensaba", "pensará"],
        "explanation": "'No creo que' expresses doubt and requires subjunctive. 'Pensar' changes e→ie in stressed syllables, but keeps the e in nosotros/vosotros.",
        "trigger_phrase": "no creo que",
        "hint": "Stem-changing verbs keep their stem change in subjunctive!",
    },
    {
        "verb_infinitive": "querer",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Dudo que ella _____ venir a la fiesta. (querer)",
        "correct_answer": "quiera",
        "alternative_answers": [],
        "distractors": ["quiere", "quería", "querrá"],
        "explanation": "'Dudo que' (I doubt that) expresses uncertainty. 'Querer' is e→ie stem-changing, so it becomes 'quiera'.",
        "trigger_phrase": "dudo que",
        "hint": "When you doubt something, subjunctive expresses that uncertainty.",
    },
    {
        "verb_infinitive": "entender",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Es posible que nosotros no _____ la lección. (entender)",
        "correct_answer": "entendamos",
        "alternative_answers": [],
        "distractors": ["entendemos", "entendíamos", "entenderemos"],
        "explanation": "'Es posible que' expresses possibility. Note: with nosotros, stem-changing verbs DON'T change (entendamos, not entendamos).",
        "trigger_phrase": "es posible que",
        "hint": "Remember: nosotros and vosotros don't stem-change in subjunctive!",
    },
    {
        "verb_infinitive": "cerrar",
        "exercise_type": ExerciseType.MULTIPLE_CHOICE,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Espero que ellos _____ la puerta con llave. (cerrar)",
        "correct_answer": "cierren",
        "alternative_answers": [],
        "distractors": ["cierran", "cerraban", "cerrarán"],
        "explanation": "'Cerrar' is e→ie stem-changing. With 'espero que', use subjunctive: cierren.",
        "trigger_phrase": "espero que",
        "hint": "This verb changes its stem in the present tense—does it change in subjunctive too?",
    },

    # ==========================================================================
    # MEDIUM LEVEL: Stem-changing verbs (o>ue)
    # ==========================================================================

    {
        "verb_infinitive": "poder",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Ojalá que yo _____ ir al concierto. (poder)",
        "correct_answer": "pueda",
        "alternative_answers": [],
        "distractors": ["puedo", "podía", "podré"],
        "explanation": "'Ojalá (que)' expresses hope and always requires subjunctive. 'Poder' changes o→ue: pueda.",
        "trigger_phrase": "ojalá que",
        "hint": "'Ojalá' always uses subjunctive—it comes from Arabic meaning 'may Allah grant'!",
    },
    {
        "verb_infinitive": "encontrar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "No pienso que tú _____ las llaves aquí. (encontrar)",
        "correct_answer": "encuentres",
        "alternative_answers": [],
        "distractors": ["encuentras", "encontrabas", "encontrarás"],
        "explanation": "'No pienso que' expresses negative opinion/doubt. 'Encontrar' is o→ue: encuentres.",
        "trigger_phrase": "no pienso que",
        "hint": "Negative opinions trigger subjunctive mood.",
    },
    {
        "verb_infinitive": "volver",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Es mejor que ella _____ temprano a casa. (volver)",
        "correct_answer": "vuelva",
        "alternative_answers": [],
        "distractors": ["vuelve", "volvía", "volverá"],
        "explanation": "'Es mejor que' is a value judgment requiring subjunctive. 'Volver' changes o→ue: vuelva.",
        "trigger_phrase": "es mejor que",
        "hint": "When giving advice or saying what's better, use subjunctive!",
    },
    {
        "verb_infinitive": "dormir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Recomiendo que ustedes _____ ocho horas. (dormir)",
        "correct_answer": "duerman",
        "alternative_answers": [],
        "distractors": ["duermen", "dormían", "dormirán"],
        "explanation": "'Dormir' is a special o→ue/u verb. In present subjunctive, it changes o→ue in most forms: duerman.",
        "trigger_phrase": "recomiendo que",
        "hint": "This verb has a boot-shaped stem change pattern!",
    },

    # ==========================================================================
    # MEDIUM LEVEL: Stem-changing verbs (e>i)
    # ==========================================================================

    {
        "verb_infinitive": "pedir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Sugiero que tú _____ ayuda cuando la necesites. (pedir)",
        "correct_answer": "pidas",
        "alternative_answers": [],
        "distractors": ["pides", "pedías", "pedirás"],
        "explanation": "'Pedir' changes e→i throughout the subjunctive (unlike some stem-changing verbs). With 'sugiero que': pidas.",
        "trigger_phrase": "sugiero que",
        "hint": "Some -IR verbs change e→i in ALL subjunctive forms!",
    },
    {
        "verb_infinitive": "servir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Es importante que el restaurante _____ comida fresca. (servir)",
        "correct_answer": "sirva",
        "alternative_answers": [],
        "distractors": ["sirve", "servía", "servirá"],
        "explanation": "'Servir' is e→i stem-changing. With impersonal expression: sirva.",
        "trigger_phrase": "es importante que",
        "hint": "This is an -ir verb that changes e to i.",
    },
    {
        "verb_infinitive": "repetir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Prefiero que nosotros no _____ los mismos errores. (repetir)",
        "correct_answer": "repitamos",
        "alternative_answers": [],
        "distractors": ["repetimos", "repetíamos", "repetiremos"],
        "explanation": "'Repetir' changes e→i even in the nosotros form in subjunctive (unlike e→ie verbs): repitamos.",
        "trigger_phrase": "prefiero que",
        "hint": "e→i verbs are special—they change in ALL forms, even nosotros!",
    },

    # ==========================================================================
    # HARD LEVEL: Irregular verbs
    # ==========================================================================

    {
        "verb_infinitive": "ser",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Es raro que él _____ tan callado hoy. (ser)",
        "correct_answer": "sea",
        "alternative_answers": [],
        "distractors": ["es", "era", "será"],
        "explanation": "'Ser' is completely irregular in subjunctive. The forms are: sea, seas, sea, seamos, seáis, sean.",
        "trigger_phrase": "es raro que",
        "hint": "'Ser' has a completely irregular subjunctive stem!",
    },
    {
        "verb_infinitive": "estar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "No creo que ellos _____ en casa ahora. (estar)",
        "correct_answer": "estén",
        "alternative_answers": [],
        "distractors": ["están", "estaban", "estarán"],
        "explanation": "'Estar' has accent marks in subjunctive: esté, estés, esté, estemos, estéis, estén.",
        "trigger_phrase": "no creo que",
        "hint": "Remember the accent marks on this irregular verb!",
    },
    {
        "verb_infinitive": "ir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Espero que tú _____ al médico pronto. (ir)",
        "correct_answer": "vayas",
        "alternative_answers": [],
        "distractors": ["vas", "ibas", "irás"],
        "explanation": "'Ir' is highly irregular: vaya, vayas, vaya, vayamos, vayáis, vayan.",
        "trigger_phrase": "espero que",
        "hint": "This verb of motion has a completely different stem in subjunctive!",
    },
    {
        "verb_infinitive": "haber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Es posible que _____ problemas mañana. (haber)",
        "correct_answer": "haya",
        "alternative_answers": [],
        "distractors": ["hay", "había", "habrá"],
        "explanation": "'Haber' in subjunctive is 'haya'. Used impersonally: 'es posible que haya' (there may be).",
        "trigger_phrase": "es posible que",
        "hint": "The impersonal form 'hay' becomes 'haya' in subjunctive.",
    },
    {
        "verb_infinitive": "saber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Dudo que ella _____ la verdad. (saber)",
        "correct_answer": "sepa",
        "alternative_answers": [],
        "distractors": ["sabe", "sabía", "sabrá"],
        "explanation": "'Saber' has irregular stem 'sep-': sepa, sepas, sepa, sepamos, sepáis, sepan.",
        "trigger_phrase": "dudo que",
        "hint": "Think of the -yo form in present: sé → sep- in subjunctive.",
    },
    {
        "verb_infinitive": "dar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Es necesario que yo le _____ las gracias. (dar)",
        "correct_answer": "dé",
        "alternative_answers": [],
        "distractors": ["doy", "daba", "daré"],
        "explanation": "'Dar' is irregular and takes accent marks: dé, des, dé, demos, deis, den. The accent on 'dé' distinguishes it from the preposition 'de'.",
        "trigger_phrase": "es necesario que",
        "hint": "Watch out for the accent mark on the yo and él forms!",
    },
    {
        "verb_infinitive": "ver",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Me sorprende que tú no _____ el problema. (ver)",
        "correct_answer": "veas",
        "alternative_answers": [],
        "distractors": ["ves", "veías", "verás"],
        "explanation": "'Ver' keeps the 'e' and adds subjunctive endings: vea, veas, vea, veamos, veáis, vean.",
        "trigger_phrase": "me sorprende que",
        "hint": "This verb is less irregular than you might think—just add the endings!",
    },
    {
        "verb_infinitive": "hacer",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Quiero que ustedes _____ la tarea ahora. (hacer)",
        "correct_answer": "hagan",
        "alternative_answers": [],
        "distractors": ["hacen", "hacían", "harán"],
        "explanation": "'Hacer' uses stem 'hag-': haga, hagas, haga, hagamos, hagáis, hagan.",
        "trigger_phrase": "quiero que",
        "hint": "Take the yo form (hago) and replace -o with subjunctive endings.",
    },
    {
        "verb_infinitive": "tener",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Es importante que ellos _____ paciencia. (tener)",
        "correct_answer": "tengan",
        "alternative_answers": [],
        "distractors": ["tienen", "tenían", "tendrán"],
        "explanation": "'Tener' uses stem 'teng-' (from yo form 'tengo'): tenga, tengas, tenga, tengamos, tengáis, tengan.",
        "trigger_phrase": "es importante que",
        "hint": "Think of the yo form: tengo → teng- + subjunctive endings.",
    },
    {
        "verb_infinitive": "venir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Ojalá que él _____ a la reunión mañana. (venir)",
        "correct_answer": "venga",
        "alternative_answers": [],
        "distractors": ["viene", "venía", "vendrá"],
        "explanation": "'Venir' is irregular with stem 'veng-': venga, vengas, venga, vengamos, vengáis, vengan.",
        "trigger_phrase": "ojalá que",
        "hint": "Based on yo form: vengo → veng- + endings.",
    },
    {
        "verb_infinitive": "decir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "No es verdad que yo _____ mentiras. (decir)",
        "correct_answer": "diga",
        "alternative_answers": [],
        "distractors": ["digo", "decía", "diré"],
        "explanation": "'Decir' has stem 'dig-': diga, digas, diga, digamos, digáis, digan.",
        "trigger_phrase": "no es verdad que",
        "hint": "From yo form: digo → dig- + subjunctive endings.",
    },

    # ==========================================================================
    # EXPERT LEVEL: Complex sentences, subtle triggers, conjunctions
    # ==========================================================================

    {
        "verb_infinitive": "llegar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Cuando tú _____ a casa, llámame. (llegar)",
        "correct_answer": "llegues",
        "alternative_answers": [],
        "distractors": ["llegas", "llegabas", "llegarás"],
        "explanation": "'Cuando' with future meaning requires subjunctive. If the action hasn't happened yet, use subjunctive after cuando.",
        "trigger_phrase": "cuando",
        "hint": "Time expressions about the future use subjunctive!",
    },
    {
        "verb_infinitive": "saber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Te llamaré en cuanto yo _____ los resultados. (saber)",
        "correct_answer": "sepa",
        "alternative_answers": [],
        "distractors": ["sé", "sabía", "sabré"],
        "explanation": "'En cuanto' (as soon as) requires subjunctive when referring to future actions.",
        "trigger_phrase": "en cuanto",
        "hint": "Conjunctions about pending future actions trigger subjunctive.",
    },
    {
        "verb_infinitive": "poder",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Trabaja duro para que tú _____ tener éxito. (poder)",
        "correct_answer": "puedas",
        "alternative_answers": [],
        "distractors": ["puedes", "podías", "podrás"],
        "explanation": "'Para que' (so that, in order that) always requires subjunctive, expressing purpose.",
        "trigger_phrase": "para que",
        "hint": "Purpose clauses with 'para que' always use subjunctive!",
    },
    {
        "verb_infinitive": "salir",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Voy a quedarme hasta que ellos _____ del edificio. (salir)",
        "correct_answer": "salgan",
        "alternative_answers": [],
        "distractors": ["salen", "salían", "saldrán"],
        "explanation": "'Hasta que' (until) requires subjunctive when the action hasn't happened yet. 'Salir' is irregular: salga.",
        "trigger_phrase": "hasta que",
        "hint": "'Salir' follows the pattern of verbs with -go endings: salgo → salga.",
    },
    {
        "verb_infinitive": "estar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Aunque _____ cansado, voy a ayudarte. (estar, yo)",
        "correct_answer": "esté",
        "alternative_answers": [],
        "distractors": ["estoy", "estaba", "estaré"],
        "explanation": "'Aunque' can use subjunctive when there's uncertainty or to emphasize regardless of circumstances.",
        "trigger_phrase": "aunque",
        "hint": "'Aunque' with subjunctive emphasizes 'no matter if' or hypothetical situations.",
    },
    {
        "verb_infinitive": "haber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Sin que _____ problemas, podemos continuar. (haber)",
        "correct_answer": "haya",
        "alternative_answers": [],
        "distractors": ["hay", "había", "habrá"],
        "explanation": "'Sin que' (without) always requires subjunctive. Using the impersonal 'haber': haya.",
        "trigger_phrase": "sin que",
        "hint": "'Sin que' expresses negation and always takes subjunctive.",
    },
    {
        "verb_infinitive": "empezar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Antes de que _____ la película, compra palomitas. (empezar)",
        "correct_answer": "empiece",
        "alternative_answers": [],
        "distractors": ["empieza", "empezaba", "empezará"],
        "explanation": "'Antes de que' (before) always requires subjunctive. 'Empezar' is e→ie stem-changing: empiece.",
        "trigger_phrase": "antes de que",
        "hint": "Time expressions with 'antes de que' always use subjunctive.",
    },
    {
        "verb_infinitive": "terminar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.PRESENT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "A menos que tú _____ temprano, llegaremos tarde. (terminar)",
        "correct_answer": "termines",
        "alternative_answers": [],
        "distractors": ["terminas", "terminabas", "terminarás"],
        "explanation": "'A menos que' (unless) expresses a condition and always requires subjunctive.",
        "trigger_phrase": "a menos que",
        "hint": "'A menos que' means 'unless' and always triggers subjunctive.",
    },

    # ==========================================================================
    # IMPERFECT SUBJUNCTIVE EXERCISES (MEDIUM-EXPERT)
    # ==========================================================================

    {
        "verb_infinitive": "hablar",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.IMPERFECT,
        "difficulty": DifficultyLevel.MEDIUM,
        "prompt": "Mi madre quería que yo _____ español en casa. (hablar)",
        "correct_answer": "hablara",
        "alternative_answers": ["hablase"],
        "distractors": ["hablaba", "hablé", "hablaría"],
        "explanation": "Past trigger 'quería que' requires imperfect subjunctive. Two forms exist: hablara (more common) or hablase.",
        "trigger_phrase": "quería que",
        "hint": "When the main verb is in the past, use imperfect subjunctive!",
    },
    {
        "verb_infinitive": "ser",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.IMPERFECT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Si yo _____ rico, viajaría por el mundo. (ser)",
        "correct_answer": "fuera",
        "alternative_answers": ["fuese"],
        "distractors": ["era", "fui", "sería"],
        "explanation": "'Si' clauses expressing hypothetical (contrary-to-fact) situations use imperfect subjunctive. 'Ser': fuera/fuese.",
        "trigger_phrase": "si",
        "hint": "Hypothetical 'if' clauses use imperfect subjunctive + conditional.",
    },
    {
        "verb_infinitive": "tener",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.IMPERFECT,
        "difficulty": DifficultyLevel.HARD,
        "prompt": "Ojalá que yo _____ más tiempo para estudiar. (tener)",
        "correct_answer": "tuviera",
        "alternative_answers": ["tuviese"],
        "distractors": ["tenía", "tuve", "tendría"],
        "explanation": "'Ojalá' + imperfect subjunctive expresses a wish about the present that's unlikely/impossible.",
        "trigger_phrase": "ojalá",
        "hint": "'Ojalá' + imperfect subjunctive = wishful thinking about now.",
    },
    {
        "verb_infinitive": "poder",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.IMPERFECT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Si tú _____ venir, sería fantástico. (poder)",
        "correct_answer": "pudieras",
        "alternative_answers": ["pudieses"],
        "distractors": ["podías", "pudiste", "podrías"],
        "explanation": "Hypothetical condition with 'si' + imperfect subjunctive. 'Poder': pudiera/pudiese.",
        "trigger_phrase": "si",
        "hint": "This is a polite way to invite someone: 'if you could come...'",
    },
    {
        "verb_infinitive": "saber",
        "exercise_type": ExerciseType.FILL_BLANK,
        "tense": SubjunctiveTense.IMPERFECT,
        "difficulty": DifficultyLevel.EXPERT,
        "prompt": "Ella dudaba que nosotros _____ la respuesta. (saber)",
        "correct_answer": "supiéramos",
        "alternative_answers": ["supiésemos"],
        "distractors": ["sabíamos", "supimos", "sabríamos"],
        "explanation": "Past doubt 'dudaba que' triggers imperfect subjunctive. 'Saber': supiera/supiese.",
        "trigger_phrase": "dudaba que",
        "hint": "Match the tense: past doubt triggers imperfect subjunctive.",
    },
]

# ==============================================================================
# CONTEXTUAL SCENARIOS FOR GROUPED EXERCISES
# ==============================================================================

SEED_SCENARIOS = [
    {
        "title": "Esperanzas y Deseos",
        "description": "Practice expressing hopes and wishes using common emotional triggers",
        "theme": "emotions",
        "context": "Learn to express what you hope will happen and what you wish others would do.",
        "recommended_level": "A2",
        "exercise_prompts": ["espero que", "ojalá", "quiero que", "deseo que"]
    },
    {
        "title": "Consejos y Recomendaciones",
        "description": "Give advice and recommendations using impersonal expressions",
        "theme": "advice",
        "context": "Master the art of giving suggestions and stating what's important or necessary.",
        "recommended_level": "A2",
        "exercise_prompts": ["es importante que", "es necesario que", "recomiendo que", "sugiero que"]
    },
    {
        "title": "Dudas e Incertidumbre",
        "description": "Express doubt, denial, and uncertainty",
        "theme": "doubt",
        "context": "Learn to talk about things you doubt or don't believe are true.",
        "recommended_level": "B1",
        "exercise_prompts": ["dudo que", "no creo que", "no es cierto que", "es imposible que"]
    },
    {
        "title": "Reacciones Emocionales",
        "description": "React emotionally to situations and news",
        "theme": "emotional_reactions",
        "context": "Express happiness, surprise, fear, and other emotions about events.",
        "recommended_level": "B1",
        "exercise_prompts": ["me alegra que", "me sorprende que", "temo que", "me molesta que"]
    },
    {
        "title": "Planes y Propósitos",
        "description": "Discuss future plans with conjunctions",
        "theme": "future_plans",
        "context": "Talk about when, until, and before things will happen using time expressions.",
        "recommended_level": "B2",
        "exercise_prompts": ["cuando", "hasta que", "antes de que", "después de que"]
    },
    {
        "title": "Condiciones e Hipótesis",
        "description": "Practice hypothetical situations and contrary-to-fact conditions",
        "theme": "hypothetical",
        "context": "Imagine different scenarios and express what would happen 'if...'",
        "recommended_level": "B2",
        "exercise_prompts": ["si", "aunque", "para que", "sin que"]
    },
    {
        "title": "En el Trabajo",
        "description": "Workplace scenarios: meetings, projects, and collaboration",
        "theme": "work",
        "context": "Professional situations requiring suggestions, requests, and expressing necessity.",
        "recommended_level": "B1",
        "exercise_prompts": ["es necesario que", "prefiero que", "sugiero que", "es importante que"]
    },
    {
        "title": "Viajes y Aventuras",
        "description": "Travel scenarios with hopes, plans, and recommendations",
        "theme": "travel",
        "context": "Planning trips, giving travel advice, and expressing wishes about destinations.",
        "recommended_level": "B1",
        "exercise_prompts": ["espero que", "recomiendo que", "cuando", "antes de que"]
    },
    {
        "title": "Relaciones Personales",
        "description": "Family, friends, and relationships",
        "theme": "relationships",
        "context": "Express emotions, wishes, and concerns about people you care about.",
        "recommended_level": "A2",
        "exercise_prompts": ["quiero que", "me alegra que", "espero que", "me preocupa que"]
    },
    {
        "title": "Salud y Bienestar",
        "description": "Health advice, medical situations, and wellness",
        "theme": "health",
        "context": "Give health recommendations and express concerns about wellbeing.",
        "recommended_level": "B1",
        "exercise_prompts": ["es importante que", "recomiendo que", "espero que", "me preocupa que"]
    },
]
