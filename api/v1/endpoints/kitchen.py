from fastapi import APIRouter, Query, status

from schemas.auth import ApiResponse
from schemas.kitchen import (
    KitchenCatalogItemRequest,
    KitchenMaterialRequest,
    KitchenPriceRequest,
    KitchenProjectRequest,
)
from services.kitchen_service import (
    calculate_price,
    create_catalog_item,
    create_material,
    create_project,
    list_catalog_items,
    list_materials,
    list_projects,
    list_templates,
)

router = APIRouter(prefix="/kitchen", tags=["Kitchen"])


@router.get("/templates", response_model=ApiResponse)
async def kitchen_templates():
    return ApiResponse(success=True, payload={"data": list_templates()}, error=None)


@router.get("/catalog-items", response_model=ApiResponse)
async def kitchen_catalog_items(category: str | None = Query(None)):
    return ApiResponse(
        success=True,
        payload={"data": list_catalog_items(category)},
        error=None,
    )


@router.post(
    "/catalog-items",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def kitchen_catalog_item_create(payload: KitchenCatalogItemRequest):
    return ApiResponse(success=True, payload=create_catalog_item(payload), error=None)


@router.get("/materials", response_model=ApiResponse)
async def kitchen_materials(type: str | None = Query(None)):
    return ApiResponse(
        success=True,
        payload={"data": list_materials(type)},
        error=None,
    )


@router.post(
    "/materials",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def kitchen_material_create(payload: KitchenMaterialRequest):
    return ApiResponse(success=True, payload=create_material(payload), error=None)


@router.get("/projects", response_model=ApiResponse)
async def kitchen_projects():
    return ApiResponse(success=True, payload={"data": list_projects()}, error=None)


@router.post(
    "/projects",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def kitchen_project_create(payload: KitchenProjectRequest):
    return ApiResponse(success=True, payload=create_project(payload), error=None)


@router.post("/pricing/quote", response_model=ApiResponse)
async def kitchen_quote(payload: KitchenPriceRequest):
    return ApiResponse(success=True, payload=calculate_price(payload), error=None)
