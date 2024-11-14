from fastapi import APIRouter
from src.api.v1.veiws.xml_router import router as xml_parser_router

router = APIRouter(prefix="/api/v1", tags=["Xml-parser"])
router.include_router(xml_parser_router)
