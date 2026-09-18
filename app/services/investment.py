from app.core.utils import get_utc_now
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def close_if_fully_invested(obj: CharityProject | Donation) -> None:
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = get_utc_now()


def invest(
    target: CharityProject | Donation, sources: list[CharityProject | Donation]
) -> list[CharityProject | Donation]:
    changed = []

    for source in sources:
        source_remaining = source.full_amount - source.invested_amount
        target_remaining = target.full_amount - target.invested_amount

        if source_remaining <= 0:
            continue
        if target_remaining <= 0:
            break

        to_invest = min(source_remaining, target_remaining)

        source.invested_amount += to_invest
        target.invested_amount += to_invest

        close_if_fully_invested(source)
        close_if_fully_invested(target)

        changed.append(source)

        if target.fully_invested:
            break

    return changed
