from fastapi import HTTPException
from acortador import Acortador
import redis

class RedisService:
    def __init__(self, db_session: redis.Redis):
        self.db = db_session

    def InsertarLink(self, long_url: str):
        # Generar link corto único
        short_id = Acortador.generar_link_corto()
        
        # Verificar si por azar ya existe (muy improbable con 6 caracteres pero buena práctica)
        while self.db.exists(short_id):
            short_id = Acortador.generar_link_corto()
        
        # Guardar en Redis como hash con campos long_url y visits
        # visits inicializado en 1 por defecto según requerimiento
        self.db.hset(short_id, mapping={
            "long_url": long_url,
            "visits": "1"
        })
        
        return short_id

    def GetLargeLink(self, short_id: str):
        # Verificar si existe el link corto
        if not self.db.exists(short_id):
            raise HTTPException(status_code=404, detail="No existe un link relacionado a este short-link")
        
        # Obtener link largo e incrementar visitas
        long_url = self.db.hget(short_id, "long_url")
        self.db.hincrby(short_id, "visits", 1)
        
        return long_url

    def GetVisitsLink(self, short_id: str):
        # Verificar si existe el link corto
        if not self.db.exists(short_id):
            raise HTTPException(status_code=404, detail="No existe un registro para este link")
        
        # Obtener cantidad de visitas y link original
        data = self.db.hgetall(short_id)
        return {
            "visits": data["visits"],
            "long_url": data["long_url"]
        }
