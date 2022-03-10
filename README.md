# `cataiamsible`

This is the “Ops” wrapper script around [Ansible]() for the [Catalyse ERM reverse proxy](), the Catalyse Satosa middleware, and other IAM-related properties for the Catalyse ecosystem.

## Roles

### `roles/erm-proxy`

A reverse-proxy built out of Apache and mod_auth_tequila, that protects Jaggaer Enterprise Reagent Manager (ERM).

### `roles/satosa`

An instance of [SATOSA](https://github.com/IdentityPython/SATOSA) to auto-reactivate Catalyse-Buyer accounts as people log in either for the first time, or after a 6-month period of inactivity.
