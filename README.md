# ParamFuzz Prep

A tiny utility to **prepare URLs for fuzzing** by replacing one parameter at a time with `FUZZ`.

I built this to leave URLs fuzz-ready, so I can move faster and stop wasting time editing parameters by hand.

The idea is simple: leave URLs ready for fuzzing and make the whole process faster.
---

## Why does this exist?

Because manually editing URLs before fuzzing is:
- Slow
- Repetitive
- Boring as hell

I built this to leave URLs **fuzz-ready**, so the testing phase is faster and you can focus on actually breaking things instead of editing parameters by hand.

---

## What it does

Given a URL like:

https://example.com/api/user?id=123&role=user


It generates:



https://example.com/api/user?id=FUZZ&role=user

https://example.com/api/user?id=123&role=FUZZ


One parameter at a time. Clean. Predictable. Ready to pipe into your favorite fuzzer.

---

## Usage

·Single URL:

```bash
python3 paramfuzz_prep.py "https://example.com/api/user?id=123&role=user"

·From a file:

python3 paramfuzz_prep.py -w urls.txt


Specify output file:

python3 paramfuzz_prep.py -w urls.txt -o fuzzed_urls.txt
