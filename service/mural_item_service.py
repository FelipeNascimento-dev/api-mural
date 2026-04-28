from datetime import datetime, timezone


class MuralItemService():
    def _build_field_name(self,  field_name: str, relation: bool = True):

        if not relation:
            return f"{field_name}"

        return f"mural_item.{field_name}"

    def build_default_filters(self, relation: bool = True):
        now = datetime.now(timezone.utc)
        return [
            {
                "field": self._build_field_name(field_name="is_active", relation=relation),
                "operator": "=",
                "value": True
            },
            {
                "field": self._build_field_name(field_name="starts_at", relation=relation),
                "operator": "<=",
                "value": now
            },
            {
                "logic": "or",
                "conditions": [
                    {
                        "field": self._build_field_name(field_name="ends_at", relation=relation),
                        "operator": ">=",
                        "value": now
                    },
                    {
                        "field": self._build_field_name(field_name="is_indefinite", relation=relation),
                        "operator": "=",
                        "value": True
                    }
                ]
            }
        ]

    def build_visibility_conditions(self, target_type: str, ids: list[int] = []):

        if ids:
            filter_final = {
                "logic": "and",
                "conditions": [
                    {
                        "field": "target_type",
                        "operator": "=",
                        "value": target_type
                    },
                    {
                        "field": "id",
                        "operator": "in",
                        "value": ids
                    }
                ]
            }
        else:
            filter_final = {
                "field": "target_type",
                "operator": "=",
                "value": target_type
            }
        return filter_final


mural_item_service = MuralItemService()
