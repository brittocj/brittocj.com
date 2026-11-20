with open('blog/devops-ready-reckoner/index.html', 'rb') as f:
    content = f.read()

# Literal angle brackets
LT = b'<'
GT = b'>'

# HTML entities using explicit bytes
# < = 26 6c 74 3b  (& l t ;)
# > = 26 67 74 3b  (& g t ;)
LT_ENT = bytes([0x26, 0x6c, 0x74, 0x3b])
GT_ENT = bytes([0x26, 0x67, 0x74, 0x3b])

print(f'LT_ENT = {LT_ENT} hex={LT_ENT.hex()}')
print(f'GT_ENT = {GT_ENT} hex={GT_ENT.hex()}')

patterns = [
    (LT + b'name' + GT, LT_ENT + b'name' + GT_ENT),
    (LT + b'type' + GT, LT_ENT + b'type' + GT_ENT),
    (LT + b'id' + GT, LT_ENT + b'id' + GT_ENT),
    (LT + b'container_name_or_id' + GT, LT_ENT + b'container_name_or_id' + GT_ENT),
]

for old, new in patterns:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f'Replaced {count} occurrences of {old}')
    else:
        print(f'Not found: {old}')

with open('blog/devops-ready-reckoner/index.html', 'wb') as f:
    f.write(content)
print('Done')

# Verify
idx = content.find(b'pulumi stack select')
if idx >= 0:
    print(content[idx:idx+80])
    print(content[idx:idx+80].hex())