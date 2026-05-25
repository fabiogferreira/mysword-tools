"""
Script de teste de conversão para verificar se as entradas do MySword estão sendo geradas e divididas corretamente.
"""
import os
import sys
import sqlite3
from pathlib import Path

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.word_to_journal import WordToJournalConverter, ConversionOptions

def test_conversion():
    test_files = [
        "examples/estudo_oracao.docx",
        "examples/template_estudo_biblico.docx"
    ]
    
    # Forçar criação
    os.makedirs("output", exist_ok=True)
    
    for input_docx in test_files:
        if not os.path.exists(input_docx):
            print(f"\nArquivo não encontrado: {input_docx}")
            continue
            
        output_db = f"output/test_{Path(input_docx).stem}.jor.mybible"
        if os.path.exists(output_db):
            os.remove(output_db)
            
        print("\n" + "="*50)
        print(f"Analisando arquivo: {input_docx}")
        print("="*50)
        
        converter = WordToJournalConverter(input_docx)
        
        # Executa a crítica (análise de estrutura)
        suggestions = converter.critique(split_by_heading=True, heading_level=1)
        print("Crítica / Sugestões:")
        for sug in suggestions:
            print(f"  [{sug.level}] {sug.message}")
            if sug.suggestion:
                print(f"    Sugestão: {sug.suggestion}")
                
        # Executa a conversão
        print(f"Convertendo para: {output_db}")
        journal = converter.convert(
            abbreviation=Path(input_docx).stem[:10].upper(),
            title=f"Estudo {Path(input_docx).stem}",
            description="Conversão de teste",
            author="Autor de Teste",
            split_by_heading=True,
            heading_level=1
        )
        journal.save(output_db)
        
        # Valida as tabelas geradas no SQLite
        print("Validando banco de dados gerado...")
        conn = sqlite3.connect(output_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM journal")
        count = cursor.fetchone()[0]
        print(f"  Número total de entradas na tabela 'journal': {count}")
        
        cursor.execute("SELECT title, length(content) FROM journal")
        rows = cursor.fetchall()
        print("  Entradas geradas:")
        for idx, (title, length) in enumerate(rows, 1):
            print(f"    {idx}. {title} ({length} caracteres de conteúdo)")
            
        conn.close()

if __name__ == "__main__":
    test_conversion()
