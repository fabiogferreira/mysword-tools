"""
Depura o XML do docx para entender a estrutura dos elementos de imagem
"""
import os
import sys
from pathlib import Path
from docx import Document

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def debug_docx():
    docx_path = "examples/test_image_doc.docx"
    doc = Document(docx_path)
    
    print("Mapeando elementos XML do corpo:")
    for idx, p in enumerate(doc.paragraphs, 1):
        print(f"Parágrafo {idx}: '{p.text}'")
        # Mostra runs
        for run_idx, run in enumerate(p.runs, 1):
            print(f"  Run {run_idx}: text='{run.text}'")
            # Procura qualquer w:drawing
            drawings = run.element.xpath('.//w:drawing')
            print(f"    w:drawing encontrados: {len(drawings)}")
            for d in drawings:
                print("      XML do desenho:")
                # Mostra namespaces
                print(f"      Namespaces no desenho: {d.nsmap}")
                # Mostra relação embed usando local-name() para ignorar namespaces no lxml
                blips = d.xpath('.//*[local-name()="blip"]')
                print(f"      Elementos blip encontrados: {len(blips)}")
                if blips:
                    # Tenta obter o atributo embed
                    rId = blips[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    print(f"      rId da relação de imagem (embed): '{rId}'")

if __name__ == "__main__":
    debug_docx()
