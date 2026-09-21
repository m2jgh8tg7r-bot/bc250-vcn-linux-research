"""Static inspection of one saved 16-MiB BC-250 ROM; no device access."""
import argparse, hashlib, json, stat, struct
from pathlib import Path

def audit(b):
    assert len(b)==0x1000000
    d=0x8e0000
    assert b[d:d+4]==b'$PSP'
    count,info=struct.unpack_from('<II',b,d+8)
    assert count==19
    mode=(info>>24)&3 if info>>31 else (info>>29)&3
    assert mode==0
    end=d+16+16*count
    # Fletcher-32 over little-endian words after the stored checksum.
    low=high=0xffff
    for (word,) in struct.iter_unpack('<H',b[d+8:end]):
        low=(low+word)%0xffff; high=(high+low)%0xffff
    actual=(high<<16)|low
    assert actual==struct.unpack_from('<I',b,d+4)[0]
    rows=[]; bodies={}
    for i in range(count):
        kind,size,addr,reserved=struct.unpack_from('<4I',b,d+16+16*i)
        if kind not in [1,8,0x12]: continue
        assert reserved==0 and addr>>24==0xff
        off=addr&0xffffff
        assert off+size<=len(b)
        h=b[off:off+256]
        if kind==1:
            rows.append(dict(type=hex(kind),index=i,rom_offset=hex(off),directory_size=size,
                             ps1_magic_at_header_0x10=h[16:20]==b'$PS1',plaintext_loader_identified=False))
            continue
        assert h[16:20]==b'$PS1'
        u=lambda n:struct.unpack_from('<I',h,n)[0]
        row=dict(type=hex(kind),index=i,rom_offset=hex(off),directory_size=size,
                 header_rom_size=u(0x6c),version=hex(u(0x60)),encrypted=u(0x18),
                 compressed=u(0x48),signed=u(0x30),signature_type=u(0x34))
        if kind in [8,0x12]:
            assert size==u(0x6c)==0x40200 and u(0x14)==u(0x50)==0x40000
            assert u(0x18)==u(0x48)==u(0x34)==0 and u(0x30)==1
            body=b[off+256:off+256+u(0x50)];bodies[kind]=body
            row.update(body_size=len(body),body_sha256=hashlib.sha256(body).hexdigest(),
                       body_checksum_matches=hashlib.sha256(body).digest()==h[0xd0:0xf0])
            assert row['body_checksum_matches']
            row['nonzero_byte_count']=sum(x!=0 for x in body)
            if kind==0x12:
                assert body[8:0x3fffc]==bytes(0x3fff4)
                assert struct.unpack_from('<II',body,0)==(0x580600,0x580600)
                assert struct.unpack_from('<I',body,0x3fffc)[0]==0x11223344
                row.update(zero_interval=['0x8','0x3fffc'],first_two_words=['0x580600','0x580600'],last_word='0x11223344')
        rows.append(row)
    assert set(bodies)=={8,0x12}
    diff=[i for i,(a,c) in enumerate(zip(bodies[8],bodies[0x12])) if a!=c]
    return dict(directory_offset=hex(d),entry_count=count,directory_checksum_matches=True,
                entries=rows,smu_body_different_bytes=len(diff),first_difference=hex(diff[0]),
                last_difference=hex(diff[-1]),hardware_access=False,
                boot_selection_proven=False,runtime_identity_proven=False)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('saved_rom');a=p.parse_args()
    f=Path(a.saved_rom).resolve()
    assert stat.S_ISREG(f.stat().st_mode) and not str(f).startswith(('/dev/','/proc/','/sys/'))
    print(json.dumps(audit(f.read_bytes()),indent=2))
