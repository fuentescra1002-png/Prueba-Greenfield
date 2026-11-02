with open('login_out.html', 'w', encoding='utf-8') as f:
    from check_login_result import post_html
    f.write(post_html)

import re
matches = re.findall(r'message|error|alerta|incorrect|bloque|fallid', post_html, re.I)
print('Keyword count:', len(matches))
for m in re.finditer(r'class=\"[^\"]*(?:error|msg|message|alert)[^\"]*\"[^>]*>(.*?)<', post_html, re.I):
    print('Match:', m.group(0)[:150])
