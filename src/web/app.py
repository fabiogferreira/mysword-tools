"""
MySword Tools Web Backend
FastAPI server para validação, conversão de documentos Word e checkout via Stripe.
"""
import os
import tempfile
import shutil
import logging
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Header
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import stripe

from src.word_to_journal import WordToJournalConverter

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mysword-backend")

app = FastAPI(title="MySword Tools API", version="1.0.0")

# Habilita CORS para o frontend (Cloudflare Pages e localhost)
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5000",
    "https://myswordtools.alt.ia.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Stripe Sandbox
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "mock_stripe_secret_key")
stripe.api_key = STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test_webhook_secret_fake")

# Preços fictícios em sandbox (ex: R$ 4,90 avulso e R$ 19,90 mensal)
PRICE_SINGLE_CONVERSION = "price_single_conversion_fake"
PRICE_MONTHLY_SUBSCRIPTION = "price_monthly_subscription_fake"

@app.get("/api/health")
def health_check():
    return {"status": "ok", "stripe_enabled": STRIPE_SECRET_KEY != "mock_stripe_secret_key"}


@app.post("/api/critique")
async def analyze_document(file: UploadFile = File(...)):
    """
    Recebe um arquivo Word (.docx), realiza o upload temporário e executa a crítica de estrutura.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .docx são suportados.")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        
    try:
        converter = WordToJournalConverter(temp_path)
        metadata = converter.get_extracted_metadata()
        suggestions = converter.critique(split_by_heading=True, heading_level=1)
        
        # Converte as sugestões para dicionários serializáveis
        suggestions_list = [
            {"level": sug.level, "message": sug.message, "suggestion": sug.suggestion}
            for sug in suggestions
        ]
        
        return {
            "filename": file.filename,
            "metadata": metadata,
            "suggestions": suggestions_list,
            "has_token": converter._has_division_tokens()
        }
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao analisar documento: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/api/convert")
async def convert_document(
    file: UploadFile = File(...),
    abbreviation: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    split_by_heading: bool = Form(True),
    heading_level: int = Form(1)
):
    """
    Recebe um arquivo .docx, valida e converte para .jor.mybible retornando o binário gerado.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .docx são suportados.")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        
    # Gera o nome de saída correspondente
    output_filename = Path(file.filename).stem + ".jor.mybible"
    output_temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_temp_dir, output_filename)
    
    try:
        converter = WordToJournalConverter(temp_path)
        
        # Executa a conversão com parâmetros
        journal = converter.convert(
            abbreviation=abbreviation,
            title=title,
            description=description,
            author=author,
            split_by_heading=split_by_heading,
            heading_level=heading_level
        )
        
        # Salva o SQLite
        journal.save(output_path)
        
        # Retorna o arquivo gerado para download
        return FileResponse(
            path=output_path, 
            filename=output_filename, 
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"Erro na conversão: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao converter documento: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        # Deletamos o diretório temporário após o envio do response

@app.post("/api/checkout")
async def create_checkout_session(
    plan: str = Form(...),  # 'single', 'monthly', 'yearly'
    success_url: str = Form(...),
    cancel_url: str = Form(...)
):
    """
    Cria uma sessão de checkout do Stripe para compra avulsa ou plano mensal/anual.
    """
    try:
        # Define preços e modos com base no plano
        if plan == "single":
            mode = "payment"
            price_data = {
                "currency": "brl",
                "product_data": {
                    "name": "Crédito Avulso - MySword Tools",
                    "description": "Conversão de 1 arquivo Word para Journal do MySword"
                },
                "unit_amount": 490, # R$ 4,90
            }
            line_items = [{"price_data": price_data, "quantity": 1}]
        elif plan == "monthly":
            mode = "subscription"
            price_data = {
                "currency": "brl",
                "product_data": {
                    "name": "Plano Criador Mensal - MySword Tools",
                    "description": "Conversões ilimitadas mensalmente"
                },
                "unit_amount": 1990, # R$ 19,90
                "recurring": {"interval": "month"}
            }
            line_items = [{"price_data": price_data, "quantity": 1}]
        elif plan == "yearly":
            mode = "subscription"
            price_data = {
                "currency": "brl",
                "product_data": {
                    "name": "Plano Criador Anual - MySword Tools",
                    "description": "Conversões ilimitadas anualmente (Desconto de 37%)"
                },
                "unit_amount": 14990, # R$ 149,90
                "recurring": {"interval": "year"}
            }
            line_items = [{"price_data": price_data, "quantity": 1}]
        else:
            raise HTTPException(status_code=400, detail="Plano inválido.")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode=mode,
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return {"checkout_url": session.url}
    except Exception as e:
        logger.error(f"Erro ao criar sessão Stripe: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no Stripe Checkout: {str(e)}")

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request, sig_header: Optional[str] = Header(None)):
    """
    Webhook do Stripe para atualizar créditos e assinaturas em sandbox.
    """
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error("Payload inválido")
        return JSONResponse(status_code=400, content={"error": "Payload inválido"})
    except stripe.error.SignatureVerificationError as e:
        logger.error("Assinatura do webhook inválida")
        return JSONResponse(status_code=400, content={"error": "Assinatura inválida"})

    # Processa os eventos concluídos
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        logger.info(f"Sessão de pagamento concluída com sucesso: {session['id']}")
        # Aqui, no ambiente real, salvaríamos no banco os créditos ou a assinatura do usuário

    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
