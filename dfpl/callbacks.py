# for NN model functions
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
# for testing in Weights & Biases
from wandb.keras import WandbCallback

from dfpl import options
from dfpl import settings


def autoencoder_callback(checkpoint_path: str, opts: options.Options) -> list:
    """
    Callbacks for fitting the autoencoder

    :param checkpoint_path: The output directory to store the checkpoint weight files
    :param opts: Training options provided to the run
    :return: List of ModelCheckpoint and EarlyStopping class.
    """

    # enable this checkpoint to restore the weights of the best performing model
    checkpoint = ModelCheckpoint(checkpoint_path,
                                 monitor="val_auc",
                                 mode='max',
                                 verbose=1,
                                 period=settings.ac_train_check_period,
                                 save_best_only=True,
                                 save_weights_only=True)

    # enable early stopping if val_loss is not improving anymore
    early_stop = EarlyStopping(monitor="val_auc",
                               mode='max',
                               patience=settings.ac_train_patience,
                               min_delta=settings.ac_train_min_delta,
                               verbose=1,
                               restore_best_weights=True)

    if opts.wabTracking:
        trackWandB_callback = WandbCallback(save_model=False)
        return [checkpoint, early_stop, trackWandB_callback]
    else:
        return [checkpoint, early_stop]


def nn_callback(checkpoint_path: str, opts: options.Options) -> list:
    """
    Callbacks for fitting the feed forward network (FNN)

    :param checkpoint_path: The output directory to store the checkpoint weight files
    :param opts: Training options provided to the run
    :return: List of ModelCheckpoint and EarlyStopping class.
    """

    # enable this checkpoint to restore the weights of the best performing model
    checkpoint = ModelCheckpoint(checkpoint_path,
                                 verbose=1,
                                 period=settings.nn_train_check_period,
                                 save_best_only=True,
                                 monitor="val_loss",
                                 mode='min',
                                 save_weights_only=True)

    # enable early stopping if val_loss is not improving anymore
    early_stop = EarlyStopping(patience=settings.nn_train_patience,
                               monitor="val_loss",
                               mode="min",
                               min_delta=settings.nn_train_min_delta,
                               verbose=1,
                               restore_best_weights=True)

    if opts.wabTracking:
        trackWandB_callback = WandbCallback(save_model=False)
        return [checkpoint, early_stop, trackWandB_callback]
    else:
        return [checkpoint, early_stop]
