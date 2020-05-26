# CNN Model using Wandb
---

1. First, install the library.

```
pipenv install wandb
```

2. Follow the quickstart guideline

- [wandb quickstart](https://docs.wandb.com/quickstart)

- [Weights and Biases](https://docs.wandb.com/sweeps/)

- [Running the Sweep File](https://www.wandb.com/articles/run-your-first-sweep)

- [Library With Example Notebooks](https://docs.wandb.com/library/example-projects)

- [Notebook With Examples on Running A Sweep](https://colab.research.google.com/drive/1gKixa6hNUB8qrn1CfHirOfTEQm0qLCSS)

- [Utilizing wandb For CNN Models](https://colab.research.google.com/drive/1S8SJvH4bqhPvurG4gjh3-t-XulX4S8JX)

---

## Training and Tuning

- Configure the hyper-parameters by editing the [sweep_cnn_model.yaml](sweep_cnn_model.yaml) file.

Before you can start training, you must initialize a sweep and run it. In the code cell below, run the first line to get a sweep id which will be needed for the second line.

```
wandb sweep -p mydish wandb_cnn_detector/sweep_cnn_model.yaml
wandb agent USER/PROJECT/SWEEP_ID
```
