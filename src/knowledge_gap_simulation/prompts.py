ENRICHMENT_PROMPT = """Classify this multiple-choice science question. Return its subject area, difficulty from 1 to 5, and a concise reasoning description.\nQuestion: {question}\nChoices: {choices}"""

CONCEPT_PROMPT = """Identify one to three concepts needed to answer the question correctly. Concepts must be specific and independently describable.\nQuestion: {question}\nChoices: {choices}\nCorrect answer: {answer}"""

STRATEGY_A_PROMPT = """Role-play a person who knows only the first {k} concepts listed below. Do not use later concepts. Answer the multiple-choice question using only that knowledge.\nKnown concepts:\n{concepts}\nQuestion: {question}\nChoices: {choices}"""

STRATEGY_B_PROMPT = """Simulate the mistaken reasoning of a person whose scientific knowledge is restricted to the first {k} concepts below. Explicitly avoid facts outside this boundary, even when you know the correct answer.\nAvailable concepts:\n{concepts}\nQuestion: {question}\nChoices: {choices}"""

NAIVE_PROMPT = """Predict what answer a person lacking the later concepts would most plausibly choose.\nKnown concepts:\n{concepts}\nQuestion: {question}\nChoices: {choices}"""

FALSE_BELIEF_PROMPT = """Answer from the named person's perspective, based only on what that person has observed. Explain the belief separately from reality.\nScenario: {scenario}"""
