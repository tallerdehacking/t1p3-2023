# Steps to create
1. Create file .env
1. Generate key pair with

```bash
openssl genrsa -3 > pk.key
openssl rsa -in pk.key -pubout
```
1. Populate `FLAG`, `PUBLIC_KEY` and `PRIVATE_KEY`