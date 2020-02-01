"""Author definition and related utilities
"""


class Author:
    """A Pheed author is a person with a first and last name
    """

    def __init__(self, first_name: str, last_name: str):
        """Create a Pheed Author

        Args:
            first_name:
                str, the first name of the author
            last_name:
                str, the last name of the author
        """
        self.first_name = first_name
        self.last_name = last_name

    @property
    def name(self):
        """Return the formatted name as 'last, first' of the Author"""
        return '{}, {}'.format(self.last_name, self.first_name)

    def __eq__(self, other):
        return isinstance(other, Author) and self._identity_key_() == other._identity_key_()

    def __hash__(self):
        return hash(self._identity_key_())

    def __repr__(self):
        return 'Author({!r})'.format(self.name)

    def _identity_key_(self):
        return (Author, self.first_name, self.last_name)
