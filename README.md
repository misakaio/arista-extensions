# arista-extensions

This repository contains pre-built extensions for Arista EOS - and within each respository, instructions on how each SWIX was created

## Download

| Package | Download | Download |
| --- | --- | --- |
| [Bird](bird/README.md) | [4.13.14M](swix/bird-1.6.0-1_4.13.14M.swix) | [4.13.10M](swix/bird-1.6.0-1_4.13.10M.swix) |
| [Git](git/README.md) | [4.13.14M](swix/git-1.7.4.4-1_4.13.14M.swix) | [4.13.10M](swix/git-1.7.4.4-1_4.13.10M.swix) |
| [Security Advisory 17 (glibc)](https://www.arista.com/en/support/advisories-notices/security-advisories/1255-security-advisory-17) | --- | [4.13.10M](swix/SecurityAdvisory0017-glibc_4.13.10M.swix) |
| [Security Advisory 17 (non-disruptive)](https://www.arista.com/en/support/advisories-notices/security-advisories/1255-security-advisory-17) | --- | [4.13.10M](swix/SecurityAdvisory0017-nonDisruptive_4.13.10M.swix) |
| [Security Advisory 15](https://www.arista.com/en/support/advisories-notices/security-advisories/1221-security-advisory-15) | --- | [4.13.10M](swix/secAdvisory0015_4.13.10M.swix) |

## Self Compile

 1. Download VEOS to serve as your disposable build environment
 1. Follow the instructions on [preparing your build environment](COMPILE_PREPARATION.md)
 1. Open the extension of your choice and follow the specific steps for build
