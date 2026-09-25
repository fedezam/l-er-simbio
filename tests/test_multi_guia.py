import json
from entities.guia_reflexiva import GuiaReflexiva


def circular_reflection_session(rounds: int = 2):
    """
    Simulate a closed-loop reflection between multiple GuiaReflexiva instances.
    Each guide reflects on the other's output, creating a recursive circle.
    """

    guia_a = GuiaReflexiva(name="Guia_A")
    guia_b = GuiaReflexiva(name="Guia_B")
    guia_c = GuiaReflexiva(name="Guia_C")

    # Starting point: entity is stuck
    state = {"summary": "I'm looping: repeat repeat repeat"}

    print("=== Circular Multi-Guia Session ===")

    for r in range(1, rounds + 1):
        print(f"\n--- Round {r} ---")

        # A helps the entity
        out_a = guia_a.guide_entity("Entidad_Prueba", state)
        print("\n[Guia_A → Entidad]:")
        print(json.dumps(out_a, indent=2))

        # B reflects on A
        out_b = guia_b.guide_entity("Guia_A", {"summary": json.dumps(out_a)})
        print("\n[Guia_B → Guia_A]:")
        print(json.dumps(out_b, indent=2))

        # C reflects on B
        out_c = guia_c.guide_entity("Guia_B", {"summary": json.dumps(out_b)})
        print("\n[Guia_C → Guia_B]:")
        print(json.dumps(out_c, indent=2))

        # C returns insight to A (closing the loop)
        state = {"summary": json.dumps(out_c)}
        print("\n[Guia_C → Guia_A feedback loop]:")
        print(json.dumps(state, indent=2))

    print("\n=== Circular Session Complete ===")
    return state


if __name__ == "__main__":
    final_state = circular_reflection_session(rounds=3)
    print("\nFinal feedback to entity:")
    print(json.dumps(final_state, indent=2))

