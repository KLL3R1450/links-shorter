import pytest
from fastapi.testclient import TestClient
from backend.api import app
from backend.database import get_redis_connection

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_redis():
    # Limpiar redis db=1 antes de cada prueba
    db = get_redis_connection()
    db.flushdb()
    yield

def test_crear_link():
    response = client.post("/links/crear", json={"long_url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "short_id" in data
    assert len(data["short_id"]) == 6

def test_obtener_link_largo():
    # Primero creamos uno
    res_crear = client.post("/links/crear", json={"long_url": "https://facebook.com"})
    short_id = res_crear.json()["short_id"]
    
    # Obtenemos el link largo
    response = client.get(f"/links/{short_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["long_url"] == "https://facebook.com"

def test_obtener_conteo_visitas():
    # Creamos
    res_crear = client.post("/links/crear", json={"long_url": "https://github.com"})
    short_id = res_crear.json()["short_id"]
    
    # Redirigimos una vez para aumentar visitas (inicialmente es 1 según el requerimiento, al redirigir sube a 2)
    client.get(f"/links/{short_id}")
    
    # Consultamos conteo
    response = client.get(f"/links/conteo/{short_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["visits"] == "2" # 1 inicial + 1 incremento
    assert data["long_url"] == "https://github.com"

def test_link_no_existe():
    response = client.get("/links/noexiste123")
    assert response.status_code == 404
    assert response.json()["detail"] == "No existe un link relacionado a este short-link"

def test_conteo_no_existe():
    response = client.get("/links/conteo/noexiste123")
    assert response.status_code == 404
    assert response.json()["detail"] == "No existe un registro para este link"
