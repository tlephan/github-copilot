# GitHub Copilot Playbook - AI Agent Instructions

## Project Overview
This repository serves as a comprehensive knowledge base and playbook for GitHub Copilot, containing curated instructions, prompts, and best practices for AI-powered development workflows.

## Repository Structure & Organization

### Core Architecture
- **Root Level**: Main documentation (`github_copilot_playbook.md`) and overview (`README.md`)
- **`.github/instructions/`**: Reusable instruction templates for specific coding tasks
- **`.github/prompts/`**: Structured prompt templates following a standardized format
- **`.github/copilot-instructions.md`**: This file - repository-level AI agent guidance

### File Naming Conventions
- Instructions: `{task_name}.instructions.md` (e.g., `summarize_logic_common.instructions.md`)
- Prompts: `{task_name}.prompt.md` (e.g., `summarize_logic_common.prompt.md`)
- Use underscore separation and descriptive names

## Key Patterns & Conventions

### Instruction Files Structure
Instructions follow a YAML frontmatter pattern:
```yaml
---
applyTo: **/*.ts, **/*.js  # File patterns where instructions apply
---
```

Instructions are comprehensive, including:
- Core principles and framework
- Step-by-step guidelines
- Quality checklists
- Anti-patterns to avoid
- Audience-specific considerations

### Prompt Files Structure
Prompts use structured frontmatter:
```yaml
---
mode: agent                        # Execution context
model: Claude Sonnet 4 (copilot)   # Preferred AI model
description: Brief task summary     # What the prompt accomplishes
---
```

### Content Organization Principles
1. **Hierarchical Structure**: General → Specific → Examples
2. **Actionable Guidelines**: Concrete, executable instructions
3. **Context-Aware**: Include relevant technical and business context
4. **Quality-Focused**: Built-in validation and best practices

## Development Workflows

### Creating New Instructions
1. Follow the established frontmatter format with `applyTo` patterns
2. Include comprehensive frameworks covering all major aspects
3. Provide both positive examples and anti-patterns
4. Add quality checklists for self-validation

### Creating New Prompts  
1. Define clear mode, model preferences, and descriptions
2. Reference corresponding instruction files when available
3. Keep prompts concise but comprehensive enough for AI understanding

### File Organization
- Place instructions in `.github/instructions/` 
- Place prompts in `.github/prompts/`
- Maintain 1:1 correspondence between instruction and prompt files when applicable

## Integration Points

### Cross-Reference System
- Prompts reference instruction files: `Use the following instructions in /instructions/{filename}.md`
- Instructions can be applied to multiple file types via `applyTo` patterns
- Maintains separation of concerns: instructions define "how", prompts define "what"

### External Dependencies
- Leverages GitHub Copilot ecosystem and documentation
- References official GitHub Copilot resources and community practices
- No build dependencies - pure documentation repository

## Project-Specific Knowledge

### Target Audience
- AI coding agents and developers using GitHub Copilot
- Teams establishing AI-assisted development workflows  
- Contributors to GitHub Copilot knowledge and best practices

### Quality Standards
- Instructions must include frameworks, not just guidelines
- All content should be immediately actionable
- Examples should be specific to real-world scenarios
- Maintain audience-appropriate technical depth

### Content Validation
Use the quality checklist pattern found in instructions:
- [ ] Main purpose clearly stated
- [ ] Key processes explained step-by-step  
- [ ] Edge cases and error handling covered
- [ ] Technical terms defined appropriately
- [ ] Examples provided where helpful

When contributing, ensure new content follows the established structural patterns and maintains the repository's focus on practical, immediately-useful AI agent guidance.