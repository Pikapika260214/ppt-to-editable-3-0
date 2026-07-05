# OCR To Reconstruction Plan Review

Use `scripts/ocr_to_reconstruction_plan_scaffold.py` only to create a review-required text scaffold. Do not treat its output as a final reconstruction plan.

## Command

```powershell
python scripts/ocr_to_reconstruction_plan_scaffold.py path\to\ocr_results.json --source-image path\to\source.png --out path\to\source_reconstruction_plan.ocr-scaffold.json --review-manifest path\to\ocr_review_manifest.json
```

## What The Script Does

- Reads OCR records and source text boxes.
- Converts OCR pixel boxes into slide-inch text boxes.
- Marks every generated text element as `review_status: "needs_review"`.
- Writes a separate review manifest for accept/correct/omit/merge decisions.

## What It Does Not Do

- It does not correct OCR text.
- It does not infer native shapes, tables, icons, or source crop boundaries.
- It does not decide line-level versus semantic paragraph grouping.
- It does not make the output acceptable for final packaging.

## Review Rules

Before packaging:

- Correct mixed Chinese/English OCR errors.
- Omit accidental icon glyphs, decorative numbers, and low-value fragments.
- Merge true multiline semantic blocks when they should remain one editable text box.
- Keep labels as line-level text when visual alignment matters.
- Add native shapes and source crops separately; the OCR scaffold contains text only.
