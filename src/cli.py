"""
CLI Principal - Interface de linha de comando para MySword Tools
"""

import click
from pathlib import Path


@click.group()
@click.version_option(version="1.0.0", prog_name="mysword-tools")
def cli():
    """
    MySword Tools - Ferramentas para criar conteúdo compatível com MySword.
    
    Uso:
        mysword-tools word2journal input.docx output.jou
    """
    pass


@cli.command('word2journal')
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(), required=False)
@click.option('--title', '-t', help='Descrição/título do Journal')
@click.option('--abbreviation', '-a', help='Abreviação do Journal (sem espaços)')
@click.option('--language', '-l', default='por', help='Código do idioma ISO (3 letras)')
@click.option('--no-split', is_flag=True, help='Não dividir documento por títulos')
@click.option('--heading-level', '-h', default=0, type=int, 
              help='Nível do heading para divisão (1-6, 0=auto)')
@click.option('--read-only', '-r', is_flag=True, help='Criar Journal somente leitura')
def word_to_journal(input_file, output_file, title, abbreviation, language, 
                    no_split, heading_level, read_only):
    """
    Converte documento Word (.docx) para Journal do MySword (.jou).
    
    Exemplos:
    
        \b
        # Conversão básica
        mysword-tools word2journal estudo.docx
        
        \b
        # Com opções
        mysword-tools word2journal estudo.docx meu_estudo.jou \\
            --title "Meus Estudos Bíblicos" \\
            --abbreviation "ESTUDOS"
    """
    from .word_to_journal import WordToJournalConverter
    
    input_path = Path(input_file)
    
    # Define arquivo de saída se não especificado
    if output_file is None:
        # Gera nome baseado no input, mas garante minúsculas
        output_file = input_path.with_suffix('.jou').name.lower()
    else:
        # Se fornecido, também garante minúsculas no nome final
        output_file = str(output_file).lower()
    
    # Define abreviação se não especificada
    if abbreviation is None:
        abbreviation = input_path.stem.replace(' ', '_')[:20].upper()
    
    # Define título se não especificado
    if title is None:
        title = f"Convertido de {input_path.name}"
    
    try:
        click.echo(f"📄 Lendo: {input_path.name}")
        
        converter = WordToJournalConverter(str(input_path))
        
        # Exibe Crítica e Sugestões
        click.echo("\n🔍 Analisando formato do documento...")
        critiques = converter.critique(
            split_by_heading=not no_split,
            heading_level=heading_level
        )
        
        if critiques:
            for c in critiques:
                color = 'cyan' if c.level == 'INFO' else 'yellow' if c.level == 'WARNING' else 'red'
                click.secho(f"   [{c.level}] {c.message}", fg=color)
                if c.suggestion:
                    click.echo(f"       💡 Sugestão: {c.suggestion}")
            click.echo("")
        else:
            click.secho("   ✅ Formato excelente! Nenhuma observação encontrada.", fg='green')
        
        # Confirmação do usuário
        if not click.confirm(" deseja continuar com a criação do arquivo?", default=True):
            click.echo("🚫 Conversão cancelada pelo usuário.")
            return

        journal = converter.convert(
            abbreviation=abbreviation,
            description=title,
            language=language,
            split_by_heading=not no_split,
            heading_level=heading_level,
            read_only=read_only
        )
        
        output_path = journal.save(str(output_file))
        
        click.echo(f"\n✅ Journal criado: {output_path}")
        click.echo(f"   📝 Entradas: {journal.get_entry_count()}")
        click.echo(f"   🏷️  Abreviação: {journal.details.abbreviation}")
        click.echo(f"   📋 Descrição: {journal.details.description}")
        
    except FileNotFoundError as e:
        click.echo(f"❌ Arquivo não encontrado: {e}", err=True)
        raise SystemExit(1)
    except Exception as e:
        click.echo(f"❌ Erro na conversão: {e}", err=True)
        raise SystemExit(1)


@cli.command('info')
@click.argument('journal_file', type=click.Path(exists=True))
def journal_info(journal_file):
    """
    Exibe informações sobre um arquivo Journal (.jou).
    
    Exemplo:
        mysword-tools info meu_journal.jou
    """
    from .mysword_journal import MySwordJournal
    
    try:
        journal = MySwordJournal.load(journal_file)
        
        click.echo(f"\n📓 Informações do Journal: {Path(journal_file).name}")
        click.echo("=" * 50)
        click.echo(f"   Abreviação:  {journal.details.abbreviation}")
        click.echo(f"   Descrição:   {journal.details.description}")
        click.echo(f"   Idioma:      {journal.details.language}")
        click.echo(f"   Data:        {journal.details.version_date}")
        click.echo(f"   Somente leitura: {'Sim' if journal.details.read_only else 'Não'}")
        click.echo(f"   Entradas:    {len(journal.entries)}")
        
        if journal.entries:
            click.echo("\n📑 Tópicos:")
            for i, entry in enumerate(journal.entries[:10], 1):
                topic = entry.topic[:50] + "..." if len(entry.topic) > 50 else entry.topic
                click.echo(f"   {i:3}. {topic}")
            
            if len(journal.entries) > 10:
                click.echo(f"   ... e mais {len(journal.entries) - 10} entradas")
        
    except Exception as e:
        click.echo(f"❌ Erro ao ler Journal: {e}", err=True)
        raise SystemExit(1)


@cli.command('list-entries')
@click.argument('journal_file', type=click.Path(exists=True))
@click.option('--full', '-f', is_flag=True, help='Mostrar conteúdo completo')
def list_entries(journal_file, full):
    """
    Lista todas as entradas de um Journal.
    """
    from .mysword_journal import MySwordJournal
    
    try:
        journal = MySwordJournal.load(journal_file)
        
        for i, entry in enumerate(journal.entries, 1):
            click.echo(f"\n{'='*60}")
            click.echo(f"[{i}] {entry.topic}")
            click.echo('='*60)
            
            if full:
                click.echo(entry.content)
            else:
                # Mostra preview do conteúdo
                preview = entry.content[:200]
                # Remove tags HTML para preview
                import re
                preview = re.sub(r'<[^>]+>', '', preview)
                if len(entry.content) > 200:
                    preview += "..."
                click.echo(preview)
        
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)
        raise SystemExit(1)


def main():
    """Ponto de entrada principal."""
    cli()


if __name__ == "__main__":
    main()
