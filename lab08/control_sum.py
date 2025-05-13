def calc_sum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b'\x00'

    res = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) | data[i + 1]
        res += word

    return res & 0xFFFF


def calc_control_sum(data: bytes) -> int:
    return calc_sum(data) ^ 0xFFFF


def verify_control_sum(data: bytes, control_sum: int) -> bool:
    total = calc_sum(data) + control_sum
    total = total & 0xFFFF
    return total == 0xFFFF


if __name__ == "__main__":
    assert verify_control_sum(b'', 0xFFFF)
    print("Test 1 passed")

    correct_bytes = b'\xAB\xCD'
    correct_control_sum = 0x5432

    incorrect_bytes = correct_bytes + b'\x01'

    assert verify_control_sum(correct_bytes, correct_control_sum)
    print("Test 2 passed")

    assert not verify_control_sum(incorrect_bytes, correct_control_sum)
    print("Test 3 passed")
