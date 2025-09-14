# Prompt vs Instruction - What is the difference?

## Overview

When working with AI tools like GitHub Copilot, Claude, ChatGPT, or other language models, understanding the distinction between **prompts** and **instructions** is crucial for effective AI-assisted development.

## Definitions

### Prompt

A **prompt** is a specific, contextual request or query that you give to an AI tool to generate an immediate response or complete a specific task. It's typically:

- **Conversational**: Written in natural language
- **Task-specific**: Focuses on a particular problem or request
- **Contextual**: Relates to the current situation or code you're working on
- **Immediate**: Expects an instant response or action

### Instruction

An **instruction** is a persistent rule, guideline, or behavioral directive that tells the AI how to operate across multiple interactions. It's typically:

- **Systematic**: Defines consistent behavior patterns
- **Persistent**: Applies across multiple sessions or interactions
- **Procedural**: Describes how to approach tasks rather than what task to do
- **Strategic**: Sets long-term operational guidelines

## Key Differences

| Aspect | Prompt | Instruction |
|--------|--------|-------------|
| **Duration** | One-time, immediate | Persistent, ongoing |
| **Scope** | Specific task or question | General behavior guidelines |
| **Format** | Natural language query | Structured rules/guidelines |
| **Purpose** | Get specific output | Shape AI behavior |
| **Context** | Current situation | Overall workflow |
| **Flexibility** | Highly specific | Broadly applicable |

## Examples in GitHub Copilot Context

### Prompts (What you ask for)

```javascript
// Generate a function to validate email addresses
// Create a REST API endpoint for user authentication
// Fix this bug in the payment processing logic
// Refactor this code to use async/await
// Add error handling to this database query
```

### Instructions (How it should behave)

```markdown
# GitHub Copilot Instructions

## Code Style Guidelines
- Always use TypeScript for new JavaScript files
- Follow clean architecture principles
- Include comprehensive error handling
- Write self-documenting code with clear variable names
- Add JSDoc comments for all public functions

## Security Guidelines
- Never hardcode API keys or secrets
- Always validate user inputs
- Use parameterized queries for database operations
- Implement proper authentication checks

## Testing Guidelines
- Write unit tests for all business logic
- Include integration tests for API endpoints
- Use meaningful test descriptions
- Follow AAA pattern (Arrange, Act, Assert)
```

## Practical Applications

### Using Prompts Effectively

1. **Be Specific**: Instead of "fix this code," say "fix the null pointer exception in the user validation function"
2. **Provide Context**: Include relevant code snippets or error messages
3. **Set Expectations**: Specify the desired output format or approach
4. **Iterate**: Refine prompts based on initial results

### Using Instructions Effectively

1. **Create Project-Specific Guidelines**: Define coding standards for your specific project
2. **Set Security Standards**: Establish consistent security practices
3. **Define Architecture Patterns**: Specify preferred design patterns and structures
4. **Establish Quality Gates**: Define testing and documentation requirements

## Best Practices

### For Prompts

1. **Context First**: Provide relevant background information
2. **Clear Intent**: State exactly what you want to achieve
3. **Examples Help**: Include sample inputs/outputs when helpful
4. **Iterate and Refine**: Adjust prompts based on results

### For Instructions

1. **Document Standards**: Create comprehensive coding guidelines
2. **Update Regularly**: Keep instructions current with project evolution
3. **Be Specific**: Avoid vague or ambiguous rules
4. **Include Examples**: Show concrete implementations of abstract concepts

## Conclusion

**Prompts** are your immediate requests - what you want the AI to do right now. **Instructions** are your long-term guidelines - how you want the AI to behave consistently across your entire project.

Effective AI-assisted development combines both:

- Use **instructions** to establish consistent coding standards and behaviors
- Use **prompts** to request specific implementations and solutions

This dual approach ensures that AI tools like GitHub Copilot not only help you solve immediate problems but do so in a way that's consistent with your project's overall architecture, security requirements, and coding standards.