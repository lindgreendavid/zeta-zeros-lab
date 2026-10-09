import data from "./registry.json";

export interface BlockStats {
  n_spacings: number;
  mean_spacing: number;
  variance: number;
  small_fraction: number;
  ks_gue: number;
  ks_poisson: number;
  r2_rms_gue: number;
  r2_rms_poisson: number;
}

export interface Block {
  first_index: number;
  n_zeros: number;
  gamma_min: number;
  gamma_max: number;
  max_count_offset: number;
  stats: BlockStats;
  spacing_histogram: number[];
  pair_correlation: number[];
}

export interface Band {
  q025: number;
  q500: number;
  q975: number;
}

export interface Registry {
  small_spacing_cutoff: number;
  blocks: Record<"low" | "high", Block>;
  reference: {
    gue_spacing_mean: number;
    gue_spacing_variance: number;
    gue_small_fraction: number;
    poisson_small_fraction: number;
    spacing_grid: number[];
    gue_pdf: number[];
    gue_cdf: number[];
    poisson_pdf: number[];
    pair_centers: number[];
    gue_pair_correlation: number[];
    gue_pair_correlation_curve_x: number[];
    gue_pair_correlation_curve: number[];
  };
  simulated_gue_null: {
    n_replicates: number;
    seed: number;
    n_spacings: number;
    ks_gue: Band;
    r2_rms_gue: Band;
    variance: Band;
    small_fraction: Band;
  };
  samples: Record<"zeta" | "poisson" | "gue", number[]>;
  hypotheses: {
    H1: { per_block: Record<string, boolean>; confirmed: boolean };
    H2: { per_block: Record<string, boolean>; confirmed: boolean };
    H3: { per_block: Record<string, Record<string, boolean>>; confirmed: boolean };
    H4: { checks: Record<string, boolean>; confirmed: boolean };
  };
}

export const registry = data as unknown as Registry;
