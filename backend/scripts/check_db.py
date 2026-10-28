import sqlite3

conn = sqlite3.connect('law_ai_demo.db')
cursor = conn.execute('SELECT name FROM sqlite_master WHERE type="table";')
tables = [row[0] for row in cursor.fetchall()]
print('Tables:', tables)

if 'documents' in tables:
    cursor = conn.execute('SELECT sql FROM sqlite_master WHERE name="documents";')
    schema = cursor.fetchone()
    if schema:
        print('Documents table schema:')
        print(schema[0])
    
    cursor = conn.execute('SELECT COUNT(*) FROM documents;')
    count = cursor.fetchone()[0]
    print(f'Documents count: {count}')

conn.close()