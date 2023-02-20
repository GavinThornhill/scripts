#!/usr/bin/env python3
from bcc import BPF

bpf_source="""
#include <uapi/linux/ptrace.h>

BPF_HASH(start, u64);
BPF_HISTOGRAM(dist);

TRACEPOINT_PROBE(block, block_rq_issue)
{
	u64 ts=bpf_ktime_get_ns();
	u64 sector=args->sector;
	start.update(&sector, &ts);
	return 0;
}

TRACEPOINT_PROBE(block, block_rq_complete)
{
	u64 *tsp, delta;
	u64 sector=args->sector;

	tsp = start.lookup(&sector);
	if (tsp != 0) {
		delta = bpf_ktime_get_ns() - *tsp;
		dist.increment(bpf_log2l(delta / 1000));
		start.delete(&sector);
	}

	return 0;
}
"""

bpf=BPF(text=bpf_source)

print("Tracing disk I/O latency... Hit Ctrl-C to end.")

try:
    while True:
        (task, pid, cpu, flags, ts, msg)=bpf.trace_fields()
        print(f"{ts:.6f} ms: {msg}")
except KeyboardInterrupt:
    pass

bpf["dist"].print_log2_hist("msecs")