from akida.core import LayerType, PoolingType, NsocVersion, ConvolutionMode
import numpy as np


def summary_hardware_incompatibilities(model, nsoc_version=None):
    """Checks a model compatibility with hardware and prints a summary.

    This method performs parameters value checking for hardware
    compatibility and prints incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    """
    incompatibilities = model_hardware_incompatibilities(model, nsoc_version)
    if incompatibilities:
        print("Hardware incompatibilities:")
    print("\n".join(incompatibilities))


def model_hardware_incompatibilities(model, nsoc_version=None):
    """Checks a model compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        a list of str containing the hardware incompatibilities of the model.
        The list is empty if the model is hardware compatible.

    """
    incompatibilities = []
    for i in range(model.get_layer_count()):
        layer_incompatibility = layer_hardware_incompatibilities(
            model, i, nsoc_version)
        if layer_incompatibility:
            incompatibilities.append(layer_incompatibility)
    return incompatibilities


def layer_hardware_incompatibilities(model, layer_index, nsoc_version=None):
    """Checks a layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilityes of the layer.
        Empty string if the layer is hardware compatible.

    """

    def get_max_num_filters(kernel_size, rgb):
        if rgb:
            if kernel_size == 3:
                return 192
            if kernel_size == 5:
                return 64
            if kernel_size == 7:
                return 32
            return 0

        if kernel_size == 3:
            return 512
        if kernel_size == 5:
            return 192
        if kernel_size == 7:
            return 96
        return 0

    def full_message(layer_name, msg_list):

        if len(msg_list) > 0:
            return str("Layer " + layer_name + " is not compatible with "
                       "hardware: \n" + "\n".join(msg_list))
        return str()

    layer = model.get_layer(layer_index)
    hw_msg = []
    # inputData layer
    if layer.parameters.layer_type == LayerType.InputData:
        return str()

    if layer.parameters.activations_params.threshold_fire_bits not in [1, 2, 4]:
        hw_msg.append(
            "- unsupported threshold_fire_bits, supported "
            "values are [1, 2, 4], currently at " +
            str(layer.parameters.activations_params.threshold_fire_bits))

    if layer.parameters.activations_params.threshold_fire not in range(
            -2**19, 2**19):
        hw_msg.append("- unsupported threshold_fire, it must fit in 20 bits")

    # fullyConnected layer
    if layer.parameters.layer_type == LayerType.FullyConnected:
        if layer.parameters.weights_bits not in [1, 2, 3, 4]:
            hw_msg.append("- weights_bits must be in [1, 2, 3, 4], "
                          "currently at " + str(layer.parameters.weights_bits))
        if layer_index > 0:
            previous_params = model.get_layer(layer_index - 1).parameters
            if "activations_params" in dir(previous_params):
                # Allowed input bitwidth
                allowed_input_bw = [1, 2]
                if nsoc_version != NsocVersion.v1:
                    allowed_input_bw.append(4)
                input_bw = previous_params.activations_params.threshold_fire_bits
                if input_bw not in allowed_input_bw:
                    hw_msg.append("- unsupported input dimensions. "
                                  "threshold_fire_bits in previous layer "
                                  "must be in " + str(allowed_input_bw) +
                                  ", currently at " + str(input_bw))
        if nsoc_version == NsocVersion.v1:
            num_neurons = layer.parameters.num_neurons
            if num_neurons < 3 and layer.parameters.activations_params.activations_enabled:
                hw_msg.append("- learn requires at least 3 neurons, "
                              "currently at " + str(num_neurons))
        return full_message(layer.name, hw_msg)

    # define aliases for readbility
    kw = layer.parameters.kernel_width
    kh = layer.parameters.kernel_height
    sx = layer.parameters.stride_x
    sy = layer.parameters.stride_y
    pw = layer.parameters.pooling_width
    ph = layer.parameters.pooling_height
    psx = layer.parameters.pooling_stride_x
    psy = layer.parameters.pooling_stride_y

    # inputConvolutional layer
    if layer.parameters.layer_type == LayerType.InputConvolutional:
        if kw != kh:
            hw_msg.append("- kernel_width and kernel_height must be "
                          "equal, currently at " + str(kw) + " and " + str(kh))
        if kw not in [3, 5, 7]:
            hw_msg.append("- kernel_width must be in [3, 5, 7], "
                          "currently at " + str(kw))
        if sx not in [1, 2, 3]:
            hw_msg.append("- stride_x must be in [1, 2, 3], "
                          "currently at " + str(sx))
        if sy not in [1, 2, 3]:
            hw_msg.append("- stride_y must be in [1, 2, 3], "
                          "currently at " + str(sy))
        # check number of neurons
        rgb = (layer.parameters.input_channels == 3)
        num_neurons = layer.parameters.num_neurons
        max_num_filters = get_max_num_filters(kw, rgb)
        if num_neurons < 1 or num_neurons > max_num_filters:
            hw_msg.append("- num_neurons should be set between 1 and " +
                          str(max_num_filters))
        # check input width limitations
        max_line_width = 256
        if layer.parameters.input_width > max_line_width:
            hw_msg.append("- input width cannot be higher than " +
                          str(max_line_width))
        if (layer.parameters.convolution_mode
                not in [ConvolutionMode.Same, ConvolutionMode.Valid]):
            hw_msg.append("- convolution_mode must be "
                          "ConvolutionMode.Same or "
                          "ConvolutionMode.Valid")
        # NSOC-V1: valid conv with stride != 1 is not supported for now
        if (nsoc_version == NsocVersion.v1 and
                layer.parameters.convolution_mode == ConvolutionMode.Valid and
            (sx > 1 or sy > 1)):
            hw_msg.append("- Convolution stride must be 1 when having "
                          "convolution mode 'VALID' for NsocVersion.v1")
        if layer.parameters.pooling_type == PoolingType.Max:
            if pw not in [1, 2]:
                hw_msg.append("- pooling_width must be in [1, 2], "
                              "currently at " + str(pw))
            if ph not in [1, 2]:
                hw_msg.append("- pooling_height must be in [1, 2], "
                              "currently at " + str(pw))
            if psx != psy:
                hw_msg.append("- pooling_stride_x and pooling_stride_y "
                              "must be equal, currently at " + str(psx) +
                              " and " + str(psy))
            if psx != 2:
                hw_msg.append("- pooling_stride_x must be 2, currently at " +
                              str(sx))
        elif layer.parameters.pooling_type == PoolingType.Average:
            hw_msg.append("- average pooling_type not supported")
        # check if we want to enable wta and if wta is hw compatible
        if layer.parameters.activations_params.activations_enabled:
            wta = layer.get_variable('wta_groups')
            if not np.array_equal(wta, np.sort(wta)):
                hw_msg.append(" - Only consecutives neurons are allowed "
                              "in the same WTA group.")

    # convolutional layers
    elif (layer.parameters.layer_type
          in [LayerType.Convolutional, LayerType.SeparableConvolutional]):
        wb = layer.parameters.weights_bits

        if kw != kh:
            hw_msg.append("- kernel_width and kernel_height must be "
                          "equal, currently at " + str(kw) + " and " + str(kh))
        if sx != 1:
            hw_msg.append("- stride_x must be set to 1, "
                          "currently at " + str(sx))
        if sy != 1:
            hw_msg.append("- stride_y must be set to 1, "
                          "currently at " + str(sy))
        if layer.parameters.convolution_mode != ConvolutionMode.Same:
            hw_msg.append("convolution_mode must be ConvolutionMode.Same")
        if layer.parameters.pooling_type == PoolingType.Max:
            # Max pooling forbidden if it is not followed by another NP
            layers_vert_pool = [
                LayerType.Convolutional, LayerType.SeparableConvolutional
            ]
            if nsoc_version != NsocVersion.v1:
                layers_vert_pool.append(LayerType.FullyConnected)
            if (layer_index == model.get_layer_count() - 1 or
                    model.get_layer(layer_index + 1).parameters.layer_type
                    not in layers_vert_pool):
                types = [str(lt).split('.')[-1] for lt in layers_vert_pool]
                types_str = ", ".join(types)
                hw_msg.append("- max pooling on convolutional or separable"
                              " convolutional layer must be followed by"
                              " another layer of one of these types: " +
                              types_str)
            if pw != ph:
                hw_msg.append("- pooling_width and pooling_height must "
                              "be equal, currently at " + str(pw) + " and " +
                              str(ph))
            if pw not in [2, 3]:
                hw_msg.append("- pooling_width must be in [2, 3], "
                              "currently at " + str(pw))
            if psx != psy:
                hw_msg.append("- pooling_stride_x and pooling_stride_y"
                              " must be equal, currently at " + str(psx) +
                              " and " + str(psy))
            if pw == 2 and psx not in [1, 2]:
                hw_msg.append("- pooling_stride_x must be in [1, 2] "
                              "for 2x2 pooling, currently at " + str(psx))
            if pw == 3 and psx not in [1, 2, 3]:
                hw_msg.append("- pooling_stride_x must be in [1, 2, 3] "
                              "for 3x3 pooling, currently at " + str(psx))
            if pw > layer.input_dims[0] or pw > layer.input_dims[1]:
                hw_msg.append(
                    "- pooling size must be lower than or equal to input dimensions"
                )
        elif layer.parameters.pooling_type == PoolingType.Average:
            if pw != -1 and ph != -1:
                hw_msg.append("- only global average pooling is supported:"
                              " pooling_width and pooling height must be "
                              "set to -1 (default)")
            if (nsoc_version == NsocVersion.v1 and
                    layer.parameters.num_neurons % 8 != 0):
                hw_msg.append("- with average pooling, number of neurons must"
                              " be a multiple of 8")
            if layer.input_dims[0] > 32:
                hw_msg.append("- with average pooling, the maximum input width"
                              " is 32")
        if layer.parameters.layer_type == LayerType.SeparableConvolutional:
            if kw not in [3, 5, 7]:
                hw_msg.append("- kernel_width must be in [3, 5, 7], "
                              "currently at " + str(kw))
            if wb not in [2, 4]:
                hw_msg.append("- weights_bits must be in [2, 4], "
                              "currently at " + str(wb))
        elif layer.parameters.layer_type == LayerType.Convolutional:
            if kw not in [1, 3, 5, 7]:
                hw_msg.append("- kernel_width must be in [1, 3, 5, 7], "
                              "currently at " + str(kw))
            if wb not in [1, 2]:
                hw_msg.append("- weights_bits must be in [1, 2], "
                              "currently at " + str(wb))
    return full_message(layer.name, hw_msg)
