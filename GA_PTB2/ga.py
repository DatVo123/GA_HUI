from bitarray import bitarray

def integer_to_bit_array(n):
    # Tạo đối tượng bitarray
    ba = bitarray()
    # Chuyển đổi số nguyên thành chuỗi nhị phân và thêm vào bitarray
    ba.frombytes(n.to_bytes((n.bit_length()), byteorder='big'))
    # Loại bỏ các bit thừa ở phía đầu
    ba = ba[-n.bit_length():]
    return ba

n = 23
bit_array = integer_to_bit_array(n)
print("Số nguyên:", n)
print("Mảng bit:", bit_array)
print("Dạng list:", bit_array.tolist())
