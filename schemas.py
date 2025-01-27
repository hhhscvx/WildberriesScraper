from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(extra="ignore")

    artikul: int = Field(alias="nm_id")
    name: str = Field(alias="imt_name")
    category: str = Field(alias="subj_name")
    price: float | None = None

    images_links: list[str] | None = None # Берется из другой апишки.
    photo_count: int | None = None
    
    specifications: list[dict] = Field(alias="options")
    description: str
    rating: float | None = None
    reviews_count: int | None = None
    