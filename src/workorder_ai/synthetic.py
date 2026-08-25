"""Generate independent synthetic facilities work orders for development and testing."""

from __future__ import annotations

import csv
import random
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

WORK_CODES = {
    "HVAC_REPAIR": [
        ("air handler is not cooling the east wing", "AHU", "HVAC"),
        ("thermostat reading high and room remains warm", "THERMOSTAT", "HVAC"),
        ("replace damaged fan belt in rooftop unit", "RTU", "HVAC"),
    ],
    "ELECTRICAL_REPAIR": [
        ("outlet has no power near the laboratory bench", "OUTLET", "ELECTRICAL"),
        ("ceiling lights flicker intermittently", "LIGHTING", "ELECTRICAL"),
        ("breaker trips when equipment starts", "PANEL", "ELECTRICAL"),
    ],
    "PLUMBING_REPAIR": [
        ("sink faucet is leaking below the handle", "FAUCET", "PLUMBING"),
        ("floor drain is backing up", "DRAIN", "PLUMBING"),
        ("toilet continues running after flush", "TOILET", "PLUMBING"),
    ],
    "PREVENTIVE_MAINTENANCE": [
        ("complete quarterly equipment inspection", "GENERAL", "MAINTENANCE"),
        ("replace filters and document condition", "FILTER", "HVAC"),
        ("inspect motor and lubricate bearings", "MOTOR", "MAINTENANCE"),
    ],
    "CARPENTRY_REPAIR": [
        ("office door does not latch correctly", "DOOR", "CARPENTRY"),
        ("repair damaged cabinet hinge", "CABINET", "CARPENTRY"),
        ("wall base is separating near entrance", "WALL", "CARPENTRY"),
    ],
}

FACILITIES = ("North Research Hall", "Riverside Center", "Orchard Library", "Summit Lab")
PRIORITIES = ("LOW", "ROUTINE", "HIGH", "URGENT")


@dataclass(frozen=True)
class WorkOrder:
    """One synthetic work-order phase at the public project grain."""

    workorder_id: str
    phase_id: str
    created_at: str
    facility_name: str
    location_code: str
    asset_id: str | None
    asset_type: str
    craft: str
    priority: str
    description: str
    historical_work_code: str
    source_batch: str


def _vary_text(text: str, rng: random.Random) -> str:
    variants = (
        text,
        text.upper(),
        text.replace("equipment", "equip").replace("laboratory", "lab"),
        f"please investigate - {text}",
    )
    return rng.choice(variants)


def generate_workorders(rows: int, seed: int = 42) -> list[WorkOrder]:
    """Return deterministic synthetic work orders with intentional quality issues."""

    if rows < 1:
        raise ValueError("rows must be at least 1")

    rng = random.Random(seed)
    codes = tuple(WORK_CODES)
    weights = (35, 25, 20, 15, 5)
    start = datetime(2024, 1, 1, 8, tzinfo=UTC)
    records: list[WorkOrder] = []

    for index in range(1, rows + 1):
        code = rng.choices(codes, weights=weights, k=1)[0]
        description, asset_type, craft = rng.choice(WORK_CODES[code])
        created_at = start + timedelta(hours=rng.randint(0, 20_000))
        asset_id = None if rng.random() < 0.08 else f"{asset_type[:3]}-{rng.randint(1, 9999):04d}"

        # A small conflicting-label rate simulates imperfect historical supervision.
        historical_code = rng.choice(codes) if rng.random() < 0.04 else code

        records.append(
            WorkOrder(
                workorder_id=f"WO-{index:08d}",
                phase_id=f"PH-{index:08d}-01",
                created_at=created_at.isoformat(),
                facility_name=rng.choice(FACILITIES),
                location_code=f"RM-{rng.randint(1, 499):03d}",
                asset_id=asset_id,
                asset_type=asset_type,
                craft=craft,
                priority=rng.choices(PRIORITIES, weights=(10, 65, 20, 5), k=1)[0],
                description=_vary_text(description, rng),
                historical_work_code=historical_code,
                source_batch=f"synthetic-{created_at:%Y-%m}",
            )
        )

    return records


def write_workorders_csv(records: list[WorkOrder], output: str | Path) -> Path:
    """Write records to CSV and return the resolved output path."""

    if not records:
        raise ValueError("records cannot be empty")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(records[0])))
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
    return output_path.resolve()
