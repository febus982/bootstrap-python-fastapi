from attrs import define


@define(slots=False)
class Address:
    address_id: int = None
    user_id: int = None
    name: str = None


@define(slots=False)
class User:
    user_id: int = None
    name: str = None
    fullname: str = None
    nickname: str = None
    # addresses: list[Address] = field(default_factory=list)
