"""Metrics timezone regression: naive SQLite timestamps must not crash alerts."""
import uuid
from datetime import datetime, timedelta, timezone

from app.models import DocumentStatus, LandRecord, RecordStatus, SourceDocument
from app.models import Discrepancy as DiscrepancyRow
from app.services.metrics import dashboard, pending_review_alerts


def _mk_record(db, **kw):
    doc = SourceDocument(
        doc_id=f"DOC-T-{uuid.uuid4().hex[:8].upper()}",
        original_filename="t.png", stored_path="/tmp/t.png",
        file_hash=uuid.uuid4().hex, status=DocumentStatus.QUEUED,
    )
    db.add(doc)
    db.flush()
    kw.setdefault("status", RecordStatus.PENDING_REVIEW)
    rec = LandRecord(document_id=doc.id, **kw)
    db.add(rec)
    db.commit()
    return rec


def test_pending_alerts_handles_naive_timestamps(db):
    old = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=50)
    _mk_record(db, record_id="LR-OLD-P", khasra_no="1/1", village="V", created_at=old)
    out = pending_review_alerts(db, 48)
    assert any(r["record_id"] == "LR-OLD-P" for r in out)
    assert out[0]["hours_pending"] >= 48


def test_dashboard_runs_on_empty_db(db):
    data = dashboard(db)
    assert data["documents"]["uploaded"] == 0
    assert data["records"]["total"] == 0
    assert data["performance"]["within_budget"] is True
    assert data["extraction"]["measured_accuracy_pct"] is None
    assert data["extraction"]["confidence_bands"] == {"high": 0, "medium": 0, "low": 0}
    assert data["progress"]["by_state"] == []


def test_dashboard_measured_accuracy_and_geo(db):
    from app.models import CorrectionDataset, ExtractionResult
    rec = _mk_record(db, record_id="LR-M", district="Khordha", state="Odisha",
                     status=RecordStatus.APPROVED)
    for name, conf, low in (("owner_name", 95.0, False), ("village", 60.0, True),
                           ("area", 80.0, False)):
        db.add(ExtractionResult(record_id=rec.id, field_name=name,
                                field_label=name, value="x", normalized_value="x",
                                confidence=conf, is_low_confidence=low))
    db.add(CorrectionDataset(record_id=rec.id, field_name="village",
                             ai_value="a", corrected_value="b"))
    db.commit()
    data = dashboard(db)
    assert data["extraction"]["confidence_bands"] == {"high": 1, "medium": 1, "low": 1}
    assert data["extraction"]["measured_accuracy_pct"] == round(100 * (1 - 1 / 3), 1)
    assert data["extraction"]["top_corrected_fields"] == [
        {"field": "village", "corrections": 1}]
    assert data["validation"]["top_error_fields"] == [
        {"field": "village", "low_confidence": 1}]
    states = {r["state"]: r["records"] for r in data["progress"]["by_state"]}
    assert states.get("Odisha") == 1
    dv = {r["district"]: r for r in data["progress"]["district_verified"]}
    assert dv["Khordha"]["verified_pct"] == 100.0
