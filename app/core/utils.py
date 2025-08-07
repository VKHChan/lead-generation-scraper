import json
from datetime import date, datetime


class FileNaming:
    """Core interface for file naming strategies"""

    def clean_url_for_file(self, url: str) -> str:
        """Convert a URL into a valid and readable file name.

        Args:
            url: The URL to convert

        Returns:
            A cleaned version of the URL suitable for use as a filename.
            Format: domain-name--path-name (limited to 100 chars)
        """
        raise NotImplementedError


class StandardFileNaming(FileNaming):
    """Standard implementation of file naming strategy"""

    def clean_url_for_file(self, url: str) -> str:
        if not url:
            return 'unnamed'

        # Remove protocol and split into domain and path
        url = url.split('://')[-1].replace('&amp;', '&')
        parts = url.split('/', 1)
        domain = parts[0].replace('.', '-')
        path = parts[1].split('?')[0].split('#')[0] if len(parts) > 1 else ''

        # Create clean name from domain and path
        name = f"{domain}--{path}" if path else domain
        name = name.replace('/', '-').replace('_', '-')
        return '-'.join(part for part in name.split('-') if part)[:100]


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
