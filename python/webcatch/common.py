dir_root = '/workspace/project/gyagp/webcatch'
dir_python = '/workspace/project/gyagp/share/python'
dir_out = dir_root + '/out'
dir_project = dir_root + '/project'
dir_log = dir_root + '/log'

server = 'ubuntu-ygu5-02'
dir_out_server = '/workspace/service/webcatch/out'

# comb: [binary_format, rev_min_built, rev_max_built]
comb_valid = {
    ('android', 'x86', 'content_shell'): ['(.*).apk$', 233137, 233137],  # 250735
    ('android', 'x86', 'webview'): ['(.*).apk$', 233137, 252136],
    ('linux', 'x86', 'chrome'): ['(.*).tar.gz$', 233137, 236088],
    #['android', 'arm', 'content_shell'],
}
COMB_VALID_INDEX_FORMAT = 0
COMB_VALID_INDEX_REV_MIN = 1
COMB_VALID_INDEX_REV_MAX = 2

# major -> svn rev, git commit, build. major commit is after build commit.
# To get this, search 'The atomic number' in 'git log origin master chrome/VERSION'
ver_info = {
    36: [260368, 'b1f8bdb570beade2a212e69bee1ea7340d80838e', 1917],
    35: [252136, '6d5ba2122914c53d753e5fb960a601b43cb79c60', 1848],
    34: [241271, '3824512f1312ec4260ad0b8bf372619c7168ef6b', 1751],
    33: [233137, 'eeaecf1bb1c52d4b9b56a620cc5119409d1ecb7b', 1701],
    32: [225138, '6a384c4afe48337237e3da81ccff8658755e2a02', 1652],
    31: [217377, 'c95dd877deb939ec7b064831c2d20d92e93a4775', 1600],
    30: [208581, '88367e9bf6a10b9e024ec99f12755b6f626bbe0c', 1548],
}
VERSION_INFO_INDEX_REV = 0
# revision range to care about
rev_default = [ver_info[31][VERSION_INFO_INDEX_REV], 999999]


def get_comb_name(os, arch, module):
    return os + '-' + arch + '-' + module
