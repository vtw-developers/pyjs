import matplotlib.pyplot as plt
import numpy as np
from typing import List

import e_common
import p_consts


def rq1_gfg_subtree_trans_success_rate(
  success_rates_per_model: List[List[float]],
  num_bins: int = p_consts.PLT_NUM_BINS,
  model_names: List[str] = p_consts.PLT_MODEL_NAMES,
  colors: List[str] = p_consts.PLT_COLORS,
  markers: List[str] = p_consts.PLT_MARKERS,
):
  '''
  Results for RQ1 on subtree-translation success-rate. The x-axis shows the bins
  of subtree-translation success-rates (in percent), and the y-axis shows the number of
  functions whose subtree-translation success rate falls into the corresponding bin.

  Dimensions of success_rates_per_model: num_models x num_samples

  NOTE subtree translation rate will be 100% for subjects that were succesfully translated.

  '''
  num_models = len(success_rates_per_model)
  assert num_models == len(model_names)
  assert num_models <= len(colors)
  for model_rates in success_rates_per_model:
    assert all(0.0 <= rate <= 1.0 for rate in model_rates), "All rates must be between 0.0 and 1.0"

  bins = [i / num_bins for i in range(num_bins + 1)]  # bins from 0.0 to 1.0

  plt.figure()
  for rates, color, label, marker in zip(success_rates_per_model, colors, model_names, markers):
    counts, bin_edges = np.histogram(rates, bins=bins)
    plt.plot(bin_edges[:-1], counts, marker=marker, color=color, label=label)

  plt.xlabel('Subtree-level Translation Success Rate')
  plt.ylabel('Count')
  plt.title('Distribution of Subtree-level Translation Success Rates')
  plt.grid(True)
  plt.legend()
  plt.savefig('rq1_subtree_trans_success_rate_gfg.png')


if __name__ == '__main__':
  data = e_common.generate_random_float_matrix()
  rq1_gfg_subtree_trans_success_rate(data, p_consts.PLT_MODEL_NAMES)
