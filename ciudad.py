from dataclasses import dataclass


@dataclass(frozen=True)
class Ciudad:
    nombre: str
    latitud: float
    longitud: float

    @property
    def coordenadas(self) -> tuple[float, float]:
        return self.latitud, self.longitud
