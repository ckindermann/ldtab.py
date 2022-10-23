# ldtab.py 

LDTab for Python

1. Project Setup
    1. `git clone git@github.com:ckindermann/ldtab.py.git`
    2. `cd ldtab.py`
    3. `git clone git@github.com:ontodev/wiring.rs.git`
    4. `git clone git@github.com:ontodev/ldtab.rs.git`
    5. `mv python_module.rs ldtab.rs/src/`
    6. add the line `mod python_module;` to the end of file `ldtab.rs/src/lib.rs`
    7. `mv Cargo.toml ldtab.rs` 

2. Installing Maturin 

    1. `python3 -m venv .venv`
    2. `source .venv/bin/activate`
    3. `pip install -U pip maturin`

3. Build
    1. `maturin develop` for local installation
    2. `maturin build` for creating a wheel

4. Test
    1. `cd ..`
    2. `python demo.py`


