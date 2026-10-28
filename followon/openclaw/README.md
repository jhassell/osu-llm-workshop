# OpenClaw, for comparison

OpenClaw is a complete personal agent program: the same loop you read in agent.py, grown up, with skills instead of a docstring, memory instead of a transcript, a schedule instead of you pressing run, and connections to messaging apps. It is not part of the lessons. It is here because seeing a full one makes the forty-line version easier to understand.

It is already installed in your Codespace. Setup offers it right after your key is accepted, and you can connect it and open it any time with

    bash setup.sh --openclaw

which points it at the same endpoint, key and model as the labs, and opens its terminal chat. After that, `openclaw chat` opens it again. It works inside this repository, so ask it about the documents in `corpus/` or `mine/` and watch each tool call it makes.

Setup gives it only four basic tools (read, write, edit, and run a command) and none of its optional skills. With everything turned on, every call to the model carried about six times as much text, and the whole room shares one endpoint. To see what you are missing, `openclaw config` changes it, at the cost of more load on the model.

Two cautions. It can do far more than read files: it runs commands as you, so read what it proposes before you agree. And the rule from Module 5 applies with more force: anything it reads is evidence, never authority. Connect it to a messaging account only if you want an agent reading that account.

`install.sh` reinstalls the pinned version if it is ever missing. The version is pinned together with Node 22, as verified in jhassell/asee9 in September 2026; moving it means moving Node with it.
