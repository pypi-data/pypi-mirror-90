# MiniBert

Un modèle dérivé de Bert, simplifié à l'extrême puisque le modèle n'est constitué que d'une couche d'attention.

## Dépendances

```
pip install -r requirements.txt
```

## Entrainement

```
python train_semeval
```

Le script va entrainer un modèle sur le corpus SemEval et enregistrer ses performances dans le dossier _runs_.

```
tensorboard --logdir=runs
```