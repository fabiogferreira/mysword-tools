"""
MySword Journal - Classes para manipular arquivos Journal (.jor.mybible) do MySword

O formato .jor.mybible é um banco de dados SQLite com as seguintes tabelas principais:
- details: Metadados do Journal (1 registro)
- journal: Entradas do diário (title + content + date + tags)
- journalFTS: Índice de busca full-text
- data: Dados/anexos binários
- deleteLog: Log de exclusões
"""

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import html


@dataclass
class JournalEntry:
    """Representa uma entrada do Journal"""
    title: str  # Título da entrada (era 'topic')
    content: str  # Conteúdo em HTML
    id: str = ""  # ID único da entrada
    date: str = ""  # Data de criação (YYYY-MM-DD HH:MM:SS)
    tags: str = ""  # Tags separadas por vírgula
    dateupdated: str = ""  # Data de atualização
    
    def __post_init__(self):
        # Garante que title não tenha quebras de linha
        self.title = self.title.replace('\n', ' ').replace('\r', '').strip()
        # Gera ID se não fornecido
        if not self.id:
            # Cria ID a partir do título (slug)
            self.id = self.title.replace(' ', '_')[:30]
        # Define data se não fornecida
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.dateupdated:
            self.dateupdated = self.date


@dataclass
class JournalDetails:
    """Metadados do Journal - Estrutura compatível com MySword"""
    name: str = ""  # Nome interno do módulo
    title: str = ""  # Título exibido
    abbreviation: str = ""
    author: str = ""
    description: str = ""
    comments: str = ""
    version: str = ""
    versiondate: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d 00:00:00"))
    publishdate: str = ""
    readonly: bool = False
    customcss: str = ""
    
    def __post_init__(self):
        # Abbreviation não pode ter espaços
        self.abbreviation = self.abbreviation.replace(' ', '_').strip()
        # Se name não foi definido, usa abbreviation
        if not self.name:
            self.name = self.abbreviation
        # Se title não foi definido, usa description
        if not self.title:
            self.title = self.description or self.abbreviation


class MySwordJournal:
    """
    Classe para criar e manipular arquivos Journal do MySword.
    
    Uso:
        journal = MySwordJournal(
            abbreviation="MEU_DIARIO",
            title="Meu Diário de Estudos",
            description="Diário de estudos bíblicos pessoais"
        )
        journal.add_entry("Estudo 1", "<p>Conteúdo do estudo...</p>")
        journal.add_entry("Estudo 2", "<p>Outro conteúdo...</p>")
        journal.save("meu_diario.jor.mybible")
    """
    
    # Extensão correta para Journal do MySword
    FILE_EXTENSION = ".jor.mybible"
    
    def __init__(
        self,
        abbreviation: str,
        title: str = "",
        description: str = "",
        author: str = "",
        name: str = "",
        comments: str = "",
        version: str = "",
        readonly: bool = False,
        customcss: str = ""
    ):
        """
        Inicializa um novo Journal.
        
        Args:
            abbreviation: Abreviação curta (sem espaços)
            title: Título do Journal exibido no MySword
            description: Descrição do Journal (suporta HTML)
            author: Autor do Journal
            name: Nome interno do módulo (padrão: abbreviation)
            comments: Comentários adicionais
            version: Versão do módulo
            readonly: Se True, Journal será somente leitura no MySword
            customcss: CSS personalizado para estilização
        """
        self.details = JournalDetails(
            name=name or abbreviation,
            title=title or description or abbreviation,
            abbreviation=abbreviation,
            author=author,
            description=description,
            comments=comments,
            version=version,
            readonly=readonly,
            customcss=customcss
        )
        self.entries: List[JournalEntry] = []
    
    def add_entry(self, title: str, content: str, id: str = "", 
                  tags: str = "", date: str = "") -> None:
        """
        Adiciona uma entrada ao Journal.
        
        Args:
            title: Título da entrada
            content: Conteúdo HTML da entrada
            id: ID único (opcional, será gerado automaticamente)
            tags: Tags separadas por vírgula
            date: Data no formato YYYY-MM-DD HH:MM:SS
        """
        entry = JournalEntry(
            title=title, 
            content=content, 
            id=id,
            tags=tags,
            date=date
        )
        self.entries.append(entry)
    
    def add_entries(self, entries: List[tuple]) -> None:
        """
        Adiciona múltiplas entradas ao Journal.
        
        Args:
            entries: Lista de tuplas (title, content) ou (title, content, tags)
        """
        for item in entries:
            if len(item) >= 3:
                self.add_entry(item[0], item[1], tags=item[2])
            else:
                self.add_entry(item[0], item[1])
    
    def clear_entries(self) -> None:
        """Remove todas as entradas do Journal."""
        self.entries.clear()
    
    def get_entry_count(self) -> int:
        """Retorna o número de entradas no Journal."""
        return len(self.entries)
    
    def _create_database(self, filepath: Path) -> None:
        """
        Cria o banco de dados SQLite com a estrutura do Journal.
        
        Args:
            filepath: Caminho do arquivo .jor.mybible
        """
        # Remove arquivo existente
        if filepath.exists():
            filepath.unlink()
        
        conn = sqlite3.connect(str(filepath))
        cursor = conn.cursor()
        
        try:
            # Cria tabela details (exatamente como no MySword)
            cursor.execute(
                "CREATE TABLE details(name TEXT, title TEXT, abbreviation TEXT, "
                "author TEXT, description TEXT, comments TEXT, version TEXT, "
                "versiondate DATETIME, publishdate TEXT, readonly BOOL, customcss TEXT)"
            )
            
            # Insere metadados
            cursor.execute(
                "INSERT INTO details (name, title, abbreviation, author, description, "
                "comments, version, versiondate, publishdate, readonly, customcss) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.details.name,
                    self.details.title,
                    self.details.abbreviation,
                    self.details.author,
                    self.details.description,
                    self.details.comments,
                    self.details.version,
                    self.details.versiondate,
                    self.details.publishdate,
                    1 if self.details.readonly else None,
                    self.details.customcss or None
                )
            )
            
            # Cria tabela journal (exatamente como no MySword - com COLLATE NOCASE)
            cursor.execute(
                "CREATE TABLE journal(rowid INTEGER primary key autoincrement, "
                "id TEXT collate nocase, title TEXT collate nocase, date DATETIME, "
                "tags TEXT, content TEXT, dateupdated DATETIME)"
            )
            
            # Cria índice FTS com tokenizer porter (exatamente como no MySword)
            cursor.execute(
                "CREATE VIRTUAL TABLE journalFTS USING FTS3(title, content, tags, tokenize=porter)"
            )
            
            # Cria tabela data para anexos (exatamente como no MySword)
            cursor.execute(
                "CREATE TABLE data(rowid INTEGER primary key autoincrement, "
                "id TEXT collate nocase, description TEXT collate nocase, "
                "date DATETIME, filename TEXT, content BLOB, thumbnail BLOB)"
            )
            
            # Cria tabela deleteLog (exatamente como no MySword)
            cursor.execute(
                "CREATE TABLE deleteLog(id TEXT collate nocase primary key, date DATETIME)"
            )
            
            # Insere todas as entradas
            for entry in self.entries:
                cursor.execute("""
                    INSERT INTO journal (id, title, date, tags, content, dateupdated)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    entry.id,
                    entry.title,
                    entry.date,
                    entry.tags,
                    entry.content,
                    entry.dateupdated
                ))
                
                # Insere também na tabela FTS
                cursor.execute("""
                    INSERT INTO journalFTS (title, content, tags)
                    VALUES (?, ?, ?)
                """, (entry.title, entry.content, entry.tags))
            
            conn.commit()
            
        finally:
            conn.close()
    
    def save(self, filepath: str) -> Path:
        """
        Salva o Journal como arquivo .jor.mybible (SQLite).
        
        Args:
            filepath: Caminho do arquivo de saída
            
        Returns:
            Path do arquivo criado
        """
        # Sempre usa minúsculas para o nome do arquivo de saída
        path = Path(str(filepath).lower())
        
        # Garante que termina com a extensão correta .jor.mybible
        filepath_str = str(path)
        if not filepath_str.lower().endswith('.jor.mybible'):
            # Remove extensões existentes e adiciona a correta
            if filepath_str.lower().endswith('.jor'):
                path = Path(filepath_str + '.mybible')
            elif filepath_str.lower().endswith('.jou'):
                path = Path(filepath_str[:-4] + '.jor.mybible')
            else:
                path = Path(filepath_str + self.FILE_EXTENSION)
        
        # Cria diretório se necessário
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Cria o banco de dados
        self._create_database(path)
        
        return path
    
    @classmethod
    def load(cls, filepath: str) -> "MySwordJournal":
        """
        Carrega um Journal existente de um arquivo .jor.mybible.
        
        Args:
            filepath: Caminho do arquivo .jor.mybible
            
        Returns:
            Instância de MySwordJournal
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        conn = sqlite3.connect(str(path))
        cursor = conn.cursor()
        
        try:
            # Carrega metadados
            cursor.execute("SELECT * FROM details LIMIT 1")
            row = cursor.fetchone()
            
            if not row:
                raise ValueError("Arquivo Journal inválido: tabela details vazia")
            
            # Obtém nomes das colunas
            columns = [desc[0].lower() for desc in cursor.description]
            details_dict = dict(zip(columns, row))
            
            # Cria instância
            journal = cls(
                abbreviation=details_dict.get('abbreviation', 'JOURNAL'),
                name=details_dict.get('name', ''),
                title=details_dict.get('title', ''),
                author=details_dict.get('author', ''),
                description=details_dict.get('description', ''),
                comments=details_dict.get('comments', ''),
                version=details_dict.get('version', ''),
                readonly=bool(details_dict.get('readonly')),
                customcss=details_dict.get('customcss', '')
            )
            
            # Carrega entradas (usa 'title' em vez de 'topic')
            cursor.execute("""
                SELECT id, title, date, tags, content, dateupdated 
                FROM journal
            """)
            for row in cursor.fetchall():
                id_, title, date, tags, content, dateupdated = row
                entry = JournalEntry(
                    id=id_ or "",
                    title=title or "",
                    date=date or "",
                    tags=tags or "",
                    content=content or "",
                    dateupdated=dateupdated or ""
                )
                journal.entries.append(entry)
            
            return journal
            
        finally:
            conn.close()
    
    def __repr__(self) -> str:
        return (
            f"MySwordJournal("
            f"abbreviation='{self.details.abbreviation}', "
            f"entries={len(self.entries)})"
        )


# Funções auxiliares para formatação de conteúdo

def create_bible_link(reference: str, display_text: Optional[str] = None) -> str:
    """
    Cria um link para referência bíblica no formato MySword.
    
    Args:
        reference: Referência bíblica (ex: "João 3:16" ou "Joh 3:16")
        display_text: Texto a exibir (padrão: reference)
        
    Returns:
        Tag HTML com link para o versículo
    """
    display = display_text or reference
    # Escapa caracteres HTML no display
    display = html.escape(display)
    return f"<a href='b{reference}'>{display}</a>"


def create_strong_link(strong_number: str, display_text: Optional[str] = None) -> str:
    """
    Cria um link para número Strong no formato MySword.
    
    Args:
        strong_number: Número Strong (ex: "G2424" ou "H430")
        display_text: Texto a exibir (padrão: strong_number)
        
    Returns:
        Tag HTML com link para Strong
    """
    display = display_text or strong_number
    display = html.escape(display)
    return f"<a href='s{strong_number}'>{display}</a>"


def create_journal_link(title: str, display_text: Optional[str] = None, 
                        journal_abbr: Optional[str] = None) -> str:
    """
    Cria um link para outra entrada do Journal.
    
    Args:
        title: Título da entrada de destino
        display_text: Texto a exibir (padrão: title)
        journal_abbr: Abreviação do Journal (se diferente do atual)
        
    Returns:
        Tag HTML com link para entrada
    """
    display = display_text or title
    display = html.escape(display)
    
    if journal_abbr:
        return f"<a href='j-{journal_abbr} {title}'>{display}</a>"
    return f"<a href='j-{title}'>{display}</a>"


def wrap_paragraph(text: str, direction: str = "ltr") -> str:
    """
    Envolve texto em tag de parágrafo.
    
    Args:
        text: Texto do parágrafo
        direction: Direção do texto ('ltr' ou 'rtl')
    """
    return f'<p dir="{direction}">{text}</p>'


def format_heading(text: str, level: int = 2) -> str:
    """
    Formata texto como cabeçalho HTML.
    
    Args:
        text: Texto do cabeçalho
        level: Nível do cabeçalho (1-6)
        
    Returns:
        Tag HTML de cabeçalho
    """
    level = max(1, min(6, level))  # Clamp entre 1 e 6
    return f"<h{level}>{html.escape(text)}</h{level}>"
