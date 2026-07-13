import os
import logging
from upstash_vector import Index
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

url = os.getenv("UPSTASH_VECTOR_REST_URL", "").strip().replace('"', '').replace("'", "")
token = os.getenv("UPSTASH_VECTOR_REST_TOKEN", "").strip().replace('"', '').replace("'", "")

if not url or not token:
    logger.info("Upstash Vector no configurado. El chatbot funcionara sin busqueda semantica.")

index = Index(url=url, token=token)

def indexar_productos(productos):
    if not url or not token:
        return
        
    vectors = []
    for p in productos:
        metadata_text = (
            f"Producto: {p.nombre}. "
            f"Descripción: {p.descripcion}. "
            f"Características: {p.caracteristicas}. "
            f"Categoría: {p.subcategoria.nombre if p.subcategoria else 'N/A'}"
            f"Cantidad: {p.cantidad}"
        )
        metadata = {
            "id": p.id,
            "nombre": p.nombre,
            "precio": float(p.precio) if p.precio else 0.0,
            "categoria": p.subcategoria.nombre if p.subcategoria else "N/A",
            "cantidad": p.cantidad
        }
        vectors.append((str(p.id), metadata_text, metadata))
    
    if vectors:
        index.upsert(vectors=vectors)

def buscar_productos_similares(query, top_k=5):
    if not url or not token:
        return []
        
    try:
        resultados = index.query(data=query, top_k=top_k, include_metadata=True, include_data=True)
        return resultados
    except Exception as e:
        logger.warning("Error al consultar Upstash: %s", e)
        return []
