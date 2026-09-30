#include <drm/amdgpu_drm.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <unistd.h>

static int query(int fd, unsigned kind, unsigned subtype, void *out, unsigned size) {
    struct drm_amdgpu_info in = {0};
    in.return_pointer = (uintptr_t)out;
    in.return_size = size;
    in.query = kind;
    if (kind == AMDGPU_INFO_HW_IP_INFO)
        in.query_hw_ip.type = subtype;
    else if (kind == AMDGPU_INFO_VIDEO_CAPS)
        in.video_cap.type = subtype;
    errno = 0;
    return ioctl(fd, DRM_IOCTL_AMDGPU_INFO, &in);
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: query RENDER_NODE\n"); return 64; }
    int fd = open(argv[1], O_RDONLY | O_CLOEXEC);
    if (fd < 0) { perror("open"); return 1; }
    unsigned accel = 0;
    int rc = query(fd, AMDGPU_INFO_ACCEL_WORKING, 0, &accel, sizeof(accel));
    int err = errno;
    printf("{\"query\":\"ACCEL_WORKING\",\"ret\":%d,\"errno\":%d,\"value\":%u}\n", rc, err, accel);
    if (rc != 0 || accel != 1) { close(fd); return 2; }
    const unsigned types[] = {AMDGPU_HW_IP_GFX, AMDGPU_HW_IP_VCN_DEC, AMDGPU_HW_IP_VCN_ENC, AMDGPU_HW_IP_VCN_JPEG};
    const char *names[] = {"GFX", "VCN_DEC", "VCN_ENC", "JPEG"};
    for (unsigned i = 0; i < 4; ++i) {
        struct drm_amdgpu_info_hw_ip ip = {0};
        rc = query(fd, AMDGPU_INFO_HW_IP_INFO, types[i], &ip, sizeof(ip));
        err = errno;
        printf("{\"query\":\"HW_IP_INFO\",\"type\":\"%s\",\"ret\":%d,\"errno\":%d", names[i], rc, err);
        if (!rc) printf(",\"major\":%u,\"minor\":%u,\"available_rings\":%u,\"ip_discovery_version\":%u", ip.hw_ip_version_major, ip.hw_ip_version_minor, ip.available_rings, ip.ip_discovery_version);
        puts("}");
        if (i == 0 && (rc != 0 || ip.available_rings == 0)) { close(fd); return 3; }
    }
    for (unsigned i = 0; i < 2; ++i) {
        struct drm_amdgpu_info_video_caps caps = {0};
        rc = query(fd, AMDGPU_INFO_VIDEO_CAPS, i, &caps, sizeof(caps));
        err = errno;
        printf("{\"query\":\"VIDEO_CAPS\",\"type\":\"%s\",\"ret\":%d,\"errno\":%d", i ? "ENCODE" : "DECODE", rc, err);
        if (!rc) {
            printf(",\"codec_valid\":[");
            for (unsigned j = 0; j < AMDGPU_INFO_VIDEO_CAPS_CODEC_IDX_COUNT; ++j)
                printf("%s%u", j ? "," : "", caps.codec_info[j].valid);
            printf("]");
        }
        puts("}");
    }
    return close(fd) ? 4 : 0;
}
