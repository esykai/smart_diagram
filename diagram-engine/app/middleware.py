from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from logging import getLogger


logger = getLogger("uvicorn")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования IP-адресов клиентов, отправляющих запросы.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Перехватывает запрос, логирует IP-адрес клиента и передает его дальше по цепочке.

        :param request: Объект запроса.
        :param call_next: Следующий обработчик в цепочке.
        :return: Ответ, возвращенный следующим обработчиком.
        """
        client_ip: str = request.client.host
        logger.info(f"Сделан запрос с айпишника: {client_ip}")
        response: Response = await call_next(request)
        return response
