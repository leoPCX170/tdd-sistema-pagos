from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Orden:
    id: str
    monto: float
    token_pago: str
    estado: str = "PENDIENTE"


class RepositorioOrdenes(ABC):
    @abstractmethod
    def obtener_orden(self, orden_id: str) -> Orden | None:
        pass

    @abstractmethod
    def guardar_orden(self, orden: Orden) -> None:
        pass


class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto: float, token: str) -> bool:
        pass


class ServicioPagos:
    def __init__(self, repositorio: RepositorioOrdenes, pasarela: PasarelaPago):
        self.repositorio = repositorio
        self.pasarela = pasarela

    def procesar_pago(self, orden_id: str) -> str:
        orden = self.repositorio.obtener_orden(orden_id)
        if orden is None:
            raise ValueError(f"Orden no encontrada: {orden_id}")

        monto_final = self._calcular_monto_final(orden.monto)
        pago_aprobado = self.pasarela.cobrar(monto_final, orden.token_pago)

        orden.estado = "PAGADA" if pago_aprobado else "FALLIDA"
        self.repositorio.guardar_orden(orden)
        return orden.estado

    def _calcular_monto_final(self, monto: float) -> float:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero")
        if monto > 1000.0:
            return round(monto * 1.05, 2)
        return monto