# R267–R269 session closure

Research stopped at the user's explicit request on 2026-10-01 JST. No background research is scheduled; resume only on a new instruction.

Completed:
- R267: ordinary DRM information-query preflight compiled but not run; saved-counter analyzer verified against 1,692 independent arithmetic cases, eight named controls and four invalid-input controls. Counts/second are not automatically VCLK Hz. No external GPCNT samples were replayed.
- R268: IRQ/fence and LMI-clean source observations separated from instruction-fetch evidence; older public claims classified by date and evidence limits.
- R269: write-disable, actual disable, CC harvesting, SMN values and discovery metadata kept separate. SMN UVD-disable fuse interpretation explicitly downgraded to an unresolved field-mapping hypothesis. Fault silence does not establish absent fetch. Ordinary-source interrupt enable is not a generic core-enable control.

The main checkpoint was published as 8be59066984a7e840b4bf4a10a1aad27f66d0e5a, with all 29 selected files verified by exact SHA256 and size. This closeout adds the existing-record observer template and the final search limitation note. The pinned original Shalasere archive remains unchanged.

No new VCN register/SMN/SMU/PSP transactions, firmware loads, video jobs, boot-option changes or reboots occurred. Cached device/module metadata was read, and Q36 GPU inference was used for advisory reviews. Critical new GPCNT/SMN acquisition is not ready; no user reboot or BIOS change is requested.

On resumption, first seek original Thomas GPCNT count/timestamp code/logs, original definitions for the two uvd_uvd_* fields, and fault/request observer coverage with positive controls. Preserve unknowns. Do not repeat harvesting-clear variants or blind field-name searches without a new discriminator.
