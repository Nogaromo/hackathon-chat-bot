from catboost import CatBoostClassifier
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


def clf(s: str) -> bool:
    model_cat = CatBoostClassifier()
    model_cat.load_model("text_clf.cbm")
    return model_cat.predict([s])


model_name = "cointegrated/rut5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)


def bran(s: str) -> bool:
    model_cat_bran = CatBoostClassifier()
    model_cat_bran.load_model("toxic_clf.cbm")
    return model_cat_bran.predict([s])


def answer(x, **kwargs):
    inputs = tokenizer(x, return_tensors='pt').to(model.device)
    with torch.no_grad():
        hypotheses = model.generate(**inputs, **kwargs)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)


def big_model(s: str) -> str:
    model.load_state_dict(torch.load('rut5_1000.pt', map_location=torch.device('cpu')))
    model.eval()
    return answer(s, max_new_tokens=10_000)
