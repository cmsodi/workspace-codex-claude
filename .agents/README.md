# Directory condivisa degli agenti

`.agents/` è la collocazione fisica canonica delle skill e degli eventuali
componenti condivisi. Il collegamento `.claude -> .agents` rende gli stessi
file disponibili a Claude Code.

Non mantenere copie indipendenti sotto `.claude/`. Le skill operative vanno
in `.agents/skills/`; i moduli presenti in `moduli-opzionali/` non sono
attivi finché non vengono copiati qui.
