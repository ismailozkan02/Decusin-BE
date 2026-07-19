from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from schemas.kitchen import (
    KitchenCatalogItemRequest,
    KitchenMaterialRequest,
    KitchenPriceRequest,
    KitchenProjectRequest,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


KITCHEN_TEMPLATES = [
    {
        "id": "template-linear-300",
        "name": "Duz mutfak 300 cm",
        "type": "linear",
        "room_dimensions": {"width": 300, "height": 260, "depth": 60, "unit": "cm"},
        "preview": {"cabinet_count": 5, "estimated_width": 300},
    },
    {
        "id": "template-l-360-240",
        "name": "L mutfak 360 x 240 cm",
        "type": "l_shape",
        "room_dimensions": {"width": 360, "height": 260, "depth": 240, "unit": "cm"},
        "preview": {"cabinet_count": 8, "estimated_width": 600},
    },
    {
        "id": "template-island-420",
        "name": "Ada mutfak 420 cm",
        "type": "island",
        "room_dimensions": {"width": 420, "height": 260, "depth": 320, "unit": "cm"},
        "preview": {"cabinet_count": 10, "estimated_width": 740},
    },
]


KITCHEN_CATALOG_ITEMS = [
    {
        "id": "cabinet-base-60",
        "sku": "ALT-060",
        "name": "Alt dolap 60 cm",
        "category": "base_cabinet",
        "dimensions": {"width": 60, "height": 72, "depth": 56, "unit": "cm"},
        "base_price": 4800,
        "model_url": None,
        "thumbnail_url": None,
        "configurable_options": {"door": True, "handle": True, "glass": False},
        "is_active": True,
        "created_at": now_iso(),
    },
    {
        "id": "cabinet-wall-80",
        "sku": "UST-080",
        "name": "Ust dolap 80 cm",
        "category": "wall_cabinet",
        "dimensions": {"width": 80, "height": 72, "depth": 34, "unit": "cm"},
        "base_price": 3900,
        "model_url": None,
        "thumbnail_url": None,
        "configurable_options": {"door": True, "handle": True, "glass": True},
        "is_active": True,
        "created_at": now_iso(),
    },
    {
        "id": "countertop-meter",
        "sku": "TEZ-MT",
        "name": "Tezgah metre",
        "category": "countertop",
        "dimensions": {"width": 100, "height": 4, "depth": 60, "unit": "cm"},
        "base_price": 2200,
        "model_url": None,
        "thumbnail_url": None,
        "configurable_options": {"material": True},
        "is_active": True,
        "created_at": now_iso(),
    },
    {
        "id": "sink-standard",
        "sku": "EVY-STD",
        "name": "Standart evye",
        "category": "appliance",
        "dimensions": {"width": 50, "height": 20, "depth": 45, "unit": "cm"},
        "base_price": 3200,
        "model_url": None,
        "thumbnail_url": None,
        "configurable_options": {"material": True},
        "is_active": True,
        "created_at": now_iso(),
    },
]


KITCHEN_MATERIALS = [
    {
        "id": "mat-door-lake-white",
        "code": "LAKE-WHITE",
        "name": "Beyaz lake kapak",
        "type": "door",
        "color_hex": "#F8FAFC",
        "texture_url": None,
        "price_modifier": 0.18,
        "modifier_type": "percent",
        "is_active": True,
    },
    {
        "id": "mat-door-wood-oak",
        "code": "WOOD-OAK",
        "name": "Meşe kapak",
        "type": "door",
        "color_hex": "#B6814A",
        "texture_url": None,
        "price_modifier": 0.12,
        "modifier_type": "percent",
        "is_active": True,
    },
    {
        "id": "mat-glass-smoked",
        "code": "GLASS-SMOKE",
        "name": "Füme cam",
        "type": "glass",
        "color_hex": "#6B7280",
        "texture_url": None,
        "price_modifier": 900,
        "modifier_type": "fixed",
        "is_active": True,
    },
    {
        "id": "mat-counter-quartz",
        "code": "QUARTZ",
        "name": "Kuvars tezgah",
        "type": "countertop",
        "color_hex": "#E5E7EB",
        "texture_url": None,
        "price_modifier": 0.32,
        "modifier_type": "percent",
        "is_active": True,
    },
]


KITCHEN_PROJECTS = [
    {
        "id": "project-demo",
        "name": "Demo L mutfak",
        "customer_name": "Demo Musteri",
        "room_dimensions": {"width": 360, "height": 260, "depth": 240, "unit": "cm"},
        "template_id": "template-l-360-240",
        "items": [
            {
                "catalog_item_id": "cabinet-base-60",
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "dimensions": None,
                "options": {"door_material_id": "mat-door-lake-white"},
                "quantity": 3,
            },
            {
                "catalog_item_id": "cabinet-wall-80",
                "position": {"x": 0, "y": 90, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "dimensions": None,
                "options": {"door_material_id": "mat-door-wood-oak", "glass_material_id": "mat-glass-smoked"},
                "quantity": 2,
            },
        ],
        "notes": "Mock proje. MySQL baglaninca tabloya tasinacak.",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
]


def list_templates() -> list[dict]:
    return deepcopy(KITCHEN_TEMPLATES)


def list_catalog_items(category: str | None = None) -> list[dict]:
    items = [item for item in KITCHEN_CATALOG_ITEMS if item["is_active"]]
    if category:
        items = [item for item in items if item["category"] == category]
    return deepcopy(items)


def create_catalog_item(payload: KitchenCatalogItemRequest) -> dict:
    item = payload.model_dump()
    item["id"] = f"item-{uuid4().hex[:10]}"
    item["created_at"] = now_iso()
    KITCHEN_CATALOG_ITEMS.append(item)
    return deepcopy(item)


def list_materials(material_type: str | None = None) -> list[dict]:
    items = [item for item in KITCHEN_MATERIALS if item["is_active"]]
    if material_type:
        items = [item for item in items if item["type"] == material_type]
    return deepcopy(items)


def create_material(payload: KitchenMaterialRequest) -> dict:
    item = payload.model_dump()
    item["id"] = f"mat-{uuid4().hex[:10]}"
    KITCHEN_MATERIALS.append(item)
    return deepcopy(item)


def list_projects() -> list[dict]:
    return deepcopy(KITCHEN_PROJECTS)


def create_project(payload: KitchenProjectRequest) -> dict:
    item = payload.model_dump()
    item["id"] = f"project-{uuid4().hex[:10]}"
    item["created_at"] = now_iso()
    item["updated_at"] = now_iso()
    KITCHEN_PROJECTS.append(item)
    return deepcopy(item)


def calculate_price(payload: KitchenPriceRequest) -> dict:
    catalog_map = {item["id"]: item for item in KITCHEN_CATALOG_ITEMS}
    material_map = {item["id"]: item for item in KITCHEN_MATERIALS}
    lines = []
    subtotal = 0.0

    for scene_item in payload.items:
        catalog_item = catalog_map.get(scene_item.catalog_item_id)
        if not catalog_item:
            continue

        quantity = scene_item.quantity
        base_total = float(catalog_item["base_price"]) * quantity
        modifiers_total = 0.0

        selected_material_ids = [
            value
            for key, value in scene_item.options.items()
            if key.endswith("_material_id") and value in material_map
        ]

        for material_id in selected_material_ids:
            material = material_map[material_id]
            modifier = float(material["price_modifier"])
            if material["modifier_type"] == "percent":
                modifiers_total += base_total * modifier
            else:
                modifiers_total += modifier * quantity

        line_total = base_total + modifiers_total
        subtotal += line_total
        lines.append(
            {
                "catalog_item_id": scene_item.catalog_item_id,
                "name": catalog_item["name"],
                "quantity": quantity,
                "base_total": round(base_total, 2),
                "modifiers_total": round(modifiers_total, 2),
                "line_total": round(line_total, 2),
            }
        )

    installation = subtotal * 0.08 if payload.include_installation else 0
    discount = subtotal * max(payload.discount_rate, 0) / 100
    total = subtotal + installation - discount

    return {
        "currency": "TRY",
        "lines": lines,
        "subtotal": round(subtotal, 2),
        "installation": round(installation, 2),
        "discount": round(discount, 2),
        "total": round(total, 2),
    }
