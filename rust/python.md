# Integrating Rust with Python

It's actually pretty easy, you just need to use 'maturin' as your build backend.
You can easily setup a project using this command set:

```bash
pip install maturin
maturin init
```

Maturin will add a Cargo.toml and a pyproject.toml to your project.


## Binding backend 

PyO3 is the most well supported for new projects.
