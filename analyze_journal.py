"""
Analisa a estrutura de um arquivo Journal MySword existente
"""
import sqlite3
import sys

def analyze_journal(filepath):
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    
    # Lista todas as tabelas
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print("=" * 60)
    print("TABELAS NO BANCO DE DADOS")
    print("=" * 60)
    for t in tables:
        print(f"  - {t[0]}")
    
    print()
    
    # Para cada tabela, mostra estrutura
    for table in tables:
        table_name = table[0]
        print("=" * 60)
        print(f"ESTRUTURA DA TABELA: {table_name}")
        print("=" * 60)
        cur.execute(f"PRAGMA table_info({table_name})")
        for col in cur.fetchall():
            cid, name, dtype, notnull, default, pk = col
            print(f"  {cid:2}. {name:25} {dtype:10} notnull={notnull} default={default} pk={pk}")
        print()
    
    # Mostra conteúdo da tabela details
    print("=" * 60)
    print("CONTEÚDO DA TABELA: details")
    print("=" * 60)
    try:
        cur.execute("SELECT * FROM details")
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            for col, val in zip(columns, row):
                if val:
                    val_str = str(val)[:100]
                    if len(str(val)) > 100:
                        val_str += "..."
                else:
                    val_str = "(vazio/NULL)"
                print(f"  {col:25}: {val_str}")
    except Exception as e:
        print(f"  Erro ao ler details: {e}")
    
    print()
    
    # Conta e mostra algumas entradas do journal
    print("=" * 60)
    print("ENTRADAS DA TABELA: journal")
    print("=" * 60)
    try:
        cur.execute("SELECT COUNT(*) FROM journal")
        count = cur.fetchone()[0]
        print(f"  Total de entradas: {count}")
        print()
        
        cur.execute("SELECT title, LENGTH(content) FROM journal LIMIT 15")
        print("  Primeiros tópicos:")
        for i, (topic, content_len) in enumerate(cur.fetchall(), 1):
            topic_str = topic[:55] + "..." if len(topic) > 55 else topic
            print(f"    {i:2}. {topic_str:60} ({content_len} chars)")
        
        if count > 15:
            print(f"    ... e mais {count - 15} entradas")
    except Exception as e:
        print(f"  Erro ao ler journal: {e}")
    
    conn.close()
    print()
    print("=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "2026-ebd-umaigrejacomproposito.jor.mybible"
    
    print(f"\nAnalisando: {filepath}\n")
    analyze_journal(filepath)
