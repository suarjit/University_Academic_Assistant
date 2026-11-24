
import json
import re
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


def normalize_text(text):
    """Normalize text for simple evidence matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def evidence_supported(expected_answer, retrieved_documents):
    """
    Check whether the retrieved expected source contains
    the expected answer's important words.

    This is a simple lexical check, not semantic verification.
    """
    expected_words = set(normalize_text(expected_answer).split())

    # Ignore very common words.
    stop_words = {
        "the", "a", "an", "is", "are", "of", "to",
        "and", "in", "for", "with", "at", "on"
    }

    important_words = expected_words - stop_words

    if not important_words:
        return False

    for document in retrieved_documents:
        document_words = set(
            normalize_text(document["text"]).split()
        )

        overlap = important_words.intersection(document_words)

        # At least 70% of important expected words must be present.
        if len(overlap) / len(important_words) >= 0.70:
            return True

    return False


def run_evaluation():
    dataset = load_evaluation_dataset()

    total = len(dataset)

    retrieval_correct = 0
    citation_correct = 0
    evidence_correct = 0
    abstention_correct = 0
    answer_generation_success = 0

    results = []

    for item in dataset:
        question_id = item["id"]
        question = item["question"]
        expected_source = item["expected_source"]
        expected_answer = item["expected_answer"]
        should_abstain = item["should_abstain"]

        print(f"\n{'=' * 60}")
        print(f"TEST {question_id}/{total}")
        print("Question:", question)

        retrieved_documents = retrieve_documents(question, k=4)

        retrieved_sources = list(
            dict.fromkeys(
                doc["source"] for doc in retrieved_documents
            )
        )

        result = answer_question(question, k=4)
        answer = result["answer"]

        if should_abstain:
            retrieval_ok = None
            citation_ok = None
            evidence_ok = None
            generation_ok = None

            abstention_ok = (
                answer.strip() == EXPECTED_ABSTENTION
            )

            if abstention_ok:
                abstention_correct += 1

        else:
            retrieval_ok = expected_source in retrieved_sources

            expected_source_documents = [
                doc for doc in retrieved_documents
                if doc["source"] == expected_source
            ]

            evidence_ok = (
                evidence_supported(
                    expected_answer,
                    expected_source_documents
                )
                if expected_source_documents
                else False
            )

            citation_ok = (
                expected_source in answer
                and evidence_ok
            )

            abstention_ok = None

            generation_ok = (
                bool(answer.strip())
                and answer.strip() != EXPECTED_ABSTENTION
            )

            if retrieval_ok:
                retrieval_correct += 1

            if citation_ok:
                citation_correct += 1

            if evidence_ok:
                evidence_correct += 1

            if generation_ok:
                answer_generation_success += 1

        print("Retrieved sources:", retrieved_sources)
        print("Answer:", answer)
        print("Retrieval:", retrieval_ok)
        print("Evidence support:", evidence_ok)
        print("Citation support:", citation_ok)
        print("Abstention:", abstention_ok)
        print("Generation:", generation_ok)

        results.append({
            "id": question_id,
            "question": question,
            "expected_source": expected_source,
            "expected_answer": expected_answer,
            "answer": answer,
            "retrieved_sources": retrieved_sources,
            "retrieval_correct": retrieval_ok,
            "evidence_supported": evidence_ok,
            "citation_supported": citation_ok,
            "abstention_correct": abstention_ok,
            "answer_generation_success": generation_ok
        })

    answerable_count = sum(
        not item["should_abstain"] for item in dataset
    )

    abstention_count = sum(
        item["should_abstain"] for item in dataset
    )

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
        f"Evidence support accuracy: "
        f"{evidence_correct}/{answerable_count} "
        f"({evidence_correct / answerable_count * 100:.2f}%)"
    )

    print(
        f"Citation support accuracy: "
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

    output_path = (
        PROJECT_ROOT / "evaluation" / "evaluation_results.json"
    )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nDetailed results saved to:", output_path)


if __name__ == "__main__":
    run_evaluation()
