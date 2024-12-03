import numpy as np


class MyMatrix:
    def __init__(self, data):
        self._data = np.array(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = np.array(new_data)

    def to_file(self, filename):
        np.savetxt(filename, self._data, fmt='%d')

    def __str__(self):
        return np.array2string(self._data)

    def __add__(self, other):
        return self.__class__(self._data + other.data)

    def __sub__(self, other):
        return self.__class__(self._data - other.data)

    def __mul__(self, other):
        return self.__class__(self._data * other.data)

    def __truediv__(self, other):
        return self.__class__(self._data / other.data)

    def __matmul__(self, other):
        return self.__class__(self._data @ other.data)

    def __pow__(self, power):
        return self.__class__(np.linalg.matrix_power(self._data, power))

    def __hash__(self):
        return int(np.sum(self._data))


class CustomMatrix(MyMatrix):
    def __init__(self, array):
        super().__init__(array)
        self._data = np.array(array)
        self._cache = {}
        self._hash = int(np.sum(self._data))

    def __hash__(self):
        return self._hash

    @property
    def array(self):
        return self._data

    @array.setter
    def array(self, value):
        self._data = np.array(value)


matrix_a = CustomMatrix(np.random.randint(0, 10, (3, 3)))
matrix_b = CustomMatrix(np.random.randint(0, 10, (3, 3)))

matrix_c_data = matrix_a.array.copy()
matrix_c_data[0, 0] += 5
matrix_c_data[1, 1] -= 5

matrix_c = CustomMatrix(matrix_c_data)

matrix_d = CustomMatrix(matrix_b.array.copy())

assert hash(matrix_a) == hash(matrix_c), "hash(A) hash(C) match"
assert not np.array_equal(matrix_a.array, matrix_c.array), "A != C"
assert np.array_equal(matrix_b.array, matrix_d.array), "B = D"
assert not np.array_equal((matrix_a @ matrix_b).array, (matrix_c @ matrix_d).array), (
    "A @ B <> C @ D "
)

matrix_a.to_file("A.txt")
matrix_b.to_file("B.txt")
matrix_c.to_file("C.txt")
matrix_d.to_file("D.txt")

result_ab = matrix_a @ matrix_b
result_cd = matrix_c @ matrix_d

result_ab.to_file("AB.txt")
result_cd.to_file("CD.txt")

with open("hash.txt", "w") as hash_file:
    hash_file.write(f"Hash of AB: {hash(result_ab)}\n")
    hash_file.write(f"Hash of CD: {hash(result_cd)}\n")
