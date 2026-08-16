# Wolfram exact replay

Independent Wolfram Language evaluation reproduced:

```text
rank 12 endpoint: K=3, T=5761, cap=16,380,678,
                  forced=80,415,635, slack=64,034,957
rank 13 endpoint: K=4, T=12233, cap=22,658,813,
                  forced=73,640,859, slack=50,982,046
rank 14 wall:     forced K=8 load=39,342,841,453,
                  one-threshold cap=56,467,502,708
```

The stronger cumulative rank-14 cap is independently reconstructed by the
shipped Python audit.
