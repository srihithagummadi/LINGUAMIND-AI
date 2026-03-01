from transformers import BartForConditionalGeneration, BartTokenizer, MarianMTModel, MarianTokenizer

# Load summarization model (lighter than mBART)
summarizer_model_name = "facebook/bart-large-cnn"
summarizer_tokenizer = BartTokenizer.from_pretrained(summarizer_model_name)
summarizer_model = BartForConditionalGeneration.from_pretrained(summarizer_model_name)

# Translation helper
def translate(text, target_lang="hi"):
    """
    Translate English text into target language using MarianMT.
    Supported codes: "hi" (Hindi), "te" (Telugu)
    """
    model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
    trans_tokenizer = MarianTokenizer.from_pretrained(model_name)
    trans_model = MarianMTModel.from_pretrained(model_name)

    inputs = trans_tokenizer(text, return_tensors="pt", truncation=True)
    translated_ids = trans_model.generate(**inputs)
    return trans_tokenizer.decode(translated_ids[0], skip_special_tokens=True)

# Summarization function
def summarize(text, max_length=150):
    """
    Summarize the given text in English using BART.
    """
    inputs = summarizer_tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = summarizer_model.generate(
        inputs["input_ids"],
        num_beams=4,
        length_penalty=2.0,
        max_length=max_length,
        early_stopping=True
    )
    return summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# -----------------------------
# Console input demo
# -----------------------------
if __name__ == "__main__":
    print("=== Multilingual Text Summarizer ===")
    print("Supported languages: English, Hindi, Telugu\n")

    text = input("Enter the text to summarize: ").strip()

    # Validate language input
    while True:
        language = input("Enter language (english/hindi/telugu): ").strip().lower()
        if language in ["english", "hindi", "telugu"]:
            break
        print("Invalid input. Please type english, hindi, or telugu.\n")

    try:
        # Step 1: Summarize in English
        summary = summarize(text)

        # Step 2: Translate if needed
        if language == "hindi":
            summary = translate(summary, "hi")
        elif language == "telugu":
            summary = translate(summary, "te")

        print("\n--- Summary ---")
        print(summary)

    except Exception as e:
        print(f"Error: {e}")