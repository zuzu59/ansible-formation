# Ansible formation

zf220329.1520

Petit dépôt pour démarrer une formation Ansible qui utilise ansible-suitecase.

J'ai pris comme *source* le dépôt:

https://github.com/epfl-si/catalyse-iam.ops

Et après, je l'ai *tordu* pour le rendre générique à la formation. Donc il va sûrement rester des *trace* du dépôt original qui n'auront rien à voir avec CE dépôt !




Tout ce qui suit apartient au dépôt *original source*





# `cataiamsible`

This is the “Ops” wrapper script around [Ansible]() for the [Catalyse ERM reverse proxy](), the Catalyse Satosa middleware, and other IAM-related properties for the Catalyse ecosystem.

## Roles

### `roles/erm-proxy`

A reverse-proxy built out of Apache and mod_auth_tequila, that protects Jaggaer Enterprise Reagent Manager (ERM).

### `roles/satosa`

An instance of [SATOSA](https://github.com/IdentityPython/SATOSA) to auto-reactivate Catalyse-Buyer accounts as people log in either for the first time, or after a 6-month period of inactivity.

Commande to deploy SATOSA :
	
	./cataiamsible [--prod] -t sativa
