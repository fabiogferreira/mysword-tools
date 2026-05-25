"""Testa extração de metadados"""
import sys
sys.path.insert(0, '.')

from src.word_to_journal import WordToJournalConverter

converter = WordToJournalConverter('examples/estudo_oracao.docx')
metadata = converter.get_extracted_metadata()

print("Metadados extraídos:")
for key, value in metadata.items():
    print(f"  {key}: '{value}'")
