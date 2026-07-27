from typing import List, Dict

class ArenaEngine:
    def __init__(self):
        self.models: Dict[str, dict] = {}

    def register_model(self, model_name: str, starting_capital: float = 1000.0):
        self.models[model_name] = {
            "starting_capital": starting_capital,
            "current_equity": starting_capital,
            "return_pct": 0.0
        }

    def update_performance(self, model_name: str, current_equity: float):
        if model_name in self.models:
            start = self.models[model_name]["starting_capital"]
            self.models[model_name]["current_equity"] = current_equity
            self.models[model_name]["return_pct"] = ((current_equity - start) / start) * 100.0

    def get_leaderboard(self) -> List[dict]:
        results = [
            {
                "model_name": name,
                "current_equity": data["current_equity"],
                "return_pct": data["return_pct"]
            }
            for name, data in self.models.items()
        ]
        return sorted(results, key=lambda x: x["return_pct"], reverse=True)
