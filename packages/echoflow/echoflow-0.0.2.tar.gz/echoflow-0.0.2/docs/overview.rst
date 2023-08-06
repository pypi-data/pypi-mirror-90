========================
Welcome to EchoFlow!
========================
This library provides tools for generative modeling of tabular datasets using normalizing flows. Some of its core features include:

- Density estimation.
- Joint + conditional sampling.
- Categorical + continuous values.
- Normalizing flows from RealNVP and MAF.

Quick Start
--------------
Install EchoFlow using ``pip``:

.. code-block:: bash

    pip install echoflow

Train a model on the demo dataset:

.. code-block:: python

    from echoflow import EchoFlow
    from echoflow.demo import load_dataset

    model = EchoFlow()
    model.fit(load_dataset())
    synthetic = model.sample(num_samples=10)
