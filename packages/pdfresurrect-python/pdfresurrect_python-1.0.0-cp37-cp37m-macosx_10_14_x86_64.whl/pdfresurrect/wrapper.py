from ctypes import (CDLL, Structure, POINTER, c_char, c_int, c_long, c_short,
                    c_char_p)


class pdf_creator(Structure):
    _fields_ = [('key', c_char * 32),
                ('value', c_char * 128)]


class xref_entry_t(Structure):
    _fields_ = [('obj_id', c_int),
                ('offset', c_long),
                ('gen_num', c_int),
                ('f_or_n', c_char)]


class xref_t(Structure):

    _fields_ = [
                ('start', c_long),
                ('end', c_long),
                ('pdf_creator_t',  POINTER(pdf_creator)),
                ('n_creator_entries', c_int),
                ('n_entries', c_int),
                ('entries', POINTER(xref_entry_t)),
                ('is_stream', c_int),
                ('is_linear', c_int),
                ('version', c_int)
                ]

    def _cache_dict(self):
        if not hasattr(self, 'creator_props'):
            self.creator_props = self._to_dict()

    def _to_dict(self):
        return {i.key.decode() : i.value for i in self.pdf_creator_t[:9]}

    @property
    def title(self):
        self._cache_dict()
        return self.creator_props['Title']

    @property
    def author(self):
        self._cache_dict()
        return self.creator_props['Author']

    @property
    def subject(self):
        self._cache_dict()
        return self.creator_props['Subject']

    @property
    def keywords(self):
        self._cache_dict()
        return self.creator_props['Keywords']

    @property
    def creator(self):
        self._cache_dict()
        return self.creator_props['Creator']

    @property
    def producer(self):
        self._cache_dict()
        return self.creator_props['Producer']

    @property
    def creation_date(self):
        self._cache_dict()
        return self.creator_props['CreationDate']

    @property
    def mod_date(self):
        self._cache_dict()
        return self.creator_props['ModDate']

    @property
    def trappes(self):
        self._cache_dict()
        return self.creator_props['Trapped']


class pdf_t(Structure):
    _fields_ = [('name', c_char_p),
                ('pdf_major_version', c_short),
                ('pdf_minor_version', c_short),
                ('n_xrefs', c_int),
                ('xrefs', POINTER(xref_t)),
                ('has_xref_streams', c_int)]

    @property
    def n_versions(self):
        """From code

        Returns:
            int: number versions of the pdf
        """
        n_versions = self.n_xrefs
        if n_versions and self.xrefs[0].is_linear:
            n_versions -= 1
        for i in range(1, self.n_xrefs):
            if self.xrefs[i].end == 0:
                n_versions -= 1
        if not self.n_xrefs or (not n_versions and self.xrefs[0].is_linear):
            n_versions = 1
        return n_versions
