## Machine Translation Modularized

- Remodularized based on file structure in this github repo: https://github.com/b-etienne/Seq2seq-PyTorch/

## Structure:
- experiments: submodule where hyperparameters are stored in json format and retrieved as config
- models: submodule where Decoder, Encoder, Seq2Seq models are stored
- utils: submodule where Word Dictionary and Data Preprocessing functions are found
- main.py: script to kick start model training
- training.py: script to walk through the whole training process
