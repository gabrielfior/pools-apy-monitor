from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TokenDict:
    token_name: str
    token_address: str
    token_decimals: int


class TokenLookup:
    def __init__(self, token_dicts: List[TokenDict]) -> None:
        self.token_wrapper: Dict[str, TokenDict] = {}
        for token_dict in token_dicts:
            self.token_wrapper[token_dict.token_name] = token_dict

    def get_all_addresses(self):
        return [i.token_address for i in self.token_wrapper.values()]

    def get_by_address(self, address) -> TokenDict:
        for k, v in self.token_wrapper.items():
            if v.token_address == address:
                return v

    def get_by_token_name(self, token_name) -> TokenDict:
        return self.token_wrapper[token_name]
