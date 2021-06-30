import royalnet.royaltyping as t
import pydantic as p
import fastapi as f
import fastapi.security as fs
import fastapi.openapi.models as fom


class OpenIDConnectDiscovery(fom.SecurityBase):
    def __init__(self):
        self.type_ = fom.SecuritySchemeType.openIdConnect
