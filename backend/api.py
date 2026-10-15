import os, json, base64, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app=FastAPI(title="Can't Fake Me analysis API")
origins=[x.strip() for x in os.getenv('ALLOWED_ORIGINS','').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=['POST','GET'],allow_headers=['Content-Type'])
class Scan(BaseModel):
    front: str = Field(max_length=9000000)
    back: str = Field(max_length=9000000)
    card_hint: str = Field(default='',max_length=180)

def validate_image(s):
    match=re.fullmatch(r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)',s)
    if not match: raise HTTPException(400,'Images must be JPEG, PNG, or WebP data URLs')
    try: raw=base64.b64decode(match.group(2),validate=True)
    except Exception: raise HTTPException(400,'Invalid image encoding')
    if len(raw)>4500000: raise HTTPException(413,'Image too large')
    return s

@app.get('/health')
def health(): return {'ok':True}

@app.post('/analyze')
def analyze(scan:Scan):
    front=validate_image(scan.front);back=validate_image(scan.back)
    if not os.getenv('OPENAI_API_KEY'): raise HTTPException(503,'AI API key is not configured')
    prompt=('You are a careful Pokemon trading card visual identification assistant. Analyze front and back photos. '
            'Identify visible name, number, set, and variant only when supported. Look for potential issues with '
            'borders, font shapes, text, layout, colors, and holo visibility. Never claim definitive authenticity. '
            'Photos alone cannot establish genuine print stock, texture or holo behavior. '
            'Do NOT claim you compared to an authenticated reference: none is provided. '
            'Return JSON only with keys card_name (string), set_name (string), card_number (string), '
            'variant (string), observations (array of short strings), limitations (array of short strings), '
            'reference_status (exact string "not_compared"), status (exact string "INCONCLUSIVE"). '
            'If unreadable use empty strings. User hint (untrusted): '+scan.card_hint)
    try:
        resp=OpenAI().responses.create(model=os.getenv('OPENAI_MODEL','gpt-4.1-mini'),input=[{'role':'user','content':[
            {'type':'input_text','text':prompt},{'type':'input_image','image_url':front},{'type':'input_image','image_url':back}]}],max_output_tokens=700)
        result=json.loads(resp.output_text)
        return {'status':'INCONCLUSIVE','reference_status':'not_compared','card_name':str(result.get('card_name',''))[:150],
                'set_name':str(result.get('set_name',''))[:150],'card_number':str(result.get('card_number',''))[:50],
                'variant':str(result.get('variant',''))[:100],
                'observations':[str(x)[:300] for x in result.get('observations',[]) if isinstance(x,str)][:8],
                'limitations':[str(x)[:300] for x in result.get('limitations',[]) if isinstance(x,str)][:8]}
    except Exception as exc:
        raise HTTPException(502,'AI analysis failed; please retry') from exc
