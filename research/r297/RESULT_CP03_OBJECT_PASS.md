# R297 CP03 candidate/object build

Date: 2026-10-02
Status: PASS

- CP03 source SHA-256: fc90416f8abb77012185343c5457b34d641dac8df0ee7bf47899c0e7906efa9b
- object SHA-256: a7eefa982174993332b65e5514d19643a156a23e27156ccbc720acd042be531a
- build log SHA-256: 781199c94026c8c50175bb4276c88f6f9b985b5e9c9f72b85e1ec0af02f15476
- source placement audit passed
- object build returned MAKE_RC=0
- required CP03/P1 markers retained
- vcn_v2_0_hw_init and cold path retained
- R152 vcn_v2_0.c restored to the exact baseline SHA-256 eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075

Next step: compose exact R274B amdgpu_vcn.c with this CP03 vcn_v2_0.c and build the full amdgpu module.
