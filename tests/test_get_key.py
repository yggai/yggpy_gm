import re
import yggpy_gm as gggm

def test_get_key_shapes_and_formats():
    sk, pk = gggm.getKey()
    assert isinstance(sk, str) and isinstance(pk, str)
    assert re.fullmatch(r"[0-9a-f]{64}", sk), sk
    assert pk.startswith("04") and len(pk) == 130 and re.fullmatch(r"04[0-9a-f]{128}", pk), pk

