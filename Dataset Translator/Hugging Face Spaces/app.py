from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import traceback

app = FastAPI(title="NLLB Translation API")

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cpu"
model.to(device)


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


@app.get("/")
def home():
    return {"message": "✅ NLLB Translation API is running!"}


@app.post("/translate")
def translate(request: TranslationRequest):
    try:
        # ✅ Convert language codes safely
        try:
            source_lang_id = tokenizer.convert_tokens_to_ids(request.source_lang)
            target_lang_id = tokenizer.convert_tokens_to_ids(request.target_lang)
        except:
            raise HTTPException(
                status_code=400,
                detail="Invalid language code"
            )

        # Set source language
        tokenizer.src_lang = request.source_lang

        # Tokenize
        inputs = tokenizer(
            request.text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)

        # Generate
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=target_lang_id,
            max_length=512,
            num_beams=4,
            early_stopping=True
        )

        # Decode
        output = tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )

        return {"translation": output[0]}

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
