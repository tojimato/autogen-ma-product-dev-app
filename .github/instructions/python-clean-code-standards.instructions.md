---
applyTo: "**"
---
# Python Clean Code Standards & Architecture Principles

**A Comprehensive Guide for Senior Engineers & Development Teams**

---

## Overview

This document establishes baseline clean code standards for professional Python development. These principles apply to all projects and should guide code generation, reviews, and architectural decisions.

**Core Values**: Maintainability > Clever Code | Clarity > Conciseness | Testability > Performance (unless profiled)

---

## 1. DRY (Don't Repeat Yourself)

### Principle
Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

### Rules & Guidelines

#### Extract Repeated Logic into Helper Methods
- **Identify**: Code blocks appearing 2+ times → Extract to method
- **Scope**: Extract at the method level first; promote to class/module level if needed across multiple classes
- **Naming**: Use descriptive names that explain the transformation (`extract_summary()` not `proc()`)
- **Testing**: Helper methods must be independently testable

#### Consolidate Configuration & Magic Numbers
- **Definition**: Any number or string appearing in code that could change → Named constant
- **Location**: Class-level constants at the top (Python convention)
- **Naming**: UPPERCASE_WITH_UNDERSCORES for module/class-level constants
- **Documentation**: Include inline comment explaining the constant's purpose/impact
- **Example**: `MAX_RETRIES = 3  # Max API retry attempts before circuit break`

#### Extract Keyword Collections & Data Structures
- **Reusability**: Shared keyword lists, enums, mappings → Class/module level
- **Discoverability**: Centralize related constants to one location for easier updates
- **Testability**: Allows unit testing without embedding test data in methods

#### Create Wrapper Methods for Repeated API Calls
- **Pattern**: Same external service called with minor variations → Single wrapper
- **Responsibility**: Wrapper handles authentication, error handling, logging
- **Flexibility**: Accept parameters for variation, keep boilerplate in wrapper
- **Example**: One `_run_llm_stage()` method instead of duplicating API calls across pipeline stages

#### Use Generators & Comprehensions Wisely
- **Generators**: Use for large sequences (memory-efficient iteration)
- **Comprehensions**: Use for simple transformations; extract to methods if complex
- **Rule**: One condition/operation per comprehension; beyond that → explicit loop

#### Avoid Copy-Paste Conditional Logic
- **Red Flag**: Same `if/elif/else` pattern repeated → Extract to boolean method
- **Naming**: Predicates should answer a yes/no question (`_should_skip()`, `_is_valid()`)
- **Complexity**: If condition takes 5+ lines to express → Extract immediately

#### DRY Applies to Tests
- **Test Fixtures**: Reuse setup code across test classes (don't duplicate test data)
- **Test Helpers**: Extract common assertions or object creation to utility functions
- **Parametrization**: Use `pytest.mark.parametrize` instead of copy-pasted test cases

---

## 2. KISS (Keep It Simple, Stupid)

### Principle
The simplest solution is usually the best. Avoid unnecessary complexity; optimize for readability first.

### Rules & Guidelines

#### Decompose Functions into Smaller Units
- **Target**: Each method < 30 lines of code
- **Red Flag**: If you can't explain the method in 1-2 sentences → Too broad
- **Strategy**: Extract helpers with clear names instead of dense logic
- **Benefit**: Easier to test, debug, and reason about independently

#### Use Early Returns & Guard Clauses
- **Pattern**: Check preconditions first; return early if unmet
- **Benefit**: Reduces nesting depth (max 3 levels)
- **Readability**: Happy path becomes main flow, not buried in nested blocks

#### Avoid Deep Nesting
- **Max Levels**: 3 levels of indentation maximum
- **Refactoring**: Extract inner loops/conditions to separate methods
- **Trade-off**: Slightly more methods beats reduced readability from nesting

#### Name Variables & Methods to Be Self-Documenting
- **Abbrevations**: Never use (except standard loop vars: `i`, `j`, `k`)
- **Length**: Longer names are fine if they clarify intent
- **Examples**: `feed_entries` not `d`, `relevance_score` not `x`
- **Boolean Names**: Prefix with `is_`, `has_`, `should_`, `can_` to make intent clear

#### Use Explicit Loops Over Complex Comprehensions
- **Rule**: If comprehension has multiple conditions or transformations → Use explicit loop
- **Clarity**: `for x in items if condition1 if condition2` is hard to read
- **Readability**: 5-line loop is clearer than dense one-liner

#### Minimize Conditional Branches
- **Polymorphism**: Use inheritance or composition instead of large switch statements
- **Strategy Pattern**: Different strategies per condition instead of one method with many branches
- **Guard Clauses**: Handle exceptions early, don't nest the main logic

# ... (truncated for brevity, full content copied from original file) ...
