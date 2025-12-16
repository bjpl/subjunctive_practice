# Quick Reference: New Subjunctive Tenses

## Present Perfect Subjunctive

### Formation
**haber (present subjunctive) + past participle**

### Conjugation of haber
| Person | Form |
|--------|------|
| yo | haya |
| tú | hayas |
| él/ella/usted | haya |
| nosotros/nosotras | hayamos |
| vosotros/vosotras | hayáis |
| ellos/ellas/ustedes | hayan |

### Examples
```
hablar → haya hablado (I have spoken)
comer → hayas comido (you have eaten)
vivir → haya vivido (he/she has lived)
hacer → hayamos hecho (we have done) [irregular participle]
decir → hayan dicho (they have said) [irregular participle]
escribir → hayas escrito (you have written) [irregular participle]
ver → hayan visto (they have seen) [irregular participle]
```

### Usage
Used when a completed action in the recent past triggers the subjunctive:
- "Es posible que haya llegado" (It's possible that he/she has arrived)
- "Dudo que hayas estudiado" (I doubt that you have studied)
- "No creo que hayan venido" (I don't think they have come)

---

## Pluperfect Subjunctive

### Formation
**haber (imperfect subjunctive -ra) + past participle**

### Conjugation of haber
| Person | Form |
|--------|------|
| yo | hubiera |
| tú | hubieras |
| él/ella/usted | hubiera |
| nosotros/nosotras | hubiéramos |
| vosotros/vosotras | hubierais |
| ellos/ellas/ustedes | hubieran |

Note: Alternative forms with -se (hubiese, hubieses, etc.) exist but -ra forms are more common.

### Examples
```
hablar → hubiera hablado (I had spoken)
comer → hubieras comido (you had eaten)
vivir → hubiera vivido (he/she had lived)
hacer → hubiéramos hecho (we had done) [irregular participle]
decir → hubieran dicho (they had said) [irregular participle]
ver → hubiera visto (I had seen) [irregular participle]
```

### Usage
Used for hypothetical or contrary-to-fact situations in the past:
- **Si clauses:** "Si hubiera sabido, habría venido" (If I had known, I would have come)
- **Regret:** "Ojalá hubiera estudiado más" (I wish I had studied more)
- **After expressions of doubt/emotion about the past:** "No creía que hubieran llegado" (I didn't believe they had arrived)

---

## Relative Clause Subjunctive

### When to Use
Use subjunctive in relative clauses when the antecedent is:
1. **Indefinite** (any/some, not specific)
2. **Non-existent** (nobody, nothing)
3. **Negated**

### Examples

#### Indefinite Antecedent → Subjunctive
```
Busco una casa que TENGA tres dormitorios.
(I'm looking for a house that has three bedrooms - any house, not specific)

Necesito alguien que SEPA francés.
(I need someone who knows French - anyone who knows)
```

#### Definite Antecedent → Indicative
```
Tengo una casa que TIENE tres dormitorios.
(I have a house that has three bedrooms - specific house)

Conozco a alguien que SABE francés.
(I know someone who knows French - specific person)
```

#### Non-existent Antecedent → Subjunctive
```
No hay nadie que PUEDA ayudarme.
(There's nobody who can help me)

No hay nada que NECESITEMOS.
(There's nothing that we need)
```

---

## Irregular Past Participles

### Common Irregular Forms
| Verb | Participle | Meaning |
|------|-----------|---------|
| hacer | hecho | done/made |
| decir | dicho | said/told |
| escribir | escrito | written |
| ver | visto | seen |
| poner | puesto | put/placed |
| volver | vuelto | returned |
| abrir | abierto | opened |
| morir | muerto | died |
| romper | roto | broken |
| cubrir | cubierto | covered |
| resolver | resuelto | resolved |
| devolver | devuelto | returned (item) |
| freír | frito | fried |
| imprimir | impreso | printed |

### Regular Past Participles
| Ending | Change | Example |
|--------|--------|---------|
| -ar | → -ado | hablar → hablado |
| -er | → -ido | comer → comido |
| -ir | → -ido | vivir → vivido |

---

## Code Examples

### Conjugation Engine Usage
```python
from backend.services.conjugation import ConjugationEngine

engine = ConjugationEngine()

# Present perfect subjunctive
result = engine.conjugate('hacer', 'present_perfect_subjunctive', 'yo')
print(result.conjugation)  # "haya hecho"

# Pluperfect subjunctive
result = engine.conjugate('decir', 'pluperfect_subjunctive', 'ellos/ellas/ustedes')
print(result.conjugation)  # "hubieran dicho"

# Relative clause (uses present subjunctive)
result = engine.conjugate('tener', 'present_subjunctive', 'él/ella/usted')
print(result.conjugation)  # "tenga"
```

### Getting Past Participle
```python
from backend.services.conjugation import PAST_PARTICIPLES

# Get participle directly
participle = PAST_PARTICIPLES.get('hacer', 'hecho')

# Or use engine method
result = engine._get_past_participle('hacer')
print(result)  # "hecho"
```

---

## Trigger Phrases

### For Present Perfect Subjunctive
- Es posible que... (It's possible that...)
- Dudo que... (I doubt that...)
- No creo que... (I don't think/believe that...)
- Es increíble que... (It's incredible that...)
- Espero que... (I hope that...)
- Me alegra que... (I'm glad that...)
- Es probable que... (It's probable that...)
- Es extraño que... (It's strange that...)
- Ojalá que... (I hope that...)

### For Pluperfect Subjunctive
- Si... (If... [contrary to fact])
- Ojalá... (I wish... [regret])
- No creía que... (I didn't believe that...)
- Era posible que... (It was possible that...)

### For Relative Clause Subjunctive
- Busco... que... (I'm looking for... that...)
- Necesito... que... (I need... that...)
- Quiero... que... (I want... that...)
- No hay nadie que... (There's nobody who...)
- No hay nada que... (There's nothing that...)

---

## Common Mistakes to Avoid

1. **Don't confuse perfect with pluperfect**
   - Perfect: Recent past action (Es posible que haya llegado)
   - Pluperfect: Hypothetical past (Si hubiera llegado...)

2. **Remember irregular participles**
   - ❌ "haya hacido" → ✅ "haya hecho"
   - ❌ "hubiera escribido" → ✅ "hubiera escrito"

3. **Relative clauses: Check if antecedent is definite**
   - Indefinite/non-existent → subjunctive
   - Definite/specific → indicative

4. **Don't use subjunctive with all relative clauses**
   - "El libro que LEÍSTE" (indicative - specific book)
   - "Un libro que TENGA fotos" (subjunctive - any book)

---

*Last updated: December 16, 2025*
