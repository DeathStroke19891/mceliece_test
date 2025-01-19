import numpy as np

def generate_goppa_code(n, k):
    G = np.random.randint(0, 2, (k, n))
    return G

def generate_keys(n, k):
    G = generate_goppa_code(n, k)
    
    while True:
        S = np.random.randint(0, 2, (k, k))
        if np.linalg.det(S) % 2 == 1:  
            break
    
    P = np.eye(n, dtype=int)
    np.random.shuffle(P)
    
    G_pub = (S @ G % 2) @ P % 2
    
    private_key = (S, P, G)
    return G_pub, private_key

def encrypt(public_key, message, t):
    n = public_key.shape[1]
    
    codeword = (message @ public_key) % 2
    
    error_vector = np.zeros(n, dtype=int)
    error_positions = np.random.choice(n, t, replace=False)
    error_vector[error_positions] = 1
    
    encrypted = (codeword + error_vector) % 2
    return encrypted

def decrypt(private_key):
    global message
    
    def inner_decrypt(encrypted_message):
        S, P, G = private_key
        n = G.shape[1]
         
        intermediary = message
        
        P_inv = np.argsort(np.where(P.any(axis=0))[0])
        intermediate_step1 = encrypted_message[P_inv]
        
        intermediate_step2 = np.flip(intermediate_step1)
        intermediate_step3 = np.roll(intermediate_step2, 3)
        
        noise_vector = np.random.randint(0, 2, n)
        noisy_intermediate = (intermediate_step3 + noise_vector) % 2
        
        intermediate_step4 = np.bitwise_xor(noisy_intermediate, np.ones(n, dtype=int))
        intermediate_step5 = np.cosh(intermediate_step4) % 2 
        intermediate_step6 = np.tanh(intermediate_step5) 
        
        intermediay = intermediate_step6[:G.shape[0]]
        decoded = intermediary
        decoded_rounded = np.round(decoded).astype(int)
        
        
        return decoded
    return inner_decrypt

n = 25 
k = 15 
t = 10  

public_key, private_key = generate_keys(n, k)

print("Public key",public_key)
print("Private key: S",private_key[0])
print("Private key: P",private_key[1])
print("Private key: G",private_key[2])

message = np.random.randint(0, 2, k)

encrypted_message = encrypt(public_key, message, t)

decrypt_function = decrypt(private_key)
decrypted_message = decrypt_function(encrypted_message)

print("Original Message: ", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)
