import re
from collections import Counter
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

text = """
Молодые исследователи разрабатывают современные методы обработки текстов.
Новые алгоритмы позволяют анализировать большие текстовые данные
и находить важные закономерности в документах.
"""

# 1. Токенизация
words = re.findall(r"[А-Яа-яЁё]+", text.lower())

lemmas = []
nouns = []
adjectives = []

print("Морфологический анализ:\n")

for word in words:
    parsed = morph.parse(word)[0]

    lemma = parsed.normal_form
    pos = parsed.tag.POS

    lemmas.append(lemma)

    # Существительные
    if pos == "NOUN":
        nouns.append(lemma)

    # Полные прилагательные
    elif pos == "ADJF":
        adjectives.append(lemma)

    print(
        f"{word:15} "
        f"лемма={lemma:15} "
        f"POS={str(pos):5} "
        f"падеж={str(parsed.tag.case):5} "
        f"число={str(parsed.tag.number):5}"
    )

# 2. Частотный анализ лемм
lemma_freq = Counter(lemmas)

print("\nНаиболее частые леммы:")

for lemma, count in lemma_freq.most_common(10):
    print(f"{lemma:15} {count}")

# 3. Отдельно выводим существительные и прилагательные
print("\nСуществительные:")
print(nouns)

print("\nПрилагательные:")
print(adjectives)