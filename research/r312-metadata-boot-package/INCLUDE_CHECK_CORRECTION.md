# R312 preflight: observed includes

User diagnostics identified three pre-BLS source commands: config_directory/bootuuid.cfg, prefix/console.cfg and prefix/user.cfg. user.cfg was reported absent. The previous guard rejected all source commands and therefore did not support this observed configuration.

The installer now reads those three conventional /boot/grub2 files without evaluating them. Absent files are recorded. Present files must match restrictive literal UUID assignment, console-only command/setting, or PBKDF2 password-assignment grammars. Values are not included in reports. Unknown sources/content still stop for review; this is not a general GRUB interpreter or a claim of live boot success.

Include hashes/existence and checker hashes are bound into preflight and rechecked at installation, with present files protected and existence/content rechecked after copying. No boot files have been changed by this correction. Normal-entry preservation and fixed-index checks remain in effect.

Validation: original 13 default-selection cases and 14 include cases pass on CPU. Actual privileged preflight is pending; bootuuid.cfg and console.cfg actual contents have not been observed by the agent. Run install.py without --install; no separate diagnostic is needed for the known source lines.
