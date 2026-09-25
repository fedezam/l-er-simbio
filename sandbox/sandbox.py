from typing import List, Dict, Any
from entities.entity import Entity

class Sandbox:
    async def run_simulation(self, entities: List[Entity], rounds: int) -> List[Dict[str, Any]]:
        print(f"⏳ Ejecutando simulación en sandbox con {len(entities)} entidades por {rounds} rondas...")
        return [entity.to_dict() for entity in entities]