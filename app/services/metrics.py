"""
MIS / monitoring metrics (SRS FR-13).

Every number on the MIS dashboard comes from a live query here - nothing is
hard-coded, so the demo can be re-run with fresh data and the figures move.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import (
    AuditLog,
    CorrectionDataset,
    Discrepancy,
    DocumentStatus,
    ExtractionResult,
    LandRecord,
    RecordStatus,
    Severity,
    SourceDocument,
)
from app.services import validation


def _pct(part: float, whole: float) -> float:
    return round(part / whole * 100, 1) if whole else 0.0


def dashboard(db: Session) -> dict:
    docs_total = db.execute(select(func.count(SourceDocument.id))).scalar() or 0
    docs_by_status = dict(
        db.execute(
            select(SourceDocument.status, func.count(SourceDocument.id)).group_by(SourceDocument.status)
        ).all()
    )
    docs_by_status = {
        (key.value if hasattr(key, "value") else str(key)): value
        for key, value in docs_by_status.items()
    }

    records_total = db.execute(select(func.count(LandRecord.id))).scalar() or 0
    records_by_status = dict(
        db.execute(
            select(LandRecord.status, func.count(LandRecord.id)).group_by(LandRecord.status)
        ).all()
    )
    records_by_status = {
        (key.value if hasattr(key, "value") else str(key)): value
        for key, value in records_by_status.items()
    }

    pending = records_by_status.get(RecordStatus.PENDING_REVIEW.value, 0)
    approved = records_by_status.get(RecordStatus.APPROVED.value, 0)
    rejected = records_by_status.get(RecordStatus.REJECTED.value, 0)
    escalated = records_by_status.get(RecordStatus.ESCALATED.value, 0)
    processed = docs_by_status.get(DocumentStatus.COMPLETED.value, 0) + docs_by_status.get(
        DocumentStatus.NEEDS_REVIEW.value, 0
    )

    # Extraction quality
    avg_confidence = db.execute(
        select(func.avg(LandRecord.record_confidence)).where(LandRecord.record_confidence > 0)
    ).scalar() or 0.0
    low_confidence_records = db.execute(
        select(func.count(LandRecord.id)).where(LandRecord.record_confidence < 70)
    ).scalar() or 0
    gis_linked = db.execute(
        select(func.count(LandRecord.id)).where(LandRecord.gis_linked.is_(True))
    ).scalar() or 0

    # Latency (SRS 7.1)
    avg_latency = db.execute(
        select(func.avg(SourceDocument.total_latency_ms)).where(SourceDocument.total_latency_ms > 0)
    ).scalar() or 0.0
    max_latency = db.execute(
        select(func.max(SourceDocument.total_latency_ms))
    ).scalar() or 0
    avg_ocr_latency = db.execute(
        select(func.avg(SourceDocument.ocr_latency_ms)).where(SourceDocument.ocr_latency_ms > 0)
    ).scalar() or 0.0

    # Discrepancies
    discrepancies_total = db.execute(select(func.count(Discrepancy.id))).scalar() or 0
    open_discrepancies = db.execute(
        select(func.count(Discrepancy.id)).where(Discrepancy.status == "open")
    ).scalar() or 0
    by_severity = dict(
        db.execute(
            select(Discrepancy.severity, func.count(Discrepancy.id)).group_by(Discrepancy.severity)
        ).all()
    )
    by_severity = {(k.value if hasattr(k, "value") else str(k)): v for k, v in by_severity.items()}
    rule_wise = validation.discrepancy_summary(db)

    # Corrections (continuous learning, FR-16)
    corrections = db.execute(select(func.count(CorrectionDataset.id))).scalar() or 0
    corrected_fields = (
        db.execute(select(func.count(CorrectionDataset.field_name))
                   .group_by(CorrectionDataset.field_name)).all()
    )
    fields_corrected = len(corrected_fields)
    top_corrected = db.execute(
        select(CorrectionDataset.field_name, func.count(CorrectionDataset.id))
        .group_by(CorrectionDataset.field_name)
        .order_by(func.count(CorrectionDataset.id).desc())
        .limit(5)
    ).all()

    # Measured accuracy: reviewer corrections against extracted fields.
    # Estimated (confidence) is a forecast; this is the observed score.
    extracted_total = db.execute(
        select(func.count(ExtractionResult.id))
        .where(ExtractionResult.normalized_value != "")
    ).scalar() or 0
    measured_accuracy = (
        round(100.0 * (1.0 - corrections / extracted_total), 1)
        if extracted_total else None
    )
    band_rows = dict(
        db.execute(
            select(
                case(
                    (ExtractionResult.confidence >= 90.0, "high"),
                    (ExtractionResult.confidence >= 70.0, "medium"),
                    else_="low",
                ),
                func.count(ExtractionResult.id),
            )
            .where(ExtractionResult.normalized_value != "")
            .group_by(
                case(
                    (ExtractionResult.confidence >= 90.0, "high"),
                    (ExtractionResult.confidence >= 70.0, "medium"),
                    else_="low",
                )
            )
        ).all()
    )
    error_fields = db.execute(
        select(ExtractionResult.field_name, func.count(ExtractionResult.id))
        .where(ExtractionResult.is_low_confidence.is_(True))
        .group_by(ExtractionResult.field_name)
        .order_by(func.count(ExtractionResult.id).desc())
        .limit(8)
    ).all()
    resolved = db.execute(
        select(func.count(Discrepancy.id)).where(Discrepancy.status != "open")
    ).scalar() or 0

    audit_events = db.execute(select(func.count(AuditLog.id))).scalar() or 0

    # District-wise rollup (prototype = single district)
    district_rows = db.execute(
        select(LandRecord.district, func.count(LandRecord.id))
        .group_by(LandRecord.district)
        .order_by(func.count(LandRecord.id).desc())
    ).all()
    tehsil_rows = db.execute(
        select(LandRecord.tehsil, func.count(LandRecord.id))
        .group_by(LandRecord.tehsil)
        .order_by(func.count(LandRecord.id).desc())
    ).all()
    state_rows = db.execute(
        select(LandRecord.state, func.count(LandRecord.id))
        .group_by(LandRecord.state)
        .order_by(func.count(LandRecord.id).desc())
    ).all()
    district_verified = db.execute(
        select(
            LandRecord.district,
            func.count(LandRecord.id),
            func.sum(case((LandRecord.status == RecordStatus.APPROVED, 1), else_=0)),
        )
        .group_by(LandRecord.district)
        .order_by(func.count(LandRecord.id).desc())
    ).all()

    # Reviewer workload
    workload = db.execute(
        select(LandRecord.assigned_to_id, func.count(LandRecord.id))
        .where(LandRecord.status == RecordStatus.PENDING_REVIEW)
        .group_by(LandRecord.assigned_to_id)
    ).all()

    # Throughput over the last 7 days
    since = datetime.now(timezone.utc) - timedelta(days=7)
    daily = db.execute(
        select(func.date(SourceDocument.created_at), func.count(SourceDocument.id))
        .where(SourceDocument.created_at >= since)
        .group_by(func.date(SourceDocument.created_at))
        .order_by(func.date(SourceDocument.created_at))
    ).all()

    high_severity = (
        by_severity.get(Severity.HIGH.value, 0) + by_severity.get(Severity.CRITICAL.value, 0)
    )

    return {
        "documents": {
            "uploaded": docs_total,
            "processed": processed,
            "failed": docs_by_status.get(DocumentStatus.FAILED.value, 0),
            "by_status": docs_by_status,
        },
        "records": {
            "total": records_total,
            "pending_review": pending,
            "approved": approved,
            "rejected": rejected,
            "escalated": escalated,
            "flagged": db.execute(
                select(func.count(LandRecord.id)).where(LandRecord.discrepancy_count > 0)
            ).scalar() or 0,
            "by_status": records_by_status,
        },
        "extraction": {
            "average_record_confidence": round(float(avg_confidence), 2),
            "low_confidence_records": low_confidence_records,
            "estimated_accuracy_pct": round(float(avg_confidence), 1),
            "measured_accuracy_pct": measured_accuracy,
            "extracted_fields": extracted_total,
            "confidence_bands": {
                "high": band_rows.get("high", 0),
                "medium": band_rows.get("medium", 0),
                "low": band_rows.get("low", 0),
            },
            "top_corrected_fields": [
                {"field": f, "corrections": c} for f, c in top_corrected
            ],
            "gis_linked_records": gis_linked,
            "gis_link_rate_pct": _pct(gis_linked, records_total),
        },
        "performance": {
            "average_pipeline_latency_ms": round(float(avg_latency), 1),
            "slowest_document_ms": int(max_latency or 0),
            "average_ocr_latency_ms": round(float(avg_ocr_latency), 1),
            "budget_ms": 10_000,
            "within_budget": (avg_latency or 0) <= 10_000,
        },
        "validation": {
            "discrepancies_total": discrepancies_total,
            "discrepancies_open": open_discrepancies,
            "discrepancies_resolved": resolved,
            "high_and_critical": high_severity,
            "by_severity": by_severity,
            "rule_wise": rule_wise,
            "top_error_fields": [
                {"field": f, "low_confidence": c} for f, c in error_fields
            ],
        },
        "learning": {
            "corrections_captured": corrections,
            "distinct_fields_corrected": fields_corrected,
        },
        "audit": {"events": audit_events},
        "progress": {
            "digitisation_pct": _pct(processed, docs_total),
            "review_completion_pct": _pct(approved + rejected, records_total),
            "by_district": [{"district": d or "(unmapped)", "records": c} for d, c in district_rows],
            "by_tehsil": [{"tehsil": t or "(unmapped)", "records": c} for t, c in tehsil_rows],
            "by_state": [{"state": s or "(unmapped)", "records": c} for s, c in state_rows],
            "district_verified": [
                {"district": d or "(unmapped)", "records": c,
                 "verified_pct": _pct(v or 0, c)}
                for d, c, v in district_verified
            ],
            "reviewer_workload": [
                {"user_id": uid, "pending": count} for uid, count in workload
            ],
            "last_7_days": [{"date": str(d), "documents": c} for d, c in daily],
        },
    }


def _as_aware(value: datetime) -> datetime:
    """SQLite strips tzinfo on read; treat naive timestamps as UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def pending_review_alerts(db: Session, threshold_hours: int = 48) -> list[dict]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=threshold_hours)
    rows = db.execute(
        select(LandRecord)
        .where(LandRecord.status == RecordStatus.PENDING_REVIEW)
        .where(LandRecord.created_at <= cutoff)
    ).scalars().all()
    return [
        {
            "record_id": row.record_id,
            "village": row.village,
            "khasra_no": row.khasra_no,
            "hours_pending": round(
                (now - _as_aware(row.created_at)).total_seconds() / 3600, 1
            ),
        }
        for row in rows
    ]
