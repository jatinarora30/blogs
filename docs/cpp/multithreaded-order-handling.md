---
title: "Handling Running Orders Across Multiple Threads"
date: 2026-11-20
released: false   # set to true to publish
tags: [concurrency, design]
---

# Handling Running Orders Across Multiple Threads

Many systems keep a set of in-flight orders — tasks, commands, requests — that several threads create, update and cancel at once. This post compares designs for keeping that state correct and fast.

<!-- more -->

## The problem

- Orders created, updated, completed and cancelled from different threads
- Requirements: consistency, no lost updates, low latency

## Approaches

1. Single global mutex
2. Sharded locks by order ID
3. Single-writer actor + message queue
4. Lock-free / RCU-style snapshots

## Implementation

```cpp
// TODO
```

## Pitfalls

- ABA, use-after-free on cancel, ordering of state transitions

## Benchmarks

| Design | Throughput | p99 latency | Complexity |
|---|---|---|---|

## Takeaways

## References
