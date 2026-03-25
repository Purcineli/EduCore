"""
Minimal pure-Python .po -> .mo compiler.
Produces a valid MO binary including the mandatory charset header entry,
so Django's gettext module can decode UTF-8 translations correctly.

Usage:
    python compile_mo.py
"""
import struct


def unescape(s):
    """Handle common escape sequences found in .po string values."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            c = s[i + 1]
            if c == 'n':
                result.append('\n')
            elif c == 't':
                result.append('\t')
            elif c == '\\':
                result.append('\\')
            elif c == '"':
                result.append('"')
            else:
                result.append('\\')
                result.append(c)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def compile_po(po_path, mo_path):
    catalog = {}
    msgid = None
    msgstr_parts = []
    state = None

    with open(po_path, encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('msgid '):
            if state == 'msgstr' and msgid is not None:
                catalog[msgid] = ''.join(msgstr_parts)
            msgid = unescape(line[7:-1])
            msgstr_parts = []
            state = 'msgid'
        elif line.startswith('msgstr '):
            state = 'msgstr'
            msgstr_parts = [unescape(line[8:-1])]
        elif line.startswith('"') and state:
            val = unescape(line[1:-1])
            if state == 'msgid':
                msgid += val
            else:
                msgstr_parts.append(val)

    # Flush last entry
    if state == 'msgstr' and msgid is not None:
        catalog[msgid] = ''.join(msgstr_parts)

    # Mandatory MO header: empty-string key with charset declaration.
    # The value from the .po file's own header msgstr is usually multi-line;
    # we ensure Content-Type is present.
    header = catalog.get('', '')
    if 'Content-Type' not in header:
        catalog[''] = (
            'Content-Type: text/plain; charset=UTF-8\n'
            'Content-Transfer-Encoding: 8bit\n'
        )

    # Sort keys as bytes (MO format requires sorted order).
    keys = sorted(k.encode('utf-8') for k in catalog)
    values = [catalog[k.decode('utf-8')].encode('utf-8') for k in keys]

    n = len(keys)
    header_size = 7 * 4          # 7 × uint32
    ktable_start = header_size
    vtable_start = ktable_start + n * 8
    data_start = vtable_start + n * 8

    ids = b''.join(k + b'\x00' for k in keys)
    strs = b''.join(v + b'\x00' for v in values)

    koffsets = []
    pos = 0
    for k in keys:
        koffsets.append((len(k), data_start + pos))
        pos += len(k) + 1

    voffsets = []
    pos = 0
    for v in values:
        voffsets.append((len(v), data_start + len(ids) + pos))
        pos += len(v) + 1

    with open(mo_path, 'wb') as f:
        f.write(struct.pack('<I', 0x950412de))    # magic number (little-endian)
        f.write(struct.pack('<I', 0))              # revision
        f.write(struct.pack('<I', n))              # number of strings
        f.write(struct.pack('<I', ktable_start))   # key table offset
        f.write(struct.pack('<I', vtable_start))   # value table offset
        f.write(struct.pack('<I', 0))              # hash table size (unused)
        f.write(struct.pack('<I', 0))              # hash table offset (unused)
        for length, offset in koffsets:
            f.write(struct.pack('<II', length, offset))
        for length, offset in voffsets:
            f.write(struct.pack('<II', length, offset))
        f.write(ids)
        f.write(strs)

    print(f'Compiled: {po_path} -> {mo_path} ({n} entries)')


if __name__ == '__main__':
    compile_po(
        'locale/pt_BR/LC_MESSAGES/django.po',
        'locale/pt_BR/LC_MESSAGES/django.mo',
    )
    compile_po(
        'locale/ru/LC_MESSAGES/django.po',
        'locale/ru/LC_MESSAGES/django.mo',
    )
