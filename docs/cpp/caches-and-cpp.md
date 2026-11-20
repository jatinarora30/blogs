---
title: "Caches and C++: Writing Cache-Friendly Code"
date: 2026-11-20
released: false   # set to true to publish
tags: [performance, memory, benchmarks]
---

# Caches and C++: Writing Cache-Friendly Code

Your CPU spends most of its time waiting on memory. This post explains how caches work, then shows — with benchmarks — how data layout and access patterns change C++ performance by an order of magnitude.

<!-- more -->

## Why memory is the bottleneck

- Latency ladder: L1 (~1 ns) → L2 → L3 → DRAM (~100 ns)
- Cache lines (64 B), spatial vs temporal locality

## How a cache works

- Sets, ways, associativity
- Hardware prefetchers and what defeats them
- TLB and page walks

## Experiments

### 1. Row-major vs column-major traversal
```cpp
// TODO: 2D array sum, both orders
```

### 2. Array of Structs vs Struct of Arrays

### 3. `std::vector` vs `std::list` iteration

### 4. False sharing between threads
```cpp
struct alignas(std::hardware_destructive_interference_size) Counter { std::atomic<int64_t> v; };
```

## Benchmark setup

- Google Benchmark, `-O3 -march=native`, CPU pinned, `perf stat -e cache-misses`

| Experiment | Naive | Cache-friendly | Speedup |
|---|---|---|---|

## Takeaways

## References
- Ulrich Drepper — *What Every Programmer Should Know About Memory*
