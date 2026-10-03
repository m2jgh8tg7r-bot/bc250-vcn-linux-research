/* Standard same-device PCI identity read, around one established posted write. */
static void bc250_r328_pci_config_probe(struct amdgpu_device *adev)
{
	u32 before = ~0U, after = ~0U;
	u32 expected = ((u32)adev->pdev->device << 16) | adev->pdev->vendor;
	int ret;

	if (adev->no_hw_access) {
		dev_emerg(adev->dev, "BC250 R328 ABORT no_hw_access; no CONFIG write\n");
		return;
	}
	dev_emerg(adev->dev, "BC250 R328 CFG_BEFORE_BEGIN\n");
	ret = pci_read_config_dword(adev->pdev, PCI_VENDOR_ID, &before);
	dev_emerg(adev->dev, "BC250 R328 CFG_BEFORE_RETURN ret=%d identity=0x%08x expected=0x%08x\n",
		  ret, before, expected);
	if (ret || before != expected) {
		dev_emerg(adev->dev, "BC250 R328 ABORT pre-read invalid; no CONFIG write\n");
		return;
	}
#ifdef BC250_R328_WITH_WRITE
	dev_emerg(adev->dev, "BC250 R328 WRITE_BEGIN config_byte=0x1f800 value=0x55555\n");
	WREG32_SOC15(VCN, 0, mmUVD_PGFSM_CONFIG, 0x55555);
	dev_emerg(adev->dev, "BC250 R328 WRITE_RETURN before PCI config read\n");
#else
	dev_emerg(adev->dev, "BC250 R328 CONTROL no CONFIG write\n");
#endif
	dev_emerg(adev->dev, "BC250 R328 CFG_AFTER_BEGIN\n");
	ret = pci_read_config_dword(adev->pdev, PCI_VENDOR_ID, &after);
	dev_emerg(adev->dev, "BC250 R328 CFG_AFTER_RETURN ret=%d identity=0x%08x expected=0x%08x match=%u\n",
		  ret, after, expected, (unsigned int)(!ret && after == expected));
}
