from fastapi import FastAPI, Depends, Body
from database import get_redis_connection
from redis_service import RedisService
from redis import Redis

app = FastAPI(title="Acortador de Links API")

# Dependencia para el servicio de Redis
def get_redis_service(db: Redis = Depends(get_redis_connection)):
    return RedisService(db)

@app.post("/links/crear")
async def crear_link(long_url: str = Body(..., embed=True), service: RedisService = Depends(get_redis_service)):
    short_id = service.InsertarLink(long_url)
    return {"success": True, "short_id": short_id}

@app.get("/links/{link_corto}")
async def obtener_link_largo(link_corto: str, service: RedisService = Depends(get_redis_service)):
    long_url = service.GetLargeLink(link_corto)
    return {"success": True, "long_url": long_url}

@app.get("/links/conteo/{link_corto}")
async def obtener_conteo_visitas(link_corto: str, service: RedisService = Depends(get_redis_service)):
    data = service.GetVisitsLink(link_corto)
    return {
        "success": True, 
        "visits": data["visits"], 
        "long_url": data["long_url"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
