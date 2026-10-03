#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
typedef uint32_t u32;
struct pci_dev { unsigned device, vendor; };
struct amdgpu_device { struct pci_dev *pdev; void *dev; bool no_hw_access; };
#define PCI_VENDOR_ID 0
#define VCN 0
#define mmUVD_PGFSM_CONFIG 0
#define dev_emerg(d, ...) printf(__VA_ARGS__)
static int calls,writes,pre_ret,post_ret; static u32 pre_id,post_id;
static int pci_read_config_dword(struct pci_dev *p,int offset,u32 *value) {
(void)p; assert(offset==0); calls++; *value=calls==1?pre_id:post_id;
return calls==1?pre_ret:post_ret;
}
#define WREG32_SOC15(block,inst,reg,val) do { assert(calls==1); assert((val)==0x55555); writes++; } while(0)
#ifdef WITH_WRITE
#define BC250_R328_WITH_WRITE
#endif
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

int main(void) {
struct pci_dev pci={.device=0x163f,.vendor=0x1002};
struct amdgpu_device a={.pdev=&pci};
for(int nh=0;nh<2;nh++) for(int pr=0;pr<2;pr++) for(int pi=0;pi<2;pi++)
for(int ar=0;ar<2;ar++) for(int ai=0;ai<2;ai++) {
calls=writes=0; a.no_hw_access=nh; pre_ret=pr; post_ret=ar;
pre_id=pi?0xffffffff:0x163f1002; post_id=ai?0xffffffff:0x163f1002;
bc250_r328_pci_config_probe(&a);
int eligible=!nh&&!pr&&!pi; assert(calls==(nh?0:eligible?2:1));
#ifdef WITH_WRITE
assert(writes==eligible);
#else
assert(writes==0);
#endif
}
puts("PASS 32 cases"); return 0;
}
