---
title: "{{TITLE}}"
date: {{DATE}}
released: false   # true removes the Draft banner
pr: https://github.com/OWNER/REPO/pull/NUMBER   # the PR this page is about
status: open      # merged | open | draft | closed
tags: []
contributors: [jatinarora30]   # GitHub usernames
---

# {{TITLE}}

**One-paragraph summary:** which project, what was broken or missing, and what the PR changed. Someone who reads only this paragraph should know what you did.

| | |
|---|---|
| **Project** | [OWNER/REPO](https://github.com/OWNER/REPO) |
| **Issue** | [#123](https://github.com/OWNER/REPO/issues/123) |
| **Area** | e.g. executor, planner, build system |
| **Language** | e.g. C++17, Python |

## The project

What the project is, who uses it, and why you were in its codebase.

## The problem

What was wrong or missing, and how it showed up. Include the smallest way to reproduce it.

```bash title="Reproduce"
colcon build --packages-select my_pkg
ros2 run my_pkg my_node
```

```text title="Output"
[ERROR] something went wrong here
```

## Finding it

How you tracked down the cause: what you read, what you tried, what turned out to matter.

## The fix

What you changed and why that's the right fix. Show the key part of the diff, not all of it.

```cpp title="Before"
// old code
```

```cpp title="After"
// new code
```

## Testing

How you checked the fix works: tests added, benchmarks, before/after numbers.

| Case | Before | After |
|---|---|---|
| example | 12 ms | 3 ms |

## Review

What the maintainers asked for, what you changed because of it, and how long it took to merge.

## Takeaways

What you learned about the codebase, the community, or the problem.
