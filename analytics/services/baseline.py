from __future__ import annotations

from typing import Dict, Iterable, List

from . import time_windows


def build_kpi_cards(
    window_keys: Iterable[str] = ("28d", "91d", "365d"),
    queryset=None,
) -> List[Dict]:
    """Shape KPI-style cards for templates."""
    summary = time_windows.compute_window_counts(queryset=queryset)
    cards: List[Dict] = []
    for key in window_keys:
        if key not in summary:
            continue
        data = summary[key]
        cards.append(
            {
                "title": data["label"],
                "current": data["current"],
                "previous": data["previous"],
                "pct_change": data["percent_change"],
                "absolute_change": data["absolute_change"],
                "narrative": default_narrative(key, data),
            }
        )
    return cards


def default_narrative(window_key: str, data: Dict) -> str:
    direction = "up" if data["absolute_change"] >= 0 else "down"
    return (
        f"{window_key.upper()} window: {data['current']} incidents vs "
        f"{data['previous']} in the previous period ({direction} {abs(data['percent_change'])}% )."
    )
