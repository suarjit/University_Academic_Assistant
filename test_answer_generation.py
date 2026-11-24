
import sys

sys.path.insert(0, "src")

from generation.answer_generator import answer_question

result = answer_question(
    "What is the minimum attendance required for students?"
)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
print(result["sources"])
