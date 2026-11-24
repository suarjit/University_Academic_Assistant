
import sys

sys.path.insert(0, "src")

from generation.answer_generator import answer_question

# Questions and their expected source documents
test_cases = [
    {
        "question": "What is the minimum attendance required for students?",
        "expected_source": "examination_rules.txt"
    },
    {
        "question": "What percentage of marks is allocated to internal assessment?",
        "expected_source": "examination_rules.txt"
    },
    {
        "question": "What is the merit scholarship for students scoring 90% or above?",
        "expected_source": "scholarship_policy.txt"
    },
    {
        "question": "What is the undergraduate admission eligibility?",
        "expected_source": "admission_policy.txt"
    },
    {
        "question": "How many books can a student borrow from the library?",
        "expected_source": "university_facilities.txt"
    }
]

passed = 0

for index, test in enumerate(test_cases, start=1):
    print(f"\nTEST {index}")
    print("Question:", test["question"])

    result = answer_question(test["question"])

    answer = result["answer"]
    expected_source = test["expected_source"]

    print("Answer:", answer)
    print("Expected source:", expected_source)

    if expected_source in answer:
        print("RESULT: PASS")
        passed += 1
    else:
        print("RESULT: FAIL")

print("\n========== CITATION TEST SUMMARY ==========")
print(f"Passed: {passed}/{len(test_cases)}")
print(f"Failed: {len(test_cases) - passed}/{len(test_cases)}")
