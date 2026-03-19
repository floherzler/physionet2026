# BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep

Saurav Raj Pandey1
  
Harlin Lee2

1Department of Computer Science, UNC Chapel Hill, Chapel Hill, NC, USA
  
2School of Data Science and Society, UNC Chapel Hill, Chapel Hill, NC, USA
  
srpandey@unc.edu, harlin@unc.edu

###### Abstract

We present BiTimeCrossNet (BTCNet), a multimodal self-supervised learning framework for long physiological recordings such as overnight sleep studies. While many existing approaches train on short segments treated as independent samples, BTCNet incorporates information about when each segment occurs within its parent recording, for example within a sleep session. BTCNet further learns pairwise interactions between physiological signals via cross-attention, without requiring task labels or sequence-level supervision.

We evaluate BTCNet on pediatric sleep data across six downstream tasks, including sleep staging, arousal detection, and respiratory event detection. Under frozen-backbone linear probing, BTCNet consistently outperforms an otherwise identical non–time-aware variant, with gains that generalize to an independent pediatric dataset. Compared to existing multimodal self-supervised sleep models, BTCNet achieves strong performance, particularly on respiration-related tasks.




## 1 Introduction

Sleep plays a critical role in physical and mental health in childhood. Disrupted sleep has been associated with adverse outcomes including anxiety, depression, hypertension, impaired academic performance, and behavioral difficulties [[22](https://arxiv.org/html/2602.02769v1#bib.bib28 "Short- and long-term health consequences of sleep disruption")]. In clinical practice, sleep is most commonly assessed using polysomnography (PSG), an overnight study that records multiple physiological signals such as electroencephalography (EEG), electrooculography (EOG), and respiratory and cardiac measurements. These recordings are manually reviewed and annotated by trained sleep technicians to identify sleep stages and clinically relevant events, including oxygen desaturations and respiratory disturbances. While effective, this process is labor-intensive, costly, and difficult to scale.

![Refer to caption](x1.png)

Figure 1: 
PHATE visualization [[23](https://arxiv.org/html/2602.02769v1#bib.bib17 "Visualizing structure and transitions in high-dimensional biological data")] of frozen embeddings from BTCNet (time-aware) and BCNet (non-time-aware) for a representative patient using SPO2 and CAPNO signals. Each point is 30 seconds of sleep colored by time of night. The time-aware model exhibits a smoother and more coherent global structure compared to the non-time-aware model.

Recent advances in machine learning offer the potential to automate large portions of PSG analysis. However, models trained primarily on adult sleep data generalize poorly to pediatric populations, even for fundamental tasks such as sleep stage classification [[24](https://arxiv.org/html/2602.02769v1#bib.bib30 "Influence of channel selection and subject’s age on the performance of the single channel eeg-based automatic sleep staging algorithms")]. This performance gap reflects well-documented physiological differences between pediatric and adult sleep [[1](https://arxiv.org/html/2602.02769v1#bib.bib35 "Differences in overnight polysomnography scores using the adult and pediatric criteria for respiratory events in adolescents"), [25](https://arxiv.org/html/2602.02769v1#bib.bib36 "Pro:“not just little adults”: aasm should require pediatric accreditation for integrated sleep medicine programs serving both children (0-16 years) and adults")]. As a result, pediatric sleep analysis requires specific data and models that can capture age-specific sleep dynamics.

Self-supervised learning (SSL) provides a promising framework for learning representations from unlabeled PSG recordings using pretext objectives such as masked signal reconstruction. These representations can then be transferred to downstream tasks with substantially reduced annotation requirements. While SSL has achieved notable success in adult sleep modeling, its adoption in pediatric sleep remains limited. Moreover, existing SSL approaches are largely optimized for sleep stage classification [[29](https://arxiv.org/html/2602.02769v1#bib.bib4 "U-sleep: resilient high-frequency sleep staging"), [38](https://arxiv.org/html/2602.02769v1#bib.bib31 "DynamicSleepNet: a multi-exit neural network with adaptive inference time for sleep stage classification"), [16](https://arxiv.org/html/2602.02769v1#bib.bib20 "Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg"), [15](https://arxiv.org/html/2602.02769v1#bib.bib18 "BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of eeg data")]. In contrast, clinically important diagnostic tasks, such as apnea, hypopnea, and oxygen desaturation detection, have received comparatively little attention, despite their strong associations with cardiovascular and neurological outcomes [[39](https://arxiv.org/html/2602.02769v1#bib.bib37 "Adult obstructive sleep apnea/hypopnea syndrome: definitions, risk factors, and pathogenesis")].

A further limitation of existing SSL formulations is their reliance on short, fixed-duration temporal windows, for example 30-second epochs. Although convenient, this design ignores the fact that clinically meaningful sleep physiology evolves over the course of an entire night (Figure [1](https://arxiv.org/html/2602.02769v1#S1.F1 "Figure 1 ‣ 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep")). Respiratory stability, autonomic tone, and heart rate dynamics vary systematically across sleep cycles and circadian time [[5](https://arxiv.org/html/2602.02769v1#bib.bib38 "Sleep effects on breathing and respiratory diseases"), [34](https://arxiv.org/html/2602.02769v1#bib.bib39 "Heart rate variability, sleep and sleep disorders")]. Nevertheless, most SSL methods treat sleep windows as temporally independent samples, without encoding information about where a given window occurs within the broader trajectory of a sleep session.

##### Main Contributions

We introduce BiTimeCrossNet (BTCNet), a multimodal self-supervised learning (SSL) framework for pediatric polysomnography (PSG) that learns physiologically meaningful representations from heterogeneous signals with minimal manual annotation. BTCNet is pretrained on the Nationwide Children’s Hospital (NCH) Sleep Databank [[17](https://arxiv.org/html/2602.02769v1#bib.bib41 "A large collection of real-world pediatric sleep studies")] using a hybrid SSL objective that combines masked autoencoder [[11](https://arxiv.org/html/2602.02769v1#bib.bib1 "Masked autoencoders are scalable vision learners")] with contrastive learning. Our contributions are as follows:

* •

  We propose BTCNet, a pediatric multimodal SSL framework that learns transferable representations across heterogeneous physiological channels and supports six clinically relevant downstream tasks.
* •

  We introduce a novel random modality-pair cross-attention pretraining strategy, in which pairs (hence the prefix “Bi”) of physiological signals are randomly sampled at each iteration. This strategy encourages robust learning of inter-modal dependencies through a cross-attention mechanism and improves resilience to missing or noisy modalities.
* •

  We present a global time-aware positional conditioning mechanism that injects night-scale temporal context into transformer representations, enabling modeling of physiological dynamics over an entire sleep session. To our knowledge, this is the first incorporation of global time-of-sleep context into SSL for sleep analysis. We show that time-aware pretraining consistently improves AUROC and F1 across all six tasks and multiple modality combinations on NCH and an independent pediatric cohort (CHAT).
* •

  We demonstrate cross-dataset generalization by evaluating BTCNet out of the box on CHAT via linear probing, where it outperforms recent publicly available multimodal SSL models on oxygen desaturation and apnea-related detection tasks.




## 2 Related Work

Self-supervised learning (SSL) has become a dominant paradigm for learning transferable representations across domains. In the sleep domain, SSL efforts have mostly focused on uni-modal EEG-based representation learning, with a strong emphasis on sleep-stage classification, including BENDR [[15](https://arxiv.org/html/2602.02769v1#bib.bib18 "BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of eeg data")], EEGPT [[37](https://arxiv.org/html/2602.02769v1#bib.bib19 "Eegpt: pretrained transformer for universal and reliable representation of eeg signals")], and NeuroNet [[16](https://arxiv.org/html/2602.02769v1#bib.bib20 "Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg")]. Recent work has also explored multimodal SSL for sleep analysis, such as COCOA [[6](https://arxiv.org/html/2602.02769v1#bib.bib21 "Cocoa: cross modality contrastive learning for sensor data")], SleepFM [[35](https://arxiv.org/html/2602.02769v1#bib.bib22 "SleepFM: multi-modal representation learning for sleep across brain activity, ecg and respiratory signals")], and SynthSleepNet [[41](https://arxiv.org/html/2602.02769v1#bib.bib3 "CASleepNet: a cross attention-based multimodal fusion approach for sleep staging with eeg and eog")]. However, multimodal SSL techniques trained to analyze pediatric sleep are further limited. To our knowledge, PedSleepMAE [[26](https://arxiv.org/html/2602.02769v1#bib.bib15 "PedSleepMAE: generative model for multimodal pediatric sleep signals")] is the only existing SSL framework trained on large-scale pediatric PSG data (NCH Sleep Databank) for sleep-stage classification and related diagnostic tasks (e.g., apnea and hypopnea detection).

Recent work by [[40](https://arxiv.org/html/2602.02769v1#bib.bib14 "Uncovering trajectory and topological signatures in multimodal pediatric sleep embeddings")] demonstrates that session-level trajectory and topological features extracted from frozen PedSleepMAE embeddings can improve diagnostic performance. These findings suggest that global time-of-sleep structure contains clinically meaningful information, motivating our approach to incorporate time-of-sleep context directly into self-supervised pretraining rather than as a downstream augmentation.

BTCNet differs from most prior self-supervised sleep representation learning methods in several key ways.
First, MAE-based approaches such as PedSleepMAE, NeuroNet, and SynthSleepNet rely on standard local positional encodings and do not explicitly model global sleep-level temporal context during pretraining. In contrast, BTCNet, in addition to positional encodings, conditions representations on where a sleep window occurs within its full sleep session. Second, while most prior multimodal SSL methods are trained and evaluated under predefined modality configurations, BTCNet uses randomly sampled modality pairs with shared cross-attention, enabling flexible and task-specific channel selection (two channels only) at evaluation time. Finally, unlike SleepFM, which emphasizes missing-modality robustness via global modality alignment, BTCNet focuses on learning pairwise physiological interactions through cross-attention.




## 3 Methods

![Refer to caption]()

Figure 2: 
Overview of BTCNet.
Stage 1: Unimodal self-supervised pretraining using masked reconstruction and contrastive learning to obtain modality-specific encoders.
Stage 2: Cross-modal self-supervised learning with randomly sampled modality pairs, time-aware conditioning, and cross-attention.

We describe the dataset and the architecture of BTCNet along with our novel time-aware mechanism. BTCNet will be made open source upon acceptance of the paper.

### 3.1 Dataset and Preprocessing

#### 3.1.1 NCH Sleep Databank

BTCNet is pretrained on the Nationwide Children’s Hospital (NCH) Sleep Databank, a large publicly available pediatric polysomnography (PSG) dataset collected in real-world clinical settings [[17](https://arxiv.org/html/2602.02769v1#bib.bib41 "A large collection of real-world pediatric sleep studies")]. We analyze 2,379 overnight PSG recordings containing a consistent set of sixteen commonly available physiological channels, including EEG, EOG, and respiratory signals.

Expert annotations are provided at 30-second resolution, including sleep stages and clinically relevant events such as apnea, hypopnea, arousal, and oxygen desaturation. Each 30-second epoch is treated as an individual training example. Additional details are in Appendix [A](https://arxiv.org/html/2602.02769v1#A1 "Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

#### 3.1.2 CHAT Dataset

The Childhood Adenotonsillectomy Trial (CHAT) is a multi-center randomized controlled study of children with mild to moderate obstructive sleep apnea, with standardized overnight polysomnography and centralized scoring [[42](https://arxiv.org/html/2602.02769v1#bib.bib45 "The national sleep research resource: towards a sleep data commons"), [20](https://arxiv.org/html/2602.02769v1#bib.bib46 "A randomized trial of adenotonsillectomy for childhood sleep apnea")]. We use the baseline subset collected prior to any intervention.

To ensure compatibility with NCH, we restrict CHAT to the twelve overlapping physiological channels, which comprises of 422 PSGs. The CHAT dataset is used exclusively for external validation and cross-dataset generalization and is not used during BTCNet pretraining. Additional details are provided in Appendix [A.2](https://arxiv.org/html/2602.02769v1#A1.SS2 "A.2 Childhood Adenotonsillectomy Trial (CHAT) ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

### 3.2 BTCNet Architecture

In this section, we discuss the architecture of model BTCNet. BTCNet is trained in two stages: (1) unimodal self-supervised pretraining for each individual physiological modality, and (2) bimodal cross-modal pretraining using randomly sampled modality pairs. The second stage augments the signals with our novel time-aware structure and cross-attention, followed by self-supervised learning, enabling BTCNet to capture both modality-specific features and inter-modal dependencies. Figure [2](https://arxiv.org/html/2602.02769v1#S3.F2 "Figure 2 ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") displays this setup in detail.

### 3.3 Stage-1: Unimodal Self-Supervised Pretraining

Each of the physiological modalities is equipped with its own encoder, trained independently to capture modality-specific structure. Similar to NeuroNet’s masked prediction combined with a contrastive learning setup [[16](https://arxiv.org/html/2602.02769v1#bib.bib20 "Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg")], we adopt a self-supervised learning (SSL) framework combining masked reconstruction, following the Masked Autoencoder (MAE) objective [[11](https://arxiv.org/html/2602.02769v1#bib.bib1 "Masked autoencoders are scalable vision learners")], and a contrastive learning objective to obtain robust and modality-invariant representations.

#### 3.3.1 Masked Reconstruction

For each 30-second input signal xx of a given modality mm, we partition the sequence into PP non-overlapping patches and randomly mask a fixed fraction rr (50%) of them after adding token-wise positional embeddings.
The visible patches are processed by modality-specific Vision Transformers [[8](https://arxiv.org/html/2602.02769v1#bib.bib2 "An image is worth 16x16 words: transformers for image recognition at scale")], producing a latent sequence
𝐇𝐦∈ℝ(1−r)​P×D,\mathbf{H\_{m}}\in\mathbb{R}^{(1-r)P\times D},
where DD is the embedding dimension. A lightweight decoder then reconstructs the full set of PP patches (both visible and masked) from this latent representation. After pretraining, this decoder is discarded, and the pretrained encoder serves as the feature extractor for downstream stages.

#### 3.3.2 Contrastive Framework

To complement the reconstruction objective, we additionally train each encoder with a contrastive loss that encourages invariance across augmented views. For each signal xx, we construct two views: the original signal and a lightly perturbed version of the same signal.

Both views are processed by the same encoder, and we obtain their CLS tokens, which are projected into a contrastive space and optimized using the NT-Xent loss [[4](https://arxiv.org/html/2602.02769v1#bib.bib8 "A simple framework for contrastive learning of visual representations")]. This encourages representations from the same signal to align while separating different signals, yielding more discriminative and robust modality-specific embeddings.

#### 3.3.3 Combined Objective

The full pretraining objective for each modality is the weighted sum of the MAE reconstruction loss and the contrastive loss:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒtotal=ℒrec+λcon​ℒcon,\mathcal{L}\_{\text{total}}=\mathcal{L}\_{\text{rec}}+\lambda\_{\text{con}}\,\mathcal{L}\_{\text{con}}, |  | (1) |

where λcon\lambda\_{\text{con}} balances the two terms. This combination encourages the encoders to learn features that best represent the input signals while remaining consistent across random perturbations. All modalities are pretrained independently under this objective, producing a set of modality-specific encoders {fm}\{f\_{m}\} used in the next cross-modal interaction stage. Additional training details of this process are included in Appendix [B.1](https://arxiv.org/html/2602.02769v1#A2.SS1 "B.1 Stage 1: Unimodal Encoder Training ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

### 3.4 Stage-2: Cross-Modal Interaction and SSL

#### 3.4.1 Random Modality Selection and Bimodal Stacking

Once the per-modality encoders have been pretrained, we construct bimodal inputs for the cross-attention module. At each training iteration (i.e. for every mini-batch), we randomly select two distinct modalities from the full set, and index individual samples within the mini-batch by
ii. This sampling strategy ensures that the model is exposed to a wide range of modality combinations, promoting robustness to missing or noisy channels, common in clinical PSG recordings, and encouraging the model to learn generalizable cross-modal relationships.

Each selected modality is then encoded independently using its pretrained Stage-1 encoder fmf\_{m}, producing patch-level embeddings.

This yields the final bimodal tensor

|  |  |  |
| --- | --- | --- |
|  | 𝐙i∈ℝ2×P×D,\mathbf{Z}\_{i}\in\mathbb{R}^{2\times P\times D}, |  |

which serves as input to the bimodal cross-attention encoder.

Relation to prior randomness-based methods.
Randomness has previously been introduced into supervised sleep staging pipelines for robustness, but for fundamentally different objectives. For example, U-Sleep [[29](https://arxiv.org/html/2602.02769v1#bib.bib4 "U-sleep: resilient high-frequency sleep staging")] randomly samples EEG and EOG channels to promote invariance to electrode placement, while wav2sleep [[3](https://arxiv.org/html/2602.02769v1#bib.bib5 "Wav2sleep: a unified multi-modal approach to sleep stage classification from physiological signals")] applies random modality dropout to maintain performance under missing sensors.

In contrast, our approach randomly samples modality pairs from a diverse set of channels and explicitly trains cross-attention in a self-supervised setting. This design is intended to learn task-agnostic physiological relationships between modalities. Additional training details of Stage 2 are provided in Appendix [B.2](https://arxiv.org/html/2602.02769v1#A2.SS2 "B.2 Stage 2: Cross-Modal Interaction and SSL ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

#### 3.4.2 Global Time-Aware Conditioning

##### Standard Positional Encodings

Before passing the bimodal embeddings 𝐙i\mathbf{Z}\_{i} to the cross-attention module, we enrich each patch with positional structure. Prior work has shown that positional encodings are essential for sleep-related transformers. In particular, Shook et al. [[32](https://arxiv.org/html/2602.02769v1#bib.bib9 "STAMP: spatial-temporal adapter with multi-head pooling")] and Irani and Metsis [[14](https://arxiv.org/html/2602.02769v1#bib.bib10 "Positional encoding in transformer-based time series models: a survey. arxiv 2025")] evaluated combinations of spatial, temporal, and token encodings, with STAMP [[32](https://arxiv.org/html/2602.02769v1#bib.bib9 "STAMP: spatial-temporal adapter with multi-head pooling")] demonstrating that using *all three* components yields the best AUROC and Cohen’s κ\kappa on 3 of 4 EEG datasets. These findings suggest that richer positional structure improves physiological representation learning.

Motivated by this general insight, we incorporate the same triplet of learnable positional components. We denote by 𝐳i,j,p\mathbf{z}\_{i,j,p} the embedding of the pp-th patch from
modality jj for the ii-th sample in the mini-batch, and augment each patch as

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐳i,j,p←𝐳i,j,p+𝐬j+𝐭p+𝐧j,p,\mathbf{z}\_{i,j,p}\leftarrow\mathbf{z}\_{i,j,p}+\mathbf{s}\_{j}+\mathbf{t}\_{p}+\mathbf{n}\_{j,p}, |  | (2) |

where 𝐬j\mathbf{s}\_{j} is a spatial (modality-wise) embedding, 𝐭p\mathbf{t}\_{p} is a temporal (patch-wise) embedding, and 𝐧j,p\mathbf{n}\_{j,p} is a token-level embedding.

##### Global Time Conditioning

While the above positional encodings capture *local* temporal structure within each 30-second window, they do not reflect the *global* progression of a full-night sleep session. Physiological patterns evolve over the night (REM density increases, respiratory stability shifts, and arousal probability decreases) yet such long-range trends are inaccessible to patch-level positional encodings. Our time conditioning instead encodes where an entire window occurs within its parent sleep session. This allows otherwise identical windows to be seen differently based on their position within the night.

To incorporate this global context, we condition each example on its position within the sleep session. Each example corresponds to a fixed-length 30-second segment, and its position in the night can be described by the order in which it appears within the session. Let sei\mathrm{se}\_{i} denote this segment index for example ii. To account for differences in session length across patients, we standardize this index using statistics of session length computed over the dataset, where μsession\mu\_{\text{session}} and σsession\sigma\_{\text{session}} denote the mean and standard deviation of the number of examples per sleep session:

|  |  |  |  |
| --- | --- | --- | --- |
|  | t^i=sei−μsessionσsession\hat{t}\_{i}=\frac{\mathrm{se}\_{i}-\mu\_{\text{session}}}{\sigma\_{\text{session}}} |  | (3) |

A lightweight two-layer network maps t^i\hat{t}\_{i} to feature-wise scale and shift parameters (γi,βi)∈ℝD(\gamma\_{i},\beta\_{i})\in\mathbb{R}^{D}. These vectors are layer-normalized and gated by learnable scalar coefficients initialized to zero, ensuring an identity transformation at initialization and a smooth learning trajectory.

Finally, we apply a time-dependent affine modulation after the spatial, temporal, and token encodings:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐳i,j,p←γi⊙𝐳i,j,p+βi,\mathbf{z}\_{i,j,p}\leftarrow\gamma\_{i}\odot\mathbf{z}\_{i,j,p}+\beta\_{i}, |  | (4) |

introducing night-scale temporal structure that cannot be modeled by local positional encodings alone. While similar in form to FiLM-style conditioning [[28](https://arxiv.org/html/2602.02769v1#bib.bib11 "Film: visual reasoning with a general conditioning layer")], our focus is on the conditioning signal—global time-of-sleep—rather than the specific conditioning mechanism.

#### 3.4.3 Bimodal Cross-Attention and SSL

After enriching the bimodal tensor 𝐙i\mathbf{Z}\_{i} with the encodings from the previous section, we apply a second MAE-style masking step identical to the unimodal pretraining in Section [3.3](https://arxiv.org/html/2602.02769v1#S3.SS3 "3.3 Stage-1: Unimodal Self-Supervised Pretraining ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") and based on He et al. [[11](https://arxiv.org/html/2602.02769v1#bib.bib1 "Masked autoencoders are scalable vision learners")]. We randomly mask 50% of all patch tokens across both modalities and retain only the VV visible patches,
𝐙ivis∈ℝ2×V×D.\mathbf{Z}\_{i}^{\text{vis}}\in\mathbb{R}^{2\times V\times D}.

These visible tokens are processed by a bimodal cross-attention encoder, which performs two directional attention flows: each modality attends to the other’s remaining patches. This enables the model to capture physiologically meaningful relationships (e.g., SpO2–respiratory coupling, EOG–EMG co-interactions). Because modality pairs are sampled randomly at every batch, the cross-attention module learns broad, dataset-agnostic structure across all modalities.
The output is a fused cross-modal representation,
𝐙~i∈ℝ2×V×D,\tilde{\mathbf{Z}}\_{i}\in\mathbb{R}^{2\times V\times D},
which serves as input to the second-stage SSL objective.

Stage-2 pretraining uses the *same* self-supervised objectives as the unimodal encoders (masked reconstruction [[11](https://arxiv.org/html/2602.02769v1#bib.bib1 "Masked autoencoders are scalable vision learners")] and NT-Xent contrastive learning [[4](https://arxiv.org/html/2602.02769v1#bib.bib8 "A simple framework for contrastive learning of visual representations")]) but now applied to cross-attended representations. This encourages the model to learn embeddings that are jointly reconstructive, meaningfully aligned, and highly transferable. While prior work such as [[41](https://arxiv.org/html/2602.02769v1#bib.bib3 "CASleepNet: a cross attention-based multimodal fusion approach for sleep staging with eeg and eog")] has applied cross-attention in supervised sleep staging, these methods typically rely on only two modalities (e.g., EEG and EOG). In contrast, our framework integrates cross-attention within a self-supervised pipeline and supports a substantially broader set of physiological signals.

##### Gated Attention.

Within the cross-attention block, we additionally apply a sigmoid-gated transformation after the scaled dot-product operation. Prior work (e.g., [[30](https://arxiv.org/html/2602.02769v1#bib.bib6 "Gated attention for large language models: non-linearity, sparsity, and attention-sink-free")]) has shown that such gating introduces beneficial non-linearities and sparsity while mitigating attention collapse.

##### LoRA-based Fine-Tuning.

During Stage-2, all modality-specific encoders are fine-tuned using Low-Rank Adaptation (LoRA) [[13](https://arxiv.org/html/2602.02769v1#bib.bib7 "LoRA: low-rank adaptation of large language models")]. LoRA injects low-rank adapters into the attention projections while keeping the majority of parameters frozen, allowing efficient adaptation of the pretrained components without overfitting.

Together, these mechanisms yield rich representations that capture both modality-specific structure and robust inter-modal dependencies, forming a strong foundation for downstream sleep-related tasks.

Table 1: 
Comparison of the non–time-aware baseline (BCNet) and BTCNet across six downstream tasks.
For each task, we report the best-performing modality pair selected using BCNet only.
Prevalence (%Pos) is shown once per task for binary classification problems.
Results are averaged over three seeds and reported as mean (SD).

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task | %Pos | Modality Pair | BCNet (Non Time-Aware) | | | BTCNet | | |
|  |  |  | Acc (%) | AUROC (%) | F1 (%) | Acc (%) | AUROC (%) | F1 (%) |
| Oxygen Desaturation | 8.78 | CAPNO – SPO2 | 88.40 (0.14) | 78.92 (0.13) | 38.91 (0.18) | 89.92 (0.26) | 81.75 (0.15) | 44.80 (0.21) |
| Hypopnea | 1.97 | EEG F4-M1 – SPO2 | 96.43 (0.05) | 82.96 (0.12) | 25.35 (0.22) | 96.50 (0.24) | 86.13 (0.14) | 29.49 (0.10) |
| Apnea–Hypopnea | 2.80 | EEG F3-M2 – SPO2 | 96.16 (0.02) | 82.83 (0.17) | 31.40 (0.57) | 96.27 (0.10) | 86.04 (0.23) | 36.55 (0.04) |
| Apnea | 0.83 | SPO2 – EOG ROC-M1 | 97.93 (0.06) | 82.16 (0.38) | 17.46 (0.66) | 98.33 (0.06) | 85.11 (0.52) | 21.41 (1.09) |
| EEG-Arousal | 4.71 | EOG LOC-M2 – EMG CHIN1–CHIN2 | 90.70 (0.30) | 78.53 (0.21) | 27.78 (0.23) | 90.87 (0.32) | 81.82 (0.07) | 31.02 (0.25) |
| 5-stage Sleep Scoring | - | EEG C3-M2 – EOG ROC-M1 | 57.12 (0.34) | 79.90 (0.01) | 55.08 (0.61) | 60.98 (0.44) | 83.67 (0.05) | 59.83 (0.48) |




## 4 Experiments and Results

We demonstrate the effectiveness of BTCNet across multiple downstream tasks and datsets. Along with accuracy, AUROC and F1 score, event prevalence for each task is reported when appropriate to contextualize these metrics.

### 4.1 Effectiveness of Global Time-Aware Pretraining

#### 4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH

In this section, we evaluate BTCNet on multiple downstream sleep-related tasks on the NCH dataset and compare its performance to an otherwise identical variant that lacks global time-awareness, which we refer to as BCNet.

We first select informative modality pairs via a lightweight linear
probing sweep over all 120 possible channel pairs (see Appendix [D.1](https://arxiv.org/html/2602.02769v1#A4.SS1 "D.1 Modality Screening Procedure ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep")).
Importantly, modality selection is performed *only* using the non–time-aware baseline (BCNet). BTCNet is then evaluated on the exact same modality combinations. Because these channels are optimized for the weaker baseline rather than for BTCNet, any observed improvements cannot be attributed to favorable channel selection and instead directly reflect the impact of incorporating global time-aware positional structure during pretraining.

For downstream evaluation, we freeze BTCNet and train linear classifiers on top of its representations. Specifically, we extract the modality-specific CLS tokens from BTCNet, concatenate them into a 1024-dimensional embedding, and use this representation as input to a linear classifier. We repeat the same procedure for BCNet. Unless stated otherwise, this linear probing setup, using frozen embeddings derived from concatenated CLS tokens, is used consistently for all BTCNet and BCNet evaluations throughout the paper. All downstream evaluations use a consistent 80/10/10 split across methods.

Table [1](https://arxiv.org/html/2602.02769v1#S3.T1 "Table 1 ‣ LoRA-based Fine-Tuning. ‣ 3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") reports results for the single best-performing modality pair per task. Despite severe class imbalance across multiple binary tasks, both models exhibit strong linear separability, with BTCNet consistently achieving higher AUROC and F1 scores than BCNet across all six downstream tasks. Notably, these gains persist across all evaluated modality combinations in Appendix [D.3](https://arxiv.org/html/2602.02769v1#A4.SS3 "D.3 Additional Comparisons: BTCNet vs BCNet on NCH ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), indicating that the improvements are not driven by a single favorable channel pairing.

Because the encoders are frozen and the downstream models are linear, these improvements cannot be attributed to task-specific fine-tuning or increased model capacity. Instead, they reflect systematic differences in representation quality learned during pretraining. The consistent gains observed across diverse clinical tasks demonstrate that explicitly modeling global time structure leads to more robust, transferable, and clinically meaningful multimodal sleep representations.

Table 2: 
Linear probing performance on downstream tasks on the NCH test set. Binary tasks report Accuracy (Acc), AUROC, and F1. Sleep scoring reports Accuracy, weighted AUROC, and weighted F1. All metrics are expressed in % and averaged across two seeds and reported as mean (SD)

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Metric | Oxygen Desaturation | Hypopnea | Apnea-Hypopnea | Apnea | EEG-Arousal | Sleep Scoring |
| SleepFM (pool) | Acc | 82.2282.22 (7.52) | 97.5697.56 (0.12) | 95.7095.70 (1.58) | 96.4396.43 (1.76) | 94.8894.88 (0.51) | 71.9571.95 (0.25) |
| AUROC | 79.7279.72 (0.41) | 85.3685.36 (0.17) | 85.4285.42 (0.00) | 87.8887.88 (0.10) | 89.5189.51 (0.04) | 92.0092.00 (0.22) |
| F1 | 32.9432.94 (0.01) | 17.1817.18 (1.72) | 14.6614.66 (12.38) | 15.4415.44 (2.17) | 28.0228.02 (14.79) | 73.0973.09 (0.20) |
| SleepFM (no pool) | Acc | 86.5686.56 (3.18) | 92.5092.50 (2.21) | 85.2385.23 (2.66) | 87.7387.73 (10.38) | 94.6794.67 (0.30) | 70.9370.93 (1.27) |
| AUROC | 78.9278.92 (0.39) | 84.2584.25 (1.11) | 83.5383.53 (1.04) | 86.4986.49 (0.77) | 88.0888.08 (1.47) | 91.3891.38 (0.40) |
| F1 | 34.1934.19 (1.26) | 19.5519.55 (2.02) | 18.8018.80 (1.47) | 10.8610.86 (5.20) | 36.9136.91 (5.89) | 70.9770.97 (1.93) |
| PedSleepMAE | Acc | 84.0884.08 (0.00) | 95.0795.07 (0.15) | 94.0594.05 (0.51) | 97.4797.47 (0.11) | 90.3490.34 (0.01) | 71.8871.88 (1.60) |
| AUROC | 77.1877.18 (0.04) | 79.4779.47 (0.08) | 79.5279.52 (0.20) | 79.6279.62 (0.71) | 79.8179.81 (0.15) | 90.8290.82 (0.22) |
| F1 | 32.4832.48 (0.10) | 16.7916.79 (0.26) | 20.6720.67 (0.50) | 10.8310.83 (0.25) | 28.8828.88 (0.61) | 71.9371.93 (0.65) |
| BTCNet (ours) | Acc | 89.9789.97 (0.13) | 96.9396.93 (0.01) | 96.3696.36 (0.21) | 98.1698.16 (0.12) | 90.7890.78 (0.28) | 61.9861.98 (0.39) |
| AUROC | 81.9581.95 (0.14) | 86.6186.61 (0.08) | 86.0386.03 (0.19) | 85.0385.03 (0.62) | 81.1681.16 (0.13) | 84.5284.52 (0.01) |
| F1 | 44.9544.95 (0.52) | 29.8829.88 (0.68) | 37.0737.07 (0.43) | 20.5920.59 (0.88) | 31.2731.27 (0.17) | 61.5561.55 (0.41) |

BTCNet uses task-specific 2-channel pairs that were one of the top combinations on NCH:
Desaturation (CAPNO–SPO2),
Hypopnea (EEG O1-M2–SPO2),
Apnea-Hypopnea (EEG-O1-M2–SPO2),
Apnea (EEG F3-M2–SPO2),
EEG-Arousal (EEG O1-M2–EMG CHIN1–CHIN2),
Sleep Scoring (EEG F3-M2–EOG ROC-M1).

Table 3: 
Cross-dataset inference performance when training on NCH and evaluating directly on the independent CHAT test set.
Binary tasks report Accuracy (Acc), AUROC, and F1.
Sleep scoring reports Accuracy, weighted AUROC, and weighted F1. All metrics are expressed in % and averaged across two seeds and reported as mean (SD).

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Metric | Oxygen Desaturation | Hypopnea | Apnea-Hypopnea | Apnea | EEG-Arousal | Sleep Scoring |
| SleepFM (pool) | Acc | 77.9577.95 (3.63) | 90.9790.97 (1.66) | 93.0493.04 (1.20) | 94.7794.77 (1.37) | 93.3293.32 (0.71) | 78.5978.59 (1.93) |
| AUROC | 84.5684.56 (0.01) | 86.7686.76 (0.05) | 87.4987.49 (0.14) | 85.8685.86 (0.50) | 94.3994.39 (0.06) | 96.6496.64 (0.06) |
| F1 | 52.3852.38 (1.57) | 29.8529.85 (1.21) | 28.7428.74 (10.96) | 21.4721.47 (0.41) | 63.3063.30 (1.07) | 79.6279.62 (1.85) |
| SleepFM (no pool) | Acc | 82.7382.73 (0.56) | 72.9572.95 (20.07) | 81.5681.56 (7.40) | 82.4182.41 (12.63) | 94.2594.25 (0.17) | 70.9370.93 (6.37) |
| AUROC | 84.7284.72 (0.12) | 85.9485.94 (0.72) | 86.9986.99 (0.25) | 85.3785.37 (0.24) | 94.2194.21 (0.09) | 95.8895.88 (0.15) |
| F1 | 54.6254.62 (0.62) | 22.3022.30 (8.92) | 33.3133.31 (5.68) | 18.0618.06 (6.15) | 60.7560.75 (3.38) | 72.4072.40 (5.70) |
| SleepFM (bimodal) | Acc | 83.3083.30 (1.27) | 94.8794.87 (1.07) | 93.5993.59 (0.52) | 95.3495.34 (0.20) | 90.6190.61 (0.16) | 76.0576.05 (2.05) |
| AUROC | 86.3986.39 (0.14) | 86.4286.42 (0.38) | 86.4386.43 (0.13) | 84.2784.27 (0.09) | 91.9191.91 (0.14) | 95.6795.67 (0.14) |
| F1 | 57.6157.61 (0.68) | 29.9129.91 (5.80) | 39.2539.25 (3.68) | 23.4323.43 (0.85) | 54.5054.50 (0.07) | 77.5577.55 (1.25) |
| BTCNet (ours) | Acc | 89.9389.93 (0.09) | 94.7894.78 (0.35) | 94.1594.15 (0.01) | 95.1595.15 (0.01) | 89.7889.78 (0.06) | 55.0155.01 (0.02) |
| AUROC | 90.6590.65 (0.04) | 88.0088.00 (0.55) | 88.3288.32 (0.29) | 84.6484.64 (0.37) | 84.9384.93 (0.31) | 84.6284.62 (0.04) |
| F1 | 68.0168.01 (0.25) | 42.4242.42 (0.85) | 49.8949.89 (0.47) | 27.8227.82 (0.65) | 44.8644.86 (0.37) | 54.8854.88 (0.46) |

BTCNet and SleepFM (bimodal) use task-specific two-channel pairs:
Desaturation (CAPNO–SPO2),
Hypopnea (EEG O1-M2–SPO2),
Apnea–Hypopnea (EEG O1-M2–SPO2),
Apnea (EEG F3-M2–SPO2),
EEG-Arousal (EEG O1-M2–EMG CHIN1–CHIN2),
and Sleep Scoring (EEG F3-M2–EEG F4-M1), where EEG F4-M1 replaces EOG ROC-M1 on CHAT due to its absence (both are BAS channels).

#### 4.1.2 Generalization of Time-Aware Pretraining to CHAT

We evaluate the generalization of our global time-aware
pretraining approach on the unseen CHAT dataset.

Both BTCNet (time-aware) and BCNet (non–time-aware), pretrained
on NCH, are fine-tuned on CHAT using LoRA adapters applied
to the attention layers of the unimodal encoders and the
cross-modal fusion module. Following the same evaluation protocol as in Section [4.1.1](https://arxiv.org/html/2602.02769v1#S4.SS1.SSS1 "4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH ‣ 4.1 Effectiveness of Global Time-Aware Pretraining ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), we first identify the best-performing modality pair using the fine-tuned non–time-aware baseline (BCNet). We then evaluate both BCNet and BTCNet on this fixed channel configuration. This controlled setup isolates the contribution of global time-aware modeling while holding both the dataset and channel selection procedure constant. Additional details are provided in Appendix [C](https://arxiv.org/html/2602.02769v1#A3 "Appendix C Fine-Tuning BTCNet on CHAT ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

Table [10](https://arxiv.org/html/2602.02769v1#A3.T10 "Table 10 ‣ Training Setup. ‣ Appendix C Fine-Tuning BTCNet on CHAT ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") in Appendix [C](https://arxiv.org/html/2602.02769v1#A3 "Appendix C Fine-Tuning BTCNet on CHAT ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") reports the results of this comparison. Across all clinical tasks, BTCNet consistently outperforms BCNet after fine-tuning on CHAT, despite modality selection being optimized for the non–time-aware baseline. While absolute accuracy remains high for both models due to class imbalance, BTCNet achieves substantially higher AUROC and F1 scores, indicating improved class separability.

These results demonstrate that the benefits of global time-aware pretraining persist under dataset shift and are not specific to the NCH cohort. Together with the NCH results, this provides strong evidence that incorporating global time-of-sleep information during pretraining leads to more robust and transferable sleep representations.

### 4.2 Comparison Against Existing SSL Baselines

#### 4.2.1 Linear Probing on NCH (In-Dataset Evaluation)

We next compare BTCNet against relevant and existing multimodal self-supervised learning (SSL) baselines for sleep representation learning whose checkpoints are publicly available and perform tasks beyond sleep staging: SleepFM and PedSleepMAE.

To ensure a fair and consistent evaluation, we follow the same frozen-backbone, linear-probe protocol described in Section [4.1.1](https://arxiv.org/html/2602.02769v1#S4.SS1.SSS1 "4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH ‣ 4.1 Effectiveness of Global Time-Aware Pretraining ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") for all methods. For identifying the two most optimal modalities for BTCNet, we follow the same fast logistic regression method described in Appendix  [D.1](https://arxiv.org/html/2602.02769v1#A4.SS1 "D.1 Modality Screening Procedure ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") for each task. For SleepFM, we follow its original input specification and utilize all available channels in the NCH dataset, grouped into BAS (brain activity signals), RESP (respiratory signals), and EMG modality categories. Because SleepFM does not report a specific linear probing setup, we evaluate multiple reasonable embedding aggregation strategies—i) flattening raw embeddings directly without any pooling and ii) average pooling across time followed by flattening—and report both results for fairness. For PedSleepMAE, we follow the authors’ original evaluation protocol and use their provided linear probing implementation without modification, as the same dataset and channel configuration are used.

According to Table [2](https://arxiv.org/html/2602.02769v1#S4.T2 "Table 2 ‣ 4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH ‣ 4.1 Effectiveness of Global Time-Aware Pretraining ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), BTCNet consistently outperforms SleepFM and PedSleepMAE on respiratory-related tasks and achieves comparable performance on EEG-Arousal and sleep staging. These results suggest that BTCNet learns robust and transferable representations that generalize well across diverse clinical sleep tasks, despite differences in task characteristics and signal types. Overall, this comparison highlights the effectiveness of BTCNet’s learned representations under a frozen-backbone, linear-probing evaluation, indicating strong representation quality rather than task-specific architectural advantages. Additional training details are included in Appendix [11](https://arxiv.org/html/2602.02769v1#A4.T11 "Table 11 ‣ D.2 Linear Probing Configurations ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

#### 4.2.2 Cross-Dataset Linear Probing on CHAT

In this section, we evaluate our models on the unseen CHAT dataset. Since this dataset was not used for pretraining by any of our models, the dataset serves as a strong choice for validating our results on an external site. We compare BTCNet (pretrained on NCH) against the two SleepFM variants described in Section [4.2.1](https://arxiv.org/html/2602.02769v1#S4.SS2.SSS1 "4.2.1 Linear Probing on NCH (In-Dataset Evaluation) ‣ 4.2 Comparison Against Existing SSL Baselines ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") in this section and report the results in Table [3](https://arxiv.org/html/2602.02769v1#S4.T3 "Table 3 ‣ 4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH ‣ 4.1 Effectiveness of Global Time-Aware Pretraining ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"). Additionally, to enable a more direct comparison, we evaluate
SleepFM using the same two task-specific modalities selected
for BTCNet, with temporal average pooling applied to the
resulting representations, noted as SleepFM (bimodal).

As shown in Table [3](https://arxiv.org/html/2602.02769v1#S4.T3 "Table 3 ‣ 4.1.1 Time-Aware vs Non–Time-Aware Pretraining on NCH ‣ 4.1 Effectiveness of Global Time-Aware Pretraining ‣ 4 Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), BTCNet demonstrates strong cross-dataset generalization when trained on NCH and evaluated directly on the independent CHAT cohort. In particular, BTCNet substantially outperforms all SleepFM variants on respiratory-related tasks, including oxygen desaturation, hypopnea, and apnea–hypopnea, achieving consistently higher F1 and AUROC scores despite severe class imbalance. In contrast, SleepFM variants outperform BTCNet on EEG-dominant tasks such as EEG-Arousal and sleep staging.

Among the SleepFM baselines, the bimodal variant consistently performs best on respiratory tasks, outperforming both pooled and all-modality variants and remaining competitive on arousal and sleep scoring. This suggests that selecting task-specific modality pairs can be more informative than indiscriminately incorporating all available channels. Notably, these informative modality pairings are identified using BTCNet’s cross-modal attention during pretraining. While further analysis is required to establish causality, this result suggests that modality relevance learned by BTCNet may transfer to other models, such as SleepFM, when used for downstream task configuration.




## 5 Discussion and Conclusion

This work examined whether explicitly modeling *global time-of-sleep context* during multimodal self-supervised pretraining improves representation quality for pediatric sleep analysis. Across all controlled experiments, our results consistently show that global time-aware conditioning provides a meaningful and transferable inductive bias.

On the NCH dataset, BTCNet systematically outperforms an otherwise identical non–time-aware baseline (BCNet) across all six downstream tasks. Because modality selection is performed exclusively using BCNet and all evaluations rely on frozen encoders with linear classifiers, these gains cannot be attributed to favorable channel choice, increased model capacity, or task-specific adaptation. Instead, they reflect differences in representation quality learned during pretraining. The largest improvements are observed for respiratory-related tasks, such as oxygen desaturation, hypopnea, and apnea detection, which exhibit strong night-scale temporal structure across sleep cycles.

For EEG-dominant tasks including EEG-Arousal and sleep staging, BTCNet remains competitive with existing multimodal SSL baselines, despite being evaluated using only bimodal inputs. This suggests that incorporating global temporal context does not compromise performance on EEG-centric tasks while substantially improving performance on respiration-driven modalities.

Importantly, the benefits of time-aware pretraining persist under dataset shift. When evaluated on the independent CHAT cohort, both via fine-tuning and direct cross-dataset linear probing, BTCNet consistently outperforms non–time-aware baselines and existing multimodal SSL models on respiratory tasks, which demonstrates its robust cross-dataset generalization. An additional observation is that SleepFM performs best on respiratory tasks when using the modality pairs identified by BTCNet rather than all modalities, though this may be coincidental. Lastly, we emphasize that global time is not intended as a standalone predictive signal, but rather as a contextual conditioning mechanism that complements multimodal physiological representations during pretraining.

##### Future work

While this work focuses on a hybrid masked-reconstruction and contrastive framework, an important future direction is to examine whether similar benefits could occur in purely contrastive SSL setups and other alternative architectures. Additionally, our linear probing experiments suggest that other temporal heads, such as lightweight sequence models fitted on top of frozen representations, may further improve downstream performance without requiring full end-to-end retraining. All in all, these directions point toward a broader role for global temporal modeling in scalable and generalizable sleep representation learning.




## Acknowledgement

This work was partially supported by the AI Acceleration Program at the University of North Carolina at Chapel Hill.

The Childhood Adenotonsillectomy Trial (CHAT) was supported by the National Institutes of Health (HL083075, HL083129, UL1-RR-024134, UL1 RR024989). The National Sleep Research Resource was supported by the National Heart, Lung, and Blood Institute (R24 HL114473, 75N92019R002).




## References

* [1]
  J. A. Accardo, J. Shults, M. B. Leonard, J. Traylor, and C. L. Marcus (2010)
  Differences in overnight polysomnography scores using the adult and pediatric criteria for respiratory events in adolescents.
  Sleep 33 (10),  pp. 1333–1339.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px1.p1.1 "Pediatric Sleep Analysis and Clinical Challenges. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p2.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [2]
  S. Blunden, K. Lushington, B. Lorenzen, T. Ooi, F. Fung, and D. Kennedy (2004)
  Are sleep problems under-recognised in general practice?.
  Archives of Disease in Childhood 89 (8),  pp. 708–712.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px1.p1.1 "Pediatric Sleep Analysis and Clinical Challenges. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [3]
  J. F. Carter and L. Tarassenko (2025-15–16 Dec)
  Wav2sleep: a unified multi-modal approach to sleep stage classification from physiological signals.
  In Proceedings of the 4th Machine Learning for Health Symposium, S. Hegselmann, H. Zhou, E. Healey, T. Chang, C. Ellington, V. Mhasawade, S. Tonekaboni, P. Argaw, and H. Zhang (Eds.),
  Proceedings of Machine Learning Research, Vol. 259,  pp. 186–202.
  Cited by: [§3.4.1](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS1.p4.1 "3.4.1 Random Modality Selection and Bimodal Stacking ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [4]
  T. Chen, S. Kornblith, M. Norouzi, and G. Hinton (2020)
  A simple framework for contrastive learning of visual representations.
  In Proceedings of the 37th International Conference on Machine Learning,
  ICML’20.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p1.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.3.2](https://arxiv.org/html/2602.02769v1#S3.SS3.SSS2.p2.1 "3.3.2 Contrastive Framework ‣ 3.3 Stage-1: Unimodal Self-Supervised Pretraining ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.p3.1 "3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [5]
  S. S. Choudhary and S. R. Choudhary (2009)
  Sleep effects on breathing and respiratory diseases.
  Lung India 26 (4),  pp. 117–122.
  Cited by: [§1](https://arxiv.org/html/2602.02769v1#S1.p4.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [6]
  S. Deldari, H. Xue, A. Saeed, D. V. Smith, and F. D. Salim (2022)
  Cocoa: cross modality contrastive learning for sensor data.
  Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 6 (3),  pp. 1–28.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p3.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [7]
  J. Devlin, M. Chang, K. Lee, and K. Toutanova (2019)
  Bert: pre-training of deep bidirectional transformers for language understanding.
  In Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers),
   pp. 4171–4186.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p1.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [8]
  A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby (2021)
  An image is worth 16x16 words: transformers for image recognition at scale.
  In 9th International Conference on Learning Representations, ICLR 2021,
  Virtual Event, Austria, May 3-7, 2021,
  Cited by: [§3.3.1](https://arxiv.org/html/2602.02769v1#S3.SS3.SSS1.p1.7 "3.3.1 Masked Reconstruction ‣ 3.3 Stage-1: Unimodal Self-Supervised Pretraining ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [9]
  E. Eldele, Z. Chen, C. Liu, M. Wu, C. Kwoh, X. Li, and C. Guan (2021)
  An attention-based deep learning approach for sleep stage classification with single-channel eeg.
  IEEE Transactions on Neural Systems and Rehabilitation Engineering 29,  pp. 809–818.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p1.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [10]
  A. L. Goldberger, L. A. Amaral, L. Glass, J. M. Hausdorff, P. C. Ivanov, R. G. Mark, J. E. Mietus, G. B. Moody, C. Peng, and H. E. Stanley (2000)
  PhysioBank, physiotoolkit, and physionet: components of a new research resource for complex physiologic signals.
  Circulation 101 (23),  pp. e215–e220.
  Cited by: [§A.1](https://arxiv.org/html/2602.02769v1#A1.SS1.SSS0.Px1.p1.1 "Selected Channels. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [11]
  K. He, X. Chen, S. Xie, Y. Li, P. Dollár, and R. Girshick (2022)
  Masked autoencoders are scalable vision learners.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
   pp. 16000–16009.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p1.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.SS0.SSS0.Px1.p1.1 "Main Contributions ‣ 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.3](https://arxiv.org/html/2602.02769v1#S3.SS3.p1.1 "3.3 Stage-1: Unimodal Self-Supervised Pretraining ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.p1.3 "3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.p3.1 "3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [12]
  K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick (2020)
  Momentum contrast for unsupervised visual representation learning.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
   pp. 9729–9738.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p1.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [13]
  E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen (2022)
  LoRA: low-rank adaptation of large language models.
  In The Tenth International Conference on Learning Representations, ICLR
  2022, Virtual Event, April 25-29, 2022,
  Cited by: [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.Px2.p1.1 "LoRA-based Fine-Tuning. ‣ 3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [14]
  H. Irani and V. Metsis
  Positional encoding in transformer-based time series models: a survey. arxiv 2025.
  arXiv preprint arXiv:2502.12370.
  Cited by: [§3.4.2](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS2.Px1.p1.2 "Standard Positional Encodings ‣ 3.4.2 Global Time-Aware Conditioning ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [15]
  D. Kostas, S. Aroca-Ouellette, and F. Rudzicz (2021)
  BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of eeg data.
  Frontiers in Human Neuroscience 15,  pp. 653659.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p2.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p2.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p3.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [16]
  C. Lee, H. Kim, H. Han, M. Jung, B. C. Yoon, and D. Kim (2024)
  Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg.
  arXiv preprint arXiv:2404.17585.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p2.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p2.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p3.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.3](https://arxiv.org/html/2602.02769v1#S3.SS3.p1.1 "3.3 Stage-1: Unimodal Self-Supervised Pretraining ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [17]
  H. Lee, B. Li, S. DeForte, M. L. Splaingard, Y. Huang, Y. Chi, and S. L. Linwood (2022)
  A large collection of real-world pediatric sleep studies.
  Scientific Data 9 (1),  pp. 421.
  Cited by: [§A.1](https://arxiv.org/html/2602.02769v1#A1.SS1.SSS0.Px1.p1.1 "Selected Channels. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.SS0.SSS0.Px1.p1.1 "Main Contributions ‣ 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.1.1](https://arxiv.org/html/2602.02769v1#S3.SS1.SSS1.p1.1 "3.1.1 NCH Sleep Databank ‣ 3.1 Dataset and Preprocessing ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [18]
  H. Lee, B. Li, Y. Huang, Y. Chi, and S. Lin (2021-10)
  NCH Sleep DataBank: A Large Collection of Real-world Pediatric Sleep Studies with Longitudinal Clinical Data.
  PhysioNet.
  Note: Version 3.1.0
  External Links: [Document](https://dx.doi.org/10.13026/p2rp-sg37),
  [Link](https://doi.org/10.13026/p2rp-sg37)
  Cited by: [§A.1](https://arxiv.org/html/2602.02769v1#A1.SS1.SSS0.Px1.p1.1 "Selected Channels. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [19]
  H. Lee and A. Saeed (2022)
  Automatic sleep scoring from large-scale multi-channel pediatric eeg.
  arXiv preprint arXiv:2207.06921.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p1.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [20]
  C. L. Marcus, R. H. Moore, C. L. Rosen, B. Giordani, S. L. Garetz, H. G. Taylor, R. B. Mitchell, R. Amin, E. S. Katz, R. Arens, et al. (2013)
  A randomized trial of adenotonsillectomy for childhood sleep apnea.
  New England Journal of Medicine 368 (25),  pp. 2366–2376.
  Cited by: [§A.2](https://arxiv.org/html/2602.02769v1#A1.SS2.SSS0.Px1.p1.2 "Selected Channels. ‣ A.2 Childhood Adenotonsillectomy Trial (CHAT) ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.1.2](https://arxiv.org/html/2602.02769v1#S3.SS1.SSS2.p1.1 "3.1.2 CHAT Dataset ‣ 3.1 Dataset and Preprocessing ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [21]
  L. McInnes, J. Healy, and J. Melville (2018)
  Umap: uniform manifold approximation and projection for dimension reduction.
  arXiv preprint arXiv:1802.03426.
  Cited by: [Appendix E](https://arxiv.org/html/2602.02769v1#A5.p1.1 "Appendix E Additional PHATE Visualizations ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [22]
  G. Medic, M. Wille, and M. E. Hemels (2017)
  Short- and long-term health consequences of sleep disruption.
  Nature and Science of Sleep 9 (),  pp. 151–161.
  External Links: [Document](https://dx.doi.org/10.2147/NSS.S134864)
  Cited by: [§1](https://arxiv.org/html/2602.02769v1#S1.p1.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [23]
  K. R. Moon, D. Van Dijk, Z. Wang, S. Gigante, D. B. Burkhardt, W. S. Chen, K. Yim, A. v. d. Elzen, M. J. Hirn, R. R. Coifman, et al. (2019)
  Visualizing structure and transitions in high-dimensional biological data.
  Nature biotechnology 37 (12),  pp. 1482–1492.
  Cited by: [Appendix E](https://arxiv.org/html/2602.02769v1#A5.p1.1 "Appendix E Additional PHATE Visualizations ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Figure 1](https://arxiv.org/html/2602.02769v1#S1.F1 "In 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Figure 1](https://arxiv.org/html/2602.02769v1#S1.F1.3.2 "In 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [24]
  W. Nazih, M. Shahin, M. I. Eldesouki, and B. Ahmed (2023)
  Influence of channel selection and subject’s age on the performance of the single channel eeg-based automatic sleep staging algorithms.
  Sensors 23 (2),  pp. 899.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px1.p1.1 "Pediatric Sleep Analysis and Clinical Challenges. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p2.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [25]
  J. Owens, S. Kothare, and S. Sheldon (2012)
  Pro:“not just little adults”: aasm should require pediatric accreditation for integrated sleep medicine programs serving both children (0-16 years) and adults.
  Journal of Clinical Sleep Medicine 8 (5),  pp. 473–476.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px1.p1.1 "Pediatric Sleep Analysis and Clinical Challenges. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p2.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [26]
  S. R. Pandey, A. Saeed, and H. Lee (2024)
  PedSleepMAE: generative model for multimodal pediatric sleep signals.
  In 2024 IEEE EMBS International Conference on Biomedical and Health Informatics (BHI),
   pp. 1–8.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p3.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [27]
  F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, et al. (2011)
  Scikit-learn: machine learning in python.
  the Journal of machine Learning research 12,  pp. 2825–2830.
  Cited by: [§D.1](https://arxiv.org/html/2602.02769v1#A4.SS1.p1.1 "D.1 Modality Screening Procedure ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [28]
  E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville (2018)
  Film: visual reasoning with a general conditioning layer.
  In Proceedings of the AAAI conference on artificial intelligence,
  Vol. 32.
  Cited by: [§3.4.2](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS2.Px2.p4.2 "Global Time Conditioning ‣ 3.4.2 Global Time-Aware Conditioning ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [29]
  M. Perslev, S. Darkner, L. Kempfner, M. Nikolic, P. J. Jennum, and C. Igel (2021)
  U-sleep: resilient high-frequency sleep staging.
  NPJ digital medicine 4 (1),  pp. 72.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p1.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p2.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p3.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.4.1](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS1.p4.1 "3.4.1 Random Modality Selection and Bimodal Stacking ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [30]
  Z. Qiu, Z. Wang, B. Zheng, Z. Huang, K. Wen, S. Yang, R. Men, L. Yu, F. Huang, S. Huang, et al. (2025)
  Gated attention for large language models: non-linearity, sparsity, and attention-sink-free.
  arXiv preprint arXiv:2505.06708.
  Cited by: [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.Px1.p1.1 "Gated Attention. ‣ 3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [31]
  A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, et al. (2021)
  Learning transferable visual models from natural language supervision.
  In International conference on machine learning,
   pp. 8748–8763.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p1.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [32]
  B. Shook, A. Turner, J. Chen, M. Wiliński, M. Goswami, J. Elmer, and A. Dubrawski (2025)
  STAMP: spatial-temporal adapter with multi-head pooling.
  arXiv preprint arXiv:2511.10848.
  Cited by: [§3.4.2](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS2.Px1.p1.2 "Standard Positional Encodings ‣ 3.4.2 Global Time-Aware Conditioning ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [33]
  M. L. Splaingard and A. May (2016-06)
  Sleep Disturbances (Nonspecific) (Chapter 194).
  In American Academy of Pediatrics Textbook of Pediatric Care,
  External Links: ISBN 978-1-61002-579-9
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px1.p1.1 "Pediatric Sleep Analysis and Clinical Challenges. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [34]
  P. K. Stein and Y. Pu (2012)
  Heart rate variability, sleep and sleep disorders.
  Sleep medicine reviews 16 (1),  pp. 47–66.
  Cited by: [§1](https://arxiv.org/html/2602.02769v1#S1.p4.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [35]
  R. Thapa, B. He, M. R. Kjær, H. Moore, G. Ganjoo, E. Mignot, and J. Zou (2024)
  SleepFM: multi-modal representation learning for sleep across brain activity, ecg and respiratory signals.
  In Proceedings of the 41st International Conference on Machine Learning,
  ICML’24.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p3.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [36]
  R. Thapa, M. R. Kjaer, B. He, I. Covert, H. Moore IV, U. Hanif, G. Ganjoo, M. B. Westover, P. Jennum, A. Brink-Kjaer, et al. (2026)
  A multimodal sleep foundation model for disease prediction.
  Nature Medicine,  pp. 1–11.
  Cited by: [§D.4](https://arxiv.org/html/2602.02769v1#A4.SS4.p1.1 "D.4 Linear Probing using SleepFM ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [37]
  G. Wang, W. Liu, Y. He, C. Xu, L. Ma, and H. Li (2024)
  Eegpt: pretrained transformer for universal and reliable representation of eeg signals.
  Advances in Neural Information Processing Systems 37,  pp. 39249–39280.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p2.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [38]
  W. Wenjian, X. Qian, X. Jun, and H. Zhikun (2023)
  DynamicSleepNet: a multi-exit neural network with adaptive inference time for sleep stage classification.
  Frontiers in Physiology 14,  pp. 1171467.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p1.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p2.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p3.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [39]
  H. K. Yaggi and K. P. Strohl (2010)
  Adult obstructive sleep apnea/hypopnea syndrome: definitions, risk factors, and pathogenesis.
  Clinics in chest medicine 31 (2),  pp. 179–186.
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px2.p2.1 "Supervised and Self-Supervised Learning for Sleep Analysis. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§1](https://arxiv.org/html/2602.02769v1#S1.p3.1 "1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [40]
  S. Ye and H. Lee (2025)
  Uncovering trajectory and topological signatures in multimodal pediatric sleep embeddings.
  In Machine Learning for Health 2025,
  Cited by: [§2](https://arxiv.org/html/2602.02769v1#S2.p2.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [41]
  W. Yu and J. Yang (2025)
  CASleepNet: a cross attention-based multimodal fusion approach for sleep staging with eeg and eog.
  In ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
  Vol. ,  pp. 1–5.
  External Links: [Document](https://dx.doi.org/10.1109/ICASSP49660.2025.10889570)
  Cited by: [Appendix F](https://arxiv.org/html/2602.02769v1#A6.SS0.SSS0.Px3.p3.1 "Self-Supervised Learning for EEG and Multimodal Sleep Data. ‣ Appendix F Expanded Background and Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§2](https://arxiv.org/html/2602.02769v1#S2.p1.1 "2 Related Work ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.4.3](https://arxiv.org/html/2602.02769v1#S3.SS4.SSS3.p3.1 "3.4.3 Bimodal Cross-Attention and SSL ‣ 3.4 Stage-2: Cross-Modal Interaction and SSL ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
* [42]
  G. Zhang, L. Cui, R. Mueller, S. Tao, M. Kim, M. Rueschman, S. Mariani, D. Mobley, and S. Redline (2018)
  The national sleep research resource: towards a sleep data commons.
  Journal of the American Medical Informatics Association 25 (10),  pp. 1351–1358.
  Cited by: [§A.2](https://arxiv.org/html/2602.02769v1#A1.SS2.SSS0.Px1.p1.2 "Selected Channels. ‣ A.2 Childhood Adenotonsillectomy Trial (CHAT) ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"),
  [§3.1.2](https://arxiv.org/html/2602.02769v1#S3.SS1.SSS2.p1.1 "3.1.2 CHAT Dataset ‣ 3.1 Dataset and Preprocessing ‣ 3 Methods ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").




## Appendix A Datasets

In this section, we provide more information about our datasets.

### A.1 Nationwide Children’s Hospital (NCH) Dataset

##### Selected Channels.

From the NCH dataset [[18](https://arxiv.org/html/2602.02769v1#bib.bib40 "NCH Sleep DataBank: A Large Collection of Real-world Pediatric Sleep Studies with Longitudinal Clinical Data"), [10](https://arxiv.org/html/2602.02769v1#bib.bib43 "PhysioBank, physiotoolkit, and physionet: components of a new research resource for complex physiologic signals"), [17](https://arxiv.org/html/2602.02769v1#bib.bib41 "A large collection of real-world pediatric sleep studies")], we select the 16 most commonly available channels, spanning the following physiological categories:

* •

  Electroencephalography (EEG, 7):
  C3–M2, O1–M2, O2–M1, CZ–O1, C4–M1, F4–M1, F3–M2
* •

  Electrooculography (EOG, 2):
  LOC–M2, ROC–M1
* •

  Electromyography (EMG, 1):
  CHIN1–CHIN2
* •

  Respiratory signals (3):
  thoracic effort, abdominal effort, CPAP airflow (C-FLOW)
* •

  Gas exchange (2):
  oxygen saturation (SpO2), end-tidal CO2 (CAPNO)
* •

  Snoring (1):
  SNORE

##### Preprocessing.

All signals are downsampled to 128 Hz and normalized to zero mean and unit variance for stable training.

##### Dataset Splits.

For downstream tasks, the dataset is partitioned into training, validation, and test splits (80-10-10).
Each split consists of fixed-length examples.
We report the total number of examples in each split in Table [4](https://arxiv.org/html/2602.02769v1#A1.T4 "Table 4 ‣ Dataset Splits. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

Table 4: Number of examples in each dataset split for NCH and CHAT.

|  |  |  |
| --- | --- | --- |
| Split | NCH | CHAT |
| Train | 1,865,984 | 412,800 |
| Validation | 233,216 | 51,584 |
| Test | 233,344 | 51,712 |
| Total | 2,332,544 | 516,096 |

##### Class Imbalance and Loss Weights.

Several downstream tasks derived from the NCH dataset exhibit substantial class imbalance, particularly for rare clinical events such as apnea, hypopnea, and oxygen desaturation.
To mitigate bias toward majority classes during supervised training, we apply task-specific class weighting in the loss function.

Table [5](https://arxiv.org/html/2602.02769v1#A1.T5 "Table 5 ‣ Class Imbalance and Loss Weights. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") summarizes the class weights used for each downstream task.
For binary tasks, weights are specified for the negative (0) and positive (1) classes.
For sleep staging, class weights are provided for all five sleep stages.

Table 5: Class weights used for downstream evaluations on NCH and CHAT.

|  |  |  |  |
| --- | --- | --- | --- |
| Task | Class | NCH | CHAT |
| Apnea | 0 / 1 | 1.0 / 121.0 | 1.02 / 41.64 |
| Hypopnea | 0 / 1 | 1.0 / 50.0 | 1.04 / 26.45 |
| Apnea–Hypopnea | 0 / 1 | 1.0 / 37.0 | 1.06 / 16.88 |
| EEG Arousal | 0 / 1 | 0.52 / 10.66 | 1.09 / 12.39 |
| Oxygen Desaturation | 0 / 1 | 0.55 / 5.67 | 1.20 / 5.99 |
| Sleep Scoring | 0–4 | 0.9 / 5.0 / 0.9 / 0.9 / 0.9 | 3.92 / 15.65 / 3.28 / 4.22 / 7.20 |

### A.2 Childhood Adenotonsillectomy Trial (CHAT)

##### Selected Channels.

For CHAT [[20](https://arxiv.org/html/2602.02769v1#bib.bib46 "A randomized trial of adenotonsillectomy for childhood sleep apnea"), [42](https://arxiv.org/html/2602.02769v1#bib.bib45 "The national sleep research resource: towards a sleep data commons")], we utilize its 12 modalities that are also present in NCH or share a similar physiological function. For example, SaO2 serves as the closest alternative to SpO2, as both measure oxygen saturation. Channels without a clear functional match are excluded from analysis.

##### Preprocessing.

Similar to NCH, all signals are downsampled to 128 Hz and normalized to zero mean and unit variance for stable training.

##### Dataset Splits.

We keep the same split as NCH and report the total number of examples in each split in Table [4](https://arxiv.org/html/2602.02769v1#A1.T4 "Table 4 ‣ Dataset Splits. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

##### Class Imbalance and Loss Weights

Similar to NCH, we report the class weights that were used when using the CHAT dataset for downstream evaluation tasks in Table [5](https://arxiv.org/html/2602.02769v1#A1.T5 "Table 5 ‣ Class Imbalance and Loss Weights. ‣ A.1 Nationwide Children’s Hospital (NCH) Dataset ‣ Appendix A Datasets ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").




## Appendix B Pretraining BTCNet

### B.1 Stage 1: Unimodal Encoder Training

##### Model Architecture.

We list our MAE architecture’s parameters in Table [6](https://arxiv.org/html/2602.02769v1#A2.T6 "Table 6 ‣ Model Architecture. ‣ B.1 Stage 1: Unimodal Encoder Training ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") trained separately for each of our modalities.

Table 6: Model architecture details for unimodal encoders.

|  |  |
| --- | --- |
| Component | Value |
| Patch Size | 8 time samples |
| Mask Ratio | 50% |
| Encoder embedding dimension | 512 |
| Encoder layers | 6 |
| Encoder attention heads | 8 |
| Decoder embedding dimension | 512 |
| Decoder layers | 4 |
| Decoder attention heads | 4 |

##### Training Setup.

Table [7](https://arxiv.org/html/2602.02769v1#A2.T7 "Table 7 ‣ Contrastive Loss (NT-Xent). ‣ B.1 Stage 1: Unimodal Encoder Training ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") lists the hyperparameters used in this experiment. For computational efficiency, each training epoch is defined as a fixed number of iterations rather than a full pass over the dataset. Under this setup, approximately eight training epochs correspond to one full pass over the training data. Because epochs are defined using a fixed iteration budget, 24 warm-up epochs and a patience of 100 epochs correspond to approximately 3 and 12 full passes over the training data, respectively. All experiments follow the same overall training protocol, with mild input noise applied only for non-respiratory channels (EEG, EOG, EMG) and standard stabilization choices used where necessary to ensure stable training.

##### Reconstruction and Contrastive Objectives.

BTCNet is trained using a combination of masked reconstruction and contrastive learning losses.
Let xx denote the input signal segmented into patches.

##### Reconstruction Loss.

We use a masked mean-squared error (MSE) reconstruction loss computed only over masked signal positions:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒrecon=1|M|​∑(c,t)∈M‖x^c,t−xc,t‖22,\mathcal{L}\_{\text{recon}}=\frac{1}{|M|}\sum\_{(c,t)\in M}\left\|\hat{x}\_{c,t}-x\_{c,t}\right\|\_{2}^{2}, |  | (5) |

where xc,tx\_{c,t} and x^c,t\hat{x}\_{c,t} denote the ground-truth and reconstructed signal values for channel cc at time index tt, and MM denotes the set of masked positions. For unimodal encoder training, this formulation reduces to just a one-channel case.

##### Contrastive Loss (NT-Xent).

Given a batch of NN paired representations {(zi(1),zi(2))}i=1N\{(z\_{i}^{(1)},z\_{i}^{(2)})\}\_{i=1}^{N} obtained from two augmented views, we construct a set of 2​N2N ℓ2\ell\_{2}-normalized embeddings {zk}k=12​N\{z\_{k}\}\_{k=1}^{2N} by concatenation.
Cosine similarity is used as the similarity function.

For a positive pair (i,j)(i,j) corresponding to two views of the same example, the NT-Xent loss is defined as

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℓi,j=−log⁡exp⁡(sim​(zi,zj)/τ)∑k=12​N𝟏​{k≠i}​exp⁡(sim​(zi,zk)/τ),\ell\_{i,j}=-\log\frac{\exp\!\left(\mathrm{sim}(z\_{i},z\_{j})/\tau\right)}{\sum\_{k=1}^{2N}\mathbf{1}\{k\neq i\}\exp\!\left(\mathrm{sim}(z\_{i},z\_{k})/\tau\right)}, |  | (6) |

where 𝟏​{⋅}\mathbf{1}\{\cdot\} denotes the indicator function, sim​(⋅,⋅)\mathrm{sim}(\cdot,\cdot) is cosine similarity, and τ\tau is a temperature parameter.
The final contrastive objective averages this loss over all positive pairs in the batch.

Table 7: Training configuration and optimization details for unimodal encoders.

|  |  |
| --- | --- |
| Parameter | Value |
| Batch size | 128 |
| Iterations per epoch | 2000 |
| Maximum epochs | 850 |
| Warm-up epochs | 24 |
| Early stopping patience | 100 epochs |
| Optimizer | Adam |
| Learning rate | 1×10−41\times 10^{-4} |
| Weight decay | 1×10−51\times 10^{-5} |
| Contrastive loss weight (λcontrast\lambda\_{\text{contrast}}) | Linearly ramped to 1.0 |
| Learning rate schedule | Linear warm-up followed by cosine decay |

### B.2 Stage 2: Cross-Modal Interaction and SSL

##### Model Architecture

We enlist the parameters used for our MAE architecture in Stage 2 in Table [8](https://arxiv.org/html/2602.02769v1#A2.T8 "Table 8 ‣ Model Architecture ‣ B.2 Stage 2: Cross-Modal Interaction and SSL ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

Table 8: Stage-2 cross-modal model architecture and pretraining configuration.

|  |  |
| --- | --- |
| Component | Value |
| Patch size | 8 samples |
| Mask ratio | 50% |
| Encoder embedding dimension | 512 |
| Encoder layers | 10 |
| Encoder attention heads | 8 |
| Decoder embedding dimension | 512 |
| Decoder layers | 4 |
| Decoder attention heads | 4 |

##### Training Setup.

During Stage-2 training, pairs of modalities are randomly sampled at each iteration and fused using a cross-attention module conditioned on global time information. Unimodal encoders pretrained in Stage-1 are frozen, with lightweight LoRA adapters applied to their attention layers. We list the hyperparameters used in this process in Table [9](https://arxiv.org/html/2602.02769v1#A2.T9 "Table 9 ‣ LoRA Adaptation Details. ‣ B.2 Stage 2: Cross-Modal Interaction and SSL ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"). Similar to the setup described in Appendix [B.1](https://arxiv.org/html/2602.02769v1#A2.SS1 "B.1 Stage 1: Unimodal Encoder Training ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), approximately eight training epochs correspond to one full pass over the training set.

##### LoRA Adaptation Details.

For parameter-efficient fine-tuning, we apply Low-Rank Adaptation (LoRA) to the attention layers of the pretrained unimodal encoders during Stage-2 training and downstream fine-tuning. Specifically, LoRA adapters are inserted into the query–key–value and output projection matrices of the self-attention blocks. We use a low-rank configuration with rank r=8r=8, scaling factor α=16\alpha=16, and dropout rate 0.050.05. All original encoder parameters remain frozen, and only the LoRA parameters are updated during training.

Table 9: Stage-2 cross-modal training configuration.

|  |  |
| --- | --- |
| Parameter | Value |
| Batch size | 64 |
| Iterations per epoch | 4000 |
| Epochs | 200 |
| Warm-up epochs | 24 |
| Optimizer | Adam |
| Learning rate | 1×10−41\times 10^{-4} |
| Weight decay | 1×10−51\times 10^{-5} |
| Learning rate schedule | Linear warm-up followed by cosine decay |




## Appendix C Fine-Tuning BTCNet on CHAT

##### LoRA Adaptation Details.

When fine-tuning BTCNet on the CHAT dataset, LoRA adapters are applied to (i) the unimodal encoders corresponding to the selected modality pair and (ii) the Stage-2 cross-modal fusion transformer.

For the Stage-2 fusion model, LoRA is inserted into the attention projections and feed-forward layers (query/key/value projections, output projection, and MLP layers), using rank r=64r=64, scaling factor α=128\alpha=128, and dropout 0.050.05.

For the unimodal encoders, LoRA is applied to the self-attention projections and MLP layers with the same configuration (r=64r=64, α=128\alpha=128, dropout 0.050.05).

##### Training Setup.

The model architecture and loss formulation follow the Stage-2 configuration described in Table [8](https://arxiv.org/html/2602.02769v1#A2.T8 "Table 8 ‣ Model Architecture ‣ B.2 Stage 2: Cross-Modal Interaction and SSL ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").
For CHAT fine-tuning, we adapt the optimization setup to reflect the smaller dataset size and the use of parameter-efficient LoRA adaptation.
Specifically, training is performed using an epoch-based schedule rather than a fixed iteration budget, corresponding to approximately 50 full passes over the CHAT training set.
We additionally use a larger effective batch size (128) and a higher learning rate (3×10−43\times 10^{-4}), which are more suitable for LoRA-only updates, while keeping all non-LoRA parameters frozen.
These changes are relative to the Stage-2 pretraining setup summarized in Table [9](https://arxiv.org/html/2602.02769v1#A2.T9 "Table 9 ‣ LoRA Adaptation Details. ‣ B.2 Stage 2: Cross-Modal Interaction and SSL ‣ Appendix B Pretraining BTCNet ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

Table 10: 
Comparison of the non–time-aware baseline BCNet and BTCNet after fine-tuning both models on the CHAT dataset.
Results are reported over three seeds.
Binary tasks report Accuracy (Acc), AUROC, and F1.
Sleep scoring reports Accuracy, weighted AUROC, and weighted F1. Results are averaged over three seeds and reported as mean (SD).

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task | %Pos | Modality Pair | BCNet (CHAT-FT) | | | BTCNet (CHAT-FT) | | |
|  |  |  | Acc (%) | AUROC (%) | F1 (%) | Acc (%) | AUROC (%) | F1 (%) |
| Oxygen Desaturation | 16.70 | EEG C4-M1 – SPO2 | 47.75 (0.37) | 59.69 (0.18) | 30.84 (0.14) | 74.56 (1.73) | 74.41 (0.12) | 42.23 (0.24) |
| Hypopnea | 3.78 | EEG C4-M1 – SPO2 | 78.47 (7.18) | 60.61 (1.05) | 9.83 (0.31) | 91.88 (0.32) | 75.02 (0.05) | 20.24 (0.55) |
| Apnea–Hypopnea | 5.92 | EEG C4-M1 – SPO2 | 66.90 (3.90) | 59.04 (0.73) | 13.64 (0.50) | 88.72 (0.84) | 73.40 (0.16) | 24.87 (0.61) |
| Apnea | 2.40 | EEG C4-M1 – SPO2 | 67.22 (3.27) | 56.35 (0.87) | 5.56 (0.26) | 92.62 (1.39) | 70.01 (0.26) | 12.00 (0.11) |
| EEG-Arousal | 8.07 | EEG O2-M1 – EEG C4-M1 | 69.97 (1.05) | 58.82 (0.25) | 17.56 (0.24) | 88.76 (0.51) | 73.66 (0.12) | 33.01 (0.21) |
| 5-stage Sleep Scoring | – | EEG C4-M1 – SPO2 | 31.30 (2.05) | 62.05 (0.09) | 29.88 (3.23) | 49.53 (0.39) | 79.93 (0.05) | 49.03 (0.83) |




## Appendix D Experiments and Results

### D.1 Modality Screening Procedure

Before evaluating BTCNet on downstream tasks, we identify
informative modality combinations using a fast screening
procedure. For each task on either NCH or CHAT, we randomly
sample a subset of examples (128,000 for NCH and 64,000
for CHAT) and extract frozen representations from the
pretrained encoders for all 120 possible modality pairs. We
then fit lightweight logistic regression classifiers using
scikit-learn [[27](https://arxiv.org/html/2602.02769v1#bib.bib16 "Scikit-learn: machine learning in python")] with ℓ2\ell\_{2}
regularization and a small number of optimization iterations.
For binary tasks, we compute AUROC scores from predicted
class probabilities, while for multiclass tasks we report
weighted one-vs-rest AUROC. Modality pairs are ranked
according to these scores, and the top-performing
combinations are selected for subsequent evaluation. For binary classification tasks, we prioritize F1 binary score when ranking modality pairs, as it best reflects performance on rare clinical events. Under severe class imbalance, absolute F1 values are expected to be low and comparable to class prevalence for random predictions; thus, improvements in F1 indicate meaningful separability. AUROC is reported to show threshold-independent separability. This
procedure is used solely for relative ranking of modality
pairs and not for reporting final downstream performance. This procedure enables efficient screening of all 120
modality combinations for each task and dataset, facilitating
the identification of robust, task-specific modality pairs.

### D.2 Linear Probing Configurations

Table [11](https://arxiv.org/html/2602.02769v1#A4.T11 "Table 11 ‣ D.2 Linear Probing Configurations ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") lists the configurations we used for fitting linear probes on the NCH and CHAT dataset.

Table 11: Linear probing configuration for downstream evaluation.

|  |  |
| --- | --- |
| Component | Setting |
| Probe architecture | Single linear layer |
| Loss function | Cross-entropy (class-weighted) |
| Optimizer | Adam |
| Batch size | 128 |
| Learning rate | 4×10−34\times 10^{-3} |
| Weight decay | 1×10−51\times 10^{-5} |
| Epochs (NCH) | 50 |
| Iterations per epoch (NCH) | 2000 |
| Epochs (CHAT) | 10 (full dataset pass) |

### D.3 Additional Comparisons: BTCNet vs BCNet on NCH

Here, we report results from the remaining two out of three modalities that we experimented with to strengthen our claim that BTCNet outperforms its non-time counterpart BCNet on the NCH dataset. According to Table [12](https://arxiv.org/html/2602.02769v1#A4.T12 "Table 12 ‣ D.3 Additional Comparisons: BTCNet vs BCNet on NCH ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep"), across all evaluated tasks and modality pairs, BTCNet consistently improves AUROC and F1 score over the non–time-aware baseline, indicating better discrimination and robustness under class imbalance. While minor variations in accuracy are observed for a small number of channel combinations, accuracy is less informative in these highly imbalanced settings and does not reflect the improved minority-class detection captured by AUROC and F1 for binary tasks.

Table 12: 
Additional modality-pair results on the NCH dataset.
Binary tasks report Accuracy (Acc), AUROC, and F1.
Sleep scoring reports Accuracy, weighted AUROC, and weighted F1.

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task | %Pos | Modality Pair | BCNet | | | BTCNet | | |
|  |  |  | Acc (%) | AUROC (%) | F1 (%) | Acc (%) | AUROC (%) | F1 (%) |
| Oxygen Desaturation | 8.78 | SPO2 – RESP ABDOMINAL | 88.48 | 78.83 | 38.78 | 90.16 | 81.59 | 44.58 |
|  | SPO2 – EOG LOC-M2 | 88.05 | 78.79 | 38.48 | 89.83 | 81.93 | 44.11 |
| Hypopnea | 1.97 | EEG CZ-O1 – SPO2 | 96.41 | 82.82 | 25.25 | 96.26 | 85.97 | 29.58 |
|  | EEG F3-M2 – SPO2 | 96.64 | 82.83 | 25.50 | 96.33 | 86.30 | 30.52 |
| Apnea–Hypopnea | 2.80 | CAPNO – SPO2 | 95.88 | 84.38 | 31.71 | 95.95 | 87.33 | 35.68 |
|  | EEG CZ-O1 – SPO2 | 95.98 | 82.60 | 31.75 | 95.92 | 85.71 | 36.19 |
| Apnea | 0.83 | EEG O1-M2 – SPO2 | 97.93 | 81.61 | 18.65 | 98.37 | 84.55 | 22.29 |
|  | EEG O2-M1 – SPO2 | 97.78 | 81.62 | 18.41 | 98.24 | 84.53 | 21.53 |
| EEG-Arousal | 4.71 | RESP THORACIC – EMG CHIN1–CHIN2 | 89.97 | 76.68 | 25.88 | 90.69 | 79.44 | 28.65 |
|  | EOG ROC-M1 – EMG CHIN1–CHIN2 | 90.18 | 78.04 | 27.99 | 90.54 | 80.61 | 28.59 |
| 5-stage Sleep Scoring | – | EEG C3-M2 – EOG LOC-M2 | 56.53 | 79.00 | 53.29 | 61.12 | 83.84 | 60.80 |
|  | EEG F4-M1 – EOG ROC-M1 | 55.66 | 78.17 | 52.46 | 61.47 | 83.61 | 60.37 |

### D.4 Linear Probing using SleepFM

We follow the embedding extraction procedure described in [[36](https://arxiv.org/html/2602.02769v1#bib.bib13 "A multimodal sleep foundation model for disease prediction")] and keep all SleepFM encoder weights frozen throughout evaluation. Specifically, we map our original PSG channels into the modality groups expected by SleepFM and extract fixed-length embeddings from the pretrained model using 5-second windows.

Consistent with SleepFM’s modality definitions, we organize the available channels into three groups: *BAS* (brain activity signals), *RESP* (respiratory and oxygen-related signals), and *EMG*. The BAS group consists of six EEG channels (C3–M2, O1–M2, O2–M1, C4–M1, F4–M1, F3–M2). The RESP group includes five respiratory-related signals (end-tidal CO2, oxygen saturation, abdominal effort, chest effort, and snoring). The EMG group contains the chin electromyography channel. Channels without a clear functional correspondence to SleepFM’s predefined modalities are excluded from evaluation. Although SleepFM additionally supports ECG inputs, these signals are not available in either CHAT or NCH and are therefore omitted.

For each modality group, SleepFM produces a modality-specific temporal embedding sequence of shape (T×128)(T\times 128), where TT denotes the number of 5-second segments. Following prior work, we either aggregate embeddings by average pooling along the temporal dimension or flatten the temporal features directly to obtain a fixed-length representation for downstream linear probing, as described in the main paper

![Refer to caption](x3.png)

Figure 3: 
PHATE and UMAP embeddings for a representative patient with apnea using CAPNO and SPO2 channels.
Positive events are indicated by ×\times markers, while color denotes
temporal order within the patient record.




## Appendix E Additional PHATE Visualizations

To gain qualitative insight into how time-aware pretraining shapes the learned representation space, we visualize frozen embeddings from the BTCNet (time-aware) and BCNet (non-time-aware) models using PHATE, a nonlinear dimensionality reduction method that preserves both local neighborhood structure and global progression in high-dimensional data  [[23](https://arxiv.org/html/2602.02769v1#bib.bib17 "Visualizing structure and transitions in high-dimensional biological data")]. These visualizations are intended to provide intuition rather than quantitative evidence. Figure [1](https://arxiv.org/html/2602.02769v1#S1.F1 "Figure 1 ‣ 1 Introduction ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") shows a representative example from a pediatric patient with frequent oxygen desaturation events, using the top-performing channel pair SPO2–CAPNO. The time-aware model exhibits a smoother and more coherent global structure, whereas the non-time-aware model produces more fragmented and scattered embeddings. This qualitative difference is consistent with our linear-probing results and provides intuition for why incorporating global time information leads to representations that are more amenable to separation in downstream tasks. Additional example PHATE plots, along with UMAP [[21](https://arxiv.org/html/2602.02769v1#bib.bib42 "Umap: uniform manifold approximation and projection for dimension reduction")], are shown in Figure [3](https://arxiv.org/html/2602.02769v1#A4.F3 "Figure 3 ‣ D.4 Linear Probing using SleepFM ‣ Appendix D Experiments and Results ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep") and Figure [4](https://arxiv.org/html/2602.02769v1#A5.F4 "Figure 4 ‣ Appendix E Additional PHATE Visualizations ‣ BiTimeCrossNet: Time-Aware Self-Supervised Learning for Pediatric Sleep").

![Refer to caption](x4.png)

Figure 4: 
PHATE and UMAP embeddings for a representative patient with hypopnea using EEG O1-M2 and SPO2 channels.
Positive events are indicated by ×\times markers, while color denotes
temporal order within the patient record.




## Appendix F Expanded Background and Related Work

##### Pediatric Sleep Analysis and Clinical Challenges.

Despite increasing interest in automated PSG analysis, most computational sleep modeling efforts have focused on adult populations, while pediatric sleep remains comparatively understudied. This gap is partly due to the scarcity of publicly available pediatric datasets, limited software support for pediatric sleep event detection, and the underdiagnosis and underreporting of sleep disorders in children [[33](https://arxiv.org/html/2602.02769v1#bib.bib29 "Sleep Disturbances (Nonspecific) (Chapter 194)"), [2](https://arxiv.org/html/2602.02769v1#bib.bib34 "Are sleep problems under-recognised in general practice?")]. Importantly, pediatric sleep physiology differs substantially from adult sleep in terms of sleep architecture, respiratory control, and autonomic regulation [[1](https://arxiv.org/html/2602.02769v1#bib.bib35 "Differences in overnight polysomnography scores using the adult and pediatric criteria for respiratory events in adolescents"), [25](https://arxiv.org/html/2602.02769v1#bib.bib36 "Pro:“not just little adults”: aasm should require pediatric accreditation for integrated sleep medicine programs serving both children (0-16 years) and adults")]. As a result, models trained on adult sleep data often generalize poorly to pediatric populations, even for foundational tasks such as sleep stage classification [[24](https://arxiv.org/html/2602.02769v1#bib.bib30 "Influence of channel selection and subject’s age on the performance of the single channel eeg-based automatic sleep staging algorithms")].

##### Supervised and Self-Supervised Learning for Sleep Analysis.

To reduce reliance on expensive expert annotations, a wide range of machine learning approaches have been explored for automated sleep assessment. However, the majority of existing methods rely on supervised learning [[29](https://arxiv.org/html/2602.02769v1#bib.bib4 "U-sleep: resilient high-frequency sleep staging"), [38](https://arxiv.org/html/2602.02769v1#bib.bib31 "DynamicSleepNet: a multi-exit neural network with adaptive inference time for sleep stage classification"), [9](https://arxiv.org/html/2602.02769v1#bib.bib32 "An attention-based deep learning approach for sleep stage classification with single-channel eeg"), [19](https://arxiv.org/html/2602.02769v1#bib.bib33 "Automatic sleep scoring from large-scale multi-channel pediatric eeg")], which requires large volumes of labeled data that are difficult to obtain in clinical practice. Self-supervised learning (SSL) offers a promising alternative by learning representations from unlabeled PSG recordings using pretext objectives such as masked signal reconstruction, which can then be transferred to downstream tasks at substantially lower annotation cost.

While SSL has been widely adopted in other domains, its application to pediatric sleep modeling remains limited. Moreover, most existing SSL-based approaches in sleep analysis are designed primarily for sleep stage classification [[29](https://arxiv.org/html/2602.02769v1#bib.bib4 "U-sleep: resilient high-frequency sleep staging"), [38](https://arxiv.org/html/2602.02769v1#bib.bib31 "DynamicSleepNet: a multi-exit neural network with adaptive inference time for sleep stage classification"), [16](https://arxiv.org/html/2602.02769v1#bib.bib20 "Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg"), [15](https://arxiv.org/html/2602.02769v1#bib.bib18 "BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of eeg data")]. Consequently, SSL methods targeting clinically important diagnostic tasks, such as apnea, hypopnea, and oxygen desaturation detection, remain relatively underexplored, despite their strong associations with cardiovascular and neurological outcomes [[39](https://arxiv.org/html/2602.02769v1#bib.bib37 "Adult obstructive sleep apnea/hypopnea syndrome: definitions, risk factors, and pathogenesis")].

##### Self-Supervised Learning for EEG and Multimodal Sleep Data.

Influential SSL approaches include masked modeling methods such as MAE [[11](https://arxiv.org/html/2602.02769v1#bib.bib1 "Masked autoencoders are scalable vision learners")] in vision and BERT [[7](https://arxiv.org/html/2602.02769v1#bib.bib25 "Bert: pre-training of deep bidirectional transformers for language understanding")] in language, as well as contrastive learning frameworks such as SimCLR [[4](https://arxiv.org/html/2602.02769v1#bib.bib8 "A simple framework for contrastive learning of visual representations")] and MoCo [[12](https://arxiv.org/html/2602.02769v1#bib.bib26 "Momentum contrast for unsupervised visual representation learning")]. Multimodal extensions, including CLIP [[31](https://arxiv.org/html/2602.02769v1#bib.bib27 "Learning transferable visual models from natural language supervision")], demonstrate the effectiveness of contrastive alignment across heterogeneous modalities.

In the sleep domain, SSL efforts have predominantly focused on uni-modal EEG-based representation learning, with an emphasis on sleep stage classification. BENDR [[15](https://arxiv.org/html/2602.02769v1#bib.bib18 "BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of eeg data")] adapts masked self-supervised objectives to raw EEG signals, while EEGPT [[37](https://arxiv.org/html/2602.02769v1#bib.bib19 "Eegpt: pretrained transformer for universal and reliable representation of eeg signals")] introduces spatio-temporal alignment and hierarchical modeling to improve representation quality. NeuroNet [[16](https://arxiv.org/html/2602.02769v1#bib.bib20 "Neuronet: a novel hybrid self-supervised learning framework for sleep stage classification using single-channel eeg")] further combines masked prediction and contrastive learning on single-channel EEG with temporal modeling across epochs.

More recent work has explored multimodal SSL for sleep analysis. COCOA [[6](https://arxiv.org/html/2602.02769v1#bib.bib21 "Cocoa: cross modality contrastive learning for sensor data")] introduces cross-modality contrastive learning for multimodal physiological time series, while SleepFM [[35](https://arxiv.org/html/2602.02769v1#bib.bib22 "SleepFM: multi-modal representation learning for sleep across brain activity, ecg and respiratory signals")] proposes a multimodal foundation model using leave-one-out contrastive alignment across modalities. SynthSleepNet [[41](https://arxiv.org/html/2602.02769v1#bib.bib3 "CASleepNet: a cross attention-based multimodal fusion approach for sleep staging with eeg and eog")] extends hybrid SSL to multimodal PSG data by integrating masked prediction and contrastive learning with temporal context modeling. However, multimodal SSL techniques trained specifically on pediatric sleep data remain scarce. To our knowledge, PedSleepMAE [[26](https://arxiv.org/html/2602.02769v1#bib.bib15 "PedSleepMAE: generative model for multimodal pediatric sleep signals")] is the only existing SSL framework trained on large-scale pediatric PSG data (NCH Sleep Databank) for sleep stage classification and related diagnostic tasks.