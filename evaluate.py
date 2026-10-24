
import csv
from pathlib import Path

from main import detect_risk, calculate_risk


DATASET_FILE = Path(__file__).parent / "test_messages.csv"


def predict_message(message):
    warning_signs = detect_risk(message)
    score, level = calculate_risk(warning_signs)

    # For this prototype, medium and high risk mean suspicious.
    prediction = "suspicious" if level in ("medium", "high") else "ordinary"

    return prediction, score, level, warning_signs


def main():
    total = 0
    correct = 0

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    print("\nGUARDIAN ANGEL - DATASET EVALUATION\n")

    with DATASET_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        required_columns = {"message", "expected_label"}
        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError(
                "CSV must contain message and expected_label columns."
            )

        for row in reader:
            message = row["message"].strip()
            expected = row["expected_label"].strip().lower()

            if expected not in ("suspicious", "ordinary"):
                raise ValueError(
                    f"Invalid label in dataset: {expected}"
                )

            predicted, score, level, signs = predict_message(message)

            total += 1
            is_correct = predicted == expected
            correct += int(is_correct)

            if expected == "suspicious" and predicted == "suspicious":
                true_positive += 1
            elif expected == "ordinary" and predicted == "ordinary":
                true_negative += 1
            elif expected == "ordinary" and predicted == "suspicious":
                false_positive += 1
            else:
                false_negative += 1

            result = "CORRECT" if is_correct else "INCORRECT"

            print(f"[{result}] {message}")
            print(
                f"  Expected: {expected} | Predicted: {predicted} "
                f"| Risk: {level} | Score: {score}"
            )
            print(f"  Warning signs: {signs or 'None'}\n")

    if total == 0:
        print("The dataset contains no messages.")
        return

    accuracy = correct / total
    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0
    )

    print("=" * 45)
    print("EVALUATION SUMMARY")
    print("=" * 45)
    print(f"Total messages:      {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy:            {accuracy:.1%}")
    print(f"Precision:           {precision:.1%}")
    print(f"Recall:              {recall:.1%}")
    print(f"True positives:      {true_positive}")
    print(f"True negatives:      {true_negative}")
    print(f"False positives:     {false_positive}")
    print(f"False negatives:     {false_negative}")


if __name__ == "__main__":
    main()
