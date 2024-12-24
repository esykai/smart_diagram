import re

from graphviz import Digraph
from pytgpt import phind
from typing import Optional, Dict, Any


NEW_PROMPT = """
Ответь только JSON без объяснений. Создай JSON для блок-схемы с ключами:
- id: уникальный идентификатор блока.
- label: текст в блоке.
- shape: форма (например, "ellipse", "parallelogram", "diamond", "box").
- edges: связи между блоками (ключи: from, to, label).

Пример JSON для алгоритма бинарного поиска:
{
  "nodes": [
    {"id": "A", "label": "Начало", "shape": "ellipse"},
    {"id": "B", "label": "Инициализация low и high", "shape": "box"},
    {"id": "C", "label": "mid = (low + high) // 2", "shape": "box"},
    {"id": "D", "label": "arr[mid] == target?", "shape": "diamond"},
    {"id": "E", "label": "Возврат mid", "shape": "box"},
    {"id": "F", "label": "arr[mid] < target?", "shape": "diamond"},
    {"id": "G", "label": "low = mid + 1", "shape": "box"},
    {"id": "H", "label": "high = mid - 1", "shape": "box"},
    {"id": "I", "label": "Элемент не найден", "shape": "box"}
  ],
  "edges": [
    {"from": "A", "to": "B", "label": "начало"},
    {"from": "B", "to": "C"},
    {"from": "C", "to": "D"},
    {"from": "D", "to": "E", "label": "Да"},
    {"from": "D", "to": "F", "label": "Нет"},
    {"from": "F", "to": "G", "label": "Да"},
    {"from": "F", "to": "H", "label": "Нет"},
    {"from": "G", "to": "C", "label": "повторить с новым low"},
    {"from": "H", "to": "C", "label": "повторить с новым high"},
    {"from": "E", "to": "I", "label": "Конец"},
    {"from": "I", "to": "I", "label": "Конец (если элемент не найден)"}
  ]
}

Сгенерируй JSON для следующего алгоритма: напиши по русски и расспиши весь алгоритм """



def chatgpt(prompt: str) -> Optional[str]:
    """
    Запрос к ChatGPT для генерации JSON, содержащего описание блок-схемы.

    :param prompt: Алгоритм в виде текста, для которого нужно сгенерировать блок-схему.
    :return: JSON-строка, содержащая описание блок-схемы или None, если запрос не удался.
    """
    if not prompt:
        return None

    bot = phind.PHIND()
    bot_response = bot.chat(NEW_PROMPT + prompt)

    try:
        return re.search(r'{.*}', bot_response, re.DOTALL).group(0)
    except Exception:
        return ""


def validate_json_structure(data: dict) -> None:
    """
    Проверка структуры JSON для блок-схемы.

    :param data: JSON, содержащий описание блок-схемы.
    :raises ValueError: Если структура JSON некорректна.
    """
    if "nodes" not in data or "edges" not in data:
        raise ValueError("JSON должен содержать ключи 'nodes' и 'edges'.")

    for node in data["nodes"]:
        if "id" not in node or "label" not in node or "shape" not in node:
            raise ValueError("Каждый узел должен содержать 'id', 'label' и 'shape'.")

    for edge in data["edges"]:
        if "from" not in edge or "to" not in edge:
            raise ValueError("Каждое ребро должно содержать 'from' и 'to'.")


def generate_flowchart(json_data: Dict[str, Any]) -> str:
    """
    Генерация блок-схемы из JSON и сохранение её как изображение.

    :param json_data: JSON, содержащий описание блок-схемы.
    :return: Путь к сохраненному изображению блок-схемы.
    """
    diagram = Digraph('Flowchart', format='jpg')

    # Создаем узлы
    for node in json_data['nodes']:
        diagram.node(node['id'], node['label'], shape=node['shape'])

    # Создаем ребра
    for edge in json_data['edges']:
        label = edge.get('label', '')
        diagram.edge(edge['from'], edge['to'], label=label)

    # Сохраняем блок-схему
    output_path = 'flowchart'
    diagram.render(output_path, cleanup=True)
    return output_path + '.jpg'
