from jinja2 import Template

# get data as strings
with open('data/expletives.json', 'rt') as f:
    expletives = f.read()

with open('data/t_cands.json', 'rt') as f:
    t_cands = f.read()

with open('templates/index.html','rt') as f:
    template = Template(f.read())

with open('index.html','wt') as f:
    f.write(template.render(t_cands = t_cands, expletives = expletives))
