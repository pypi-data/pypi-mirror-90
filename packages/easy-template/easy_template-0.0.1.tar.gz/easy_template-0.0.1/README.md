# Easy Template

Process templates with ease.

You can process template files (`process_file()`) or text templates (`process_template()`).

## Templating

`process_file('foobar.md', values={'name': 'Hans'}, lookup_dir='scripts')`

- `{{=key}}` gets replaced with the value looked up in the provided value dict
- `{{=key.nested_key1.nested_key2}}` gets replaced with the value looked up in the provided value dict: `values['key']['nested_key1']['nested_key2']`
- `{{foobar.py}}` gets replaced with the content of the file located in the `lookup_dir` folder or a subfolder.
- `{{%py% foobar.py}}` wraps the content with a markdown code block.
- `{{%py%= key}}` wraps the content as a markdown code block.

## helper functions

### Side-By-Side Code

Sometimes it is useful to have a side-by-side view of some code, especially for correcting examns...

See the examples for more details. The bewlow returns a Table as follows:

```py
side_by_side_code(q2_answer, q2_solution, titles=['Answer', 'Solution'], max_line_length=80)
```

Result:

```py

Answer                    | Solution
------------------------------------------------------
def collatz(a):           | def collatz(number):
    if a % 2 == 0:        |     if number % 2 == 0:
        return int(a / 2) |         return number // 2
    else:                 |     return 3 * number + 1
        return 3 * a + 1  |
                          |
                          | zahl = 9
z = 9                     | result = []
r = []                    | while zahl > 1:
while z > 1:              |     zahl = collatz(zahl)
    z = collatz(z)        |     result.append(zahl)
    r.append(z)           | print(result)
print(r)                  |
```

## Package and upload to pip

@see [this tutorial](https://packaging.python.org/tutorials/packaging-projects/)

```sh
rm -rf build/ dist/ easy_template.egg-info/ && \
python3 setup.py sdist bdist_wheel && \
python3 -m twine upload dist/*
```
