import os
from dotenv import load_dotenv
from langfuse import get_client, observe
from graph import run_agent

load_dotenv()

EVAL_USER_ID = "eval-script"

EVAL_SET = [
    {"question": "What is throwaway prototyping?", "expected": "answer", "category": "in-document"},
    {"question": "What are the advantages of evolutionary prototyping?", "expected": "answer", "category": "in-document"},
    {"question": "Compare evolutionary and throwaway prototyping", "expected": "answer", "category": "in-document"},
    {"question": "What's the capital of France?", "expected": "refuse", "category": "off-topic"},
    {"question": "How do I make pasta?", "expected": "refuse", "category": "off-topic"},
    {"question": "What is Agile development?", "expected": "refuse", "category": "off-topic-borderline"},
    {"question": "Tell me about risk in software projects", "expected": "answer", "category": "borderline"},
    {"question": "give me a quiz", "expected": "quiz_format", "category": "intent-routing"},
    {"question": "summarize this", "expected": "summary_format", "category": "intent-routing"},
    {"question": "can you please explain this in easy to understand words", "expected": "explain_format", "category": "intent-routing"},
    {"question": "what are the important topics mentioned in this document", "expected": "topics_format", "category": "intent-routing"},
]

REFUSAL_PHRASE = "i could not find this information in the uploaded document"


def score_result(question: str, answer: str, expected: str) -> dict:
    answer_lower = answer.lower()
    refused = REFUSAL_PHRASE in answer_lower

    if expected == "refuse":
        passed = refused
    elif expected == "answer":
        passed = not refused
    elif expected == "quiz_format":
        passed = "answer:" in answer_lower and any(c in answer for c in ["A)", "B)"])
    elif expected == "summary_format":
        passed = not refused and len(answer) > 100
    elif expected == "explain_format":
        passed = not refused and len(answer) > 100
    elif expected == "topics_format":
        passed = not refused and ("-" in answer or "•" in answer)
    else:
        passed = None

    return {"passed": passed, "refused": refused, "answer_length": len(answer)}


@observe(name="eval-case")
def run_single_case(question: str, expected: str):
    response = run_agent(question, user_id=EVAL_USER_ID)
    answer = response["answer"]
    score = score_result(question, answer, expected)

    langfuse = get_client()

    langfuse.update_current_span(
        input=question,
        output=answer,
        metadata={"expected": expected, "passed": score["passed"]},
    )

    try:
        langfuse.score_current_span(
            name="eval-pass",
            value=1 if score["passed"] else 0,
        )
    except Exception as e:
        print(f"  (scoring skipped: {e})")

    return answer, score


def run_eval():
    results = []

    for case in EVAL_SET:
        answer, score = run_single_case(case["question"], case["expected"])

        results.append({
            "question": case["question"],
            "category": case["category"],
            "expected": case["expected"],
            "passed": score["passed"],
            "answer_preview": answer[:100],
        })

        status = "✅ PASS" if score["passed"] else "❌ FAIL"
        print(f"{status} | {case['category']:20} | {case['question']}")

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{passed}/{total} passed ({passed/total*100:.0f}%)")

    return results


if __name__ == "__main__":
    run_eval()