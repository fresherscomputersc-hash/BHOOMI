import sqlite3
c = sqlite3.connect("data/bhuverify.db")
print("docs", c.execute("select count(*) from source_documents").fetchone())
print("records", c.execute("select count(*) from land_records").fetchone())
for row in c.execute("select actor_label, count(*) from audit_logs group by 1 order by 2 desc"):
    print(row)
print("verifier-hits", c.execute(
    "select count(*) from audit_logs where actor_label in "
    "('spacy-ner-verifier','hf-transformer-verifier','groq-llm-verifier')").fetchone())
print("spacy-src", c.execute(
    "select count(*) from extraction_results where source='spacy-ner'").fetchone())
print("hf-src", c.execute(
    "select count(*) from extraction_results where source='hf-transformer'").fetchone())
