from typing import Any

from pydantic import BaseModel, Field


class KitchenDimensions(BaseModel):
    width: float = Field(ge=0)
    height: float = Field(ge=0)
    depth: float = Field(ge=0)
    unit: str = "cm"


class KitchenCatalogItemRequest(BaseModel):
    sku: str
    name: str
    category: str
    dimensions: KitchenDimensions
    base_price: float = Field(ge=0)
    model_url: str | None = None
    thumbnail_url: str | None = None
    configurable_options: dict[str, Any] = {}
    is_active: bool = True


class KitchenMaterialRequest(BaseModel):
    code: str
    name: str
    type: str
    color_hex: str | None = None
    texture_url: str | None = None
    price_modifier: float = 0
    modifier_type: str = "fixed"
    is_active: bool = True


class KitchenSceneItemRequest(BaseModel):
    catalog_item_id: str
    position: dict[str, float] = {"x": 0, "y": 0, "z": 0}
    rotation: dict[str, float] = {"x": 0, "y": 0, "z": 0}
    dimensions: KitchenDimensions | None = None
    options: dict[str, Any] = {}
    quantity: int = Field(default=1, ge=1)


class KitchenProjectRequest(BaseModel):
    name: str
    customer_name: str | None = None
    room_dimensions: KitchenDimensions | None = None
    template_id: str | None = None
    items: list[KitchenSceneItemRequest] = []
    notes: str | None = None


class KitchenPriceRequest(BaseModel):
    items: list[KitchenSceneItemRequest] = []
    discount_rate: float = 0
    include_installation: bool = False
