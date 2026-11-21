# Caches: further reading (private, not published)

Roughly in recommended order.

### Talks

- [CPU Caches and Why You Care](https://www.youtube.
com/watch?v=WDIkqP4JbkE) — Scott Meyers, code::dive 2014. The best place to start: cache lines, prefetching and false sharing, explained with real examples.
- [Want fast C++? Know your hardware!](https://www.youtube.com/watch?v=BP6NxVxDQIs) — Timur Doumler, CppCon 2016. A practical tour of the hardware effects that matter to C++ code.
- [Efficiency with Algorithms, Performance with Data Structures](https://www.youtube.com/watch?v=fHNmRkzxHWs) — Chandler Carruth, CppCon 2014. Why `std::vector` beats `std::list`, and how to think about data structures in terms of memory.
- [Data-Oriented Design and C++](https://www.youtube.com/watch?v=rX0ItVEVjHc) — Mike Acton, CppCon 2014. Designing around how data flows through the cache instead of around objects.
- [Machine Architecture: Things Your Programming Language Never Told You](https://www.youtube.com/watch?v=L7zSU9HI-6I) — Herb Sutter, NWCPP. Latency, the memory wall, and why the hardware doesn't run your code the way you wrote it.

### Articles

- [Gallery of Processor Cache Effects](http://igoro.com/archive/gallery-of-processor-cache-effects/) — Igor Ostrovsky. Seven short experiments you can run yourself. A great companion to this post.
- [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832) — the classic table of L1, L2, RAM, SSD and network latencies.
- [What Every Programmer Should Know About Memory](https://lwn.net/Articles/250967/) — Ulrich Drepper. The deep reference on caches, TLBs and NUMA. Long, but worth it once the talks have clicked.


cache friendly cpp