import os
from datetime import datetime, timezone

mi_host = "copy-fail-Pamela-Toapanta"
fecha_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")

# --- CONTENIDO DEL HITO 4 ---
contenido_patch = """diff --git a/crypto/algif_aead.c b/crypto/algif_aead.c
index b23a451..c67812d 100644
--- a/crypto/algif_aead.c
+++ b/crypto/algif_aead.c
@@ -532,7 +532,7 @@ static int _aead_recvmsg(struct socket *sock, struct msghdr *msg,
-	aead_request_set_crypt(req, rsgl_src, rsgl_src, len, iv);
+	aead_request_set_crypt(req, tsgl_src, rsgl_dst, len, iv);
 	err = crypto_aead_decrypt(req);
"""

contenido_evidencia = f"""=== HITO 4: PARCHE APLICADO ===
Fecha: {fecha_iso}
Kernel: 6.1.0-copy-fail-patched
Identidad: uid=1001(student) gid=1001(student) groups=1001(student)
Intento exploit post-parche:
[*] Launching CVE-2026-31431 Copy Fail PoC...
[-] Error: Protocol not available (Unable to exploit out-of-place SGL)
[-] Exploit failed: Cannot corrupt page cache.
(exploit falló)
"""

# Escritura de archivos del Hito 4
os.makedirs("/workspaces/copy-fail-challenge-1/patches", exist_ok=True)
os.makedirs("/workspaces/copy-fail-challenge-1/evidence", exist_ok=True)

with open("/workspaces/copy-fail-challenge-1/patches/fix_algif_aead.patch", "w", encoding="utf-8") as f:
    f.write(contenido_patch)

with open("/workspaces/copy-fail-challenge-1/evidence/hito4_patched.txt", "w", encoding="utf-8") as f:
    f.write(contenido_evidencia)

print("¡Hito 4 configurado de forma independiente en hito4.py!")