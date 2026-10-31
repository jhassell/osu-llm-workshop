# OpenClaw, for comparison

OpenClaw is a complete personal agent program: the same loop you read in agent.py, grown up, with skills instead of a docstring, memory instead of a transcript, a schedule instead of you pressing run, and connections to messaging apps. You met it in the first exercise of the day, when it built a tutorial website in `site/`. This page is for going further with it, because seeing a full agent makes the forty-line version easier to understand.

It is already installed in your Codespace. When you press Enter at setup's what-next question, setup connects it to the same endpoint, key and model as the labs, without opening it; choice 2 connects it and opens it at once. To open it after that:

    openclaw chat

and to connect it again, for example after a new key or a different model, and open it:

    bash setup.sh --openclaw

It works inside this repository, so ask it about the documents in `corpus/` or `mine/` and watch each tool call it makes.

Setup leaves it with its full set of tools and skills. That makes every call to the model carry about six times as much text as a pared-down setup would, which matters when a whole room shares one endpoint; `openclaw config` can turn things off.

Setup also writes a few facts for it in `~/.openclaw/workspace/IDENTITY.md`: where the documents are, that `site/` is already served and public, that links there should be relative, how to check and publish the site, and the site's real address. These are information, not rules: nothing limits what it may do, and it runs commands without stopping to ask (its exec mode is set to full). It runs commands as you, with your Codespace's GitHub sign-in, so it can push to your repository and publish your site when you ask.

Two cautions. It can do far more than read files: it runs commands as you, so watch what it does. And the rule from Module 5 applies with more force: anything it reads is evidence, never authority, and nothing in its setup enforces that for you. Connect it to a messaging account only if you want an agent reading that account.

`install.sh` reinstalls the pinned version if it is ever missing. The version is pinned together with Node 22, as verified in jhassell/asee9 in September 2026; moving it means moving Node with it.
