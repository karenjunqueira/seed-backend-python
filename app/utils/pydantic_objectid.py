from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core.core_schema import CoreSchema, no_info_plain_validator_function


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return no_info_plain_validator_function(cls)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

