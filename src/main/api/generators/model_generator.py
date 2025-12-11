import random
import uuid

from typing import Any, get_type_hints, get_origin, Annotated, get_args, Union

import rstr

from src.main.api.generators.creation_rule import CreationRule


class RandomModelGeneration:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule is not None and rule.regex is not None:
                value = RandomModelGeneration._generate_from_regex(rule.regex, actual_type)
            elif rule is not None and rule.min_value is not None and rule.max_value is not None:
                value = RandomModelGeneration._generate_from_range(rule.min_value, rule.max_value, actual_type)
            else:
                value = RandomModelGeneration._generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, actual_type: type) -> Any:
        generated = rstr.xeger(regex)
        if actual_type is int:
            return int(generated)
        if actual_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_from_range(min_value: Union[int, float], max_value: Union[int, float], actual_type: type) -> Any:
        if actual_type is int:
            return random.randint(int(min_value), int(max_value))
        if actual_type is float:
            return round(random.uniform(float(min_value), float(max_value)), 2)
        return random.randint(int(min_value), int(max_value))

    @staticmethod
    def _generate_value(actual_type: type) -> Any:
        if actual_type is str:
            return str(uuid.uuid4())[:8]
        elif actual_type is int:
            return random.randint(1, 9999)
        elif actual_type is float:
            return round(random.uniform(0, 100), 2)
        elif actual_type is bool:
            return random.choice([True, False])
        elif actual_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(actual_type, type):
            return RandomModelGeneration.generate(actual_type)
        return None