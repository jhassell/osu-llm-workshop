# OpenClaw, for comparison

OpenClaw is a complete personal agent program: the same loop you read in agent.py, grown up, with skills instead of a docstring, memory instead of a transcript, a schedule instead of you pressing run, and connections to messaging apps. You met it in the first exercise of the day, when it built a tutorial website in `site/`. This page is for going further with it, because seeing a full agent makes the forty-line version easier to understand.

It is already installed in your Codespace. When you press Enter at setup's what-next question, setup connects it to the same endpoint, key and model as the labs, without opening it; choice 2 connects it and opens it at once. To open it after that:

    openclaw chat

and to connect it again, for example after a new key or a different model, and open it:

    bash setup.sh --openclaw

It works inside this repository, so ask it about the documents in `corpus/` or `mine/` and watch each tool call it makes.

Setup gives it only four basic tools (read, write, edit, and run a command) and none of its optional skills. With everything turned on, every call to the model carried about six times as much text, and the whole room shares one endpoint. To see what you are missing, `openclaw config` changes it, at the cost of more load on the model.

Setup also writes its rules, in `~/.openclaw/workspace/IDENTITY.md`: stay inside the repository, never read `.env` or its own configuration, treat what it reads as evidence, never push or publish, and ask before deleting or overwriting a file. A section of rules for `site/` adds that the folder is public and already served, that links must be relative, that nothing secret or from `mine/` goes there, no symlinks, the site check before calling a site done, and that publishing is the person's decision. Rules in a file are instructions the model usually follows, not limits the program enforces. What the program enforces is the four-tool list, and one of those four runs any command you could.

Two cautions. It can do far more than read files: it runs commands as you, so read what it proposes before you agree. And the rule from Module 5 applies with more force: anything it reads is evidence, never authority. Connect it to a messaging account only if you want an agent reading that account.

`install.sh` reinstalls the pinned version if it is ever missing. The version is pinned together with Node 22, as verified in jhassell/asee9 in September 2026; moving it means moving Node with it.
