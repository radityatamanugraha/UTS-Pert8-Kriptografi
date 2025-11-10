import numpy as np

MOD = 26

K = np.array([
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
])

def text_to_numbers(text):
    return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]

def numbers_to_text(nums):
    return ''.join(chr(int(n) % MOD + ord('A')) for n in nums)

def pad(nums, n):
    while len(nums) % n != 0:
        nums.append(ord('X') - ord('A'))
    return nums

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError(f"Tidak ada invers untuk {a} mod {m}")
    return x % m

def matrix_mod_inv(A, mod):
    det = int(round(np.linalg.det(A))) % mod
    inv_det = modinv(det, mod)

    cofactors = np.zeros(A.shape, dtype=int)
    for r in range(A.shape[0]):
        for c in range(A.shape[1]):
            minor = np.delete(np.delete(A, r, axis=0), c, axis=1)
            cofactors[r, c] = ((-1) ** (r + c)) * int(round(np.linalg.det(minor)))

    adjugate = cofactors.T % mod
    return (inv_det * adjugate) % mod

def encrypt(plaintext, K):
    n = K.shape[0]
    nums = text_to_numbers(plaintext)
    nums = pad(nums, n)
    cipher_nums = []

    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        res = (K.dot(block) % MOD)
        cipher_nums.extend(res.tolist())

    return numbers_to_text(cipher_nums)

def decrypt(ciphertext, K):
    n = K.shape[0]
    nums = text_to_numbers(ciphertext)
    Kinv = matrix_mod_inv(K, MOD)
    plain_nums = []

    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        res = (Kinv.dot(block) % MOD)
        plain_nums.extend(res.tolist())

    return numbers_to_text(plain_nums)

if __name__ == "__main__":
    username = "radityatama nugraha"
    password = "raditya"

    c_user = encrypt(username, K)
    c_pass = encrypt(password, K)

    print("=== HASIL ENKRIPSI ===")
    print("Plain username :", username)
    print("Cipher username:", c_user)
    print("Decrypt username:", decrypt(c_user, K))

    print("\nPlain password :", password)
    print("Cipher password:", c_pass)
    print("Decrypt password:", decrypt(c_pass, K))
