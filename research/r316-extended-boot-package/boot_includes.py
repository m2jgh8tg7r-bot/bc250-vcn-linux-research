"""Validate only the three observed pre-BLS includes; never evaluate shell code."""
import re
SOURCES={
 'source ${config_directory}/bootuuid.cfg':'bootuuid.cfg',
 'source $prefix/console.cfg':'console.cfg',
 'source ${prefix}/user.cfg':'user.cfg',
}
def validate_include(name,text):
 if text is None:return {'exists':False,'classification':'absent'}
 lines=[s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith('#')]
 for line in lines:
  if name=='bootuuid.cfg':
   ok=re.fullmatch(r'''(?:set\s+)?BOOT_UUID=(?:"[0-9a-fA-F-]{1,64}"|'[0-9a-fA-F-]{1,64}'|[0-9a-fA-F-]{1,64})''',line)
  elif name=='user.cfg':
   ok=re.fullmatch(r'''GRUB2_PASSWORD=(?:"grub\.pbkdf2\.sha512\.[0-9]+\.[0-9a-fA-F]+\.[0-9a-fA-F]+"|'grub\.pbkdf2\.sha512\.[0-9]+\.[0-9a-fA-F]+\.[0-9a-fA-F]+'|grub\.pbkdf2\.sha512\.[0-9]+\.[0-9a-fA-F]+\.[0-9a-fA-F]+)''',line)
  elif name=='console.cfg':
   ok=(re.fullmatch(r'terminal_(?:input|output)\s+(?:--append\s+|--remove\s+)?(?:console|serial|gfxterm)(?:\s+(?:console|serial|gfxterm))*',line)
       or re.fullmatch(r'serial(?:\s+--(?:unit|port|speed|word|parity|stop)=[a-zA-Z0-9]+)+',line)
       or re.fullmatch(r'''set\s+(?:gfxmode|gfxpayload|color_normal|color_highlight)=(?:[a-zA-Z0-9_,/ -]+|"[a-zA-Z0-9_,/ -]+"|'[a-zA-Z0-9_,/ -]+')''',line))
  else:ok=False
  assert ok, name+': unsupported content; no values disclosed, stop for review'
 return {'exists':True,'classification':'restricted_'+name,'active_lines':len(lines)}

def inspect_sources(config,includes):
 lines=[s.strip() for s in config.splitlines() if s.strip() and not s.lstrip().startswith('#')]
 end=lines.index('blscfg');checked={}
 for line in lines[:end]:
  if not re.search(r'\b(menuentry|submenu|configfile|source)\b',line):continue
  assert line in SOURCES, 'Unknown pre-BLS menu/config command; stop for review'
  name=SOURCES[line];assert name in includes, 'Missing include observation: '+name
  checked[name]=validate_include(name,includes[name])
 return checked
