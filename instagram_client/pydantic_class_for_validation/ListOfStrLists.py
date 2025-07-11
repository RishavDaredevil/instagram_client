from typing import List
from pydantic import BaseModel, field_validator, ValidationError

class ListOfStrLists(BaseModel):
    """
    A model that validates a list of string lists,
    where each inner list must contain exactly two strings.
    """
    items: List[List[str]]

    @field_validator('items')
    @classmethod
    def check_inner_list_lengths(cls, v: List[List[str]]) -> List[List[str]]:
        """
        Validates that each inner list contains exactly two elements.
        """
        for inner_list in v:
            if len(inner_list) != 2:
                raise ValueError('Each inner list must contain exactly two string elements')
        return v

if __name__ == '__main__':
    # --- Validation Examples ---

    # ✅ Example of successful validation
    try:
        valid_data = {"items": [["user1", "comment1"], ["user2", "comment2"]]}
        list_of_lists = ListOfStrLists(**valid_data)
        print("✅ Validation successful:")
        print(list_of_lists.model_dump())
    except ValidationError as e:
        print("❌ Validation failed:")
        print(e)

    print("-" * 20)

    # ❌ Example of failed validation (incorrect inner list length)
    try:
        invalid_data = {"items": [["user1", "comment1"], ["user2"]]}
        list_of_lists = ListOfStrLists(**invalid_data)
    except ValidationError as e:
        print("❌ Validation failed (incorrect inner list length):")
        print(e)

    print("-" * 20)

    # ❌ Example of failed validation (incorrect type in inner list)
    try:
        invalid_data_type = {"items": [["user1", "comment1"], ["user2", 123]]}
        list_of_lists = ListOfStrLists(**invalid_data_type)
    except ValidationError as e:
        print("❌ Validation failed (incorrect type in inner list):")
        print(e)