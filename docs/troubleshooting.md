# Troubleshooting

## Conexão com Postgres falhou
- O serviço `db` está de pé? Porta `5432` livre?
- `DATABASE_URL` correto? Tente: `psql <connstring>`

## `role ... does not exist`
- Crie role/usuário e permissões (ver **Perfis de acesso**).

## `relation ... does not exist`
- Execute o seed: `psql -d processos -f sql/init.sql`

## `uv` não encontrado
- Instale com `pipx install uv` ou gerenciador do seu OS.

## `Address already in use`
- A porta `8000` já está ocupada. Pare o processo antigo ou use `--port 8001`.
