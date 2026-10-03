/*
 * Copyright 2018 Advanced Micro Devices, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE COPYRIGHT HOLDER(S) OR AUTHOR(S) BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <stdbool.h>
#include <stdarg.h>
typedef uint8_t u8; typedef uint32_t u32; typedef uint64_t u64;
#define LITTLEENDIAN_CPU
#define __packed __attribute__((packed))
#define __counted_by(x)
#define DECLARE_FLEX_ARRAY(type, name) type name[0]
#define le16_to_cpu(x) (x)
#define le32_to_cpu(x) (x)
#define ARRAY_SIZE(a) (sizeof(a)/sizeof((a)[0]))
#define VCN_HWID 12
#define VCN_HWIP 0
#define mmUVD_PGFSM_CONFIG 0
#define mmUVD_PGFSM_STATUS 1
#define mmUVD_PGFSM_CONFIG_BASE_IDX 1
#define mmUVD_PGFSM_STATUS_BASE_IDX 1
#define PSP_HEADER_SIZE                 256
#define BINARY_SIGNATURE                0x28211407
#define DISCOVERY_TABLE_SIGNATURE       0x53445049
#define GC_TABLE_ID                     0x4347
#define HARVEST_TABLE_SIGNATURE         0x56524148
#define VCN_INFO_TABLE_ID               0x004E4356
#define MALL_INFO_TABLE_ID              0x4C4C414D
#define NPS_INFO_TABLE_ID 0x0053504E

typedef enum {
	IP_DISCOVERY = 0,
	GC,
	HARVEST_INFO,
	VCN_INFO,
	MALL_INFO,
	NPS_INFO,
	TOTAL_TABLES = 6
} table;

#pragma pack(1)

typedef struct table_info
{
	uint16_t offset;   /* Byte offset */
	uint16_t checksum; /* Byte sum of the table */
	uint16_t size;     /* Table size */
	uint16_t padding;
} table_info;

typedef struct binary_header
{
	/* psp structure should go at the top of this structure */
	uint32_t binary_signature; /* 0x7, 0x14, 0x21, 0x28 */
	uint16_t version_major;
	uint16_t version_minor;
	uint16_t binary_checksum;  /* Byte sum of the binary after this field */
	uint16_t binary_size;      /* Binary Size*/
	table_info table_list[TOTAL_TABLES];
} binary_header;

typedef struct binary_header_v2
{
	/* psp structure should go at the top of this structure */
	uint32_t binary_signature; /* 0x7, 0x14, 0x21, 0x28 */
	uint16_t version_major;     /* 0x02 */
	uint16_t version_minor;
	uint16_t binary_checksum;  /* Byte sum of the binary after this field */
	uint16_t binary_size;      /* Binary Size*/
	uint16_t num_tables;
	uint16_t padding;
	table_info table_list[] __counted_by(num_tables);
} binary_header_v2;

typedef struct die_info
{
	uint16_t die_id;
	uint16_t die_offset; /* Points to the corresponding die_header structure */
} die_info;


typedef struct ip_discovery_header
{
	uint32_t signature;    /* Table Signature */
	uint16_t version;      /* Table Version */
	uint16_t size;         /* Table Size */
	uint32_t id;           /* Table ID */
	uint16_t num_dies;     /* Number of Dies */
	die_info die_info[16]; /* list die information for up to 16 dies */
	union {
		uint16_t padding[1];	/* version <= 3 */
		struct {		/* version == 4 */
			uint8_t base_addr_64_bit : 1; /* ip structures are using 64 bit base address */
			uint8_t reserved : 7;
			uint8_t reserved2;
		};
	};
} ip_discovery_header;

typedef struct ip
{
	uint16_t hw_id;           /* Hardware ID */
	uint8_t number_instance;  /* instance of the IP */
	uint8_t num_base_address; /* Number of Base Addresses */
	uint8_t major;            /* HCID Major */
	uint8_t minor;            /* HCID Minor */
	uint8_t revision;         /* HCID Revision */
#if defined(__BIG_ENDIAN)
	uint8_t reserved : 4;     /* Placeholder field */
	uint8_t harvest : 4;      /* Harvest */
#else
	uint8_t harvest : 4;      /* Harvest */
	uint8_t reserved : 4;     /* Placeholder field */
#endif
	uint32_t base_address[]; /* variable number of Addresses */
} ip;

typedef struct ip_v3
{
	uint16_t hw_id;                         /* Hardware ID */
	uint8_t instance_number;                /* Instance number for the IP */
	uint8_t num_base_address;               /* Number of base addresses*/
	uint8_t major;                          /* Hardware ID.major version */
	uint8_t minor;                          /* Hardware ID.minor version */
	uint8_t revision;                       /* Hardware ID.revision version */
#if defined(__BIG_ENDIAN)
	uint8_t variant : 4;                    /* HW variant */
	uint8_t sub_revision : 4;               /* HCID Sub-Revision */
#else
	uint8_t sub_revision : 4;               /* HCID Sub-Revision */
	uint8_t variant : 4;                    /* HW variant */
#endif
	uint32_t base_address[];		/* Base Address list. Corresponds to the num_base_address field*/
} ip_v3;

typedef struct ip_v4 {
	uint16_t hw_id;                         /* Hardware ID */
	uint8_t instance_number;                /* Instance number for the IP */
	uint8_t num_base_address;               /* Number of base addresses*/
	uint8_t major;                          /* Hardware ID.major version */
	uint8_t minor;                          /* Hardware ID.minor version */
	uint8_t revision;                       /* Hardware ID.revision version */
#if defined(LITTLEENDIAN_CPU)
	uint8_t sub_revision : 4;               /* HCID Sub-Revision */
	uint8_t variant : 4;                    /* HW variant */
#elif defined(BIGENDIAN_CPU)
	uint8_t variant : 4;                    /* HW variant */
	uint8_t sub_revision : 4;               /* HCID Sub-Revision */
#endif
	union {
		DECLARE_FLEX_ARRAY(uint32_t, base_address);	/* 32-bit Base Address list. Corresponds to the num_base_address field*/
		DECLARE_FLEX_ARRAY(uint64_t, base_address_64);	/* 64-bit Base Address list. Corresponds to the num_base_address field*/
	} __packed;
} ip_v4;

typedef struct die_header
{
	uint16_t die_id;
	uint16_t num_ips;
} die_header;


#pragma pack()
struct amdgpu_device { struct { u8 *bin; size_t size; } discovery; u32 *reg_offset[1][1]; void *dev; u64 rmmio_size; };
#define dev_emerg(dev, ...) printf(__VA_ARGS__)
#include "observer.inc"
int main(int argc, char **argv) {
 if(argc != 3) return 2;
 FILE *f=fopen(argv[1],"rb"); if(!f)return 2;
 fseek(f,0,SEEK_END); long len=ftell(f); rewind(f);
 u8 *b=malloc(len?len:1); if(fread(b,1,len,f)!=(size_t)len)return 2; fclose(f);
 struct amdgpu_device d={0}; d.discovery.bin=b; d.discovery.size=len; d.rmmio_size=524288;
 long off=strtol(argv[2],NULL,0); if(off>=0 && off<=len)d.reg_offset[0][0]=(void *)(b+off);
 bc250_r324_final_base(&d); free(b); return 0;
}
