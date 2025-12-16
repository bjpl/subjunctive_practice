#!/usr/bin/env python3
"""
Verification script for Spanish Subjunctive Content Expansion
Tests all new conjugation features and seed data.
"""

import sys
sys.path.insert(0, 'backend')

from services.conjugation import ConjugationEngine, PAST_PARTICIPLES


def test_perfect_subjunctive():
    """Test present perfect subjunctive conjugations."""
    print("\n" + "="*60)
    print("TESTING PRESENT PERFECT SUBJUNCTIVE")
    print("="*60)

    engine = ConjugationEngine()
    tests = [
        ("hablar", "yo", "haya hablado"),
        ("comer", "tú", "hayas comido"),
        ("vivir", "él/ella/usted", "haya vivido"),
        ("hacer", "nosotros/nosotras", "hayamos hecho"),
        ("decir", "vosotros/vosotras", "hayáis dicho"),
        ("escribir", "ellos/ellas/ustedes", "hayan escrito"),
    ]

    passed = 0
    failed = 0

    for verb, person, expected in tests:
        result = engine.conjugate(verb, 'present_perfect_subjunctive', person)
        status = "✓" if result.conjugation == expected else "✗"

        if result.conjugation == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {verb} ({person}): {result.conjugation} {'==' if result.conjugation == expected else '!='} {expected}")

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_pluperfect_subjunctive():
    """Test pluperfect subjunctive conjugations."""
    print("\n" + "="*60)
    print("TESTING PLUPERFECT SUBJUNCTIVE")
    print("="*60)

    engine = ConjugationEngine()
    tests = [
        ("saber", "yo", "hubiera sabido"),
        ("estudiar", "tú", "hubieras estudiado"),
        ("hacer", "él/ella/usted", "hubiera hecho"),
        ("decir", "nosotros/nosotras", "hubiéramos dicho"),
        ("ver", "vosotros/vosotras", "hubierais visto"),
        ("poner", "ellos/ellas/ustedes", "hubieran puesto"),
    ]

    passed = 0
    failed = 0

    for verb, person, expected in tests:
        result = engine.conjugate(verb, 'pluperfect_subjunctive', person)
        status = "✓" if result.conjugation == expected else "✗"

        if result.conjugation == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {verb} ({person}): {result.conjugation} {'==' if result.conjugation == expected else '!='} {expected}")

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_past_participles():
    """Test past participle dictionary."""
    print("\n" + "="*60)
    print("TESTING PAST PARTICIPLES")
    print("="*60)

    # Test irregular participles
    irregular_tests = {
        "hacer": "hecho",
        "decir": "dicho",
        "escribir": "escrito",
        "ver": "visto",
        "poner": "puesto",
        "volver": "vuelto",
        "abrir": "abierto",
        "romper": "roto",
        "morir": "muerto",
    }

    print("\nIrregular Participles:")
    passed = 0
    failed = 0

    for verb, expected in irregular_tests.items():
        actual = PAST_PARTICIPLES.get(verb)
        status = "✓" if actual == expected else "✗"

        if actual == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {verb} → {actual} {'==' if actual == expected else '!='} {expected}")

    # Test regular participles
    print("\nRegular Participles (generated):")
    engine = ConjugationEngine()
    regular_tests = {
        "hablar": "hablado",
        "comer": "comido",
        "vivir": "vivido",
    }

    for verb, expected in regular_tests.items():
        actual = engine._get_regular_participle(verb)
        status = "✓" if actual == expected else "✗"

        if actual == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {verb} → {actual} {'==' if actual == expected else '!='} {expected}")

    print(f"\nResults: {passed} passed, {failed} failed")
    print(f"Total participles in dictionary: {len(PAST_PARTICIPLES)}")
    return failed == 0


def test_relative_clause():
    """Test relative clause subjunctive (uses present subjunctive)."""
    print("\n" + "="*60)
    print("TESTING RELATIVE CLAUSE SUBJUNCTIVE")
    print("="*60)

    engine = ConjugationEngine()
    tests = [
        ("tener", "él/ella/usted", "tenga"),
        ("saber", "él/ella/usted", "sepa"),
        ("poder", "él/ella/usted", "pueda"),
        ("ser", "él/ella/usted", "sea"),
        ("hacer", "nosotros/nosotras", "hagamos"),
    ]

    passed = 0
    failed = 0

    for verb, person, expected in tests:
        result = engine.conjugate(verb, 'present_subjunctive', person)
        status = "✓" if result.conjugation == expected else "✗"

        if result.conjugation == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {verb} ({person}): {result.conjugation} {'==' if result.conjugation == expected else '!='} {expected}")

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def verify_seed_data():
    """Verify seed data structure."""
    print("\n" + "="*60)
    print("VERIFYING SEED DATA")
    print("="*60)

    try:
        with open('backend/core/seed_data.py', 'r') as f:
            content = f.read()

        # Check for SEED_EXERCISES
        if 'SEED_EXERCISES' in content:
            print("✓ SEED_EXERCISES dictionary found")
        else:
            print("✗ SEED_EXERCISES dictionary not found")
            return False

        # Check for exercise categories
        categories = [
            'perfect_subjunctive',
            'relative_clause_subjunctive',
            'pluperfect_subjunctive'
        ]

        for category in categories:
            if f'"{category}"' in content:
                print(f"✓ {category} exercises found")
            else:
                print(f"✗ {category} exercises not found")
                return False

        # Count exercises
        perfect_count = content[content.find('"perfect_subjunctive"'):content.find('"relative_clause_subjunctive"')].count('"verb":')
        relative_count = content[content.find('"relative_clause_subjunctive"'):content.find('"pluperfect_subjunctive"')].count('"verb":')
        pluperfect_count = content[content.find('"pluperfect_subjunctive"'):].count('"verb":') - 1  # Subtract 1 for closing

        print(f"\nExercise Counts:")
        print(f"  Perfect Subjunctive: {perfect_count} exercises")
        print(f"  Relative Clause: {relative_count} exercises")
        print(f"  Pluperfect Subjunctive: {pluperfect_count} exercises")
        print(f"  Total: {perfect_count + relative_count + pluperfect_count} exercises")

        expected_total = 35
        if perfect_count + relative_count + pluperfect_count >= expected_total:
            print(f"✓ Total exercises ({perfect_count + relative_count + pluperfect_count}) meets or exceeds target ({expected_total})")
            return True
        else:
            print(f"✗ Total exercises ({perfect_count + relative_count + pluperfect_count}) below target ({expected_total})")
            return False

    except Exception as e:
        print(f"✗ Error reading seed data: {e}")
        return False


def main():
    """Run all verification tests."""
    print("\n" + "="*60)
    print("SPANISH SUBJUNCTIVE EXPANSION VERIFICATION")
    print("="*60)

    results = []

    # Run all tests
    results.append(("Present Perfect Subjunctive", test_perfect_subjunctive()))
    results.append(("Pluperfect Subjunctive", test_pluperfect_subjunctive()))
    results.append(("Past Participles", test_past_participles()))
    results.append(("Relative Clause Subjunctive", test_relative_clause()))
    results.append(("Seed Data", verify_seed_data()))

    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} test suites passed")

    if passed == total:
        print("\n✓ ALL TESTS PASSED - Expansion verified successfully!")
        return 0
    else:
        print(f"\n✗ {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
