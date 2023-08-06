from streamer import DictStream, Stream


def test_dict_main():
    simple_dict = {k: k for k in range(10)}
    s1 = DictStream(simple_dict) \
        .map_keys(lambda k: chr(0x41 + k)) \
        .build_dict()
    assert s1 == {chr(0x41 + k): k for k in range(10)}

    s2 = DictStream(simple_dict) \
        .with_overrides({k: chr(0x41 + k) for k in range(15)}) \
        .build_dict()
    assert s2 == {k: chr(0x41 + k) for k in range(15)}

    s3 = DictStream(simple_dict) \
        .filter_values(lambda k: k % 2) \
        .build_dict()
    assert s3 == {k: k for k in range(1, 10, 2)}

    s4 = DictStream(simple_dict) \
        .map_key_values(lambda k: k + 1, lambda v: v ** 2) \
        .build_dict()
    assert s4 == {k + 1: k ** 2 for k in range(10)}


def test_to_dict_stream():
    s1 = DictStream(wrap=Stream("abcdefg").enumerate()) \
        .collect_dict()
    assert s1 == {i: ch for i, ch in enumerate("abcdefg")}