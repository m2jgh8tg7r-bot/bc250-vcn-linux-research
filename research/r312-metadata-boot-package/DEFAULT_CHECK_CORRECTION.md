# R312 preflight correction: fixed default index

The user-run preflight stopped before installation because saved_entry is absent. Read-only user diagnostics showed one literal `set default=1`, followed by blscfg. The original new guard incorrectly required an explicit saved normal ID.

The guard now supports this narrowly scoped layout: no saved_entry, fixed index1, conventional OSTree filenames with matching positive numeric versions, research entries with version0, unchanged normal entries before/after replacement, and no detected earlier menu/config source or environment override. Other layouts stop for review. It is not a general GRUB interpreter. The current readable files predict the normal prefix ostree-2.conf then ostree-1.conf; this does not identify the running deployment.

Fedora documents BLS filename ordering with rpmvercmp: https://fedoraproject.org/wiki/Changes/BootLoaderSpecByDefault . In this restricted filename set, OSTree entries precede boot-entry research names and their numeric suffixes distinguish the normal entries. Both normal BLS contents and the GRUB configuration are protected from modification.

13 CPU cases pass, including rejection of changed defaults, extra menu/config sources, overrides, normal entry changes and elevated candidate version. Actual privileged preflight remains pending. No boot files, image bytes, saved selection or reboot state changed. Default checker content and its decision are bound into the preflight snapshot and rechecked for installation.

Next: rerun install.py without --install. It is still read-only with respect to /boot. Do not run installation or reboot until its output is reviewed.
