# Directory condivisa degli agenti

`.agents/` è la collocazione fisica canonica delle skill e degli eventuali
componenti condivisi. Il collegamento `.claude -> .agents` rende gli stessi
file disponibili a Claude Code.

Non mantenere copie indipendenti sotto `.claude/`. Le skill operative vanno
in `.agents/skills/`; i moduli presenti in `moduli-opzionali/` non sono
attivi finché non vengono copiati qui.

Il modello include `verifica-workspace`: quando l'utente chiede di controllare
o diagnosticare la configurazione, la skill verifica il nucleo, il collegamento
simbolico e l'eventuale modulo di scrittura senza richiedere comandi manuali.
