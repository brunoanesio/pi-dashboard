# Instruções

1. Conda instalado
2. Use o seguinte comando:

```bash
conda env create -f environment.yml
```

3. Ative o env:

```bash
conda activate projeto
```

4. De preferência utilize o script.py com o seguinte comando:

```bash
# Também pode-se usar main.ipynb no lugar de script.py
panel serve script.py --show --autoreload
```

_ou_

Abra o notebook usando jupyter/colab/etc
