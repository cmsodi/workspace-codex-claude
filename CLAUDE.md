# Istruzioni per Claude Code

## Parte specifica di Claude Code

- Le skill locali condivise sono visibili in `.claude/skills/`.
- La loro collocazione fisica canonica è `.agents/skills/`.
- `.claude` è un collegamento simbolico alla directory fisica `.agents/`:
  non sostituirlo con una directory indipendente.
- Se viene attivato il modulo di scrittura, i plugin sono visibili in
  `.claude/scrittura-plugins/` e risiedono fisicamente in
  `.agents/scrittura-plugins/`.
- Nei file condivisi usa i percorsi canonici `.agents/...`.

## Parte comune

Prima di operare, leggi per intero `PROJECT_GUIDE.md` nella radice del
progetto e applicane le istruzioni.
