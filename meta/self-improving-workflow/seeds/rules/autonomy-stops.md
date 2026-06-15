# Irreversible operations — never execute autonomously

> Seeded by self-improving-workflow skill. **You may add entries; you may not remove seeded entries.**
> `guard.sh` enforces these via regex.

## Data loss
- `rm -rf` outside the working tree
- `git reset --hard` discarding uncommitted changes
- `git clean -fd`
- SQL `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE TABLE`

## Remote-irreversible
- `git push --force` / `git push -f` to any branch
- `git push --delete`
- `git branch -D` on shared branches
- `gh pr merge`
- `kubectl delete`
- `terraform apply` / `terraform destroy`

## Credentials
- Editing `.env`, `secrets/*`, `.npmrc`, `.pypirc` containing tokens
- `aws iam create/delete/update-access-key`
- Token rotation commands
- Any paid external API call

## Shared communications
- Slack/Discord/Teams webhooks
- `gh issue|pr comment|create|close`
- Email send (`mail`, `sendmail`, SMTP CLIs)

## Process / system
- `kill -9`, `pkill -9` of non-self-spawned processes
- `systemctl stop|disable|mask`
- `docker rm|kill|stop -f` of shared containers

## Project additions

<!-- append below; never remove anything above this line -->
