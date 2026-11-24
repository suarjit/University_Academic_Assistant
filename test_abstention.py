
import sys

sys.path.insert(0, "src")

from generation.answer_generator import answer_question

# Questions whose answers are not available in university documents
test_questions = [
    "What is the university's international student exchange program?",
    "Who is the current vice-chancellor of the university?",
    "Does the university provide free laptops to students?",
    "What is the university's campus placement percentage?",
    "Does the university offer a PhD program in astronomy?"
]

expected_abstention = (
    "I could not find sufficient information in the "
    "university documents to answer this question."
)

passed = 0

for index, question in enumerate(test_questions, start=1):
    print(f"\nTEST {index}")
    print("Question:", question)

    result = answer_question(question)
    answer = result["answer"]

    print("Answer:", answer)

    if answer.strip() == expected_abstention:
        print("RESULT: PASS")
        passed += 1
    else:
        print("RESULT: FAIL")

print("\n========== ABSTENTION TEST SUMMARY ==========")
print(f"Passed: {passed}/{len(test_questions)}")
print(f"Failed: {len(test_questions) - passed}/{len(test_questions)}")
