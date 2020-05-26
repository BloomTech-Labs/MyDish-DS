# CNN Model using Wandb
---

1. First, install the library.

```
pipenv install wandb
```

2. Follow the quickstart guideline

- [wandb quickstart](https://docs.wandb.com/quickstart)

  - [Further Information](https://docs.wandb.com/sweeps/)

---

## Training and Tuning

- Configure the hyper-parameters by editing the [sweep_cnn_model.yml](sweep_cnn_model.yml) file.

Before you can start training, you must initialize a sweep and run it. In the code cell below, run the first line to get a sweep id which will be needed for the second line.

```
wandb sweep -p mydish wandb_cnn_detector/<sweep_cnn_model.yml>
wandb agent USER/PROJECT/SWEEP_ID
```
