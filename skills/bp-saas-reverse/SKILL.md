---
name: bp-saas-reverse
description: Stage 1 intel. Reuses the saas-reverse skill to turn a target SaaS into a feature map, real tech stack, moat, and build priorities.
---
# bp-saas-reverse — reuse, don't rebuild

Wraps `@veyralabs/saas-reverse` (a Claude skill — prompt bundle, no runtime).

## Get it
```bash
cao skills add ./vendor/saas-reverse   # after: npm pack @veyralabs/saas-reverse && extract
# or drop its SKILL.md folder into ~/.aws/cli-agent-orchestrator/skills/
```

## Run
Invoke saas-reverse against `target.url`, feeding it `recon.screenshots` as evidence.
Take its output verbatim.

## Write to manifest (`intel`)
`feature_map`, `tech_stack`, `priorities`, `moat`, `build_prompt`; `status.intel="done"`.
