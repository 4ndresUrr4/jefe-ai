#!/usr/bin/env python3
"""
Carlos Memory Integration - Mem0
Usar para recordar contexto de conversaciones con Andres
"""

from mem0 import MemoryClient
import os

API_KEY = "m0-bku8Hrss2JJwRsBMLNhr0INlmPlAvw46b2aAiFr7"
USER_ID = "carlos-jefe-proyecto"

client = MemoryClient(api_key=API_KEY)

def remember(fact: str):
    """Guarda un hecho importante"""
    client.add(
        messages=[{"role": "user", "content": fact}],
        user_id=USER_ID
    )
    print(f"💾 Recordado: {fact}")

def recall(query: str):
    """Busca memorias relacionadas"""
    results = client.search(query, filters={"user_id": USER_ID})
    return results.get("results", [])

def show_all():
    """Muestra todas las memorias"""
    # Mem0 no tiene listar todas, pero podemos hacer búsquedas genéricas
    return recall("")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: mem0_integration.py [remember|recall] [texto]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "remember":
        fact = sys.argv[2] if len(sys.argv) > 2 else "Algo importante"
        remember(fact)
    elif action == "recall":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = recall(query)
        for r in results:
            print(f"📝 {r.get('memory', 'N/A')}")
    else:
        print("Acción desconocida")
