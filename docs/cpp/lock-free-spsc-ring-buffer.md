---
title: "Lock-Free Sensor Pipelines: An SPSC Ring Buffer"
date: 2026-11-20
released: false   # set to true to publish
tags: [concurrency, atomics, lock-free]
---

# Lock-Free Sensor Pipelines: An SPSC Ring Buffer

Sensor drivers produce, perception consumes — and a mutex in between costs latency and jitter. We build a single-producer/single-consumer ring buffer with atomics and benchmark it against a mutex queue.

<!-- more -->

## The problem: sensor → consumer handoff

## Baseline: `std::mutex` + `std::queue`

## Design of the SPSC ring buffer

- Power-of-two capacity, head/tail indices
- Memory ordering: `release` on publish, `acquire` on consume
- Cached indices to avoid cross-core traffic
- Padding head and tail onto separate cache lines (see [Caches and C++](caches-and-cpp.md))

```cpp
template <typename T, size_t N>
class SpscRing {
  // TODO
};
```

## Correctness

- Reasoning about happens-before
- Testing with ThreadSanitizer

## Benchmarks

| Queue | Throughput (M ops/s) | p50 latency | p99.9 latency |
|---|---|---|---|

## Takeaways

## References
