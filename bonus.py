import os

# --- CONTENIDO DEL BONUS: REPORT.MD (Más de 300 palabras en inglés) ---
contenido_reporte = """# Technical Analysis Report: CVE-2026-31431 "Copy Fail"
**Student:** Pamela Toapanta  
**Course:** Introduction to UNIX - UIDE  

## 1. Root Bug and Vulnerable Function
The root cause of CVE-2026-31431 resides in the Linux kernel's cryptographic subsystem, specifically within the `crypto/algif_aead.c` file inside the `_aead_recvmsg()` function. In 2017, an optimization was introduced to process data "in-place" using `sg_chain()` to append the destination buffers directly to the source scatterlist. This configuration caused `req->src` to equal `req->dst`, breaking the isolation between data read operations and network sockets memory spaces.

## 2. Danger of Destination Buffer Writing
Writing directly to `dst[assoclen + cryptlen]` is extremely dangerous because, under an "in-place" execution layout, the memory mappings overlap. Instead of modifying an isolated user-space pointer, the operations point straight into a scatterlist tracking the operating system's internal structures. An unprivileged user can misuse the `splice()` system call to pass a read-only file descriptor into an AF_ALG socket, coercing the kernel into interpreting critical file pages as destination target buffers.

## 3. Stealth Nature of the Exploit
The exploit is highly stealthy because it bypasses standard storage layers completely. When writing the 4 controlled bytes, the payload targets the Page Cache, which is the system's volatile memory representation of files. Binaries like `/usr/bin/su` are loaded into memory; by altering their memory pages without synchronizing changes back to the actual disk blocks, no integrity monitoring tool tracks physical file changes, leaving zero conventional filesystem footprints.

## 4. Connection to Core UNIX Concepts
This vulnerability directly interacts with key concepts studied in class:
* **Page Cache:** The exploit operates exclusively here, demonstrating how UNIX treats files as memory-mapped segments.
* **Setuid Bit:** The target binary `/usr/bin/su` has the setuid privilege bit enabled, meaning it executes with root permissions regardless of who calls it. By corrupting its memory image, the execution path transfers root control to the caller.
* **Inodes:** Since the physical inode data remains intact, the modification is transient and strictly resides in RAM.

## 5. Security Engineering Lesson
The biggest takeaway from Copy Fail is that chaining multiple individually "reasonable" or optimized performance modifications can lead to catastrophic logical flaws. Performance choices should never override absolute memory isolation boundaries.
"""

# Escritura exclusiva del reporte técnico
with open("/workspaces/copy-fail-challenge-1/REPORT.md", "w", encoding="utf-8") as f:
    f.write(contenido_reporte)

print("Reporte Técnico de Bonus")