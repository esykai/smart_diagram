import json

from fastapi import HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any

from utils import chatgpt, validate_json_structure, generate_flowchart


async def generate_flowchart_api(algorithm: str) -> FileResponse:
    """
    Генерация блок-схемы на основе алгоритма, переданного в виде строки.
    Вызывается ChatGPT для получения JSON, затем проверяется структура и генерируется изображение.

    :param algorithm: Описание алгоритма для ChatGPT.
    :return: Файл с изображением блок-схемы.
    :raises HTTPException: В случае ошибки обработки запроса или некорректного формата JSON.
    """
    try:
        # Получаем ответ ChatGPT
        response = chatgpt(algorithm)
        if not response:
            raise HTTPException(status_code=400, detail="Ошибка обработки запроса.")

        # Преобразуем в JSON
        try:
            data: Dict[str, Any] = json.loads(response)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Ответ ChatGPT не является валидным JSON.")

        # Проверяем структуру JSON
        validate_json_structure(data)

        # Генерируем блок-схему
        image_path: str = generate_flowchart(data)
        return FileResponse(image_path, media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=flowchart.jpg"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


async def health_check() -> Dict[str, str]:
    """
    Проверка состояния сервера.

    :return: Словарь с состоянием сервера и текущим временем.
    """
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "ok", "time": current_time}
