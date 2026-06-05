import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.word_to_journal import WordToJournalConverter, HTMLListManager

def main():
    docx_path = "UICP-2026.docx"
    print("Iniciando depuração minuciosa...")
    converter = WordToJournalConverter(docx_path)
    
    p_map = {p._element: p for p in converter.document.paragraphs}
    tbl_map = {t._element: t for t in converter.document.tables}
    
    list_manager = HTMLListManager(converter._get_list_tag)
    
    print(f"Total de elementos no body: {len(converter.document.element.body)}")
    
    for idx, element in enumerate(converter.document.element.body):
        print(f"Elemento {idx}: tag={element.tag}")
        if element.tag.endswith('p'):
            para = p_map.get(element)
            if para:
                text_preview = para.text.strip()[:30].replace('\n', ' ')
                print(f"  Parágrafo: '{text_preview}'")
                
                # Vamos testar _get_paragraph_info
                info = converter._get_paragraph_info(para)
                print(f"    info: {info}")
                
                # Vamos testar handle_paragraph
                print("    Chamando handle_paragraph...")
                list_tags = list_manager.handle_paragraph(info)
                print(f"    list_tags: {list_tags}")
                
                # Vamos testar _paragraph_to_html
                print("    Chamando _paragraph_to_html...")
                inner_html = converter._paragraph_to_html(para)
                print(f"    inner_html tamanho: {len(inner_html)}")
        elif element.tag.endswith('tbl'):
            table = tbl_map.get(element)
            if table:
                print("  Tabela encontrada.")
                print("    Chamando _table_to_html...")
                table_html = converter._table_to_html(table)
                print(f"    table_html tamanho: {len(table_html)}")
                
    print("Fim do teste sem travamentos!")

if __name__ == "__main__":
    main()
