# input is given as state matrix
def shiftrow(_matrix:list):
    output = _matrix.copy()
    output[1] = _matrix[5]
    output[5] = _matrix[9]
    output[9] = _matrix[13]
    output[13] = _matrix[1]
    output[2] = _matrix[10]
    output[6] = _matrix[14]
    output[10] = _matrix[2]
    output[14] = _matrix[6]
    output[3] = _matrix[15]
    output[7] = _matrix[3]
    output[11] = _matrix[7]
    output[15] = _matrix[11]
    return output

def mixcolumn(_matrix:list):
    output:list = _matrix.copy()
    def mul2mod(val:int):
        val = val << 1
        if val > 0xFF:
            val = val ^ 0b100011011
        return val
    def mul3mod(val:int):
        tmp = val
        val = val << 1
        val ^= tmp
        if val > 0xFF:
            val = val ^ 0b100011011
        return val
    arr = {0,4,8,12}
    for i in arr:
        output[i] = mul2mod(_matrix[i]) ^ mul3mod(_matrix[i+1]) ^ _matrix[i+2] ^ _matrix[i+3]
        output[i+1] = _matrix[i] ^ mul2mod(_matrix[i+1]) ^ mul3mod(_matrix[i+2]) ^ _matrix[i+3]
        output[i+2] = _matrix[i] ^ _matrix[i+1] ^ mul2mod(_matrix[i+2]) ^ mul3mod(_matrix[i+3])
        output[i+3] = mul3mod(_matrix[i]) ^ _matrix[i+1] ^ _matrix[i+2] ^ mul2mod(_matrix[i+3])
    return output
