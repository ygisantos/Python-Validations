import re
from datetime import datetime
from urllib.parse import urlparse
import ipaddress

class Validator:
    @staticmethod
    def _can_convert(value, converter):
        try:
            converter(value)
            return True
        except (ValueError, TypeError):
            return False
    
    # ---- TYPE VALIDATORS ---
    @staticmethod
    def is_integer(value): return Validator._can_convert(value, int)
    
    @staticmethod
    def is_float(value): return Validator._can_convert(value, float)
    
    @staticmethod
    def is_string(value): return isinstance(value, str)
    
    @staticmethod
    def is_list(value): return isinstance(value, list)
    
    @staticmethod
    def is_dict(value): return isinstance(value, dict)
    
    @staticmethod
    def is_tuple(value): return isinstance(value, tuple)
    
    @staticmethod
    def is_none(value): return value is None
    
    # ---- STRING VALIDATORS ----
    @staticmethod
    def is_empty(value): return not bool(str(value).strip())
    
    # ---- LENGTH VALIDATORS ----
    @staticmethod
    def min_length(value, min_len): return len(str(value)) >= min_len
    
    @staticmethod
    def max_length(value, max_len): return len(str(value)) <= max_len
    
    @staticmethod
    def exact_length(value, length): return len(str(value)) == length
    
    # ---- RANGE VALIDATORS ----
    @staticmethod
    def in_range(value, min_val, max_val): return min_val <= value <= max_val
    
    # Pattern validators
    @staticmethod
    def matches_pattern(value, pattern): return bool(re.match(pattern, str(value)))
    
    @staticmethod
    def contains_pattern(value, pattern): return bool(re.search(pattern, str(value)))
    
    # Email validator
    @staticmethod
    def is_email(value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, str(value)))
    
    # URL validator
    @staticmethod
    def is_url(value):
        try:
            result = urlparse(str(value))
            return all([result.scheme, result.netloc])
        except:
            return False
    
    # IP validators
    @staticmethod
    def is_ipv4(value):
        try:
            ipaddress.IPv4Address(str(value))
            return True
        except:
            return False
    
    @staticmethod
    def is_ipv6(value):
        try:
            ipaddress.IPv6Address(str(value))
            return True
        except:
            return False
    
    @staticmethod
    def is_ip(value): return Validator.is_ipv4(value) or Validator.is_ipv6(value)
    
    # Phone validator (basic)
    @staticmethod
    def is_phone(value):
        pattern = r'^[\+]?[1-9][\d]{0,15}$'
        clean = re.sub(r'[\s\-\(\)]', '', str(value))
        return bool(re.match(pattern, clean))
    
    # Date validators
    @staticmethod
    def is_date(value, format='%Y-%m-%d'):
        try:
            datetime.strptime(str(value), format)
            return True
        except:
            return False
    
    # Credit card validator (Luhn algorithm)
    @staticmethod
    def is_credit_card(value):
        clean = re.sub(r'[\s\-]', '', str(value))
        if not clean.isdigit() or len(clean) < 13 or len(clean) > 19:
            return False
        
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            for i in range(len(digits) - 2, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
            return sum(digits) % 10 == 0
        
        return luhn_check(clean)
    
    # Password strength
    @staticmethod
    def is_strong_password(value, min_len=8):
        s = str(value)
        return (len(s) >= min_len and 
                re.search(r'[A-Z]', s) and 
                re.search(r'[a-z]', s) and 
                re.search(r'\d', s) and 
                re.search(r'[!@#$%^&*(),.?":{}|<>]', s))
    
    # UUID validator
    @staticmethod
    def is_uuid(value):
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        return bool(re.match(pattern, str(value).lower()))
    
    # JSON validator
    @staticmethod
    def is_json(value):
        import json
        try:
            json.loads(str(value))
            return True
        except:
            return False
    
    # Base64 validator
    @staticmethod
    def is_base64(value):
        import base64
        try:
            encoded = str(value)
            if len(encoded) % 4 != 0:
                return False
            base64.b64decode(encoded, validate=True)
            return True
        except:
            return False
    
    # Hex color validator
    @staticmethod
    def is_hex_color(value):
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, str(value)))
    
    # File extension validator
    @staticmethod
    def has_extension(value, extensions):
        if isinstance(extensions, str):
            extensions = [extensions]
        return any(str(value).lower().endswith(f'.{ext.lower()}') for ext in extensions)
    
    # ---- COLLECTION VALIDATORS ----
    @staticmethod
    def is_in(value, collection): return value in collection
    
    @staticmethod
    def not_in(value, collection): return value not in collection
    
    @staticmethod
    def is_in_list(value, lst): return isinstance(lst, list) and value in lst
    
    @staticmethod
    def is_in_array(value, arr): return hasattr(arr, '__iter__') and value in arr
    
    @staticmethod
    def all_in_list(values, lst): return isinstance(lst, list) and all(v in lst for v in values)
    
    @staticmethod
    def any_in_list(values, lst): return isinstance(lst, list) and any(v in lst for v in values)
    
    @staticmethod
    def none_in_list(values, lst): return isinstance(lst, list) and not any(v in lst for v in values)