

from fastapi import APIRouter, Body
from pydantic import BaseModel
from transformers import GPT2TokenizerFast

router = APIRouter()
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

class TokenInput(BaseModel):
    text: str

@router.post("/tokenize")
async def tokenize(input: TokenInput):
    tokens = tokenizer.encode(input.text)
    return {
        "input": input.text,
        "token_count": len(tokens),
        "tokens": tokens
    }