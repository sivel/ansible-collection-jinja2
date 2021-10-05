# sivel.jinja2

This Ansible collection provides all [Jinja2](https://jinja.palletsprojects.com/)
[filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-filters)
and [tests](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-tests)
from the most recent Jinja2 release.

This can be useful for users who are using an OS that only offers an older version of Jinja2, and cannot install Jinja2 from [PyPI](https://pypi.org/project/Jinja2).

## Jinja2 Version

3.0.2

## Jinja2 Documentation

[https://jinja.palletsprojects.com/en/3.0.x/templates/](https://jinja.palletsprojects.com/en/3.0.x/templates/)

## Installation

```shell
ansible-galaxy collection install sivel.jinja2
```

## Usage

```yaml
- debug:
    msg: "{{ result.results|sivel.jinja2.map(attribute='stdout')|list }}"
```
