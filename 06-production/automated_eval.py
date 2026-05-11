from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

"""
================================================================================
LLM-AS-A-JUDGE: Automated Quality Auditing
================================================================================
We use RAGAS to ensure:
1. Faithfulness: Is the answer derived ONLY from the retrieved context?
2. Relevancy: Does the answer actually address the user's question?
================================================================================
"""

# Example data from production logs
data_sample = {
    'question': ['موجودی حساب من چقدر است؟'],
    'answer': ['موجودی شما ۱۰ میلیون تومان است.'],
    'contexts': [['طبق آخرین تراکنش، حساب شما دارای ۱۰ میلیون تومان مانده است.']],
}

dataset = Dataset.from_dict(data_sample)
score = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

print(f"RAG Quality Scores: {score}")