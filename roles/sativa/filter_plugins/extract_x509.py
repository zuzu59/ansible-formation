import re
from ansible.errors import AnsibleError

class FilterModule(object):
    '''
    custom jinja2 filters to extract X509 fragments out of e.g.
    `openssl req -x509 -batch` output.
    '''

    def filters(self):
        return {
            'extract_private_key': self.extract_private_key,
            'extract_certificate': self.extract_certificate,
        }

    def extract_private_key(self, text):
        return self._extract_begin_end(text, 'PRIVATE KEY')

    def extract_certificate(self, text):
        return self._extract_begin_end(text, '(?:X509 )?CERTIFICATE')

    def _extract_begin_end(self, text, pattern):
        matched = re.search(
            "(-----BEGIN %s-----\n.*?-----END %s-----\n)" % (pattern, pattern),
            text + '\n',
            re.DOTALL)
        if matched:
            return matched[1]
        else:
            raise AnsibleError("No %s found" % pattern)
