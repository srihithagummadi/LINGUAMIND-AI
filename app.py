from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import os

# Disable HF Hub symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load model and tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

lang_codes = {
    "english": "en_XX",
    "hindi": "hi_IN",
    "telugu": "te_IN"
}

app = Flask(__name__)

def generate_summary(text, language="english", max_length=150):
    if language not in lang_codes:
        return f"Unsupported language. Choose from {list(lang_codes.keys())}"

    tokenizer.src_lang = lang_codes["english"]  # assume input text is English
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding="longest")

    target_lang_code = lang_codes[language]
    forced_bos_token_id = tokenizer.lang_code_to_id[target_lang_code]

    summary_ids = model.generate(
        **encoded,
        max_length=max_length,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True,
        forced_bos_token_id=forced_bos_token_id
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "english").lower()

    summary = generate_summary(text, language)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)