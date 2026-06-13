import json
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import precision_score, recall_score, f1_score
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "sshleifer/tiny-gpt2"
ADAPTER_PATH = "outputs/sft_lora_final"


def load_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))

    return rows


def build_prompt(row):
    return f"""
Instruction:
{row['instruction']}

User Request:
{row['input']}

Answer:
"""


def extract_json(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return text[start:end]
    except:
        return ""


def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False


def normalize_json(text):
    try:
        return json.dumps(json.loads(text), sort_keys=True)
    except:
        return None


def extract_tool_name(json_text):
    try:
        data = json.loads(json_text)
        return data.get("tool_name", "unknown")
    except:
        return "invalid"


print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH
)

model.eval()

print("Loading test dataset...")

test_data = load_jsonl("data/test.jsonl")

results = []

y_true = []
y_pred = []

for row in tqdm(test_data[:100]):

    prompt = build_prompt(row)

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    output_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    decoded = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    prediction = decoded.split("Answer:")[-1].strip()

    prediction_json = extract_json(prediction)

    gold_json = row["output"]

    valid = is_valid_json(prediction_json)

    exact_match = (
        normalize_json(prediction_json)
        ==
        normalize_json(gold_json)
    )

    gold_tool = extract_tool_name(gold_json)
    pred_tool = extract_tool_name(prediction_json)

    y_true.append(gold_tool)
    y_pred.append(pred_tool)

    results.append({
        "input": row["input"],
        "gold": gold_json,
        "prediction": prediction_json,
        "gold_tool": gold_tool,
        "predicted_tool": pred_tool,
        "valid_json": valid,
        "exact_match": exact_match
    })

df = pd.DataFrame(results)

json_validity_rate = df["valid_json"].mean() * 100
exact_match_rate = df["exact_match"].mean() * 100

tool_accuracy = (
    sum(
        g == p
        for g, p in zip(y_true, y_pred)
    )
    / len(y_true)
) * 100

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n========== EVALUATION ==========")
print(f"JSON Validity Rate : {json_validity_rate:.2f}%")
print(f"Exact Match Rate   : {exact_match_rate:.2f}%")
print(f"Tool Accuracy      : {tool_accuracy:.2f}%")
print(f"Precision          : {precision:.4f}")
print(f"Recall             : {recall:.4f}")
print(f"F1 Score           : {f1:.4f}")

df.to_csv(
    "reports/evaluation_results.csv",
    index=False
)

metrics = pd.DataFrame([
    {
        "JSON Validity Rate": round(json_validity_rate, 2),
        "Exact Match Accuracy": round(exact_match_rate, 2),
        "Tool Accuracy": round(tool_accuracy, 2),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4)
    }
])

metrics.to_csv(
    "reports/metrics.csv",
    index=False
)

with open(
    "reports/metrics.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(f"JSON Validity Rate: {json_validity_rate:.2f}%\n")
    f.write(f"Exact Match Accuracy: {exact_match_rate:.2f}%\n")
    f.write(f"Tool Accuracy: {tool_accuracy:.2f}%\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")

print("\nSaved:")
print("reports/evaluation_results.csv")
print("reports/metrics.csv")
print("reports/metrics.txt")