
import subprocess
import re
from typing import List, Tuple


class VersionManager(object):

    # m_pkg_name = 'pandas-coder'
    m_pkg_name = 'test-myp'
    m_current_version = tuple('0.1.0'.split('.'))
    m_version_re = re.compile(r'\((from versions: (.*?))\)')

    def has_updated(self) -> bool:
        return self.m_current_version < self.get_last_version()

    def get_versions(self):
        ret = self._use_pip(['install', f'{self.m_pkg_name}=='])
        ret = str(ret.stderr)

        vs = self.m_version_re.search(ret).groups()[1].split(',')
        assert vs[0] != 'none' '未找到任何版本，请检查网络连接'
        return [tuple(v.strip().split('.')) for v in vs]

    def get_last_version(self) -> Tuple:
        last = self.get_versions()[-1]
        return last

    def update(self):
        self._use_pip(['install', self.m_pkg_name, '-U'])

    def _use_pip(self, cmds: List[str]):
        cmds = ['pip'] + cmds + ['-i', 'https://pypi.douban.com/simple/']

        return subprocess.run(cmds,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
