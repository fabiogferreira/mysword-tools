"""
Script de teste de API para validar os endpoints usando FastAPI TestClient
"""
import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.web.app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    print(f"Health Check Response: {response.status_code}")
    print(response.json())
    assert response.status_code == 200

def test_critique_endpoint():
    print("\nTestando /api/critique...")
    docx_path = "examples/test_token.docx"
    
    if not os.path.exists(docx_path):
        print(f"Erro: arquivo de teste {docx_path} não existe.")
        return
        
    with open(docx_path, "rb") as f:
        response = client.post(
            "/api/critique",
            files={"file": (os.path.basename(docx_path), f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Metadados: {data['metadata']}")
        print(f"Tem Token @@---@@? {data['has_token']}")
        print("Sugestões:")
        for sug in data["suggestions"]:
            print(f"  [{sug['level']}] {sug['message']}")
    else:
        print(response.text)
        
    assert response.status_code == 200

def test_convert_endpoint():
    print("\nTestando /api/convert...")
    docx_path = "examples/test_token.docx"
    output_db = "output/test_api_conversion.jor.mybible"
    
    if os.path.exists(output_db):
        os.remove(output_db)
        
    with open(docx_path, "rb") as f:
        response = client.post(
            "/api/convert",
            files={"file": (os.path.basename(docx_path), f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={
                "abbreviation": "APITEST",
                "title": "API Test Journal",
                "author": "FastAPI Tester",
                "split_by_heading": True,
                "heading_level": 1
            }
        )
        
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        # Salva o arquivo retornado
        os.makedirs("output", exist_ok=True)
        with open(output_db, "wb") as f:
            f.write(response.content)
        print(f"Arquivo gerado salvo em: {output_db}")
        assert os.path.exists(output_db)
    else:
        print(response.text)
        
    assert response.status_code == 200

if __name__ == "__main__":
    test_health()
    test_critique_endpoint()
    test_convert_endpoint()
    print("\nTodos os testes de API foram concluídos com sucesso!")
