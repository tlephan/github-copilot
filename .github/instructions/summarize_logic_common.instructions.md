````instructions
---
applyTo: "**/*.ts, **/*.js"
---

# Common Instructions for Summarize Logic

## Overview
These instructions provide a standardized approach for summarizing code logic, functions, classes, and systems. Use these guidelines to ensure consistent, clear, and comprehensive summaries.

## Core Principles

### 1. Structure and Organization
- Start with a high-level overview
- Break down complex logic into digestible sections
- Use hierarchical organization (main → sub-components → details)
- Maintain logical flow from general to specific

### 2. Clarity and Conciseness
- Use clear, non-technical language when possible
- Define technical terms when first introduced
- Keep sentences concise but complete
- Avoid unnecessary jargon or overly complex explanations

### 3. Completeness
- Cover all major functionality and logic paths
- Include error handling and edge cases
- Mention important dependencies and relationships
- Note any assumptions or limitations

## Summarization Framework

### For Functions/Methods
1. **Purpose**: What does this function do?
2. **Parameters**: What inputs does it accept?
3. **Process**: How does it accomplish its task?
4. **Output**: What does it return or produce?
5. **Side Effects**: Any external changes or dependencies?
6. **Edge Cases**: How does it handle unusual inputs or errors?

### For Classes
1. **Responsibility**: What is the class's main purpose?
2. **Key Properties**: Important attributes and their roles
3. **Main Methods**: Core functionality and public interface
4. **Relationships**: How it interacts with other classes
5. **Usage Pattern**: Typical instantiation and usage flow

### For Systems/Modules
1. **Architecture**: Overall structure and components
2. **Data Flow**: How information moves through the system
3. **Key Interactions**: Important communication between parts
4. **External Dependencies**: Third-party libraries or services
5. **Configuration**: Important setup or configuration requirements

## Language and Style Guidelines

### Use Active Voice
- ✅ "The function validates user input"
- ❌ "User input is validated by the function"

### Be Specific About Actions
- ✅ "Converts timestamps to ISO format"
- ❌ "Handles timestamps"

### Include Context When Relevant
- ✅ "Caches results to improve performance on repeated calls"
- ❌ "Caches results"

### Quantify When Possible
- ✅ "Processes up to 1000 records per batch"
- ❌ "Processes records in batches"

## Common Patterns to Address

### Error Handling
- How errors are detected and reported
- What happens when invalid input is received
- Recovery mechanisms or fallback behavior

### Performance Considerations
- Time complexity for algorithms
- Memory usage patterns
- Optimization techniques employed

### Security Aspects
- Input validation and sanitization
- Authentication and authorization checks
- Data protection measures

### Scalability Features
- How the code handles increasing load
- Bottlenecks and their mitigation
- Resource management strategies

## Template Structure

```markdown
## Summary
Brief one-paragraph overview of the main functionality.

## Key Components
- **Component 1**: Description of role and responsibility
- **Component 2**: Description of role and responsibility

## Process Flow
1. Step-by-step breakdown of the main logic
2. Important decision points or branching
3. Final output or result

## Important Details
- Notable implementation choices
- Performance characteristics
- Error handling approach
- Dependencies or requirements

## Usage Example
Brief example of how this would typically be used or called.
```

## Quality Checklist

Before finalizing a summary, verify:
- [ ] Main purpose is clearly stated
- [ ] Key logic flows are explained
- [ ] Important edge cases are covered
- [ ] Technical terms are defined or explained
- [ ] Code dependencies are mentioned
- [ ] Performance implications are noted (if relevant)
- [ ] Security considerations are addressed (if applicable)
- [ ] The summary is accessible to the intended audience

## Audience Considerations

### For Technical Teams
- Include implementation details
- Mention design patterns and architectural decisions
- Cover performance and scalability aspects
- Reference relevant documentation or standards

### For Non-Technical Stakeholders
- Focus on business logic and outcomes
- Minimize technical jargon
- Emphasize user-facing functionality
- Highlight business value and impact

### For Code Reviews
- Emphasize maintainability aspects
- Point out potential improvements
- Highlight complex or risky sections
- Suggest testing strategies

## Examples of Good Summary Elements

### Opening Statements
- "This module provides a centralized authentication system that..."
- "The UserService class manages all user-related operations including..."
- "This algorithm efficiently sorts large datasets by..."

### Process Descriptions
- "First, the input is validated against the schema, then..."
- "The system attempts to fetch from cache, falling back to database if needed"
- "Using a binary search approach, it locates the target element..."

### Conclusion Statements
- "The result is a validated user object ready for database insertion"
- "This approach ensures O(log n) lookup time while maintaining data integrity"
- "The module exposes a clean API that abstracts the underlying complexity"

## Anti-Patterns to Avoid

### Don't Just List Code
- ❌ "Line 5 creates a variable, line 6 calls a function..."
- ✅ "The function initializes user preferences and validates permissions..."

### Avoid Obvious Statements
- ❌ "This function has parameters and returns a value"
- ✅ "This function transforms user input into a standardized format"

### Don't Ignore Context
- ❌ "Loops through an array"
- ✅ "Iterates through user permissions to check access rights"

### Avoid Technical Depth Without Purpose
- ❌ "Uses a HashMap with SHA-256 hashing and linear probing collision resolution"
- ✅ "Uses an efficient lookup table to quickly match user credentials"
