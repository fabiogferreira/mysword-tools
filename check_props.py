from docx import Document
doc = Document('examples/estudo_oracao.docx')
print('Propriedades do documento:')
print(f'  title: "{doc.core_properties.title}"')
print(f'  author: "{doc.core_properties.author}"')
print(f'  subject: "{doc.core_properties.subject}"')
print(f'  keywords: "{doc.core_properties.keywords}"')
