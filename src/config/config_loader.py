import json
import os
from typing import List, Dict, Optional

class ConfigLoader:
    def __init__(self):
        self._account_types = None
        self._config_dir = os.path.dirname(__file__)
        self._account_types_file = os.path.join(self._config_dir, 'account_types.json')
    
    def _load_account_types(self) -> List[Dict]:
        if self._account_types is None:
            try:
                with open(self._account_types_file, 'r') as f:
                    config = json.load(f)
                    self._account_types = config['account_types']
            except FileNotFoundError:
                print(f"Configuration file not found: {self._account_types_file}")
                return []
            except json.JSONDecodeError as e:
                print(f"Error parsing configuration file: {e}")
                return []
        return self._account_types

    def get_account_types(self) -> List[str]:
        account_types = self._load_account_types()
        return [account_type['display_name'] for account_type in account_types]
    
    def is_credit_account(self, account_type: str) -> bool:
        account_types = self._load_account_types()
        for acc_type in account_types:
            if acc_type['name'].lower() == account_type.lower() or acc_type['display_name'].lower() == account_type.lower():
                return acc_type['is_credit']
        return False
    
    def get_account_type_by_name(self, account_type: str) -> Optional[Dict]:
        account_types = self._load_account_types()
        for acc_type in account_types:
            if acc_type['name'].lower() == account_type.lower() or acc_type['display_name'].lower() == account_type.lower():
                return acc_type
        return None 