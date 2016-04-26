import json, datetime
from jinja2 import Template

from download_crx import DOWNLOAD_URL

VIEW_SOURCE_URL = "https://robwu.nl/crxviewer/crxviewer.html?crx="

template = Template(open('stats/template.html').read())

exts = json.load(open('data/_merged.json'))
print('enriched loaded')
crxs = json.load(open('data/crx_stats.json'))
print('file stats loaded')

for ext in exts:
	ext_id = ext['ext_id']
	ext['files'] = crxs.get(ext_id,[])
	ext['download_link'] = DOWNLOAD_URL.format(ID=ext_id)
	ext['view_source'] = VIEW_SOURCE_URL+ext['download_link']
	for file in ext['files']:
		file['storage_url'] = "https://storage.googleapis.com/chrmexts/crx/{ext_id}/{file}".format(
			ext_id=ext_id, file=file['name'])

def safeint(n):
    try:
        return int(n)
    except:
        return -1 

exts = sorted((ext for ext in exts if len(ext['files']) > 0), key=lambda x: -safeint(x.get('user_count')))

files_count = sum(len(ext['files']) for ext in exts)
result = template.render(exts=exts, exts_count=len(exts),
	files_count=files_count, VIEW_SOURCE_URL=VIEW_SOURCE_URL,
	now=datetime.datetime.now())
open('../exts-site/index.html','w').write(result)