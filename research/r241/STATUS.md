# R241 — community VA-API implementation routes

Pinned simpmix commit `7d9c38bdfdc469505eeb94864a203c0b4ffee12c` and Shalasere commit `732dfb57dda4e08c4b31d95039e99dc232d0a809` remain the checked heads. Selected public text files were downloaded and verified against Git blob IDs; no installer or driver code was run in this stage.

In simpmix, H264 defaults to **CPU libx264** if the optional build dependency is found, no compute/hybrid/gpu override is selected and its object allocation succeeds. Missing x264 or an explicit override selects the compute/hybrid path. Later x264 encoder-open failure is not shown here to trigger an automatic compute retry. A `gpu` mode label disables governor offload but does not remove all host bitstream/entropy work.

HEVC encoding **does exist**: VA context creation and end-picture dispatch call the implemented encoder. Eight-bit encoding can use Vulkan compute motion estimation with host encoding work. The ten-bit path explicitly disables that compute motion-estimation stage, while still allowing GPU-surface transfer. H264 and HEVC decode routes call host decoder functions and then upload/map completed output planes to Vulkan-backed surfaces. Surface allocation or GPU transfer activity is not proof that decoding happened in VCN.

Both inspected gpu_compute.c files contain compute dispatch calls and no Vulkan video encode/decode API tokens in the bounded search. This complements the positive route tracing; an absent string alone is not a whole-program proof. VA-API profile/entrypoint advertisement, codec correctness, performance and engine attribution remain separate claims. Project performance and factory-fuse assertions are not independently verified or adopted.

Q36 source assistance ran for 848.82 seconds. Its report incorrectly claimed HEVC encoding was absent and gpu mode eliminated CPU work. These conclusions were rejected using exact source calls and definitions. Other usable observations were independently checked; raw model output is not published as evidence. See `results.json` and `q36-disposition.json` for accepted source facts and corrections.
