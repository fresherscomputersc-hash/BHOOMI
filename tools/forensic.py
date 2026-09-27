import sqlite3
c = sqlite3.connect("data/bhusure.db")
for doc_id, wants in (
    ("DOC-5F11B732FA", ("previous_owner", "new_owner", "mutation_no", "owner_name")),
    ("DOC-D31D0C5D90", ("khata_no", "plot_no", "village")),
    ("DOC-F935EE7D6B", ("previous_owner", "new_owner", "registration_no")),
):
    doc = c.execute("select id from source_documents where doc_id=?", (doc_id,)).fetchone()
    rec = c.execute("select id from land_records where document_id=?", (doc[0],)).fetchone()
    print("=" * 30, doc_id)
    for r in c.execute("select field_name, value, normalized_value, confidence, source, evidence_text from extraction_results where record_id=?", (rec[0],)):
        if r[0] in wants:
            print(f"  {r[0]}: val={r[1][:40]!r} norm={r[2][:40]!r} conf={r[3]} src={r[4]}")
            print(f"    ev={r[5][:100]!r}")
