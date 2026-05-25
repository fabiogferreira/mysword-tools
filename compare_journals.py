"""
Compara estrutura de dois arquivos Journal MySword
"""
import sqlite3
import sys

def compare_journals(filepath1, filepath2):
    print("=" * 70)
    print(f"COMPARANDO:")
    print(f"  1. {filepath1}")
    print(f"  2. {filepath2}")
    print("=" * 70)
    print()
    
    conn1 = sqlite3.connect(filepath1)
    conn2 = sqlite3.connect(filepath2)
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    
    # Compara SQL de criação das tabelas
    print("=== SQL DE CRIAÇÃO DAS TABELAS ===")
    print()
    
    cur1.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
    tables1 = dict(cur1.fetchall())
    
    cur2.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
    tables2 = dict(cur2.fetchall())
    
    all_tables = set(tables1.keys()) | set(tables2.keys())
    
    for table in sorted(all_tables):
        sql1 = tables1.get(table, "(não existe)")
        sql2 = tables2.get(table, "(não existe)")
        
        if sql1 == sql2:
            print(f"[OK] {table}: IDÊNTICO")
        else:
            print(f"[DIFF] {table}:")
            print(f"  REFERÊNCIA:")
            print(f"    {sql1}")
            print(f"  GERADO:")
            print(f"    {sql2}")
        print()
    
    # Compara conteúdo da tabela details
    print("=== COMPARANDO TABELA DETAILS ===")
    print()
    
    cur1.execute("SELECT * FROM details LIMIT 1")
    row1 = cur1.fetchone()
    cols1 = [desc[0] for desc in cur1.description]
    
    cur2.execute("SELECT * FROM details LIMIT 1")
    row2 = cur2.fetchone()
    cols2 = [desc[0] for desc in cur2.description]
    
    print("Colunas REFERÊNCIA:", cols1)
    print("Colunas GERADO:", cols2)
    print()
    
    if cols1 != cols2:
        print("[DIFF] AS COLUNAS SÃO DIFERENTES!")
        print(f"  Faltando no gerado: {set(cols1) - set(cols2)}")
        print(f"  Extra no gerado: {set(cols2) - set(cols1)}")
    else:
        print("[OK] Colunas são idênticas")
    
    conn1.close()
    conn2.close()


if __name__ == "__main__":
    file1 = "2026-ebd-umaigrejacomproposito.jor.mybible"
    file2 = "output/sermao_v2.jor.mybible"
    
    if len(sys.argv) > 2:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    
    compare_journals(file1, file2)
