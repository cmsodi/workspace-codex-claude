# Directory condivisa di Claude e Codex

`.claude/` è la collocazione fisica canonica delle skill e degli eventuali
componenti condivisi. Questa rimane la fonte canonica anche quando una skill
viene creata o aggiornata da Codex.

Codex scopre le skill attraverso entrypoint locali generati sotto
`.agents/skills/`. Non modificarli a mano: dopo una variazione alle skill
canoniche esegui `$genera-entrypoint-codex` oppure lo script indicato nel
`README.md` della radice.

I moduli presenti in `moduli-opzionali/` non sono attivi finché non vengono
copiati qui.

Il modello include `verifica-workspace`: quando l'utente chiede di controllare
o diagnosticare la configurazione, la skill verifica il nucleo, l'allineamento
degli entrypoint Codex e l'eventuale modulo di scrittura senza richiedere
comandi manuali.
