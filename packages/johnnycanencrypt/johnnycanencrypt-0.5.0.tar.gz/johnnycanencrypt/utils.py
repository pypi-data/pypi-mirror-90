import datetime

createdb = """
CREATE TABLE keys (
	id INTEGER PRIMARY KEY,
	keyvalue BLOB NOT NULL,
	fingerprint TEXT NOT NULL,
	keyid TEXT NOT NULL,
	expiration TEXT,
	creation TEXT,
	keytype INTEGER,
    oncard TEXT
);

CREATE TABLE subkeys (
	id INTEGER PRIMARY KEY,
	key_id INTEGER,
	fingerprint TEXT NOT NULL,
	keyid TEXT NOT NULL,
	expiration TEXT,
	creation TEXT,
	keytype TEXT,
	revoked INTEGER,
	FOREIGN KEY (key_id)
	REFERENCES keys (id)
		ON DELETE CASCADE
);

CREATE TABLE uidvalues (
	id INTEGER PRIMARY KEY,
	value TEXT,
	key_id INTEGER,
	FOREIGN KEY (key_id)
	REFERENCES keys (id)
		ON DELETE CASCADE
);

CREATE TABLE uidemails (
	id INTEGER PRIMARY KEY,
	value TEXT,
	key_id INTEGER,
	value_id INTEGER,
	FOREIGN KEY (key_id)
	REFERENCES keys (id)
		ON DELETE CASCADE
	FOREIGN KEY (value_id)
	REFERENCES uidvalues (id)
		ON DELETE CASCADE
);

CREATE TABLE uidnames (
	id INTEGER PRIMARY KEY,
	value TEXT,
	key_id INTEGER,
	value_id INTEGER,
	FOREIGN KEY (key_id)
	REFERENCES keys (id)
		ON DELETE CASCADE
	FOREIGN KEY (value_id)
	REFERENCES uidvalues (id)
		ON DELETE CASCADE
);

CREATE TABLE uiduris (
	id INTEGER PRIMARY KEY,
	value TEXT,
	key_id INTEGER,
	value_id INTEGER,
	FOREIGN KEY (key_id)
	REFERENCES keys (id)
		ON DELETE CASCADE
	FOREIGN KEY (value_id)
	REFERENCES uidvalues (id)
		ON DELETE CASCADE
);
"""


def _get_cert_data(filepath):
    "Returns the filepath content as bytes"
    with open(filepath, "rb") as fobj:
        return fobj.read()


def __get_cert_data(filepath):
    "Returns the filepath content as bytes"
    with open(filepath, "rb") as fobj:
        return fobj.read()


def convert_fingerprint(data):
    "Converts binary data to fingerprint string"
    s = ""
    for x in data:
        s += format(x, "02x")
    return s.upper()

def to_sort_by_expiary(date):
    "To help to sort based on expiration date"
    if date["expiration"] is not None:
        return date["expiration"]
    return datetime.datetime(2050, 3, 24, 23, 49, 1)
