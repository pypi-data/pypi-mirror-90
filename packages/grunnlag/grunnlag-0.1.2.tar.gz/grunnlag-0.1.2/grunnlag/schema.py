from grunnlag.gql import CREATE_REPRESENTATION, GET_REPRESENTATION, UPDATE_REPRESENTATION, FILTER_REPRESENTATION
from grunnlag.managers import RepresentationManager
from typing import List, Optional
from bergen.schema import ArnheimModel, User
from grunnlag.extenders import Array, RepresentationPrettifier

class Representation(RepresentationPrettifier, Array, ArnheimModel):
    id: Optional[int]
    name: Optional[str]
    package: Optional[str]
    store: Optional[str]
    shape: Optional[List[int]]
    image: Optional[str]
    creator: Optional[User]
    unique: Optional[str]

    objects = RepresentationManager

    class Meta:
        identifier = "representation"
        get = GET_REPRESENTATION
        create = CREATE_REPRESENTATION
        update = UPDATE_REPRESENTATION
        filter = FILTER_REPRESENTATION




