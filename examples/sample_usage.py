"""
Exemplo de uso do MySword Tools

Este script demonstra como usar as classes do MySword Tools
para criar um Journal programaticamente.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mysword_journal import (
    MySwordJournal,
    create_bible_link,
    create_strong_link,
    format_heading,
    wrap_paragraph
)


def create_sample_journal():
    """Cria um Journal de exemplo com estudos bíblicos."""
    
    # Cria o Journal
    journal = MySwordJournal(
        abbreviation="EXEMPLO",
        title="Journal de Exemplo",
        description="Journal de Exemplo - MySword Tools",
        author="MySword Tools",
        language="por",
        read_only=False
    )
    
    # ===== Entrada 1: Introdução =====
    content1 = f"""
    {format_heading("Bem-vindo ao MySword Tools", 2)}
    
    {wrap_paragraph("Este é um exemplo de Journal criado com o MySword Tools. "
                   "Você pode criar entradas com formatação HTML, links para versículos, "
                   "referências Strong e muito mais.")}
    
    {format_heading("Recursos Disponíveis", 3)}
    <ul>
        <li><b>Formatação HTML</b> - Negrito, itálico, cores, etc.</li>
        <li><b>Links Bíblicos</b> - Links clicáveis para versículos</li>
        <li><b>Números Strong</b> - Links para o dicionário Strong</li>
        <li><b>Tabelas</b> - Dados organizados em tabelas</li>
    </ul>
    """
    
    journal.add_entry("Introdução", content1)
    
    # ===== Entrada 2: O Amor de Deus =====
    content2 = f"""
    {format_heading("O Amor de Deus", 2)}
    
    {wrap_paragraph(f"Um dos versículos mais conhecidos da Bíblia é {create_bible_link('João 3:16', 'João 3:16')}:")}
    
    <blockquote style='background:#f5f5f5; padding:10px; border-left:3px solid #007bff;'>
    "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, 
    para que todo aquele que nele crê não pereça, mas tenha a vida eterna."
    </blockquote>
    
    {format_heading("Palavras-chave em Grego", 3)}
    
    <ul>
        <li><b>Amou</b> ({create_strong_link('G25', 'ἀγαπάω - agapaō')}) - Amor incondicional</li>
        <li><b>Mundo</b> ({create_strong_link('G2889', 'κόσμος - kosmos')}) - O mundo, humanidade</li>
        <li><b>Vida</b> ({create_strong_link('G2222', 'ζωή - zōē')}) - Vida eterna, espiritual</li>
    </ul>
    
    {format_heading("Referências Relacionadas", 3)}
    
    <p>Veja também:</p>
    <ul>
        <li>{create_bible_link('Romanos 5:8')}</li>
        <li>{create_bible_link('1 João 4:9-10')}</li>
        <li>{create_bible_link('Efésios 2:4-5')}</li>
    </ul>
    """
    
    journal.add_entry("O Amor de Deus", content2)
    
    # ===== Entrada 3: Tabela de Livros =====
    content3 = f"""
    {format_heading("Os Livros da Bíblia", 2)}
    
    {wrap_paragraph("A Bíblia é composta por 66 livros, divididos em Antigo e Novo Testamento.")}
    
    {format_heading("Antigo Testamento (39 livros)", 3)}
    
    <table border='1' cellpadding='8' cellspacing='0' style='border-collapse:collapse; width:100%;'>
        <tr style='background:#e9ecef;'>
            <th>Divisão</th>
            <th>Livros</th>
            <th>Quantidade</th>
        </tr>
        <tr>
            <td><b>Pentateuco</b></td>
            <td>Gênesis a Deuteronômio</td>
            <td style='text-align:center;'>5</td>
        </tr>
        <tr>
            <td><b>Históricos</b></td>
            <td>Josué a Ester</td>
            <td style='text-align:center;'>12</td>
        </tr>
        <tr>
            <td><b>Poéticos</b></td>
            <td>Jó a Cantares</td>
            <td style='text-align:center;'>5</td>
        </tr>
        <tr>
            <td><b>Profetas Maiores</b></td>
            <td>Isaías a Daniel</td>
            <td style='text-align:center;'>5</td>
        </tr>
        <tr>
            <td><b>Profetas Menores</b></td>
            <td>Oséias a Malaquias</td>
            <td style='text-align:center;'>12</td>
        </tr>
    </table>
    
    {format_heading("Novo Testamento (27 livros)", 3)}
    
    <table border='1' cellpadding='8' cellspacing='0' style='border-collapse:collapse; width:100%;'>
        <tr style='background:#e9ecef;'>
            <th>Divisão</th>
            <th>Livros</th>
            <th>Quantidade</th>
        </tr>
        <tr>
            <td><b>Evangelhos</b></td>
            <td>Mateus a João</td>
            <td style='text-align:center;'>4</td>
        </tr>
        <tr>
            <td><b>Histórico</b></td>
            <td>Atos</td>
            <td style='text-align:center;'>1</td>
        </tr>
        <tr>
            <td><b>Cartas Paulinas</b></td>
            <td>Romanos a Filemom</td>
            <td style='text-align:center;'>13</td>
        </tr>
        <tr>
            <td><b>Cartas Gerais</b></td>
            <td>Hebreus a Judas</td>
            <td style='text-align:center;'>8</td>
        </tr>
        <tr>
            <td><b>Profético</b></td>
            <td>Apocalipse</td>
            <td style='text-align:center;'>1</td>
        </tr>
    </table>
    """
    
    journal.add_entry("Livros da Bíblia", content3)
    
    # ===== Entrada 4: Notas de Estudo =====
    content4 = f"""
    {format_heading("Anotações Pessoais", 2)}
    
    {wrap_paragraph("Use esta seção para suas anotações pessoais de estudo bíblico.")}
    
    {format_heading("Dicas de Estudo", 3)}
    
    <ol>
        <li><b>Ore antes de estudar</b> - Peça orientação ao Espírito Santo</li>
        <li><b>Leia o contexto</b> - Entenda o versículo no seu contexto</li>
        <li><b>Use referências cruzadas</b> - Compare com outros textos</li>
        <li><b>Estude palavras-chave</b> - Use o dicionário Strong</li>
        <li><b>Aplique à sua vida</b> - Busque aplicação prática</li>
    </ol>
    
    {format_heading("Versículo do Dia", 3)}
    
    <p style='text-align:center; font-size:larger;'>
        <i>"Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho."</i>
        <br/>
        — {create_bible_link('Salmo 119:105')}
    </p>
    """
    
    journal.add_entry("Notas de Estudo", content4)
    
    # Salva o Journal
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "exemplo.jor.mybible"
    journal.save(str(output_file))
    
    print(f"✅ Journal criado: {output_file}")
    print(f"   📝 Entradas: {journal.get_entry_count()}")
    print(f"   🏷️  Abreviação: {journal.details.abbreviation}")
    
    return journal


if __name__ == "__main__":
    create_sample_journal()
