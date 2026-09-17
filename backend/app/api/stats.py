from fastapi import APIRouter
from sqlmodel import func, select

from app.db.database import get_session
from app.db.models import RequestLog
from app.models.schemas import StatsSummary, TierCounts

router = APIRouter()


@router.get("/stats/summary", response_model=StatsSummary)
async def stats_summary() -> StatsSummary:
    with get_session() as session:
        total_requests = session.exec(select(func.count()).select_from(RequestLog)).one()
        total_cost_actual = session.exec(select(func.coalesce(func.sum(RequestLog.cost_actual), 0.0))).one()
        total_cost_baseline = session.exec(select(func.coalesce(func.sum(RequestLog.cost_baseline), 0.0))).one()
        total_saved = session.exec(select(func.coalesce(func.sum(RequestLog.cost_saved), 0.0))).one()

        tier_rows = session.exec(
            select(RequestLog.complexity_tier, func.count()).group_by(RequestLog.complexity_tier)
        ).all()

    by_tier = TierCounts(**{tier: count for tier, count in tier_rows if tier in TierCounts.model_fields})

    return StatsSummary(
        total_requests=total_requests,
        total_cost_actual=total_cost_actual,
        total_cost_baseline=total_cost_baseline,
        total_saved=total_saved,
        by_tier=by_tier,
    )
