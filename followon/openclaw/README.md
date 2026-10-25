# OpenClaw, for comparison

OpenClaw is a complete personal agent program: the same loop you read in agent.py, grown up, with skills instead of a docstring, memory instead of a transcript, a schedule instead of you pressing run, and connections to messaging apps. It is not part of the workshop. It is here because seeing a full one makes the forty-line version easier to understand, and because the container already has Node for it.

    bash followon/openclaw/install.sh

installs a pinned version in about a minute and prints how to point it at the same endpoint the labs use. Two cautions. It can do far more than read files, so read what a skill does before you enable it, and the rule from Module 5 applies with more force: anything it reads is evidence, never authority. And connect it to a messaging account only if you want an agent reading that account.

The install is pinned to the version verified in jhassell/asee9 in September 2026. Moving it means moving the Node version with it.
