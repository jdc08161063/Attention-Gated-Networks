import torchvision.models as models
from .unet_2D import *
from .unet_3D import *
from .unet_nonlocal_2D import *
from .unet_nonlocal_3D import *
from .unet_grid_attention_3D import *
from .unet_CT_dsv_3D import *
from .unet_CT_single_att_dsv_2_3D import *
from .unet_CT_multi_att_dsv_3D import *
from .unet_CT_multi_att_dsv_2_3D import *
from .unet_CT_multi_att_dsv_2_demo_3D import *
from .unet_CT_multi_att_dsv_4_3D import *
from .unet_CT_multi_att_dsv_4_demo_3D import *

def get_network(name, n_classes, in_channels=3, feature_scale=4, tensor_dim='2D',
                nonlocal_mode='embedded_gaussian', attention_dsample=(2,2,2)):
    model = _get_model_instance(name, tensor_dim)

    if name in ['unet', 'unet_ct_dsv']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      feature_scale=feature_scale,
                      is_deconv=False)
    elif name in ['unet_nonlocal']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      is_deconv=False,
                      nonlocal_mode=nonlocal_mode,
                      feature_scale=feature_scale)
    elif name in ['unet_grid_gating', 'unet_ct_multi_att_dsv',
                  'unet_ct_single_att_dsv_2',
                  'unet_ct_multi_att_dsv_2', 'unet_ct_multi_att_dsv_2_demo',
                  'unet_ct_multi_att_dsv_4', 'unet_ct_multi_att_dsv_4_demo']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      nonlocal_mode=nonlocal_mode,
                      feature_scale=feature_scale,
                      attention_dsample=attention_dsample,
                      is_deconv=False)
    else:
        raise 'Model {} not available'.format(name)

    return model


def _get_model_instance(name, tensor_dim):
    return {
        'unet':{'2D': unet_2D, '3D': unet_3D},
        'unet_nonlocal':{'2D': unet_nonlocal_2D, '3D': unet_nonlocal_3D},
        'unet_grid_gating': {'3D': unet_grid_attention_3D},
        'unet_ct_dsv': {'3D': unet_CT_dsv_3D},
        'unet_ct_single_att_dsv_2': {'3D': unet_CT_single_att_dsv_2_3D},
        'unet_ct_multi_att_dsv': {'3D': unet_CT_multi_att_dsv_3D},
        'unet_ct_multi_att_dsv_2': {'3D': unet_CT_multi_att_dsv_2_3D},
        'unet_ct_multi_att_dsv_2_demo': {'3D': unet_CT_multi_att_dsv_2_demo_3D},
        'unet_ct_multi_att_dsv_4': {'3D': unet_CT_multi_att_dsv_4_3D},
        'unet_ct_multi_att_dsv_4_demo': {'3D': unet_CT_multi_att_dsv_4_demo_3D},
    }[name][tensor_dim]
