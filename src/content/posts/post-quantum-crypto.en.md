---
lang: en
title: "A Beginner's Guide to Post-Quantum Cryptography: Will Quantum Computers Break HTTPS?"
date: 2025-07-30T10:00:00+08:00
categories: ['Technology']
description: "Learn about the threat quantum computing poses to existing encryption systems, and the NIST-standardized post-quantum cryptographic algorithms."
---

Quantum computers are still far from practical use, but the transition of encryption algorithms has already begun.

## Why Quantum Computers Threaten Encryption

Today's HTTPS relies on two types of encryption:

- Symmetric encryption (AES): Quantum computers using Grover's algorithm can reduce the cracking time from 2^128 to 2^64. The solution is to extend the key length to 256 bits.
- Asymmetric encryption (RSA/ECC): Shor's algorithm on quantum computers can break these in polynomial time. This is fatal—the entire foundation of current public-key systems is invalidated.

## Post-Quantum Cryptography (PQC)

NIST has already standardized three families of algorithms in 2024:

- CRYSTALS-Kyber: Public-key encryption/key exchange
- CRYSTALS-Dilithium: Digital signatures
- SPHINCS+: Digital signatures (backup option)

These algorithms are based on lattice mathematics problems, which quantum computers cannot efficiently solve.

## Timeline

- 2024: NIST standards released
- 2025-2026: Mainstream browsers and operating systems begin support
- 2028-2030: Enterprise-level migration
- 2030+: Full transition to post-quantum encryption

## What Developers Need to Do

There's nothing urgent to do right now. But you can keep an eye on:
- PQC support progress in OpenSSL and BoringSSL
- Updates to cloud providers' key management services
- Avoid hardcoding encryption algorithms in code—switch them via configuration

This isn't an urgent issue, but all encryption systems need to complete migration within a decade.

---

**References:**

- [NIST — Post-Quantum Cryptography Standards](https://www.nist.gov/pqcrypto)