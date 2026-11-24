
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from generation.answer_generator import answer_question
from retrieval.retriever import retrieve_documents


DATASET_PATH = PROJECT_ROOT / "evaluation" / "evaluation_dataset.json"

EXPECTED_ABSTENTION = (
    "I could not find sufficient information in the "
    "university documents to answer this question."
)


def load_evaluation_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation():
    dataset = load_evaluation_dataset()

    total = len(dataset)
    retrieval_correct = 0
    citation_correct = 0
    abstention_correct = 0
    answer_generation_success = 0

    results = []

    for item in dataset:
        question_id = item["id"]
        question = item["question"]
        expected_source = item["expected_source"]
        should_abstain = item["should_abstain"]

        print(f"\n{'=' * 60}")
        print(f"TEST {question_id}/{total}")
        print("Question:", question)

        retrieved_documents = retrieve_documents(question, k=4)
        retrieved_sources = list(
            dict.fromkeys(doc["source"] for doc in retrieved_documents)
        )

        result = answer_question(question, k=4)
        answer = result["answer"]

        if should_abstain:
            retrieval_ok = None
            citation_ok = None
            abstention_ok = answer.strip() == EXPECTED_ABSTENTION
            generation_ok = None

            if abstention_ok:
                abstention_correct += 1

        else:
            retrieval_ok = expected_source in retrieved_sources
            citation_ok = expected_source in answer
            abstention_ok = None
            generation_ok = bool(answer.strip()) and answer.strip() != EXPECTED_ABSTENTION

            if retrieval_ok:
                retrieval_correct += 1

            if citation_ok:
                citation_correct += 1

            if generation_ok:
                answer_generation_success += 1

        print("Retrieved sources:", retrieved_sources)
        print("Answer:", answer)
        print("Retrieval:", retrieval_ok)
        print("Citation:", citation_ok)
        print("Abstention:", abstention_ok)
        print("Generation:", generation_ok)

        results.append({
            "id": question_id,
            "question": question,
            "answer": answer,
            "retrieved_sources": retrieved_sources,
            "retrieval_correct": retrieval_ok,
            "citation_correct": citation_ok,
            "abstention_correct": abstention_ok,
            "answer_generation_success": generation_ok
        })

    answerable_count = sum(not x["should_abstain"] for x in dataset)
    abstention_count = sum(x["should_abstain"] for x in dataset)

    print("\n" + "=" * 60)
    print("FINAL EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total questions: {total}")

    print(
        f"Retrieval source accuracy: "
        f"{retrieval_correct}/{answerable_count} "
        f"({retrieval_correct / answerable_count * 100:.2f}%)"
    )

    print(
        f"Citation filename accuracy: "
        f"{citation_correct}/{answerable_count} "
        f"({citation_correct / answerable_count * 100:.2f}%)"
    )

    print(
        f"Abstention accuracy: "
        f"{abstention_correct}/{abstention_count} "
        f"({abstention_correct / abstention_count * 100:.2f}%)"
    )

    print(
        f"Answer generation success: "
        f"{answer_generation_success}/{answerable_count} "
        f"({answer_generation_success / answerable_count * 100:.2f}%)"
    )

    output_path = PROJECT_ROOT / "evaluation" / "evaluation_results.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nDetailed results saved to:", output_path)


if __name__ == "__main__":
    run_evaluation()
