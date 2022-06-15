This is part of a project started by Vincent Georges related to the identification of geometric ornaments by artificial inteligence. Web app and machine learning model were done by Arnaud Cayrol.
This repo contains the code for a web app hosted at https://ai-geometric-ornaments.herokuapp.com/
This web app is a tool for helping with the identification of geometric ornaments.
It works by runing user submitted images through a machine learning classifier.
The AI is a convolutional neural network (CNN) using the Resnet18 architecture.
The training of the model was done with pytorch, starting from a pretrained state (trained with image net). (More info to come)