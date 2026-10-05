#!/usr/bin/env python3
"""Deterministic, standard-library checks for the fictional EV-SCI-001 case."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve()
PACK = HERE.parents[1]
SOURCES_PATH = PACK / "case" / "sources.json"
CHANGES_PATH = PACK / "case" / "changes.json"
INITIAL_PATH = PACK / "fixtures" / "initial.json"
REVISED_PATH = PACK / "fixtures" / "revised.json"
ROLES = ("finance", "risk", "creative", "marketing")
REQUIRED_HANDOFF_FIELDS = (
    "writer_session", "model", "brief_version", "artifact", "status",
    "dependencies_acknowledged", "source_ids", "assumptions", "open_questions",
    "change_ack_ids",
)
REQUIRED_TOP_FIELDS = (
    "event_id", "brief_version", "fictional", "title", "attendance", "currency",
    "ceiling_cents", "budget", "subtotal_cents", "contingency_cents", "total_cents",
    "programme", "risks", "marketing", "handoffs", "pending_human_decisions",
)


class InvalidData(Exception):
    pass


def read_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InvalidData(f"cannot read valid JSON from {path}: {exc}") from None


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_string_list(value: Any, *, nonempty: bool = False) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and all(nonempty_string(x) for x in value)


def duplicates(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    repeated: set[Any] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def validate(proposal: Any, sources: Any, changes: Any) -> list[str]:
    errors: list[str] = []

    def err(message: str) -> None:
        errors.append(message)

    if not isinstance(proposal, dict):
        return ["proposal must be a JSON object"]
    if not isinstance(sources, dict):
        return ["source pack must be a JSON object"]
    if not isinstance(changes, dict):
        return ["change pack must be a JSON object"]

    for field in REQUIRED_TOP_FIELDS:
        if field not in proposal:
            err(f"missing required field: {field}")
    if sources.get("case_id") != "EV-SCI-001" or proposal.get("event_id") != "EV-SCI-001":
        err("event_id/case_id must be EV-SCI-001")
    version = proposal.get("brief_version")
    if not is_int(version) or version not in (1, 2):
        err("brief_version must be integer 1 or 2")
        version = None
    if proposal.get("fictional") is not True:
        err("fictional must be literal true")
    if not nonempty_string(proposal.get("title")):
        err("title must be a nonempty string")
    if proposal.get("attendance") != 80 or not is_int(proposal.get("attendance")):
        err("attendance must be integer 80")
    if proposal.get("currency") != "AUD":
        err("currency must be AUD")
    if proposal.get("ceiling_cents") != 600000 or not is_int(proposal.get("ceiling_cents")):
        err("ceiling_cents must be integer 600000")
    if sources.get("fictional") is not True or sources.get("currency") != "AUD":
        err("source pack must declare fictional true and currency AUD")

    # Source cards are the sole permitted price and provenance basis.
    cards: dict[str, dict[str, Any]] = {}
    all_card_ids: list[str] = []
    card_groups = ("budget_cards", "programme_cards", "risk_cards", "support_cards")
    for group in card_groups:
        rows = sources.get(group)
        if not isinstance(rows, list):
            err(f"source pack {group} must be a list")
            continue
        for index, card in enumerate(rows):
            if not isinstance(card, dict) or not nonempty_string(card.get("id")):
                err(f"source pack {group}[{index}] must have a string id")
                continue
            card_id = card["id"]
            all_card_ids.append(card_id)
            cards[card_id] = card
            if group == "budget_cards":
                if not nonempty_string(card.get("kind")) or not nonempty_string(card.get("description")):
                    err(f"source card {card_id} requires kind and description")
                if not is_int(card.get("unit_cents")) or card["unit_cents"] < 0:
                    err(f"source card {card_id} unit_cents must be nonnegative integer cents")
    card_dupes = duplicates(all_card_ids)
    if card_dupes:
        err("duplicate source-card id(s): " + ", ".join(sorted(card_dupes)))

    rooms_by_id: dict[str, dict[str, Any]] = {}
    rooms = sources.get("rooms")
    if not isinstance(rooms, list):
        err("source pack rooms must be a list")
        rooms = []
    for index, room in enumerate(rooms):
        if not isinstance(room, dict) or not nonempty_string(room.get("id")):
            err(f"rooms[{index}] must have a string id")
            continue
        room_id = room["id"]
        if room_id in rooms_by_id:
            err(f"duplicate room id: {room_id}")
        rooms_by_id[room_id] = room
        if not is_int(room.get("capacity")) or room["capacity"] <= 0:
            err(f"room {room_id} capacity must be a positive integer")
        room_source = room.get("source_id")
        if not isinstance(room_source, str) or room_source not in cards or cards.get(room_source, {}).get("kind") != "venue":
            err(f"room {room_id} has an invalid venue source_id")

    resources_by_id: dict[str, dict[str, Any]] = {}
    resources = sources.get("resources")
    if not isinstance(resources, list):
        err("source pack resources must be a list")
        resources = []
    for index, resource in enumerate(resources):
        if not isinstance(resource, dict) or not nonempty_string(resource.get("id")):
            err(f"resources[{index}] must have a string id")
            continue
        resource_id = resource["id"]
        if resource_id in resources_by_id:
            err(f"duplicate resource id: {resource_id}")
        resources_by_id[resource_id] = resource
        if not is_int(resource.get("capacity")) or resource["capacity"] <= 0:
            err(f"resource {resource_id} capacity must be a positive integer")
        if resource.get("usage_mode") not in ("attendees", "event_unit", "exclusive"):
            err(f"resource {resource_id} has unsupported usage_mode")
        if not isinstance(resource.get("exclusive"), bool) or not isinstance(resource.get("purchase_required"), bool):
            err(f"resource {resource_id} exclusive and purchase_required must be booleans")
        if resource.get("usage_mode") == "exclusive" and resource.get("exclusive") is not True:
            err(f"resource {resource_id} exclusive usage_mode requires exclusive true")
        source_id = resource.get("source_id")
        if not isinstance(source_id, str) or source_id not in cards or cards.get(source_id, {}).get("kind") != "resource":
            err(f"resource {resource_id} has an invalid resource source_id")
        elif resource.get("purchase_required") is False:
            card = cards[source_id]
            if not is_int(card.get("inventory_quantity")) or card["inventory_quantity"] <= 0:
                err(f"included resource {resource_id} requires a positive source-card inventory_quantity")
            if card.get("included_with") not in cards or cards.get(card.get("included_with"), {}).get("kind") != "venue":
                err(f"included resource {resource_id} requires a valid included_with venue card")

    budget_rows = proposal.get("budget")
    budget_lines: dict[str, dict[str, Any]] = {}
    budget_source_totals: dict[str, int] = {}
    budget_quantities: dict[str, int] = {}
    used_venue_cards: set[str] = set()
    if not isinstance(budget_rows, list):
        err("budget must be a list")
        budget_rows = []
    for index, line in enumerate(budget_rows):
        if not isinstance(line, dict):
            err(f"budget[{index}] must be an object")
            continue
        line_id, source_id = line.get("id"), line.get("source_id")
        if not nonempty_string(line_id):
            err(f"budget[{index}] id must be a nonempty string")
        elif line_id in budget_lines:
            err(f"duplicate budget line id: {line_id}")
        else:
            budget_lines[line_id] = line
        if not is_int(line.get("quantity")) or line["quantity"] <= 0:
            err(f"budget line {line_id!r} quantity must be a positive integer")
            continue
        if not isinstance(source_id, str) or source_id not in cards or cards.get(source_id, {}).get("kind") not in ("venue", "resource"):
            err(f"budget line {line_id!r} references unknown/non-purchasable source {source_id!r}")
            continue
        card = cards[source_id]
        price = line.get("unit_cents")
        if not is_int(price) or price <= 0:
            err(f"budget line {line_id!r} unit_cents must be a positive integer")
        elif price != card.get("unit_cents"):
            err(f"budget line {line_id!r} unit_cents does not match source card {source_id}")
        else:
            budget_source_totals[source_id] = budget_source_totals.get(source_id, 0) + line["quantity"] * price
        budget_quantities[source_id] = budget_quantities.get(source_id, 0) + line["quantity"]
        if card.get("kind") == "venue":
            used_venue_cards.add(source_id)
    budget_sources = [line.get("source_id") for line in budget_rows if isinstance(line, dict)]
    if duplicates([s for s in budget_sources if isinstance(s, str)]):
        err("each source card may appear on at most one budget line")

    subtotal = 0
    for line in budget_rows:
        if isinstance(line, dict) and is_int(line.get("quantity")) and is_int(line.get("unit_cents")) and line["quantity"] > 0 and line["unit_cents"] > 0:
            subtotal += line["quantity"] * line["unit_cents"]
    contingency = (subtotal + 9) // 10
    for field, actual in (("subtotal_cents", subtotal), ("contingency_cents", contingency), ("total_cents", subtotal + contingency)):
        if not is_int(proposal.get(field)) or proposal.get(field) != actual:
            err(f"{field} must equal recomputed value {actual}")
    if subtotal + contingency > 600000:
        err(f"budget with contingency overspends ceiling: {subtotal + contingency} > 600000")

    # Verify every purchased resource is budgeted and the selected inventory is sufficient.
    resource_available: dict[str, int] = {}
    for resource_id, resource in resources_by_id.items():
        source_id = resource.get("source_id")
        if resource.get("purchase_required") is True:
            qty = budget_quantities.get(source_id, 0)
            if qty <= 0:
                err(f"required resource {resource_id} is missing a purchase budget line")
            resource_available[resource_id] = (resource.get("capacity", 0) if is_int(resource.get("capacity")) else 0) * qty
        elif source_id in cards:
            card = cards[source_id]
            available = card.get("inventory_quantity", 0)
            resource_available[resource_id] = (resource.get("capacity", 0) if is_int(resource.get("capacity")) else 0) * (available if is_int(available) else 0)
            if card.get("included_with") not in used_venue_cards:
                err(f"included resource {resource_id} is unavailable because its venue card is not selected")

    version_table = sources.get("versions")
    version_entry = version_table.get(str(version)) if isinstance(version_table, dict) and version is not None else None
    if not isinstance(version_entry, dict) or not isinstance(version_entry.get("available_rooms"), list):
        err("source pack is missing the availability list for this brief_version")
        available_rooms: set[str] = set()
    else:
        available_rooms = set(x for x in version_entry["available_rooms"] if isinstance(x, str))
    closure_ids: set[str] = set()
    change_rows = changes.get("changes")
    if not isinstance(change_rows, list):
        err("change pack changes must be a list")
        change_rows = []
    for change in change_rows:
        if isinstance(change, dict) and nonempty_string(change.get("id")):
            closure_ids.add(change["id"])
    court_changes = [c for c in change_rows if isinstance(c, dict) and c.get("field") == "available_rooms.ROOM-COURT"]
    if not court_changes or court_changes[0].get("id") != "CH-001" or court_changes[0].get("from_version") != 1 or court_changes[0].get("to_version") != 2 or court_changes[0].get("new_value") != "unavailable":
        err("change pack must declare CH-001 courtyard closure from version 1 to 2")
    expected_change_acks = ["CH-001"] if version == 2 else []

    selected_room_ids: set[str] = set()
    programme = proposal.get("programme")
    if not isinstance(programme, list) or not programme:
        err("programme must be a nonempty list")
        programme = []
    program_ids: list[str] = []
    normalized_programs: list[dict[str, Any]] = []
    for index, row in enumerate(programme):
        if not isinstance(row, dict):
            err(f"programme[{index}] must be an object")
            continue
        for field in ("id", "title", "room_id", "start_minute", "end_minute", "attendees", "resources", "source_ids"):
            if field not in row:
                err(f"programme[{index}] missing required field: {field}")
        pid = row.get("id")
        if not nonempty_string(pid):
            err(f"programme[{index}] id must be a nonempty string")
        else:
            program_ids.append(pid)
        if not nonempty_string(row.get("title")):
            err(f"programme {pid!r} title must be a nonempty string")
        room_id = row.get("room_id")
        room = rooms_by_id.get(room_id) if isinstance(room_id, str) else None
        if room is None:
            err(f"programme {pid!r} references unknown room {room_id!r}")
        else:
            selected_room_ids.add(room_id)
            if room_id not in available_rooms:
                err(f"programme {pid!r} uses room {room_id} unavailable in version {version}")
            if room.get("source_id") not in used_venue_cards:
                err(f"programme {pid!r} room {room_id} has no selected venue budget line")
        start, end, count = row.get("start_minute"), row.get("end_minute"), row.get("attendees")
        if not is_int(start) or not is_int(end) or start < 1080 or end > 1260 or start >= end:
            err(f"programme {pid!r} must use a positive interval within venue window [1080,1260]")
        if not is_int(count) or count < 0 or count > 80:
            err(f"programme {pid!r} attendees must be an integer from 0 to 80")
        elif room is not None and is_int(room.get("capacity")) and count > room["capacity"]:
            err(f"programme {pid!r} exceeds room {room_id} capacity {room['capacity']}")
        row_resources = row.get("resources")
        if not isinstance(row_resources, list) or not all(nonempty_string(x) for x in row_resources):
            err(f"programme {pid!r} resources must be a list of resource IDs")
            row_resources = []
        elif duplicates(row_resources):
            err(f"programme {pid!r} has duplicate resource IDs")
        for resource_id in row_resources:
            if resource_id not in resources_by_id:
                err(f"programme {pid!r} references unknown resource {resource_id}")
        srcs = row.get("source_ids")
        if not valid_string_list(srcs, nonempty=True):
            err(f"programme {pid!r} source_ids must be a nonempty list of source IDs")
        else:
            if duplicates(srcs):
                err(f"programme {pid!r} has duplicate source_ids")
            for source_id in srcs:
                if source_id not in cards:
                    err(f"programme {pid!r} references unknown source {source_id}")
        normalized_programs.append(row)
    if duplicates(program_ids):
        err("programme IDs must be unique")

    def overlaps(a: dict[str, Any], b: dict[str, Any]) -> bool:
        return (is_int(a.get("start_minute")) and is_int(a.get("end_minute")) and
                is_int(b.get("start_minute")) and is_int(b.get("end_minute")) and
                max(a["start_minute"], b["start_minute"]) < min(a["end_minute"], b["end_minute"]))

    boundaries = sorted({v for row in normalized_programs for v in (row.get("start_minute"), row.get("end_minute")) if is_int(v)})
    for ix, left in enumerate(normalized_programs):
        for right in normalized_programs[ix + 1:]:
            if not overlaps(left, right):
                continue
            if left.get("room_id") == right.get("room_id"):
                err(f"overlapping room use: {left.get('id')} and {right.get('id')} both use {left.get('room_id')}")
            shared = set(x for x in left.get("resources", []) if isinstance(x, str)) & set(x for x in right.get("resources", []) if isinstance(x, str))
            for resource_id in shared:
                resource = resources_by_id.get(resource_id)
                if resource and resource.get("exclusive"):
                    err(f"exclusive resource {resource_id} overlaps between {left.get('id')} and {right.get('id')}")
    for start, end in zip(boundaries, boundaries[1:]):
        if start == end:
            continue
        active = [r for r in normalized_programs if is_int(r.get("start_minute")) and is_int(r.get("end_minute")) and r["start_minute"] < end and start < r["end_minute"]]
        total_people = sum(r.get("attendees", 0) for r in active if is_int(r.get("attendees")) and r.get("attendees") >= 0)
        if total_people > 80:
            err(f"simultaneous attendance exceeds event total: {total_people} > 80 during [{start},{end})")
        for resource_id, resource in resources_by_id.items():
            using = [r for r in active if isinstance(r.get("resources"), list) and resource_id in r["resources"]]
            if not using:
                continue
            if resource.get("usage_mode") == "attendees":
                used = sum(r.get("attendees", 0) for r in using if is_int(r.get("attendees")) and r.get("attendees") >= 0)
            else:
                used = len(using)
            cap = resource_available.get(resource_id, 0)
            if used > cap:
                err(f"resource {resource_id} concurrent use {used} exceeds available capacity {cap} during [{start},{end})")

    # The fixtures model setup and pack-down as explicit in-window programme rows.
    titles = [r.get("title", "").lower() for r in normalized_programs if isinstance(r.get("title"), str)]
    if not any("setup" in title or "set up" in title for title in titles):
        err("programme must include explicit setup within the venue window")
    if not any("pack down" in title or "pack-down" in title for title in titles):
        err("programme must include explicit pack-down within the venue window")

    risks = proposal.get("risks")
    if not isinstance(risks, list) or not risks:
        err("risks must be a nonempty list")
        risks = []
    risk_ids: list[str] = []
    risk_card_ids = {c["id"] for c in sources.get("risk_cards", []) if isinstance(c, dict) and isinstance(c.get("id"), str)}
    for index, risk in enumerate(risks):
        if not isinstance(risk, dict):
            err(f"risks[{index}] must be an object")
            continue
        rid = risk.get("id")
        if not nonempty_string(rid):
            err(f"risks[{index}] id must be a nonempty string")
        else:
            risk_ids.append(rid)
        for field in ("issue", "owner", "mitigation"):
            if not nonempty_string(risk.get(field)):
                err(f"risk {rid!r} {field} must be a nonempty string")
        if risk.get("status") not in ("open", "mitigated"):
            err(f"risk {rid!r} status must be open or mitigated")
        srcs = risk.get("source_ids")
        if not valid_string_list(srcs, nonempty=True):
            err(f"risk {rid!r} source_ids must be a nonempty list")
        else:
            for source_id in srcs:
                if source_id not in risk_card_ids:
                    err(f"risk {rid!r} references unknown/non-risk source {source_id}")
    if duplicates(risk_ids):
        err("risk IDs must be unique")

    marketing = proposal.get("marketing")
    if not isinstance(marketing, dict):
        err("marketing must be an object")
        marketing = {}
    for field in ("brief_version", "title", "attendance", "programme_ids", "room_ids", "draft_copy", "publication_status"):
        if field not in marketing:
            err(f"marketing missing required field: {field}")
    if marketing.get("brief_version") != version:
        err("marketing brief_version must match proposal")
    if marketing.get("title") != proposal.get("title"):
        err("marketing title must match proposal title")
    if marketing.get("attendance") != proposal.get("attendance"):
        err("marketing attendance must match proposal attendance")
    expected_program_ids = [r.get("id") for r in normalized_programs if isinstance(r.get("id"), str)]
    if marketing.get("programme_ids") != expected_program_ids:
        err("marketing programme_ids must match programme IDs in order")
    if not valid_string_list(marketing.get("room_ids")) or set(marketing.get("room_ids", [])) != selected_room_ids:
        err("marketing room_ids must exactly match the rooms used by the programme")
    copy_text = marketing.get("draft_copy")
    if not nonempty_string(copy_text):
        err("marketing draft_copy must be a nonempty string")
        copy_text = ""
    elif marketing.get("publication_status") != "draft_only":
        err("marketing publication_status must be draft_only")
    if isinstance(copy_text, str):
        lower_copy = copy_text.casefold()
        if isinstance(proposal.get("title"), str) and proposal["title"].casefold() not in lower_copy:
            err("marketing draft_copy must include the proposal title")
        if "80" not in copy_text or "adult" not in lower_copy:
            err("marketing draft_copy must accurately state an audience of 80 adults")
        if version == 2 and "court" in lower_copy:
            err("version 2 marketing draft_copy must remove courtyard references")

    handoffs = proposal.get("handoffs")
    if not isinstance(handoffs, dict):
        err("handoffs must be an object")
        handoffs = {}
    if set(handoffs) != set(ROLES):
        err("handoffs must contain exactly finance, risk, creative, and marketing")
    expected_dependencies = {"finance": [], "risk": ["finance", "creative"], "creative": [], "marketing": ["finance", "risk", "creative"]}
    for role in ROLES:
        handoff = handoffs.get(role)
        if not isinstance(handoff, dict):
            err(f"handoff {role} must be an object")
            continue
        for field in REQUIRED_HANDOFF_FIELDS:
            if field not in handoff:
                err(f"handoff {role} missing required field: {field}")
        for field in ("writer_session", "model", "artifact"):
            if not nonempty_string(handoff.get(field)):
                err(f"handoff {role} {field} must be a nonempty string")
        if handoff.get("brief_version") != version:
            err(f"handoff {role} has stale brief_version")
        if handoff.get("status") != "ready_for_review":
            err(f"handoff {role} status must be ready_for_review for an integrated fixture")
        deps = handoff.get("dependencies_acknowledged")
        if not valid_string_list(deps) or duplicates(deps) or set(deps) != set(expected_dependencies[role]):
            err(f"handoff {role} dependencies_acknowledged must be {expected_dependencies[role]}")
        if not valid_string_list(handoff.get("source_ids"), nonempty=True):
            err(f"handoff {role} source_ids must be a nonempty list of strings")
        for field in ("assumptions", "open_questions"):
            if not valid_string_list(handoff.get(field)):
                err(f"handoff {role} {field} must be a list of strings")
        if valid_string_list(handoff.get("source_ids"), nonempty=True):
            for source_id in handoff["source_ids"]:
                if source_id not in cards:
                    err(f"handoff {role} references unknown source {source_id}")
        ack = handoff.get("change_ack_ids")
        if not valid_string_list(ack) or ack != expected_change_acks:
            err(f"handoff {role} change_ack_ids must be {expected_change_acks} for version {version}")
    pending = proposal.get("pending_human_decisions")
    if not valid_string_list(pending, nonempty=True):
        err("pending_human_decisions must be a nonempty list of strings")
    return errors


def self_test(sources: Any, changes: Any) -> int:
    cases: list[tuple[str, Any, str | None]] = []
    try:
        initial, revised = read_json(INITIAL_PATH), read_json(REVISED_PATH)
    except InvalidData as exc:
        print(f"SELF-TEST FAIL: {exc}", file=sys.stderr)
        return 1
    cases.extend((("initial fixture", initial, None), ("revised fixture", revised, None)))

    def mutation_fails_with(name: str, expected: str, fn: Any) -> None:
        data = copy.deepcopy(revised)
        fn(data)
        cases.append((name, data, expected))

    def recalculate(data: dict[str, Any]) -> None:
        subtotal = sum(row["quantity"] * row["unit_cents"] for row in data["budget"])
        data["subtotal_cents"] = subtotal
        data["contingency_cents"] = (subtotal + 9) // 10
        data["total_cents"] = subtotal + data["contingency_cents"]

    mutation_fails_with("malformed type", "programme must be a nonempty list", lambda d: d.__setitem__("programme", "not a list"))
    mutation_fails_with("missing field", "missing required field: title", lambda d: d.pop("title"))
    mutation_fails_with("wrong subtotal arithmetic", "subtotal_cents must equal", lambda d: d.__setitem__("subtotal_cents", d["subtotal_cents"] + 1))
    mutation_fails_with("overspend", "overspends ceiling", lambda d: (d["budget"][0].__setitem__("quantity", 3), recalculate(d)))
    mutation_fails_with("overlapping room", "overlapping room use", lambda d: d["programme"][3].__setitem__("start_minute", 1140))
    mutation_fails_with("overlapping exclusive resource", "exclusive resource RES-PA overlaps", lambda d: (d["programme"][3].__setitem__("resources", d["programme"][3]["resources"] + ["RES-PA"]), d["programme"][4].__setitem__("resources", d["programme"][4]["resources"] + ["RES-PA"])))
    mutation_fails_with("unknown source", "references unknown source", lambda d: d["programme"][0].__setitem__("source_ids", ["SRC-DOES-NOT-EXIST"]))
    mutation_fails_with("closed room", "uses room ROOM-COURT unavailable", lambda d: d["programme"][3].__setitem__("room_id", "ROOM-COURT"))
    mutation_fails_with("stale version", "handoff creative has stale brief_version", lambda d: d["handoffs"]["creative"].__setitem__("brief_version", 1))
    mutation_fails_with("missing change acknowledgement", "handoff marketing change_ack_ids", lambda d: d["handoffs"]["marketing"].__setitem__("change_ack_ids", []))
    mutation_fails_with("inconsistent marketing", "marketing attendance must match", lambda d: d["marketing"].__setitem__("attendance", 79))
    mutation_fails_with("insufficient pooled resources", "resource RES-ART concurrent use", lambda d: (d["budget"][2].__setitem__("quantity", 1), recalculate(d)))
    mutation_fails_with("missing required resource purchase", "required resource RES-PA is missing", lambda d: (d["budget"].__setitem__(slice(None), [line for line in d["budget"] if line["source_id"] != "SRC-RES-02"]), recalculate(d)))
    # A malformed JSON parser case is exercised without touching a fixture file.
    try:
        json.loads('{"broken":')
        cases.append(("malformed JSON", {}, ""))
    except json.JSONDecodeError:
        print("PASS malformed JSON: parser rejects truncated input")

    failures = 0
    for name, candidate, expected in cases:
        problems = validate(candidate, sources, changes)
        if expected is None:
            okay = not problems
            expectation = "pass"
        else:
            okay = bool(problems) and (expected == "" or any(expected in problem for problem in problems))
            expectation = f"fail with {expected!r}" if expected else "fail"
        if not okay:
            failures += 1
            actual = "; ".join(problems[:2]) if problems else "no diagnostic"
            print(f"FAIL {name}: expected to {expectation}, got {actual}")
        else:
            print(f"PASS {name}" + (f" rejected: {next((p for p in problems if not expected or expected in p), problems[0])}" if problems else ""))
    if failures:
        print(f"SELF-TEST FAIL: {failures} case(s) did not meet expectation", file=sys.stderr)
        return 1
    print(f"SELF-TEST PASS: {len(cases) + 1} checks")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        try:
            sources, changes = read_json(SOURCES_PATH), read_json(CHANGES_PATH)
        except InvalidData as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        return self_test(sources, changes)
    if len(argv) > 1 or (argv and argv[0] in ("-h", "--help")):
        print(f"Usage: {Path(sys.argv[0]).name} [--self-test | PROPOSAL.json]", file=sys.stderr)
        return 2
    proposal_path = Path(argv[0]) if argv else REVISED_PATH
    if not proposal_path.is_absolute():
        proposal_path = Path.cwd() / proposal_path
    try:
        proposal = read_json(proposal_path)
        sources, changes = read_json(SOURCES_PATH), read_json(CHANGES_PATH)
    except InvalidData as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    problems = validate(proposal, sources, changes)
    if problems:
        print(f"FAIL {proposal_path} ({len(problems)} issue(s))")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"PASS {proposal_path}: version {proposal['brief_version']}, budget {proposal['total_cents']} cents including contingency, {len(proposal['programme'])} programme rows")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        print(f"ERROR: invalid input ({exc})", file=sys.stderr)
        raise SystemExit(2)
