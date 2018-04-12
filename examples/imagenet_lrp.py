# Begin: Python 2/3 compatibility header small
# Get Python 3 functionality:
from __future__ import\
    absolute_import, print_function, division, unicode_literals
from future.utils import raise_with_traceback, raise_from
# catch exception with: except Exception as e
from builtins import range, map, zip, filter
from io import open
import six
# End: Python 2/3 compatability header small


###############################################################################
###############################################################################
###############################################################################


import matplotlib

import imp
import keras.backend as K
import keras.models
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time

import innvestigate
import innvestigate.utils as iutils
import innvestigate.utils.tests.networks.imagenet
import innvestigate.utils.visualizations as ivis


###############################################################################
###############################################################################
###############################################################################


base_dir = os.path.dirname(__file__)
eutils = imp.load_source("utils", os.path.join(base_dir, "utils.py"))


###############################################################################
###############################################################################
###############################################################################

if __name__ == "__main__":

    netname = sys.argv[1] if len(sys.argv) > 1 else "vgg16"
    pattern_type = False

    # Get some example test set images.
    images, label_to_class_name = eutils.get_imagenet_data()[:2]


    ###########################################################################
    # Build model.
    ###########################################################################
    tmp = getattr(innvestigate.applications.imagenet, netname)
    # todo: specify type of patterns:
    net = tmp(load_weights=True, load_patterns=pattern_type)
    model = keras.models.Model(inputs=net["in"], outputs=net["out"])
    model.compile(optimizer="adam", loss="categorical_crossentropy")
    modelp = keras.models.Model(inputs=net["in"], outputs=net["sm_out"])
    modelp.compile(optimizer="adam", loss="categorical_crossentropy")

    ###########################################################################
    # Utility functions.
    ###########################################################################
    color_conversion = "BGRtoRGB" if net["color_coding"] == "BGR" else None
    channels_first = K.image_data_format == "channels_first"

    def preprocess(X):
        X = X.copy()
        X = net["preprocess_f"](X)
        return X

    def postprocess(X):
        X = X.copy()
        X = iutils.postprocess_images(X,
                                      color_coding=color_conversion,
                                      channels_first=channels_first)
        return X

    def image(X):
        X = X.copy()
        return ivis.project(X, absmax=255.0, input_is_postive_only=True)

    def bk_proj(X):
        X = ivis.clip_quantile(X, 1)
        return ivis.project(X)

    def heatmap(X):
        X = ivis.gamma(X, minamp=0, gamma=0.95)
        return ivis.heatmap(X)

    def graymap(X):
        return ivis.graymap(np.abs(X), input_is_postive_only=True)


    def get_methods(netname):
        # NAME  POSTPROCESSING      TITLE
        # Show input.
        methods = [ ("input",                 {},                       image,   "Input"), ]
        if netname in ["vgg16", "vgg19"]:
            methods += [("lrp.z",                 {},                       heatmap, "LRP-Z"),
                        ("lrp.epsilon",           {"epsilon": 1e-1},         heatmap, "LRP-Epsilon 1e-1"),
                        ("lrp.epsilon",           {"epsilon": 10},         heatmap, "LRP-Epsilon 10"),
                        ("lrp.epsilon",           {"epsilon": 1e2},          heatmap, "LRP-Epsilon 1e2"),
                        ("lrp.alpha_2_beta_1",    {},                       heatmap, "LRP-A2B1"),
                        ("lrp.alpha_1_beta_0",    {},                       heatmap, "LRP-A1B0"),
                        ("lrp.composite_a",           {},                     heatmap, "LRP-CompositeA"),
                        ("lrp.composite_b",           {},                     heatmap, "LRP-CompositeB"),
                        ("lrp.composite_a_flat",      {},                     heatmap, "LRP-CompositeAFlat"),
                        ("lrp.composite_b_flat",      {},                     heatmap, "LRP-CompositeBFlat"),
            ]

        elif netname == "inception_v3":
            methods += [
                # NAME             POSTPROCESSING     TITLE
                ("lrp.z",                 {},                       heatmap, "LRP-Z")
                ("lrp.epsilon",           {"epsilon": 1},           heatmap, "LRP-Epsilon 1"),
                ("lrp.epsilon",           {"epsilon": 1e2},          heatmap, "LRP-Epsilon 1e2"),
                ("lrp.alpha_2_beta_1",    {},                       heatmap, "LRP-A2B1"),
                ("lrp.alpha_1_beta_0",    {},                       heatmap, "LRP-A1B0"),
                ("lrp.composite_a",           {},                     heatmap, "LRP-CompositeA"),
                ("lrp.composite_b",           {},                     heatmap, "LRP-CompositeB"),
                ("lrp.composite_a_flat",      {},                     heatmap, "LRP-CompositeAFlat"),
                ("lrp.composite_b_flat",      {},                     heatmap, "LRP-CompositeBFlat"),
            ]

        elif netname == "resnet50":
            methods += [
                # NAME             POSTPROCESSING     TITLE
                ("lrp.z",                 {},                       heatmap, "LRP-Z")
                ("lrp.epsilon",           {"epsilon": 1},           heatmap, "LRP-Epsilon 1"),
                ("lrp.epsilon",           {"epsilon": 1e2},          heatmap, "LRP-Epsilon 1e2"),
                ("lrp.alpha_2_beta_1",    {},                       heatmap, "LRP-A2B1"),
                ("lrp.alpha_1_beta_0",    {},                       heatmap, "LRP-A1B0"),
                ("lrp.composite_a",           {},                     heatmap, "LRP-CompositeA"),
                ("lrp.composite_b",           {},                     heatmap, "LRP-CompositeB"),
                ("lrp.composite_a_flat",      {},                     heatmap, "LRP-CompositeAFlat"),
                ("lrp.composite_b_flat",      {},                     heatmap, "LRP-CompositeBFlat"),
            ]

        else:
            methods += [
                # NAME             POSTPROCESSING     TITLE
                ("lrp.z",                 {},                       heatmap, "LRP-Z")
                ("lrp.epsilon",           {"epsilon": 1},           heatmap, "LRP-Epsilon 1"),
                ("lrp.epsilon",           {"epsilon": 1e2},          heatmap, "LRP-Epsilon 1e2"),
                ("lrp.alpha_2_beta_1",    {},                       heatmap, "LRP-A2B1"),
                ("lrp.alpha_1_beta_0",    {},                       heatmap, "LRP-A1B0"),
                ("lrp.composite_a",           {},                     heatmap, "LRP-CompositeA"),
                ("lrp.composite_b",           {},                     heatmap, "LRP-CompositeB"),
                ("lrp.composite_a_flat",      {},                     heatmap, "LRP-CompositeAFlat"),
                ("lrp.composite_b_flat",      {},                     heatmap, "LRP-CompositeBFlat"),
            ]
        return methods


    ###########################################################################
    # Analysis.
    ###########################################################################

    print(model.summary())#debug
    #collect all model layer classes
    all_layer_classes = list(set([l.__class__.__name__ for  l in model.layers]))
    print("{} contains the following layers: {}".format(netname, all_layer_classes))
    #exit() #debug

    patterns = net["patterns"]
    # Methods we use and some properties.
    methods = get_methods(netname)


    # Create analyzers.
    analyzers = []
    for method in methods:
        analyzers.append(innvestigate.create_analyzer(method[0],
                                                      model,
                                                      **method[1]))

    # Create analysis.
    analysis = np.zeros([len(images), len(analyzers), 224, 224, 3])
    text = []
    for i, (image, y) in enumerate(images):
        print ('Image {}: '.format(i), end='')
        image = image[None, :, :, :]
        # Predict label.
        x = preprocess(image)
        presm = model.predict_on_batch(x)[0]
        prob = modelp.predict_on_batch(x)[0]
        y_hat = prob.argmax()

        text.append((r"%s" % label_to_class_name[y],
                     r"%.2f" % presm.max(),
                     r"(%.2f)" % prob.max(),
                     r"%s" % label_to_class_name[y_hat]))

        for aidx, analyzer in enumerate(analyzers):
            #measure execution time
            t_start = time.time()
            print('{} '.format(methods[aidx][-1]), end='')

            is_input_analyzer = methods[aidx][0] == "input"
            # Analyze.
            a = analyzer.analyze(image if is_input_analyzer else x)

            t_elapsed = time.time() - t_start
            print('({:.4f}s) '.format(t_elapsed), end='')

            # Postprocess.
            if not np.all(np.isfinite(a)):
                print("Image %i, analysis of %s not finite: nan %s inf %s" %
                      (i, methods[aidx][3],
                       np.any(np.isnan(a)), np.any(np.isinf(a))))
            if not is_input_analyzer:
                a = postprocess(a)
            a = methods[aidx][2](a)
            analysis[i, aidx] = a[0]
        print('')

    ###########################################################################
    # Plot the analysis.
    ###########################################################################

    grid = [[analysis[i, j] for j in range(analysis.shape[1])]
            for i in range(analysis.shape[0])]
    row_labels = text
    col_labels = [method[3] for method in methods]

    eutils.plot_image_grid(grid, row_labels, col_labels,
                           row_label_offset=50,
                           col_label_offset=-50,
                           usetex=False,
                           is_fontsize_adaptive=False,
                           file_name="imagenet_lrp_%s.pdf" % netname)

    #clean shutdown for tf.
    if K.backend() == 'tensorflow':
        K.clear_session()
