from pykeepass import PyKeePass


def pretty_print_dict(_dict):
    for k, v in _dict.items():
        print("%-10s: %s" % (k, v if v else ""))


class Attributes(object):
    GROUP = ["name", "notes"]
    ENTRY = ["title", "url", "username", "password", "notes"]
    SAFE_ENTRY = ["title", "url", "username", "notes"]  # remove password


class Uri(object):
    def __init__(self, uri):
        self.uri = uri
        self.scheme, self.path = uri.split(":", 1)

        if self.scheme not in ["e", "g"]:
            raise TypeError(f"{self.scheme} is not supported")

    def is_entry(self):
        return True if self.scheme == "e" else False

    def is_group(self):
        return True if self.scheme == "g" else False


class FuzeePass(object):
    def __init__(self, db_file, password=None, key_file=None):
        self._db_file = db_file
        self.k = PyKeePass(db_file, password, key_file)

    def _save(self):
        self.k.save()

    def ls(self):
        [print(f"e:{e.path}") for e in self.k.entries]
        [print(f"g:{g.path}") for g in self.k.groups]

    def _show_group(self, path):
        group = self.k.find_groups_by_path(path)
        group_info = {k: getattr(group, k) for k in ["path"] + Attributes.GROUP}
        print("[Group Info]")
        pretty_print_dict(group_info)

    def _show_entry(self, path, include_password, only_password):
        entry = self.k.find_entries_by_path(path)
        if only_password:
            print(entry.password, end="")
            return

        return_attrs = ["path"] + (
            Attributes.ENTRY if include_password else Attributes.SAFE_ENTRY
        )
        entry_info = {k: getattr(entry, k) for k in return_attrs}
        print("[Entry Info]")
        pretty_print_dict(entry_info)

    def get(self, uri, include_password=False, only_password=False):
        u = Uri(uri)
        if u.is_group():
            if only_password:
                return
            self._show_group(u.path)
        else:
            self._show_entry(u.path, include_password, only_password)

    def set(self, uri, **kwargs):
        """
        Update values of attributes for entry or group
        """
        attributes = None
        resource = None
        u = Uri(uri)
        if u.is_group():
            attributes = Attributes.GROUP
            resource = self.k.find_groups_by_path(u.path)
        else:
            attributes = Attributes.ENTRY
            resource = self.k.find_entries_by_path(u.path)

        for attr in attributes:
            if kwargs.get(attr):
                setattr(resource, attr, kwargs.get(attr))

        self._save()

    def _lookup_group(self, uri):
        u = Uri(uri)
        if not u.is_group():
            raise TypeError("Not a group uri")
        return self.k.find_groups_by_path(u.path)

    def create_entry(self, group_uri, title, username, password, url=None, notes=None):
        group = self._lookup_group(group_uri)
        self.k.add_entry(group, title, username, password, url=url, notes=notes)
        self._save()

    def create_group(self, group_uri, group_name, notes=None):
        group = self._lookup_group(group_uri)
        self.k.add_group(group, group_name, notes=notes)
        self._save()

    def delete(self, uri):
        u = Uri(uri)
        if u.is_group():
            group = self.k.find_groups_by_path(u.path)
            self.k.delete_group(group)
        else:
            entry = self.k.find_entries_by_path(u.path)
            self.k.delete_entry(entry)

        self._save()
