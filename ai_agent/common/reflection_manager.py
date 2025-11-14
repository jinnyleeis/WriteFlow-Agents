
import json, os, uuid
from pydantic import BaseModel, Field

class Reflection(BaseModel):
    id: str = ""
    task: str
    reflection: str
    needs_retry: bool = False
    confidence: float = 0.8

class ReflectionManager:
    def __init__(self, file_path: str = "tmp/reflections.json"):
        self.file_path = file_path
        self._items: list[Reflection] = []
        self._load()
    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._items = [Reflection(**x) for x in data]
    def save(self, r: Reflection) -> str:
        r.id = r.id or str(uuid.uuid4())
        self._items.append(r)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([x.model_dump() for x in self._items], f, ensure_ascii=False, indent=2)
        return r.id
    def relevant(self, query: str, k: int = 3) -> list[Reflection]:
        return self._items[-k:]
