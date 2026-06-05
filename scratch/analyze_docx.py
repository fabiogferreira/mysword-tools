import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.word_to_journal import WordToJournalConverter

def main():
    docx_path = "UICP-2026.docx"
    if not os.path.exists(docx_path):
        print(f"Erro: {docx_path} não encontrado na raiz.")
        return
        
    print(f"Analisando documento: {docx_path}")
    converter = WordToJournalConverter(docx_path)
    
    # 1. Metadados extraídos
    metadata = converter.get_extracted_metadata()
    print("\n--- METADADOS EXTRAÍDOS ---")
    for k, v in metadata.items():
        print(f"  {k}: '{v}'")
        
    # 2. Presença de token de divisão explícita
    has_token = converter._has_division_tokens()
    print(f"\nTem token de divisão '@@---@@'? {has_token}")
    if has_token:
        token_count = sum(1 for p in converter.document.paragraphs if p.text.strip() == "@@---@@")
        print(f"  Quantidade de tokens: {token_count}")
        
    # 3. Estatística de estilos
    styles = {}
    headings_found = []
    for i, p in enumerate(converter.document.paragraphs):
        style_name = p.style.name if p.style else "Sem Estilo"
        styles[style_name] = styles.get(style_name, 0) + 1
        
        # Se parecer heading
        style_lower = style_name.lower()
        if "heading" in style_lower or "título" in style_lower or "title" in style_lower:
            headings_found.append((i, style_name, p.text.strip()[:60]))
            
    print("\n--- CONTAGEM DE ESTILOS NO DOCUMENTO ---")
    for style, count in sorted(styles.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {style}: {count} parágrafos")
        
    print("\n--- PARÁGRAFOS COM ESTILO DE HEADING/TÍTULO (Primeiros 20) ---")
    for i, style, text in headings_found[:20]:
        print(f"  Linha {i:4d} | Estilo: {style:20} | Conteúdo: {text}")
    if len(headings_found) > 20:
        print(f"  ... e mais {len(headings_found) - 20} headings")
        
    # 4. Tenta rodar a divisão de seções padrão
    print("\n--- TESTANDO DIVISÃO POR SEÇÕES (split_by_heading=True, level=1) ---")
    try:
        sections = converter._split_by_headings(heading_level=1)
        print(f"Total de seções geradas com level=1: {len(sections)}")
        for idx, (title, content, entry_id) in enumerate(sections[:5], 1):
            print(f"  Seção {idx}: Título='{title}' | ID='{entry_id}' | Tamanho={len(content)} caracteres")
    except Exception as e:
        print(f"Erro ao dividir level=1: {e}")
        
    # Testando com level detectado
    best_level = converter._detect_best_heading_level()
    print(f"\nNível de heading recomendado detectado: Heading {best_level}")
    try:
        sections_best = converter._split_by_headings(heading_level=best_level)
        print(f"Total de seções geradas com level recomendado ({best_level}): {len(sections_best)}")
        for idx, (title, content, entry_id) in enumerate(sections_best[:5], 1):
            print(f"  Seção {idx}: Título='{title}' | ID='{entry_id}' | Tamanho={len(content)} caracteres")
    except Exception as e:
        print(f"Erro ao dividir com level recomendado: {e}")

if __name__ == "__main__":
    main()
