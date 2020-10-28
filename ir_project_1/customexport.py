import os
from scrapy.extensions.feedexport import FileFeedStorage


class CustomFileFeedStorage(FileFeedStorage):

    def open(self, spider):
        """Return the opened file."""
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        # changed from 'ab' to 'wb' to truncate file when it exists
        return open(self.path, 'wb')