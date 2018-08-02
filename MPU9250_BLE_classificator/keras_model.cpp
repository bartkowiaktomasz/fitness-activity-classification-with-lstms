/*
 * Copyright (c) 2016 Robert W. Rose
 *
 * MIT License, see LICENSE file.
 */

#include "keras_model.h"
#include "LSTM_model.h"

#include <cmath>
#include <limits>
#include <stdio.h>

bool KerasLayerActivation::LoadActivation(ActivationType activation_) {
    switch (activation_) {
    case kLinear:
        activation_type_ = kLinear;
        break;
    case kRelu:
        activation_type_ = kRelu;
        break;
    case kSoftPlus:
        activation_type_ = kSoftPlus;
        break;
    case kHardSigmoid:
        activation_type_ = kHardSigmoid;
        break;
    case kSigmoid:
        activation_type_ = kSigmoid;
        break;
    case kTanh:
        activation_type_ = kTanh;
        break;
    default:
        KASSERT(false, "Unsupported activation type %d", activation_);
    }

    return true;
}

bool KerasLayerActivation::Apply(Tensor* in, Tensor* out) {
    KASSERT(in, "Invalid input");
    KASSERT(out, "Invalid output");

    *out = *in;

    switch (activation_type_) {
    case kLinear:
        break;
    case kRelu:
        for (size_t i = 0; i < out->data_.size(); i++) {
            if (out->data_[i] < 0.0) {
                out->data_[i] = 0.0;
            }
        }
        break;
    case kSoftPlus:
        for (size_t i = 0; i < out->data_.size(); i++) {
            out->data_[i] = std::log(1.0 + std::exp(out->data_[i]));
        }
        break;
    case kHardSigmoid:
        for (size_t i = 0; i < out->data_.size(); i++) {
            float x = (out->data_[i] * 0.2) + 0.5;

            if (x <= 0) {
                out->data_[i] = 0.0;
            } else if (x >= 1) {
                out->data_[i] = 1.0;
            } else {
                out->data_[i] = x;
            }
        }
        break;
    case kSigmoid:
        for (size_t i = 0; i < out->data_.size(); i++) {
            float& x = out->data_[i];

            if (x >= 0) {
                out->data_[i] = 1.0 / (1.0 + std::exp(-x));
            } else {
                float z = std::exp(x);
                out->data_[i] = z / (1.0 + z);
            }
        }
        break;
    case kTanh:
        for (size_t i = 0; i < out->data_.size(); i++) {
            out->data_[i] = std::tanh(out->data_[i]);
        }
        break;
    default:
        break;
    }

    return true;
}

bool KerasLayerDense::LoadLayer() {
    unsigned int weights_rows = DENSE_WEIGHTS_ROWS;
    unsigned int weights_cols = DENSE_WEIGHTS_COLS;
    unsigned int biases_shape = DENSE_BIASES_SHAPE;

    weights_.Resize(weights_rows, weights_cols);
    weights_.data_ = DENSE_WEIGHTS;
    biases_.Resize(biases_shape);
    biases_.data_ = DENSE_BIASES;
    activation_.LoadActivation(ActivationType::kSigmoid);
    return true;
}

bool KerasLayerDense::Apply(Tensor* in, Tensor* out) {
    KASSERT(in, "Invalid input");
    KASSERT(out, "Invalid output");
    KASSERT(in->dims_.size() <= 2, "Invalid input dimensions");

    if (in->dims_.size() == 2) {
        KASSERT(in->dims_[1] == weights_.dims_[0], "Dimension mismatch %d %d",
                in->dims_[1], weights_.dims_[0]);
    }

    Tensor tmp(weights_.dims_[1]);

    for (int i = 0; i < weights_.dims_[0]; i++) {
        for (int j = 0; j < weights_.dims_[1]; j++) {
            tmp(j) += (*in)(i)*weights_(i, j);
        }
    }

    for (int i = 0; i < biases_.dims_[0]; i++) {
        tmp(i) += biases_(i);
    }

    KASSERT(activation_.Apply(&tmp, out), "Failed to apply activation");

    return true;
}

bool KerasLayerLSTM::LoadLayer() {
    unsigned int wi_rows = W_i_ROWS;
    unsigned int wi_cols = W_i_COLS;
    unsigned int ui_rows = U_i_ROWS;
    unsigned int ui_cols = U_i_COLS;
    unsigned int bi_shape = b_i_SHAPE;
    unsigned int wf_rows = W_f_ROWS;
    unsigned int wf_cols = W_f_COLS;
    unsigned int uf_rows = U_f_ROWS;
    unsigned int uf_cols = U_f_COLS;
    unsigned int bf_shape = b_f_SHAPE;
    unsigned int wc_rows = W_c_ROWS;
    unsigned int wc_cols = W_c_COLS;
    unsigned int uc_rows = U_c_ROWS;
    unsigned int uc_cols = U_c_COLS;
    unsigned int bc_shape = b_c_SHAPE;
    unsigned int wo_rows = W_o_ROWS;
    unsigned int wo_cols = W_o_COLS;
    unsigned int uo_rows = U_o_ROWS;
    unsigned int uo_cols = U_o_COLS;
    unsigned int bo_shape = b_o_SHAPE;

    // Load Input Weights and Biases
    Wi_.Resize(wi_rows, wi_cols);
    Ui_.Resize(ui_rows, ui_cols);
    bi_.Resize(1, bi_shape);
    Wi_.data_ = W_i;
    Ui_.data_ = U_i;
    bi_.data_ = b_i;

    // Load Forget Weights and Biases
    Wf_.Resize(wf_rows, wf_cols);
    Uf_.Resize(uf_rows, uf_cols);
    bf_.Resize(1, bf_shape);
    Wf_.data_ = W_f;
    Uf_.data_ = U_f;
    bf_.data_ = b_f;

    // Load State Weights and Biases
    Wc_.Resize(wc_rows, wc_cols);
    Uc_.Resize(uc_rows, uc_cols);
    bc_.Resize(1, bc_shape);
    Wc_.data_ = W_c;
    Uc_.data_ = U_c;
    bc_.data_ = b_c;

    // Load Output Weights and Biases
    Wo_.Resize(wo_rows, wo_cols);
    Uo_.Resize(uo_rows, uo_cols);
    bo_.Resize(1, bo_shape);
    Wo_.data_ = W_o;
    Uo_.data_ = U_o;
    bo_.data_ = b_o;

    innerActivation_.LoadActivation(ActivationType::kHardSigmoid);
    activation_.LoadActivation(ActivationType::kTanh);
    return_sequences_ = (bool)RETURN_SEQUENCES;

    return true;
}

bool KerasLayerLSTM::Apply(Tensor* in, Tensor* out) {
    // Assume bo always keeps the output shape and we will always receive one
    // single sample.
    int outputDim = bo_.dims_[1];
    Tensor ht_1 = Tensor(1, outputDim);
    Tensor ct_1 = Tensor(1, outputDim);

    ht_1.Fill(0.0f);
    ct_1.Fill(0.0f);

    int steps = in->dims_[0];

    Tensor outputs, lastOutput;

    if (return_sequences_) {
        outputs.dims_ = {steps, outputDim};
        outputs.data_.reserve(steps * outputDim);
    }

    for (int s = 0; s < steps; s++) {
        Tensor x = in->Select(s);

        KASSERT(Step(&x, &lastOutput, &ht_1, &ct_1), "Failed to execute step");

        if (return_sequences_) {
            outputs.data_.insert(outputs.data_.end(), lastOutput.data_.begin(),
                                 lastOutput.data_.end());
        }
    }

    if (return_sequences_) {
        *out = outputs;
    } else {
        *out = lastOutput;
    }

    return true;
}

bool KerasLayerLSTM::Step(Tensor* x, Tensor* out, Tensor* ht_1, Tensor* ct_1) {
    Tensor xi = x->Dot(Wi_) + bi_;
    Tensor xf = x->Dot(Wf_) + bf_;
    Tensor xc = x->Dot(Wc_) + bc_;
    Tensor xo = x->Dot(Wo_) + bo_;

    Tensor i_ = xi + ht_1->Dot(Ui_);
    Tensor f_ = xf + ht_1->Dot(Uf_);
    Tensor c_ = xc + ht_1->Dot(Uc_);
    Tensor o_ = xo + ht_1->Dot(Uo_);

    Tensor i, f, cc, o;

    KASSERT(innerActivation_.Apply(&i_, &i),
            "Failed to apply inner activation on i");
    KASSERT(innerActivation_.Apply(&f_, &f),
            "Failed to apply inner activation on f");
    KASSERT(activation_.Apply(&c_, &cc), "Failed to apply activation on c_");
    KASSERT(innerActivation_.Apply(&o_, &o),
            "Failed to apply inner activation on o");

    *ct_1 = f.Multiply(*ct_1) + i.Multiply(cc);

    KASSERT(activation_.Apply(ct_1, &cc), "Failed to apply activation on c");
    *out = *ht_1 = o.Multiply(cc);

    return true;
}

bool KerasModel::LoadModel() {
    unsigned int num_layers = NUM_LAYERS;

    LayerType layer_types[2] = {LayerType::kLSTM, LayerType::kDense};
    for (unsigned int i = 0; i < num_layers; i++) {
        LayerType layer_type = layer_types[i];
        KerasLayer* layer = NULL;

        switch (layer_type) {
        case kDense:
            layer = new KerasLayerDense();
            break;
        case kActivation:
            layer = new KerasLayerActivation();
            break;
        case kLSTM:
            layer = new KerasLayerLSTM();
            break;
        default:
            break;
        }

        bool result = layer->LoadLayer();
        if (!result) {
            printf("Failed to load layer %d", i);
            delete layer;
            return false;
        }

        layers_.push_back(layer);
    }

    return true;
}

bool KerasModel::Apply(Tensor* in, Tensor* out) {
    Tensor temp_in, temp_out;

    for (unsigned int i = 0; i < layers_.size(); i++) {
        if (i == 0) {
            temp_in = *in;
        }

        KASSERT(layers_[i]->Apply(&temp_in, &temp_out),
                "Failed to apply layer %d", i);

        temp_in = temp_out;
    }

    *out = temp_out;

    return true;
}
