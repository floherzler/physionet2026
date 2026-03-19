# A multimodal sleep foundation model for disease prediction

A multimodal sleep foundation model for disease prediction

[Download PDF](/articles/s41591-025-04133-4.pdf)

* Article
* [Open access](https://www.springernature.com/gp/open-science/about/the-fundamentals-of-open-access-and-open-research)
* Published: 06 January 2026




# A multimodal sleep foundation model for disease prediction

* [Rahul Thapa](#auth-Rahul-Thapa-Aff1-Aff2)[1](#Aff1),[2](#Aff2)[na1](#na1),
* [Magnus Ruud Kjaer](#auth-Magnus_Ruud-Kjaer-Aff3-Aff4-Aff5) 
  [ORCID: orcid.org/0009-0007-2963-0945](https://orcid.org/0009-0007-2963-0945)[3](#Aff3),[4](#Aff4),[5](#Aff5)[na1](#na1),
* [Bryan He](#auth-Bryan-He-Aff2)[2](#Aff2),
* [Ian Covert](#auth-Ian-Covert-Aff2)[2](#Aff2),
* [Hyatt Moore IV](#auth-Hyatt-Moore_IV-Aff3-Aff6)[3](#Aff3),[6](#Aff6),
* [Umaer Hanif](#auth-Umaer-Hanif-Aff5-Aff7)[5](#Aff5),[7](#Aff7),
* [Gauri Ganjoo](#auth-Gauri-Ganjoo-Aff3)[3](#Aff3),
* [M. Brandon Westover](#auth-M__Brandon-Westover-Aff8)[8](#Aff8),
* [Poul Jennum](#auth-Poul-Jennum-Aff5-Aff9)[5](#Aff5),[9](#Aff9),
* [Andreas Brink-Kjaer](#auth-Andreas-Brink_Kjaer-Aff4)[4](#Aff4),
* [Emmanuel Mignot](#auth-Emmanuel-Mignot-Aff3) 
  [ORCID: orcid.org/0000-0002-6928-5310](https://orcid.org/0000-0002-6928-5310)[3](#Aff3)[na2](#na2) &
* …
* [James Zou](#auth-James-Zou-Aff1-Aff2) 
  [ORCID: orcid.org/0000-0001-8880-4764](https://orcid.org/0000-0001-8880-4764)[1](#Aff1),[2](#Aff2)[na2](#na2)

Show authors

[*Nature Medicine*](/nm)
**volume 32**, pages 752–762 (2026)[Cite this article](#citeas)

* 233k Accesses
* 5 Citations
* 1391 Altmetric
* [Metrics details](/articles/s41591-025-04133-4/metrics)

### Subjects

* [Biomedical engineering](/subjects/biomedical-engineering)
* [Diseases](/subjects/diseases)




## Abstract

Sleep is a fundamental biological process with broad implications for physical and mental health, yet its complex relationship with disease remains poorly understood. Polysomnography (PSG)—the gold standard for sleep analysis—captures rich physiological signals but is underutilized due to challenges in standardization, generalizability and multimodal integration. To address these challenges, we developed SleepFM, a multimodal sleep foundation model trained with a new contrastive learning approach that accommodates multiple PSG configurations. Trained on a curated dataset of over 585,000 hours of PSG recordings from approximately 65,000 participants across several cohorts, SleepFM produces latent sleep representations that capture the physiological and temporal structure of sleep and enable accurate prediction of future disease risk. From one night of sleep, SleepFM accurately predicts 130 conditions with a C-Index of at least 0.75 (Bonferroni-corrected *P* < 0.01), including all-cause mortality (C-Index, 0.84), dementia (0.85), myocardial infarction (0.81), heart failure (0.80), chronic kidney disease (0.79), stroke (0.78) and atrial fibrillation (0.78). Moreover, the model demonstrates strong transfer learning performance on a dataset from the Sleep Heart Health Study—a dataset that was excluded from pretraining—and performs competitively with specialized sleep-staging models such as U-Sleep and YASA on common sleep analysis tasks, achieving mean *F*1 scores of 0.70–0.78 for sleep staging and accuracies of 0.69 and 0.87 for classifying sleep apnea severity and presence. This work shows that foundation models can learn the language of sleep from multimodal sleep recordings, enabling scalable, label-efficient analysis and disease prediction.


## Main

Sleep is a complex process characterized by intricate interactions across physiological systems, including brain, heart, respiratory and muscle activity[1](/articles/s41591-025-04133-4#ref-CR1 "Berry, R. B et al. The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications (American Academy of Sleep Medicine, 2012)."). PSG—the gold standard for sleep evaluation—captures these interactions through recordings of several modalities, including brain activity signals (BAS, including electroencephalogram (EEG) and electrooculogram (EOG)), electrocardiography (ECG), electromyography (EMG) and respiratory signals[2](/articles/s41591-025-04133-4#ref-CR2 "Kryger, M. H., Roth, T. & Dement, W. C. (eds). Principles and Practice of Sleep Medicine (Saunders, 2010).").

Sleep disorders affect millions of people and are increasingly recognized as indicators of, and contributors to, various health conditions[3](/articles/s41591-025-04133-4#ref-CR3 "Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. NPJ Digit. Med. 5, 103 (2022)."). Sleep disturbances often precede the clinical onset of numerous conditions, such as psychiatric disorders[4](/articles/s41591-025-04133-4#ref-CR4 "Riemann, D. Insomnia and comorbid psychiatric disorders. Sleep Med. 8, S15–S20 (2007)."), neurodegenerative diseases[5](/articles/s41591-025-04133-4#ref-CR5 "André, C. et al. Association of sleep-disordered breathing with Alzheimer disease biomarkers in community-dwelling older adults: a secondary analysis of a randomized clinical trial. JAMA Neurol. 77, 716–724 (2020).") and cardiovascular disorders[6](/articles/s41591-025-04133-4#ref-CR6 "Nii Ossah Addo, P. et al. Associations between sleep duration, sleep disturbance and cardiovascular disease biomarkers among adults in the united states. BMC Public Health 24, 947 (2024)."). These associations highlight the important role sleep plays in maintaining overall health and underscores its predictive potential across a wide spectrum of diseases. However, most existing studies have focused on identifying links between sleep and specific diseases using isolated metrics or manual annotations, leaving much of the complexity of sleep physiology, as captured in PSG, underutilized.

Recent advances in deep learning have enabled the use of PSG’s multimodal data for tasks ranging from sleep staging and apnea detection to predicting conditions such as atrial fibrillation, biological aging and narcolepsy[3](/articles/s41591-025-04133-4#ref-CR3 "Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. NPJ Digit. Med. 5, 103 (2022)."),[7](#ref-CR7 "Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. NPJ Digit. Med. 4, 72 (2021)."),[8](#ref-CR8 "Nassi, T. E. et al. Automated scoring of respiratory events in sleep with a single effort belt and deep neural networks. IEEE Trans. Biomed. Eng. 69, 2094–2104 (2021)."),[9](#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024)."),[10](/articles/s41591-025-04133-4#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018)."). Despite this progress, current approaches face key limitations: they focus on individual outcomes, depend on supervised learning with expert-labeled data and are trained on relatively small datasets (2,500–15,913 recordings)[3](/articles/s41591-025-04133-4#ref-CR3 "Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. NPJ Digit. Med. 5, 103 (2022)."),[7](/articles/s41591-025-04133-4#ref-CR7 "Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. NPJ Digit. Med. 4, 72 (2021)."),[9](#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024)."),[10](#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018)."),[11](/articles/s41591-025-04133-4#ref-CR11 "Thapa, R. et al. SleepFM: multi-modal representation learning for sleep across brain activity, ECG and respiratory signals. Proc. Mach. Learning Res. 235, 48019–48037 (2024)."). Manual annotations are time consuming and prone to inter-rater variability, making scaling difficult. Moreover, existing models lack flexibility across recording environments, generalize poorly across cohorts and often fail to exploit the richness of multimodal sleep signals. There remains a need for robust, generalizable architectures and systematic evaluation of sleep’s predictive value across a broad range of health conditions.

Foundation models have emerged as a transformative approach in machine learning, enabling robust representation learning from large-scale, unlabeled data[12](/articles/s41591-025-04133-4#ref-CR12 "Bommasani, R. et al. On the opportunities and risks of foundation models. Preprint at 
                  https://arxiv.org/abs/2108.07258v3
                  
                 (2021)."). By leveraging self-supervised learning, these models can be fine-tuned efficiently for diverse applications. In biomedicine, foundation models have demonstrated remarkable capabilities in analyzing complex, heterogeneous datasets, driving advances in disease prediction, patient stratification and therapeutic discovery[13](/articles/s41591-025-04133-4#ref-CR13 "Saab, K. et al. Capabilities of Gemini models in medicine. Preprint at 
                  https://arxiv.org/abs/2404.18416v2
                  
                 (2024)."),[14](/articles/s41591-025-04133-4#ref-CR14 "Zhao, T. et al. A foundation model for joint segmentation, detection and recognition of biomedical objects across nine modalities. Nat. Methods 22, 166–176 (2025)."). Their ability to extract meaningful patterns from large-scale data has addressed many challenges associated with the diverse and high-dimensional nature of clinical datasets.

Despite these successes, their application to sleep remains limited. Sleep data, particularly from PSG, presents unique challenges due to its complexity and variability, including differences in the number and types of recording channel across clinical cohorts. Most sleep studies have focused narrowly on sleep-specific outcomes, constraining the broader potential of foundation models for disease prediction. In preliminary work, we explored self-supervised learning on PSG data in a smaller cohort of participants[11](/articles/s41591-025-04133-4#ref-CR11 "Thapa, R. et al. SleepFM: multi-modal representation learning for sleep across brain activity, ECG and respiratory signals. Proc. Mach. Learning Res. 235, 48019–48037 (2024)."). Although this effort highlighted the potential of foundation models for analyzing sleep data, it targeted primarily sleep-specific outcomes and lacked the flexibility to accommodate the diverse configurations of PSG recordings. These limitations emphasize the need for models that can generalize across heterogeneous datasets and systematically uncover the role of sleep in predicting a wider range of diseases.

In this paper we present SleepFM, a foundation model trained on over 585,000 h of PSG data from 65,000+ participants. SleepFM captures the diverse information present in multimodal sleep recordings—integrating EEG, ECG, EMG and respiratory signals. Its channel-agnostic architecture enables joint learning across several modalities, producing representations that generalize across environments. We also introduce a new leave-one-out (LOO) contrastive learning (CL) (LOO-CL) algorithm that aligns information across modalities during pretraining while remaining resilient to missing or heterogeneous channels during inference. Our model uses 5–25 times more data than previously trained supervised sleep[3](/articles/s41591-025-04133-4#ref-CR3 "Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. NPJ Digit. Med. 5, 103 (2022)."),[7](/articles/s41591-025-04133-4#ref-CR7 "Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. NPJ Digit. Med. 4, 72 (2021)."),[9](/articles/s41591-025-04133-4#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024)."),[10](/articles/s41591-025-04133-4#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018).") or biosignal models[15](/articles/s41591-025-04133-4#ref-CR15 "Zhang, S. et al. ECGFM: a foundation model for ecg analysis trained on a multi-center million-ECG dataset. Inform. Fusion 124, 103363 (2025)."),[16](/articles/s41591-025-04133-4#ref-CR16 "Cui, W. et al. Neuro-GPT: towards a foundation model for EEG. In Proc 2024 IEEE International Symposium on Biomedical Imaging (ISBI) 1–5 (IEEE, 2024).").

Inspired by phenome-wide association studies (PheWAS)[17](/articles/s41591-025-04133-4#ref-CR17 "Pendergrass, S. A. et al. The use of phenome-wide association studies (PheWAS) for exploration of novel genotype-phenotype relationships and pleiotropy discovery. Genet. Epidemiol. 35, 410–422 (2011)."), we examined whether sleep characteristics, as captured by SleepFM, can predict the onset of a wide range of diseases. Leveraging electronic health record (EHR) disease codes, we develop a framework to systematically explore predictive associations between multimodal sleep and diverse health conditions.




## Dataset and SleepFM architecture

We describe our dataset and training procedures in detail in [Methods](/articles/s41591-025-04133-4#Sec8). Briefly, we used PSG data from four primary cohorts: Stanford Sleep Clinic (SSC)[11](/articles/s41591-025-04133-4#ref-CR11 "Thapa, R. et al. SleepFM: multi-modal representation learning for sleep across brain activity, ECG and respiratory signals. Proc. Mach. Learning Res. 235, 48019–48037 (2024)."), BioSerenity[18](/articles/s41591-025-04133-4#ref-CR18 "Hanif, U. et al. Automatic detection of chronic insomnia from polysomnographic and clinical variables using machine learning. In Proc 2023 45th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC) 1–5 (IEEE, 2023)."),[19](/articles/s41591-025-04133-4#ref-CR19 "Hanif, U. et al. Associations between self-reported parasomnias and psychiatric illness in 370,000 patients with sleep disorders. Psychiatr. Clin. Neurosci. 78, 667–677 (2024)."), the Multi-Ethnic Study of Atherosclerosis (MESA)[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[21](/articles/s41591-025-04133-4#ref-CR21 "Chen, X. et al. Racial/ethnic differences in sleep disturbances: the multi-ethnic study of atherosclerosis (MESA). Sleep 38, 877–888 (2015).") and the Outcomes of Sleep Disorders in Older Men (MrOS)[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[22](/articles/s41591-025-04133-4#ref-CR22 "Blackwell, T. et al. Associations between sleep architecture and sleep-disordered breathing and cognition in older community-dwelling men: the osteoporotic fractures in men sleep study. J. Am. Geriatr. Soc. 59, 2217–2225 (2011)."). SSC includes 35,052 studies from participants aged 1–100 years; BioSerenity adds 18,900 studies from people aged 7–90 years; MESA and MrOS contribute 2,237 and 3,930 PSGs, respectively, from older adults. Together, these cohorts span 65,000 participants and more than 585,000 h of sleep recordings. We further evaluated generalization using the Sleep Heart Health Study (SHHS)[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[23](/articles/s41591-025-04133-4#ref-CR23 "Quan, S. F. et al. The sleep heart health study: design, rationale, and methods. Sleep 20, 1077–1085 (1997).")—a multicenter dataset of 6,441 adults aged 40 years and older, held out from pretraining and used solely for transfer learning. Dataset distributions postfiltering are shown in Table [1](/articles/s41591-025-04133-4#Tab1). Demographics for SSC and BioSerenity appear in Extended Data Tables [1](/articles/s41591-025-04133-4#Tab3) and [2](/articles/s41591-025-04133-4#Tab4), whereas details for SHHS, MrOS and MESA are available in their respective publications.

**Table 1 Distribution of PSG recordings across cohorts and data splits**

[Full size table](/articles/s41591-025-04133-4/tables/1)

Our preprocessing pipeline begins by resampling all signals to 128 Hz for consistency across cohorts. Signals are then segmented into 5-s windows, which serve as the model’s fundamental input tokens. The architecture includes one-dimensional (1D) convolutional layers for feature extraction, followed by channel-agnostic attention pooling to address variability in channel number and order across cohorts. A transformer block captures temporal dependencies over a 5-min context window. During pretraining, we use a multimodal CL objective to align representations across all modalities. The robustness of the model stems from its channel-agnostic design, enabling it to accommodate missing channels, varying channel counts and heterogeneous signal types.

For downstream tasks, we leverage the pretrained model’s embeddings through lightweight fine-tuning. The token embeddings from different modalities are pooled again and processed by a two-layer long short-term memory (LSTM) network before passing through task-specific output heads. For patient-level prediction tasks (for example, disease prediction), an additional temporal pooling layer before the output layer compresses all token embeddings into a single 128-dimensional embedding.

To evaluate model performance across tasks, we use appropriate task-specific metrics. For classification tasks such as sex classification, we report area under the receiver operating characteristic curve (AUROC) and area under the precision-recall curve (AUPRC); for sleep apnea classification we show confusion matrices and report accuracy; for age estimation, we use mean absolute error (MAE) and Pearson correlation. Sleep staging is evaluated using the *F*1 score, which is well suited for class-imbalanced settings. For disease prediction, we report AUROC and Harrell’s concordance index (C-Index)—a standard survival analysis metric that measures the proportion of correctly ranked risk pairs. All metrics range from 0 to 1, with higher values indicating better performance; 95% confidence intervals (CIs) are computed using bootstrapping.




## SleepFM supports standard sleep analysis tasks

After pretraining SleepFM, we assessed the general utility of its learned representations by fine-tuning on four common benchmark tasks: age estimation, sex classification, sleep stage classification and sleep apnea classification. Although these tasks are not the main focus of our work, they are useful validations showing that the model captures fundamental sleep patterns. For all tasks, we trained lightweight LSTM-based heads on top of the frozen multimodal embeddings derived from entire nights of PSG data.

For age estimation, we assessed the ability of the model to predict chronological age. Overall performance is shown in Extended Data Fig. [1](/articles/s41591-025-04133-4#Fig5), with the model achieving a MAE of 7.33 years and a correlation coefficient of 0.88. Performance varied across age groups, with higher accuracy in pediatric and middle-aged participants and greater error in elderly adults, suggesting that age prediction is more challenging at the extremes of the age spectrum. Sex classification yielded an AUROC of 0.86 (0.85–0.87) and AUPRC of 0.90 (0.89–0.91). For sleep stage classification, we fine-tuned a LSTM-based classifier to distinguish Wake, Stage 1, Stage 2, Stage 3 and rapid eye movement (REM) using 5-s windows—a more granular resolution than the standard 30-s epochs, which has been shown to improve precision in certain conditions (for example, narcolepsy[10](/articles/s41591-025-04133-4#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018).")). As shown in Supplementary Fig. [1](/articles/s41591-025-04133-4#MOESM1), SleepFM performs well on Wake, Stage 2 and REM, with expected confusion in transitional stages like Stage 1—consistent with known human scoring variability. We report results across SSC, MESA, MrOS and SHHS, where SleepFM achieves competitive performance compared to U-Sleep[7](/articles/s41591-025-04133-4#ref-CR7 "Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. NPJ Digit. Med. 4, 72 (2021)."), YASA[24](/articles/s41591-025-04133-4#ref-CR24 "Vallat, R. & Walker, M. P. An open-source, high-performance tool for automated sleep staging. eLife 10, e70092 (2021)."), GSSC[25](/articles/s41591-025-04133-4#ref-CR25 "Hanna, J. & Flöel, A. An accessible and versatile deep learning-based sleep stage classifier. Front. Neuroinform. 17, 1086634 (2023).") and STAGES[10](/articles/s41591-025-04133-4#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018).")—state-of-the-art sleep staging models, as shown in Extended Data Tables [3](/articles/s41591-025-04133-4#Tab5) and [4](/articles/s41591-025-04133-4#Tab6). Furthermore, we compare SleepFM to three PhysioEx[26](/articles/s41591-025-04133-4#ref-CR26 "Gagliardi, G., Alfeo, L., Cimino, M. G. C. A., Valenza, G. & De Vos, M. Physioex, a new Python library for explainable sleep staging through deep learning. Physiol Meas. 46, 025006 (2025).") models on the public datasets DCSM[27](/articles/s41591-025-04133-4#ref-CR27 "Perslev, M. et al. DCSM Sleep staging dataset (University of Copenhagen). Electronic Research Data Archive 
                  https://erda.ku.dk/public/archives/db553715ecbe1f3ac66c1dc569826eef/published-archive.html
                  
                 (2021).") and HMC[28](/articles/s41591-025-04133-4#ref-CR28 "Alvarez-Estevez, D. & Rijsman, R. Haaglanden Medisch Centrum sleep staging database (v.1.1). PhysioNet 
                  https://doi.org/10.13026/t79q-fr32
                  
                 (2022).") in a fully external validation setting, achieving an *F*1 score of 0.68 on DCSM—outperforming all models—and 0.55 on HMC (Supplementary Table [1](/articles/s41591-025-04133-4#MOESM1)). Although the source alone has little impact, using several datasets for pretraining and fine-tuning improves generalization, boosting macro *F*1 by around 0.1 (Supplementary Tables [2](/articles/s41591-025-04133-4#MOESM1), [3](/articles/s41591-025-04133-4#MOESM1) and [4](/articles/s41591-025-04133-4#MOESM1)), consistent with previous work[26](/articles/s41591-025-04133-4#ref-CR26 "Gagliardi, G., Alfeo, L., Cimino, M. G. C. A., Valenza, G. & De Vos, M. Physioex, a new Python library for explainable sleep staging through deep learning. Physiol Meas. 46, 025006 (2025).").

For sleep apnea classification, we performed patient-level severity classification to distinguish between four commonly used severity groups on the basis of the apnea–hypopnea index (AHI): none (AHI < 5), mild (5 ≤ AHI < 15), moderate (15 ≤ AHI < 30) and severe (AHI ≥ 30). Across MESA, MrOs and SHHS, we observe competitive performance, with a severity classification accuracy of 0.69 and a presence classification accuracy (none/mild versus moderate/severe) of 0.87. The confusion matrix for apnea classification is shown in Fig. [1](/articles/s41591-025-04133-4#Fig1).

**Fig. 1: Overview of SleepFM framework.**

[![Fig. 1: Overview of SleepFM framework.](//media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_Fig1_HTML.png)](/articles/s41591-025-04133-4/figures/1)

**a**, PSG setup and dataset statistics across several sleep centers. Bars show the number of independent PSG recordings (participants) per cohort and the corresponding total recording hours. **b**, Multimodal contrastive pretraining: raw signals from each modality are encoded by a CNN, channel embeddings are pooled within modality and a temporal transformer with temporal pooling yields sequence-level representations for LOO-CL. C: channels, S: sequence length, D: embedding dimension. **c**, Fine-tuning using frozen embeddings for downstream tasks (sleep staging, apnea detection, disease prediction). Eight hours of multimodal embeddings are aggregated to patient-level representations, concatenated with age and sex, and passed to an LSTM followed by a fully connected layer. **d**, Evaluation across representative tasks and clinical applications. Left and middle: confusion matrices for sleep staging (SHHS) and AHI categories (SSC) shown as row-normalized percentages. Right: disease prediction performance on the Stanford cohort (*n* = 5,019 participants). Box plots summarize 1,000 patient-level bootstrap resamples: faint dots (individual bootstrap draws), and vertical line with end caps (95% bootstrap percentile CI). Numeric labels are means. Number of positive samples for each disease: CKD (354), death (224), dementia (221), HF (283) and stroke (297).

[Full size image](/articles/s41591-025-04133-4/figures/1)




## SleepFM enables comprehensive disease prediction from sleep data

To enable disease prediction, we paired SSC data with EHRs, extracting all diagnostic codes (International Classification of Diseases, ninth revision (ICD-9) and International Classification of Diseases, tenth revision (ICD-10)) and their timestamps. These codes were mapped to phecodes—a hierarchical system of 1,868 disease categories designed for PheWAS[29](/articles/s41591-025-04133-4#ref-CR29 "Wu, P. et al. Mapping ICD-10 and ICD-10-CM codes to phecodes: workflow development and initial evaluation. JMIR Med. Inform. 7, e14325 (2019)."). The timestamp of each phecode was defined as the earliest among its corresponding ICD codes. Positive cases were defined as patients whose first phecode instance occurred more than 7 days after the sleep study, avoiding trivial associations. We excluded phecodes with prevalence below 1.5% to ensure statistical power, resulting in 1,041 phecodes for evaluation. For model fine-tuning, we used a multilabel extension of the Cox proportional hazards (CoxPH) loss, averaging independent losses computed for each label.

Figure [2](/articles/s41591-025-04133-4#Fig2) illustrates the performance of SleepFM across disease categories on the test set. Although performance varies across categories, SleepFM demonstrates strong results in several areas, including neoplasms, pregnancy complications, circulatory conditions and mental disorders. Overall, 130 future diseases achieved a C-Index and AUROC of at least 0.75 on held-out participants (Bonferroni-corrected *P* < 0.01), as summarized in Supplementary Table [5](/articles/s41591-025-04133-4#MOESM1). AUROC was calculated using a 6-year horizon, meaning a condition is considered positive if the patient develops the disease within 6 years of their PSG study. The 6-year horizon for AUROC calculation was chosen to balance performance and account for both long-term and short-term conditions. Supplementary Fig. [2](/articles/s41591-025-04133-4#MOESM1) shows AUROC values across 1–6 year horizons for several conditions.

**Fig. 2: Performance of SleepFM on the held-out test set (*n* = 5,019) as stratified by disease category.**

[![Fig. 2: Performance of SleepFM on the held-out test set (n = 5,019) as stratified by disease category.](//media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_Fig2_HTML.png)](/articles/s41591-025-04133-4/figures/2)

Individual dots represent a disease within a category. The results are evaluated using two metrics: the C-Index, which measures the model’s ability to rank patient risk accurately, and the 6-year AUROC, which assesses the model’s discrimination performance by evaluating its ability to distinguish between patients who experience the event of interest and those who do not within a 6-year prediction window. For reference, the horizontal dashed line indicates a threshold of 0.75.

[Full size image](/articles/s41591-025-04133-4/figures/2)

The model showed high accuracy for mild cognitive impairment (AUROC 0.84 (0.80–0.880)), aligning with studies showing sleep disturbances as early markers of cognitive decline[30](/articles/s41591-025-04133-4#ref-CR30 "Wennberg, A. M. V., Wu, M. N., Rosenberg, P. B. & Spira, A. P. Sleep disturbance, cognitive decline, and dementia: a review. Semin. Neurol. 37, 395–406 (2017)."). Strong performance was observed for Parkinson’s disease (0.93 (0.89–0.96)), where sleep disorders are increasingly recognized as potential early indicators[31](/articles/s41591-025-04133-4#ref-CR31 "Stefani, A. & Högl, B. Sleep in Parkinson’s disease. Neuropsychopharmacology 45, 121–128 (2020)."), and developmental delays and disorders (0.84 (0.79–0.87)). Among circulatory conditions, the model effectively predicted hypertensive heart disease (0.88 (0.85–0.91)) and intracranial hemorrhage (0.82 (0.73–0.90)), consistent with established links between sleep disorders and cardiovascular risk[32](/articles/s41591-025-04133-4#ref-CR32 "Ravichandran, R. et al. The interplay between sleep disorders and cardiovascular diseases: a systematic review. Cureus 15, e45898 (2023)."). In the Neoplasm category, the model showed strong predictive performance for several cancers: prostate cancer (0.90 (0.87–0.93)), breast cancer (0.90 (0.86–0.93)) and melanomas of skin (0.83 (0.76–0.90)). These findings align with existing literature linking sleep patterns to cancer risk[33](/articles/s41591-025-04133-4#ref-CR33 "Shigesato, M. et al. Association between sleep duration and breast cancer incidence: the multiethnic cohort. Int. J. Cancer 146, 664–670 (2020)."),[34](/articles/s41591-025-04133-4#ref-CR34 "Freeman, J. R. et al. Actigraphy-derived measures of sleep and risk of prostate cancer in the UK Biobank. J. Natl Cancer Inst. 116, 434–444 (2024).").

Drawing on sleep expertise and previous literature, we identified 14 conditions with strong potential links to sleep patterns. Previous studies associate sleep regularity with mortality[35](/articles/s41591-025-04133-4#ref-CR35 "Windred, D. P. et al. Sleep regularity is a stronger predictor of mortality risk than sleep duration: a prospective cohort study. Sleep 47, zsad253 (2024)."), prolonged sleep with early neurodegeneration[36](/articles/s41591-025-04133-4#ref-CR36 "Westwood, A. J. et al. Prolonged sleep duration as a marker of early neurodegeneration predicting incident dementia. Neurology 88, 1172–1179 (2017).") and sleep disturbances with dementia[37](/articles/s41591-025-04133-4#ref-CR37 "Shi, L. et al. Sleep disturbances increase the risk of dementia: a systematic review and meta-analysis. Sleep Med. Rev. 40, 4–16 (2018)."), stroke[38](/articles/s41591-025-04133-4#ref-CR38 "Mc Carthy, C. E. et al. Sleep patterns and the risk of acute stroke: results from the interstroke international case-control study. Neurology 100, e2191–e2203 (2023).") and cardiovascular outcomes[9](/articles/s41591-025-04133-4#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024)."). Related phecodes were grouped into unified disease categories in consultation with a medical doctor (Supplementary Table [6](/articles/s41591-025-04133-4#MOESM1)). Results for selected conditions—including death, stroke, heart failure (HF) and dementia—are shown in Extended Data Fig.[2](/articles/s41591-025-04133-4#Fig6). SleepFM demonstrates strong predictive performance, with particularly high accuracy for death (AUROC 0.84 (0.80–0.88)), HF (0.83 (0.79–0.86)), chronic kidney disease (CKD) (0.82 (0.79–0.85)), dementia (0.87 (0.84–0.91)) and stroke (0.81 (0.78–0.85)). All reported associations are statistically significant (*P* < 0.01, Bonferroni-corrected).

To better understand the physiological basis of disease prediction, we analyzed model performance stratified by both sleep stages and signal modalities. We found that although most sleep stages contribute similarly to disease prediction, certain stages such as Stage 1/2 and REM can offer slightly better predictive power for specific conditions, including cardiovascular and neurodegenerative diseases. Likewise, different signal modalities showed nuanced differences, with BAS signals better capturing mental and neurological conditions, respiratory signals more predictive of respiratory and metabolic disorders, and electrocardiogram (EKG) signals more informative for circulatory diseases. Although these differences align with known physiology, the overall predictive performance was highest when combining all modalities. Full results and condition-specific breakdowns are provided in Supplementary Figs. [3](/articles/s41591-025-04133-4#MOESM1) and [4](/articles/s41591-025-04133-4#MOESM1) and Supplementary Tables [7](/articles/s41591-025-04133-4#MOESM1) and [8](/articles/s41591-025-04133-4#MOESM1). Furthermore, we trained separate SleepFM models on each modality to directly assess modality-level importance. Performance comparisons stratified by disease category, presented in Supplementary Tables [9](/articles/s41591-025-04133-4#MOESM1) and [10](/articles/s41591-025-04133-4#MOESM1), further confirm that combining all modalities yields the optimal performance.




## SleepFM demonstrates robust generalization across time and cohorts

We evaluate the generalization capabilities of SleepFM across temporal distribution shifts and external site validation. For temporal generalization, we test the model on a separate cohort comprising Stanford patients from 2020 onwards. All model pretraining and training was done on data from before 2020. Despite the limited follow-up period, SleepFM maintains strong predictive performance. Extended Data Fig. [3](/articles/s41591-025-04133-4#Fig7) shows results for our 14 selected conditions, with particularly robust and statistically significant performance (Bonferroni-corrected *P* < 0.01) for death (0.83 (0.73–0.91)), HF (0.80 (0.75–0.85)) and dementia (0.83 (0.76–0.89)). Comprehensive temporal-split performance across all disease phenotypes and categories is provided in Supplementary Figs. [5](/articles/s41591-025-04133-4#MOESM1) and [6](/articles/s41591-025-04133-4#MOESM1). Supplementary Fig. [7](/articles/s41591-025-04133-4#MOESM1) further reports temporal-split performance comparisons with baseline models, stratified by disease category.

To assess cross-site generalization, we evaluate SleepFM’s transfer learning capabilities on SHHS—a dataset entirely excluded from the pretraining phase. We use the pretrained model to extract embeddings and then fine-tune it on a subset of SHHS. Specifically, the SHHS fine-tuning set includes 3,291 participants, and the test set includes 2,000 participants. Due to differences in task availability between SSC and SHHS, our evaluation focuses on six overlapping cardiovascular conditions. This setup mimics real-world deployment scenarios where foundation models must be adapted to new clinical sites with minimal supervision.

As shown in Fig. [3](/articles/s41591-025-04133-4#Fig3), SleepFM demonstrates strong transfer learning performance across key outcomes. For example, the model achieves statistically significant predictive accuracy (Bonferroni-corrected *P* < 0.01) for stroke (0.82 (0.76–0.87)), congestive HF (0.85 (0.82–0.88)) and mortality related to cardiovascular disease (0.88 (0.83–0.91)).

**Fig. 3: SleepFM prediction performance on the SHHS test set (*n* = 2,000 participants).**

[![Fig. 3: SleepFM prediction performance on the SHHS test set (n = 2,000 participants).](//media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_Fig3_HTML.png)](/articles/s41591-025-04133-4/figures/3)

Due to differences in available outcome data between SHHS and Stanford datasets, evaluation was limited to a subset of conditions. Results demonstrate transfer learning capabilities across these key clinical outcomes, including stroke, congestive HF and cardiovascular disease-related mortality. Each panel uses barplots derived from 1,000 patient-level bootstrapping: faint points are individual bootstrap draws, and the vertical line with end caps marks the 95% bootstrap percentile CI. Numbers above bars report the mean. Metrics are C-Index (top) and AUROC at 6 years (bottom). The number of positive samples for each outcome is as follows: angina (704), cardiovascular disease death (128), congestive HF (190), coronary heart disease death (80), myocardial infarction (103) and stroke (95). All conditions are statistically significant with a *P* value <0.01 after Bonferroni correction.

[Full size image](/articles/s41591-025-04133-4/figures/3)




## SleepFM surpasses supervised baselines in disease prediction

We compare SleepFM against two supervised baselines: Demographics and End-to-End PSG. The demographics baseline is a multilayer perceptron (MLP) trained on structured clinical features (age, sex, race/ethnicity and body mass index (BMI)). This baseline includes more demographic variables than the SleepFM-based models, which only use age and sex. The End-to-End PSG model is trained directly on raw PSG data using the same architecture and parameter count as SleepFM, and it includes age and sex but does not use any pretraining. From Fig. [4](/articles/s41591-025-04133-4#Fig4), we observe that the percentage difference in AUROC between SleepFM and both baseline models ranges from 5% to 17%. The magnitude of improvement varies across disease categories; for example, gains are more pronounced in neurological and hematopoietic conditions, whereas in neoplasm-related conditions the improvements are comparatively modest. Supplementary Fig. [8](/articles/s41591-025-04133-4#MOESM1) reports the overall test-set performance comparison between SleepFM and the baseline models across all disease phenotypes.

**Fig. 4: Performance improvements of SleepFM over baseline models across disease categories on Stanford test set (*n* = 5,019 participants).**

[![Fig. 4: Performance improvements of SleepFM over baseline models across disease categories on Stanford test set (n = 5,019 participants).](//media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_Fig4_HTML.png)](/articles/s41591-025-04133-4/figures/4)

SleepFM and the End-to-End PSG model include age and sex demographic features, whereas the demographics-only model includes age, sex, BMI and race/ethnicity. Each box shows the distribution of disease-level percentage improvements of SleepFM relative to each baseline within the indicated disease category. Improvements are shown for both C-Index (top) and 6-year AUROC (bottom) metrics. Boxes represent the interquartile range (IQR), with whiskers extending to 1.5× IQR and outliers shown as points. Diamonds denote the mean improvement within each category. The horizontal dashed line at zero indicates no improvement.

[Full size image](/articles/s41591-025-04133-4/figures/4)

Next, we evaluated three different variants of SleepFM using identical training configurations, as shown in Table [2](/articles/s41591-025-04133-4#Tab2) and Extended Data Table [5](/articles/s41591-025-04133-4#Tab7). SleepFM-LSTM (without Demo) uses SleepFM embeddings with a two-layer LSTM fine-tuning head but no demographic features. SleepFM-Linear uses SleepFM embeddings with a simple linear prediction head and includes age and sex. Finally, SleepFM-LSTM, combines the pretrained SleepFM embeddings with a two-layer LSTM head and includes age and sex.

**Table 2 Comparison of category-averaged AUROC across SleepFM variants and baselines**

[Full size table](/articles/s41591-025-04133-4/tables/2)

As seen in Table [2](/articles/s41591-025-04133-4#Tab2), the demographics-only baseline performs well, reflecting the fact that many diseases are associated strongly with age, sex, BMI and race/ethnicity. For example, in the Neoplasm category, older age is a strong predictor of cancer risk. Nevertheless, all SleepFM-based models, including the SleepFM-LSTM (without Demo) variant, consistently outperform the demographics and End-to-End PSG baselines across most disease categories. This demonstrates the benefit of using pretrained SleepFM embeddings for disease prediction. Furthermore, SleepFM-LSTM (without Demo) achieves over +5 AUROC points in 9 out of 14 conditions, whereas SleepFM-Linear and SleepFM-LSTM achieve over +5 AUROC points in 12 out of 14 conditions, compared to supervised demographics baseline. As seen from the 95% CI bars, these improvements are robust, with most differences being larger than the uncertainty intervals. Finally, SleepFM-Linear performs comparably to SleepFM-LSTM, suggesting that the strength of the model lies in the pretrained embeddings rather than the complexity of the downstream head. Percentage improvement comparisons across models are provided in Supplementary Fig. [9](/articles/s41591-025-04133-4#MOESM1), and a scatterplot comparison of all disease phenotypes across different fine-tuning architectures on top of SleepFM is shown in Supplementary Fig. [10](/articles/s41591-025-04133-4#MOESM1).

To further examine disease-specific performance, full results are provided in Supplementary Tables [11](/articles/s41591-025-04133-4#MOESM1), [12](/articles/s41591-025-04133-4#MOESM1) and [13](/articles/s41591-025-04133-4#MOESM1), and clinician-selected conditions are presented in Supplementary Fig. [11](/articles/s41591-025-04133-4#MOESM1). These comparisons show that SleepFM achieves substantial gains across several neurological, mental, circulatory, endocrine/metabolic and respiratory conditions. For neurological and mental disorders, SleepFM attains higher C-Index scores for senile dementia (0.99 (0.98–1.00) versus 0.87 (0.75–0.96)), myoneural disorders (0.81 (0.73–0.88) versus 0.42 (0.28–0.55)) and developmental delays (0.80 (0.77–0.84) versus 0.58 (0.51–0.64)). For circulatory diseases, SleepFM outperforms in atherosclerosis (0.92 (0.88–0.95) versus 0.74 (0.64–0.89)) and acute pulmonary heart disease (0.80 (0.75–0.85) versus 0.74 (0.68–0.80)). Improvements in endocrine/metabolic conditions include diabetes type 2 with circulatory complications (0.87 (0.83–0.91) versus 0.79 (0.74–0.85)) and diabetic retinopathy (0.81 (0.77–0.85) versus 0.75 (0.69–0.80)). For respiratory conditions, SleepFM achieves higher C-Index in respiratory insufficiency (0.79 (0.72–0.85)] versus 0.59 (0.51–0.67)) and failure (0.77 (0.73–0.80) versus 0.70 (0.65–0.74)). These findings highlight the versatility of SleepFM in predicting a broad range of diseases beyond what is captured by demographics alone.

Similarly, full comparisons with the End-to-End PSG model are provided in Supplementary Table [14](/articles/s41591-025-04133-4#MOESM1). This comparison highlights the value of foundation model pretraining: although both models share similar architecture and input signals, SleepFM benefits from self-supervised pretraining, enabling more robust and informative representations. This advantage is reflected in consistent performance gains across neurological, circulatory, endocrine/metabolic and respiratory conditions. For neurological and mental disorders, SleepFM outperforms the end-to-end model in myoneural disorders (0.84 (0.75–0.91) versus 0.54 (0.40–0.69)), developmental delays (0.84 (0.79–0.87) versus 0.61 (0.52–0.69)) and speech/language disorders (0.83 (0.74–0.90) versus 0.71 (0.60–0.83)). For circulatory conditions, improvements are observed in atherosclerosis of native arteries of the extremities (0.95 (0.92–0.98) versus 0.65 (0.61–0.69)), atherosclerosis of the extremities (0.84 (0.75–0.90) versus 0.78 (0.71–0.85)) and acute pulmonary heart disease (0.84 (0.77–0.90) versus 0.76 (0.69–0.83)). In endocrine/metabolic disorders, SleepFM demonstrates stronger performance for predicting diabetes with circulatory complications (0.89 (0.85–0.93) versus 0.79 (0.70–0.87)), neurological manifestations (0.86 (0.81–0.90) versus 0.73 (0.67–0.78)) and diabetic retinopathy (0.84 (0.79, 0.89) versus 0.76 (0.69–0.82)). Respiratory conditions also benefit, with better performance in predicting respiratory insufficiency (0.82 (0.72–0.91) versus 0.64 (0.54–0.73)) and respiratory failure (0.76 (0.71–0.82) versus 0.68 (0.62–0.74)). In predicting all-cause mortality, SleepFM achieves a AUROC of 0.85 (0.80–0.89), outperforming both the Demographic baseline and End-to-End PSG model, which achieve AUROC of 0.78 (0.72–0.82).

Finally, we compare fine-tuning scalability by evaluating SleepFM alongside two baseline models as we increase the amount of fine-tuning data and measure performance on the same test set. These results are shown in Extended Data Fig. [4](/articles/s41591-025-04133-4#Fig8) for SHHS and Extended Data Fig. [5](/articles/s41591-025-04133-4#Fig9) and Supplementary Fig. [12](/articles/s41591-025-04133-4#MOESM1) for SSC. In both plots, the key observation is that SleepFM consistently outperforms the supervised baselines, with its performance improving steadily as more data are used, remaining above the baseline curves for nearly all conditions. For SHHS, SleepFM surpasses the Demographics baseline in five out of six conditions across all data percentages, with particularly large improvements in smaller dataset splits. For example, SleepFM trained on just 10% of the data outperforms the Demographics baseline trained on five times more data across all conditions in SSC and four out of six conditions in SHHS (for example, cardiovascular disease death, congestive HF, myocardial infarction and stroke). SleepFM also outperforms the End-to-End PSG baseline in five out of six conditions, although the gap is slightly smaller than with the Demographics baseline. SleepFM exhibits stable scaling behavior across data percentages, with smoother performance improvements, whereas the baseline models show greater variability.




## Discussion

This study presents a large-scale foundation model for sleep analysis, developed on more than 585,000 h of PSG data from 65,000 participants. Our work makes several contributions. First, we address challenges in sleep analysis by leveraging self-supervised learning to train a foundation model that learns from unlabeled data and is agnostic to channel type and number, enabling broad exploration of sleep data across diverse clinical settings. Second, through extensive evaluation across 1,041 disease phenotypes, we demonstrate sleep’s broad predictive power for diverse health outcomes. The model shows strong performance in predicting death (C-Index 0.84), dementia (0.85), HF (0.80) and CKD (0.79). Third, we demonstrated transfer learning capabilities through strong performance on the SHHS dataset. Despite SHHS being entirely excluded from pretraining, our model maintains robust predictive power for key outcomes such as stroke (C-Index 0.81), congestive HF (0.83) and death related to cardiovascular disease (0.86). Finally, SleepFM achieves competitive performance on standard sleep analysis tasks, including sleep staging and apnea detection, with mean *F*1 scores ranging from 0.70 to 0.78 across cohorts—comparable to state-of-the-art models such as U-Sleep[7](/articles/s41591-025-04133-4#ref-CR7 "Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. NPJ Digit. Med. 4, 72 (2021)."), GSSC[25](/articles/s41591-025-04133-4#ref-CR25 "Hanna, J. & Flöel, A. An accessible and versatile deep learning-based sleep stage classifier. Front. Neuroinform. 17, 1086634 (2023)."), STAGES[10](/articles/s41591-025-04133-4#ref-CR10 "Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. Nat. Commun. 9, 5229 (2018).") and YASA[24](/articles/s41591-025-04133-4#ref-CR24 "Vallat, R. & Walker, M. P. An open-source, high-performance tool for automated sleep staging. eLife 10, e70092 (2021)."). Furthermore, in a fully external validation setting, SleepFM outperforms all models on DCSM (*F*1 = 0.68) and is competitive with the PhysioEx[26](/articles/s41591-025-04133-4#ref-CR26 "Gagliardi, G., Alfeo, L., Cimino, M. G. C. A., Valenza, G. & De Vos, M. Physioex, a new Python library for explainable sleep staging through deep learning. Physiol Meas. 46, 025006 (2025).") models. For apnea classification, SleepFM achieves 87% accuracy in MESA, MrOS and SHHS, comparable to state-of-the-art models[8](/articles/s41591-025-04133-4#ref-CR8 "Nassi, T. E. et al. Automated scoring of respiratory events in sleep with a single effort belt and deep neural networks. IEEE Trans. Biomed. Eng. 69, 2094–2104 (2021).").

SleepFM predicts all-cause mortality more accurately than both the Demographics-based model and the End-to-End PSG model, achieving a higher C-Index of 0.84 (0.81–0.87), compared to 0.79 (0.75–0.82). This indicates that pretraining efficiently captures subtle mortality-related signals in the PSG data. Research shows strong association between all-cause mortality and sleep-related factors, including high arousal burden[39](/articles/s41591-025-04133-4#ref-CR39 "Shahrbabaki, S. S., Linz, D., Hartmann, S., Redline, S. & Baumert, M. Sleep arousal burden is associated with long-term all-cause and cardiovascular mortality in 8001 community-dwelling older men and women. Eur. Heart J. 42, 2088–2099 (2021)."), low REM sleep[40](/articles/s41591-025-04133-4#ref-CR40 "Leary, E. B. et al. Association of rapid eye movement sleep with mortality in middle-aged and older adults. JAMA Neurol. 77, 1241–1251 (2020)."), sleep-disordered breathing[41](/articles/s41591-025-04133-4#ref-CR41 "Young, T. et al. Sleep disordered breathing and mortality: eighteen-year follow-up of the Wisconsin sleep cohort. Sleep 31, 1071–1078 (2008)."), hypoxemia and low sleep efficiency[42](/articles/s41591-025-04133-4#ref-CR42 "Wallace, M. L. et al. Physiological sleep measures predict time to 15-year mortality in community adults: application of a novel machine learning framework. J. Sleep Res. 30, e13386 (2021)."). Increased ‘brain age’ derived from EEG has also been identified as an important predictor of mortality[3](/articles/s41591-025-04133-4#ref-CR3 "Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. NPJ Digit. Med. 5, 103 (2022)."). SleepFM probably integrates these multifactorial contributors, capturing respiratory events, sleep fragmentation, arousal burden and sleep efficiency, along with markers of cardiovascular, metabolic and other diseases.

Predictive and prognostic models for neurological and mental disorders are advancing rapidly, offering the potential for earlier and more individualized treatment. Among the top conditions predicted by SleepFM were Alzheimer’s disease and Parkinson’s disease, with C-Indices of 0.91 (0.87–0.98) and 0.89 (0.85–0.92), respectively. Sleep disorders are associated strongly with preclinical Alzheimer’s disease[43](/articles/s41591-025-04133-4#ref-CR43 "Bubu, O. M. et al. Sleep, cognitive impairment, and Alzheimer’s disease: a systematic review and meta-analysis. Sleep 40, zsw032 (2017)."), including abnormalities in non-REM sleep, such as reduced slow-wave activity[44](/articles/s41591-025-04133-4#ref-CR44 "Ju, Yo-El. S. et al. Slow wave sleep disruption increases cerebrospinal fluid amyloid-β levels. Brain 140, 2104–2111 (2017)."), REM sleep disturbances[45](/articles/s41591-025-04133-4#ref-CR45 "Falgàs, N. & Walsh, C. M. The importance of rapid eye movement sleep and its implications for Alzheimer’s disease. Sleep 47, zsae117 (2024).") and decreased spindle activity[46](/articles/s41591-025-04133-4#ref-CR46 "Weng, Yuan-Yuan, Lei, X. & Yu, J. Sleep spindle abnormalities related to Alzheimer’s disease: a systematic mini-review. Sleep Med. 75, 37–44 (2020)."). In early Alzheimer’s disease, REM sleep abnormalities have been linked to basal forebrain cholinergic lesions, which probably contribute to cognitive decline[47](/articles/s41591-025-04133-4#ref-CR47 "André, C. et al. REM sleep is associated with the volume of the cholinergic basal forebrain in aMCI individuals. Alzheimers Res Ther 15, 151 (2023)."). Similarly, Parkinson’s disease is frequently preceded by REM sleep behavior disorder, characterized by REM sleep without atonia and abnormalities in BAS and ECG patterns[48](/articles/s41591-025-04133-4#ref-CR48 "Brink-Kjaer, A. et al. End-to-end deep learning of polysomnograms for classification of rem sleep behavior disorder. In Proc 2022 44th Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC) 2941–2944 (IEEE, 2022)."). Recent studies have also shown that respiratory signals can capture phenotypes specific to Parkinson’s disease[49](/articles/s41591-025-04133-4#ref-CR49 "Yang, Y. et al. Artificial intelligence-enabled detection and assessment of Parkinson’s disease using nocturnal breathing signals. Nature Med. 28, 2207–2215 (2022).").

Consistent with these findings, SleepFM identified BAS as the strongest predictor of neurological and mental disorders, whereas respiratory signals were particularly effective in predicting senile dementia. Most studies in this domain rely on imaging modalities such as magnetic resonance imaging (MRI) and functional MRI (fMRI) to predict dementia. For example, one study using hippocampal MRI achieved a C-Index of 0.86 (ref. [50](/articles/s41591-025-04133-4#ref-CR50 "Li, H. et al. A deep learning model for early prediction of Alzheimer’s disease dementia based on hippocampal magnetic resonance imaging data. Alzheimers Dementia 15, 1059–1070 (2019).")), whereas another using fMRI reported an AUROC of 0.82 for predicting dementia up to 9 years in advance[51](/articles/s41591-025-04133-4#ref-CR51 "Ereira, S., Waters, S., Razi, A. & Marshall, C. R. Early detection of dementia with default-mode network effective connectivity. Nat. Mental Health 2, 787–800 (2024)."). Although direct performance comparisons are challenging due to differences in sample distributions, the ability of SleepFM to leverage PSG data to predict neurological and mental disorders underscores its potential as an alternative to imaging-based approaches.

Other established biomarkers for Alzheimer’s disease—such as amyloid PET, decreased cerebrospinal fluid β-amyloid42, and increased cerebrospinal fluid phosphorylated tau (for example, p-tau129)[52](/articles/s41591-025-04133-4#ref-CR52 "Hansson, O. et al. Association between CSF biomarkers and incipient Alzheimer’s disease in patients with mild cognitive impairment: a follow-up study. Lancet Neurol. 5, 228–234 (2006)."),[53](/articles/s41591-025-04133-4#ref-CR53 "Klunk, W. E. et al. Imaging brain amyloid in Alzheimer’s disease with Pittsburgh Compound-B. Ann. Neurol. 55, 306–319 (2004).")—have been used widely for diagnosis and prognosis. More recently, plasma p-tau217 has emerged as a promising less invasive marker[54](/articles/s41591-025-04133-4#ref-CR54 "Janelidze, S. et al. Plasma p-tau181 in Alzheimer’s disease: relationship to other biomarkers, differential diagnosis, neuropathology and longitudinal progression to Alzheimer’s dementia. Nature Med. 26, 379–386 (2020)."). Sleep biomarkers from PSG data offer a complementary, noninvasive tool for the prognosis of dementia and mild cognitive impairment.

SleepFM accurately modeled cardiovascular disease in both the SSC and SHHS datasets, leveraging data-driven methods commonly used in prognostic modeling of cardiovascular disease, particularly with ECG data[55](/articles/s41591-025-04133-4#ref-CR55 "Moreno-Sánchez, P. A. et al. ECG-based data-driven solutions for diagnosis and prognosis of cardiovascular diseases: a systematic review. Comput. Biol. Med. 172, 108235 (2024).") and lead II ECG from PSG studies[9](/articles/s41591-025-04133-4#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024)."). Foundation models have demonstrated state-of-the-art performance with ECG data in various cross-sectional tasks[15](/articles/s41591-025-04133-4#ref-CR15 "Zhang, S. et al. ECGFM: a foundation model for ecg analysis trained on a multi-center million-ECG dataset. Inform. Fusion 124, 103363 (2025)."). For predicting cardiovascular mortality over 10 years, a previous study reported an AUROC of 0.84 (0.78–0.89) in a subset of SHHS participants with sleep apnea, whereas SleepFM achieved a slightly higher AUROC of 0.88 (0.83–0.91). Similarly, for atrial fibrillation, earlier work reported an AUROC of 0.82 (ref. [9](/articles/s41591-025-04133-4#ref-CR9 "Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. J. Electrocardiol. 86, 153759 (2024).")), which aligns with SleepFM’s performance of 0.81 (0.78–0.84). Our ablation study further demonstrated that both ECG and respiratory signals contribute to the prediction of circulatory system phenotypes, suggesting that SleepFM integrates information on sleep apnea and heart activity in ways that are consistent with known disease mechanisms[56](/articles/s41591-025-04133-4#ref-CR56 "Mitra, A. K., Bhuiyan, A. R. & Jones, E. A. Association and risk factors for obstructive sleep apnea and cardiovascular diseases: a systematic review. Diseases 9, 88 (2021).").

Most disease categories, including neurological, circulatory, hematopoietic, mental disorders and endocrine/metabolic, were predicted with notably improved performance by SleepFM compared to the Demographics-based and End-to-End PSG baseline models. Many of these diseases are either associated with sleep (for example, type 2 diabetes[57](/articles/s41591-025-04133-4#ref-CR57 "Barone, M. T. U. & Menna-Barreto, L. Diabetes and sleep: a complex cause-and-effect relationship. Diabetes Res. Clin. Pract. 91, 129–137 (2011).")) or influenced directly by the signal modalities (for example, heart arrhythmia). Disrupted and unhealthy sleep contributes to dysfunction across several physiological systems, increasing the risk of diseases such as obesity, type 2 diabetes, hypertension, stroke and cardiovascular disease[58](/articles/s41591-025-04133-4#ref-CR58 "Yang, C. et al. Associations of sleep with cardiometabolic risk factors and cardiovascular diseases: an umbrella review of observational and Mendelian randomization studies. Sleep Med. Rev. 77, 101965 (2024)."). Sleep-specific conditions, including sleep apnea[56](/articles/s41591-025-04133-4#ref-CR56 "Mitra, A. K., Bhuiyan, A. R. & Jones, E. A. Association and risk factors for obstructive sleep apnea and cardiovascular diseases: a systematic review. Diseases 9, 88 (2021).") and less conclusively periodic leg movements[59](/articles/s41591-025-04133-4#ref-CR59 "Figorilli, M., Puligheddu, M., Congiu, P. & Ferri, R. The clinical importance of periodic leg movements in sleep. Curr. Treatment Options Neurol. 19, 10 (2017)."), are also linked to cardiovascular outcomes. Furthermore, specific EEG waveforms, such as coupled slow-wave and spindle activity, have been identified as markers of next-day blood glucose regulation[60](/articles/s41591-025-04133-4#ref-CR60 "Vallat, R., Shah, V. D. & Walker, M. P. Coordinated human sleeping brainwaves map peripheral body glucose homeostasis. Cell Rep. Med. 4, 101100 (2023).").

Despite these promising results, several limitations should be acknowledged. Although our dataset is large, it consists primarily of patients referred for sleep studies due to suspected sleep disorders or other medical conditions requiring overnight monitoring. This selection bias means our cohort is not representative of the general population, as people without sleep complaints or those with limited access to specialized sleep clinics are underrepresented. The model’s performance shows some degradation in temporal test sets, highlighting the challenge of maintaining predictive accuracy over time as clinical practices and patient populations evolve. Furthermore, interpreting the predictions made by SleepFM is inherently challenging due to the complexity of the learned features during training by a deep model. To mitigate this, we stratified the model’s performance across sleep stages and data modalities, and conducted evaluations on temporal test sets and unseen datasets to gain insights into its behavior. However, further work is needed to enhance case-level interpretability and understand the specific sleep patterns and features driving these predictions.

In building our model, we selected hyperparameters for SleepFM based on previous work and ensured all training converged in loss; more extensive hyperparameter searches may further boost performance. Furthermore, although we evaluated SleepFM’s transfer learning performance on an independent dataset, SHHS, only a subset of the full 1,041 conditions could be assessed in this sample due to limited diagnostic overlap with SSC; this prevented a comprehensive evaluation of generalization across the full spectrum of diseases. Our sleep apnea analysis was limited to binary and four-class classification on the basis of AHI thresholds; we did not explore more granular formulations such as AHI regression or event detection, we leave this for future research. Similarly, although SleepFM achieves competitive results on sleep staging tasks across most datasets, it lags behind specialized sleep staging models on certain external validation datasets (for example, HMC). Further specialized modeling may be necessary to optimize SleepFM for sleep staging.

This study underscores the potential of sleep-based foundation models for risk stratification and longitudinal health monitoring. By integrating several physiological signals and leveraging large-scale pretraining, SleepFM performs consistently well across diverse disease categories and outperforms supervised baselines. Its stable performance across fine-tuning splits suggests that pretraining may improve model generalizability, particularly in clinical contexts with limited labeled data. These results suggest that SleepFM can complement existing risk assessment tools and help identify early signs of diseases. As wearable sleep technologies continue to advance, models such as SleepFM may offer opportunities for noninvasive, real-time health monitoring. Future efforts should explore how combining sleep-based models with data from EHRs, omics and imaging can further enhance their utility.




## Methods

### Dataset and preprocessing

Our dataset includes PSG recordings from four different sites: SSC, BioSerenity, MESA[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[21](/articles/s41591-025-04133-4#ref-CR21 "Chen, X. et al. Racial/ethnic differences in sleep disturbances: the multi-ethnic study of atherosclerosis (MESA). Sleep 38, 877–888 (2015).") and MROS[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[22](/articles/s41591-025-04133-4#ref-CR22 "Blackwell, T. et al. Associations between sleep architecture and sleep-disordered breathing and cognition in older community-dwelling men: the osteoporotic fractures in men sleep study. J. Am. Geriatr. Soc. 59, 2217–2225 (2011)."), with SHHS[20](/articles/s41591-025-04133-4#ref-CR20 "Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. J. Am. Med. Inform. Assoc. 25, 1351–1358 (2018)."),[23](/articles/s41591-025-04133-4#ref-CR23 "Quan, S. F. et al. The sleep heart health study: design, rationale, and methods. Sleep 20, 1077–1085 (1997).") serving as an external validation dataset. Among these, MESA, MROS and SHHS are publicly available datasets, whereas SSC is our proprietary dataset. The BioSerenity dataset, provided by the BioSerenity company, contains 18,869 overnight recordings lasting 7–11 h each. This dataset is a subset of a larger collection from SleepMed and BioSerenity sleep laboratories, gathered between 2004 and 2019 across 240 US facilities[19](/articles/s41591-025-04133-4#ref-CR19 "Hanif, U. et al. Associations between self-reported parasomnias and psychiatric illness in 370,000 patients with sleep disorders. Psychiatr. Clin. Neurosci. 78, 667–677 (2024)."). At the time of this study, approximately 20,000 deidentified PSGs were available for analysis. The dataset distribution across different splits is shown in Fig. [1](/articles/s41591-025-04133-4#Fig1), with SSC constituting the largest cohort. To prevent data leakage, participants with several PSG recordings were assigned to a single split. For MESA, MROS and SHHS details, we refer readers to their original publications. Below, we describe our internal SSC dataset in more detail.

The SSC dataset comprises 35,052 recordings, each lasting approximately 8 h overnight. It includes diverse waveforms such as BAS, ECG, EMG and respiratory channels, making it a high-quality resource for sleep-related research. The dataset spans recordings from 1999 to 2024 and includes participants aged 2 to 96 years. The patient demographic statistics for SSC and BioSerenity are summarized in Extended Data Tables [1](/articles/s41591-025-04133-4#Tab3) and [2](/articles/s41591-025-04133-4#Tab4), respectively.

Our preprocessing strategy minimizes alterations to preserve raw signal characteristics crucial for identifying nuanced patterns. Each recording contains up to four modalities: BAS, ECG, EMG and respiratory, with variable numbers of channels. For BAS, we allowed up to ten channels, for ECG two channels, for EMG four channels and for respiratory seven channels. The number and type of channels vary across sites and even between patients within the same site, depending on the study type. The types of channel available across sites are described in Supplementary Tables [15–19](/articles/s41591-025-04133-4#MOESM1). BAS includes channels that measure brain activity from different regions (frontal, central, occipital) as well as EOG for eye movements. EMG records electrical activity in muscles, whereas ECG captures cardiac electrical function. Respiratory channels measure chest and abdominal movements, pulse readings and nasal/oral airflow. These channels were selected based on their relevance to sleep studies, guided by sleep experts[1](/articles/s41591-025-04133-4#ref-CR1 "Berry, R. B et al. The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications (American Academy of Sleep Medicine, 2012).").

Each PSG recording is resampled to 128 Hz to standardize sampling rates across participants and sites. Before downsampling, we utilized a fourth-order low-pass Butterworth filter to prevent aliasing, applied in a zero-phase setting to avoid phase distortion. Finally, we standardized the signal to have zero mean and unit variance. For any signals that needed to be upsampled, this was done using linear interpolation. Due to the channel-agnostic model design, we did not need any other data harmonization. Signals are segmented into 5-s patches, with each segment embedded into a vector representation for transformer model processing. To prevent data leakage, PSGs were split into pretrain, train, validation, test and temporal test sets early in the preprocessing pipeline. Although there is overlap between the pretraining and training sets, no overlap exists with the validation, test or temporal test sets. The SHHS serves as an independent dataset not used during pretraining, instead being used to evaluate the model’s ability to adapt to a new site through lightweight fine-tuning.

During pretraining, the only required labels are the modality types of the signals. A self-supervised CL objective is employed for pretraining. For downstream evaluations, we consider canonical tasks such as age/sex prediction, sleep stage classification, sleep apnea classification and various patient conditions extracted from EHR data. Sleep staging and apnea labels for SSC, MESA, MROS and SHHS were annotated by sleep experts. To ensure consistency across and within datasets, Rechtschaffen and Kales labels were converted to American Academy of Sleep Medicine standard by mapping Rechtschaffen and Kales stages 3 and 4 to American Academy of Sleep Medicine standard N3. SHHS also includes diagnostic information for conditions such as myocardial infarction, stroke, angina, congestive heart failure and death. For SSC, we paired PSG data with Stanford EHR data using deidentified patient IDs to extract demographic and diagnostic information. As BioSerenity lacks associated labels, it was used exclusively for pretraining.

### SleepFM model architecture

Our model architecture is illustrated in Fig. [1](/articles/s41591-025-04133-4#Fig1). The architecture includes several key components that differ slightly between the pretraining and fine-tuning stages. During pretraining, we employ CL as the objective function for representation learning. A single model processes all four modalities.

The first component of the architecture is the *Encoder*, a 1D convolutional neural network (CNN) that processes raw signal data for each modality separately. The encoder takes raw input vectors, where the length of each vector corresponds to a 5-s segment of the signal, referred to as a token. The input dimensions are (*B*, *T*, *C*), where *B* is the batch size, *T* is the raw temporal length of the input and *C* is the number of channels for each modality. These inputs are reshaped into (*B*, *C*, *S*, *L*), where *S* is the sequence length representing the number of tokens (*S* = *T*/*L*) and *L* corresponds to the raw vector length for a single token (for example, 640 samples). Each token is then processed individually through a stack of six convolutional layers, each followed by normalization and ELU activation layers. These layers progressively reduce the temporal resolution while increasing the number of feature channels, converting the input from 1 channel to 128 channels. After this, adaptive average pooling further reduces the temporal dimensions, and a fully connected layer compresses the representation into a 128-dimensional embedding for each token. The final output of the encoder has dimensions (*B*, *C*, *S*, *D*), where *D* = 128.

Following the encoder, a sequence of transformer-based operations is applied to extract and aggregate modality-specific and temporal features. The first step is channel pooling, which aggregates token embeddings from all channels within a given modality. This operation uses an attention pooling mechanism based on a transformer layer to compute attention scores for each channel and produces a single aggregated embedding per time segment by averaging over the channel dimension. The resulting embeddings, with dimensions (*B*, *S*, *D*), are then passed through a temporal transformer, which operates along the temporal dimension to capture dependencies between tokens. The temporal transformer applies sinusoidal positional encoding to the token embeddings, followed by two transformer blocks consisting of self-attention and feedforward layers, enabling the model to learn contextual relationships across the sequence. After temporal modeling, the embeddings are processed through temporal pooling, which aggregates token embeddings over the sequence length (*S*) for each modality. Similar to channel pooling, temporal pooling uses an attention mechanism to compute weighted averages, generating a compact representation of size (*B*, 128) per modality. These steps collectively ensure that the model captures both spatial and temporal dependencies while reducing dimensionality for computational efficiency.

The final output is a single 128-dimensional embedding for each modality, used for CL during pretraining. Whereas the 5-min recordings are used exclusively for pretraining, we retain the 5-s-level embeddings for each modality for downstream tasks such as sleep staging and disease classification.

### Baseline models

We evaluate SleepFM against two carefully chosen baseline approaches to demonstrate the value of our foundation model methodology.

The first baseline is a simple demographic model that processes only patient characteristics, including age, sex, BMI and race/ethnicity information. This demographic baseline is implemented as a one-layer MLP to establish a minimum performance threshold using only basic patient data available in most clinical settings.

The second baseline is the more sophisticated End-to-End PSG model that directly processes raw sleep recordings. This model uses the same architecture as SleepFM, including the 1D CNN encoder, channel pooling transformer block, temporal transformer block, temporal pooling transformer block and the LSTM layers, and is trained from scratch on the same dataset used for downstream evaluation. It also includes age and sex demographic features to ensure a fair comparison, but does not leverage any pretraining, serving to isolate the benefit of task-specific supervised learning on PSG signals without a foundation model.

All baseline models were trained using dataset splits shown in Table [1](/articles/s41591-025-04133-4#Tab1). The foundation model was first pretrained on the training dataset using a self-supervised objective, and subsequently fine-tuned on the same data. In contrast, the supervised baseline models were trained end-to-end without any pretraining. Although all models share identical architectures, training objectives and data splits, SleepFM consistently outperforms both baselines across a range of clinical prediction tasks. Although this may seem counterintuitive—given that the supervised PSG baseline is trained on the same data—these results align with well-established benefits of pretraining in representation learning. Self-supervised pretraining enables the model to learn more generalizable physiological representations, facilitates better convergence through improved initialization and makes more efficient use of sparse or noisy supervision during fine-tuning, as demonstrated in previous work[11](/articles/s41591-025-04133-4#ref-CR11 "Thapa, R. et al. SleepFM: multi-modal representation learning for sleep across brain activity, ECG and respiratory signals. Proc. Mach. Learning Res. 235, 48019–48037 (2024).").

### Model training

Model training can be categorized into two segments: pretraining and fine-tuning. The pretraining stage involves self-supervised representation learning with a CL objective and fine-tuning involves training the model with supervised learning objective for specific tasks such as sleep stage classification, sleep apnea classification and disease prediction. We describe these in more details below.

#### Pretraining

Model pretraining is performed using a self-supervised learning objective called CL. Specifically, we employ a CL objective for several modalities, referred to as LOO-CL. The key idea behind CL is to bring positive pairs of embeddings from different modalities closer in the latent space while pushing apart negative pairs. Positive pairs are derived from temporally aligned 5-min aggregated embeddings, obtained after temporal pooling, across four different modalities. All other nonmatching instances within a training batch are treated as negative pairs.

In LOO-CL, we define a predictive task where an embedding from one modality attempts to identify the corresponding embeddings from the remaining modalities. For each modality *i*, we construct an embedding \({\bar{x}}\_{k}^{-i}\) by averaging over embeddings from all other modalities, excluding modality *i*. We then apply a contrastive loss between the embedding of modality *i* and this LOO representation:

$${{\mathcal{L}}}\_{i,k}=-\log \frac{\exp \left({\rm{sim}}({x}\_{k}^{i},{\bar{x}}\_{k}^{-i})/\tau \right)}{\mathop{\sum }\nolimits\_{m = 1}^{N}\exp \left({\rm{sim}}({x}\_{k}^{i},{\bar{x}}\_{m}^{-i})/\tau \right)},$$

where \({{\mathcal{L}}}\_{i,k}\) is the loss for a sample *k* from modality *i* in a given batch, \({\rm{sim}}(\cdot )\) represents a similarity function (for example, cosine similarity) and *τ* is a temperature scaling parameter. The numerator computes the similarity between the embedding of modality *i* and the LOO representation of the corresponding sample, whereas the denominator sums the similarities across all samples within the batch. The motivation behind the LOO method is to encourage each embedding to align semantically with all other modalities.

#### Fine-tuning

After pretraining with the CL objective, we extract 5-s embeddings for all patient PSG data across modalities. We standardize the temporal context to 9 h for all patients—longer recordings are cropped and shorter ones are zero-padded to ensure consistent input dimensions. For example, for a patient’s standardized 9-h sleep data, the resulting patient matrix has dimensions (4 × 6,480 × 128), where 4 represents the number of modalities, 6,480 is the number of 5-s embeddings for 9 h of sleep and 128 is the embedding vector dimension.

During fine-tuning, we first apply a channel pooling operation across different modalities, reducing the dimensions to (6,480 × 128) for our example patient matrix. The pooled embeddings are then processed through a two-layer LSTM block, which is designed to handle temporal sequences. For sleep staging tasks, these 5-s embeddings are passed directly through a classification layer. For all other tasks, the embeddings are first pooled along the temporal dimension before being passed through an output layer.

For disease classification, we append age and sex features to the mean-pooled embedding vector after the LSTM block, before passing it to the final output layer. This addition empirically improves performance and surpasses the demographic baseline.

The fine-tuning objective for disease prediction uses the CoxPH loss function—a standard approach in survival analysis for modeling time-to-event data. The CoxPH loss maximizes the partial likelihood and is defined for a single label as:

$${{\mathcal{L}}}\_{{\rm{CoxPH}}}=-\frac{1}{{N}\_{e}}\mathop{\sum }\limits\_{i=1}^{n}{\delta }\_{i}\left({h}\_{i}-\log \sum \_{j\in R({t}\_{i})}\exp ({h}\_{j})\right),$$

where *h**i* is the predicted hazard for the *i*th patient, *δ**i* is the event indicator (1 for event occurrence, 0 otherwise), *t**i* is the event or censoring time, *R*(*t**i*) represents the risk set of all patients with event times greater than or equal to *t**i*, *n* is the total number of patients and \({N}\_{e}=\mathop{\sum }\nolimits\_{i = 1}^{n}{\delta }\_{i}\) is the number of events.

For our multilabel setup with 1,041 labels, we extend the CoxPH loss by computing it independently for each label and summing the results:

$${{\mathcal{L}}}\_{{\rm{total}}}=\mathop{\sum }\limits\_{k=1}^{L}{{\mathcal{L}}}\_{{\rm{CoxPH}}}^{(k)},$$

where *L* is the total number of labels.

Given the large dataset size, computing the loss for all patients in a single batch is computationally infeasible. Therefore, we calculate the loss in smaller batches of 32 samples, with patients sorted by event time in descending order to ensure correct computation of the partial likelihood. This batching strategy, combined with the summation of per-label losses, provides an efficient and scalable approach for multilabel time-to-event modeling.

#### Architectural details

We provide additional implementation-level details to clarify how SleepFM is constructed and trained. The design of SleepFM was developed through an empirical and iterative process, informed by domain knowledge and guided by practical training considerations. Although we did not perform an exhaustive hyperparameter search, we systematically evaluated architectural variants through trial-and-error by monitoring loss convergence, training stability and downstream performance.

Each 5-s segment of raw PSG signals (640 timepoints at 128 Hz) is passed through a tokenizer composed of six convolutional layers with increasing feature maps: 1 → 4 → 8 → 16 → 32 → 64 → 128. Each convolutional block includes BatchNorm, ELU activation and LayerNorm. After convolution, adaptive average pooling reduces the temporal axis to 1, and a linear layer projects the features to a fixed 128-dimensional token embedding. The resulting output shape is (*B*, *C*, *S*, 128), where *C* is the number of channels and *S* is the number of 5-s tokens.

To accommodate variability in the number and ordering of channels across different PSG datasets, we introduced an attention-based spatial pooling layer that operates across channels using a transformer encoder. This design makes the model robust to inconsistencies in recording configurations across sites. Specifically, embeddings from several channels within a modality are pooled using multihead self-attention, producing a modality-specific sequence of shape (*B*, *S*, 128).

To capture long-range temporal dependencies in sleep signals, the pooled token sequence is passed through three transformer encoder layers (each with eight heads, batch-first configuration and a dropout rate of 0.3), along with sinusoidal positional encoding and LayerNorm. This component enables modeling of contextual relationships across the sleep sequence. The output shape remains (*B*, *S*, 128).

An additional attention-based pooling layer aggregates the temporal sequence across timesteps, resulting in a single 128-dimensional embedding for each modality (for example, BAS, ECG, EMG or respiratory). These fixed-size modality-specific embeddings are used for pretraining with a self-supervised CL objective.

For downstream disease prediction, 5-s token embeddings spanning a standardized 9-h window are processed by a fine-tuning head. This head includes spatial pooling followed by a two-layer bidirectional LSTM (hidden size: 64). Temporal mean pooling is applied across valid timesteps, and normalized age and sex features are concatenated with the pooled output. The combined vector is then passed through a final linear layer to generate hazard scores for each disease. The total number of learnable parameters in this setup is approximately 0.91 million.

The supervised baseline model uses the same architecture as SleepFM but is trained from scratch without pretraining. The demographics-only baseline passes four input features—age, sex, BMI and race/ethnicity—through a shallow MLP with dimensions 4 → 128 → output.

#### Implementation details

All implementations were carried out using PyTorch, a library used widely for deep learning. The PSG data was gathered and processed within a HIPAA-compliant and secure compute cluster on Google Cloud Platform. Patient EHR data was likewise stored and analyzed exclusively within this secure environment.

For pretraining, the model was trained with a batch size of 32, a learning rate of 0.001, eight pooling heads, three transformer layers and a dropout rate of 0.3. As previously described, each patch size corresponds to a 5-s segment, and the total sequence length is 5 min for the transformer model. The total parameter count for the model was approximately 4.44 million. Pretraining was performed on 432,000 h of sleep data collected from 48,000 participants for one epoch, using an NVIDIA A100 GPU. The entire pretraining process took approximately 15 h.

For fine-tuning, the batch size was also set to 32, with a learning rate of 0.001, four pooling heads, two LSTM layers and a dropout rate of 0.3. The fine-tuned model had approximately 0.91 million learnable parameters. Training was conducted on patient data, with each token embedding represented as a 128-dimensional vector, over ten epochs. The fine-tuning process was performed on an NVIDIA A100 GPU, with the total training time per epoch ranging from 2 to 5 min, depending on the task.

All data analysis and preprocessing were performed using Python (v.3.10.14) and its data analysis libraries, including Pandas (v.2.1.1), NumPy (v.1.25.2), SciPy (v.1.11.3), scikit-survival (v.0.23.0), scikit-learn (v.1.5.2) and PyTorch (v.2.0.1).

### Reporting summary

Further information on research design is available in the [Nature Portfolio Reporting Summary](/articles/s41591-025-04133-4#MOESM2) linked to this article.




## Data availability

Of the five data sources used in this study, four datasets are available publicly and can be accessed at the following links: SHHS (<https://sleepdata.org/datasets/shhs>), MrOS (<https://sleepdata.org/datasets/mros>), MESA (<https://sleepdata.org/datasets/mesa>) and SSC (<https://sleepdata.org/datasets/ssc>). The BioSerenity dataset is proprietary and owned by BioSerenity, which has granted Stanford University access under a research and development agreement; please contact BioSerenity directly for data agreement. Stanford sleep data is available upon publication at <https://bdsp.io/content/hsp/2.0/>. Access to these data is provided solely for research purposes and is subject to data use restrictions that prohibit redistribution or sharing with third parties.




## Code availability

All of the SleepFM code is open source and available at <https://github.com/zou-group/sleepfm-clinical>.




## References

1. Berry, R. B et al. *The AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications* (American Academy of Sleep Medicine, 2012).

   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20AASM%20Manual%20for%20the%20Scoring%20of%20Sleep%20and%20Associated%20Events%3A%20Rules%2C%20Terminology%20and%20Technical%20Specifications&publication_year=2012&author=Berry%2CRB)
2. Kryger, M. H., Roth, T. & Dement, W. C. (eds). *Principles and Practice of Sleep Medicine* (Saunders, 2010).

   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Principles%20and%20Practice%20of%20Sleep%20Medicine&publication_year=2010)
3. Brink-Kjaer, A. et al. Age estimation from sleep studies using deep learning predicts life expectancy. *NPJ Digit. Med.* **5**, 103 (2022).

   [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35869169) 
   [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9307657) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Age%20estimation%20from%20sleep%20studies%20using%20deep%20learning%20predicts%20life%20expectancy&journal=NPJ%20Digit.%20Med.&volume=5&publication_year=2022&author=Brink-Kjaer%2CA)
4. Riemann, D. Insomnia and comorbid psychiatric disorders. *Sleep Med.* **8**, S15–S20 (2007).

   [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=18346672) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Insomnia%20and%20comorbid%20psychiatric%20disorders&journal=Sleep%20Med.&volume=8&pages=S15-S20&publication_year=2007&author=Riemann%2CD)
5. André, C. et al. Association of sleep-disordered breathing with Alzheimer disease biomarkers in community-dwelling older adults: a secondary analysis of a randomized clinical trial. *JAMA Neurol.* **77**, 716–724 (2020).

   [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32202593) 
   [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7091393) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20of%20sleep-disordered%20breathing%20with%20Alzheimer%20disease%20biomarkers%20in%20community-dwelling%20older%20adults%3A%20a%20secondary%20analysis%20of%20a%20randomized%20clinical%20trial&journal=JAMA%20Neurol.&volume=77&pages=716-724&publication_year=2020&author=Andr%C3%A9%2CC)
6. Nii Ossah Addo, P. et al. Associations between sleep duration, sleep disturbance and cardiovascular disease biomarkers among adults in the united states. *BMC Public Health* **24**, 947 (2024).

   [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10985959) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Associations%20between%20sleep%20duration%2C%20sleep%20disturbance%20and%20cardiovascular%20disease%20biomarkers%20among%20adults%20in%20the%20united%20states&journal=BMC%20Public%20Health&volume=24&publication_year=2024&author=Nii%20Ossah%20Addo%2CP)
7. Perslev, M. et al. U-sleep: resilient high-frequency sleep staging. *NPJ Digit. Med.* **4**, 72 (2021).

   [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33859353) 
   [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8050216) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=U-sleep%3A%20resilient%20high-frequency%20sleep%20staging&journal=NPJ%20Digit.%20Med.&volume=4&publication_year=2021&author=Perslev%2CM)
8. Nassi, T. E. et al. Automated scoring of respiratory events in sleep with a single effort belt and deep neural networks. *IEEE Trans. Biomed. Eng.* **69**, 2094–2104 (2021).

   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Automated%20scoring%20of%20respiratory%20events%20in%20sleep%20with%20a%20single%20effort%20belt%20and%20deep%20neural%20networks&journal=IEEE%20Trans.%20Biomed.%20Eng.&volume=69&pages=2094-2104&publication_year=2021&author=Nassi%2CTE)
9. Koscova, Z. et al. From sleep patterns to heart rhythm: predicting atrial fibrillation from overnight polysomnograms. *J. Electrocardiol.* **86**, 153759 (2024).

   [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39067281) 
   [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC11401747) 
   [Google Scholar](http://scholar.google.com/scholar_lookup?&title=From%20sleep%20patterns%20to%20heart%20rhythm%3A%20predicting%20atrial%20fibrillation%20from%20overnight%20polysomnograms&journal=J.%20Electrocardiol.&volume=86&publication_year=2024&author=Koscova%2CZ)
10. Stephansen, J. B. et al. Neural network analysis of sleep stages enables efficient diagnosis of narcolepsy. *Nat. Commun.* **9**, 5229 (2018).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30523329) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6283836) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1cXisVKisLfP) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Neural%20network%20analysis%20of%20sleep%20stages%20enables%20efficient%20diagnosis%20of%20narcolepsy&journal=Nat.%20Commun.&volume=9&publication_year=2018&author=Stephansen%2CJB)
11. Thapa, R. et al. SleepFM: multi-modal representation learning for sleep across brain activity, ECG and respiratory signals. *Proc. Mach. Learning Res.* **235**, 48019–48037 (2024).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=SleepFM%3A%20multi-modal%20representation%20learning%20for%20sleep%20across%20brain%20activity%2C%20ECG%20and%20respiratory%20signals.&journal=Proc.%20Mach.%20Learning%20Res.&volume=235&pages=48019-48037&publication_year=2024&author=Thapa%2CR)
12. Bommasani, R. et al. On the opportunities and risks of foundation models. Preprint at <https://arxiv.org/abs/2108.07258v3> (2021).
13. Saab, K. et al. Capabilities of Gemini models in medicine. Preprint at <https://arxiv.org/abs/2404.18416v2> (2024).
14. Zhao, T. et al. A foundation model for joint segmentation, detection and recognition of biomedical objects across nine modalities. *Nat. Methods* **22**, 166–176 (2025).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39558098) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXisFCru7rF) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20foundation%20model%20for%20joint%20segmentation%2C%20detection%20and%20recognition%20of%20biomedical%20objects%20across%20nine%20modalities&journal=Nat.%20Methods&volume=22&pages=166-176&publication_year=2025&author=Zhao%2CT)
15. Zhang, S. et al. ECGFM: a foundation model for ecg analysis trained on a multi-center million-ECG dataset. *Inform. Fusion* **124**, 103363 (2025).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=ECGFM%3A%20a%20foundation%20model%20for%20ecg%20analysis%20trained%20on%20a%20multi-center%20million-ECG%20dataset&journal=Inform.%20Fusion&volume=124&publication_year=2025&author=Zhang%2CS)
16. Cui, W. et al. Neuro-GPT: towards a foundation model for EEG. In *Proc 2024 IEEE International Symposium on Biomedical Imaging (ISBI)* 1–5 (IEEE, 2024).
17. Pendergrass, S. A. et al. The use of phenome-wide association studies (PheWAS) for exploration of novel genotype-phenotype relationships and pleiotropy discovery. *Genet. Epidemiol.* **35**, 410–422 (2011).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=21594894) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3116446) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20use%20of%20phenome-wide%20association%20studies%20%28PheWAS%29%20for%20exploration%20of%20novel%20genotype-phenotype%20relationships%20and%20pleiotropy%20discovery&journal=Genet.%20Epidemiol.&volume=35&pages=410-422&publication_year=2011&author=Pendergrass%2CSA)
18. Hanif, U. et al. Automatic detection of chronic insomnia from polysomnographic and clinical variables using machine learning. In *Proc 2023 45th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC)* 1–5 (IEEE, 2023).
19. Hanif, U. et al. Associations between self-reported parasomnias and psychiatric illness in 370,000 patients with sleep disorders. *Psychiatr. Clin. Neurosci.* **78**, 667–677 (2024).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Associations%20between%20self-reported%20parasomnias%20and%20psychiatric%20illness%20in%20370%2C000%20patients%20with%20sleep%20disorders&journal=Psychiatr.%20Clin.%20Neurosci.&volume=78&pages=667-677&publication_year=2024&author=Hanif%2CU)
20. Zhang, Guo-Qiang et al. The National Sleep Research resource: towards a sleep data commons. *J. Am. Med. Inform. Assoc.* **25**, 1351–1358 (2018).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=29860441) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6188513) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20National%20Sleep%20Research%20resource%3A%20towards%20a%20sleep%20data%20commons&journal=J.%20Am.%20Med.%20Inform.%20Assoc.&volume=25&pages=1351-1358&publication_year=2018&author=Zhang%2CGuo-Qiang)
21. Chen, X. et al. Racial/ethnic differences in sleep disturbances: the multi-ethnic study of atherosclerosis (MESA). *Sleep* **38**, 877–888 (2015).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=25409106) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4434554) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Racial%2Fethnic%20differences%20in%20sleep%20disturbances%3A%20the%20multi-ethnic%20study%20of%20atherosclerosis%20%28MESA%29&journal=Sleep&volume=38&pages=877-888&publication_year=2015&author=Chen%2CX)
22. Blackwell, T. et al. Associations between sleep architecture and sleep-disordered breathing and cognition in older community-dwelling men: the osteoporotic fractures in men sleep study. *J. Am. Geriatr. Soc.* **59**, 2217–2225 (2011).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=22188071) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3245643) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Associations%20between%20sleep%20architecture%20and%20sleep-disordered%20breathing%20and%20cognition%20in%20older%20community-dwelling%20men%3A%20the%20osteoporotic%20fractures%20in%20men%20sleep%20study&journal=J.%20Am.%20Geriatr.%20Soc.&volume=59&pages=2217-2225&publication_year=2011&author=Blackwell%2CT)
23. Quan, S. F. et al. The sleep heart health study: design, rationale, and methods. *Sleep* **20**, 1077–1085 (1997).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=9493915) 
    [CAS](/articles/cas-redirect/1:STN:280:DyaK1c7lt12gtg%3D%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20sleep%20heart%20health%20study%3A%20design%2C%20rationale%2C%20and%20methods&journal=Sleep&volume=20&pages=1077-1085&publication_year=1997&author=Quan%2CSF)
24. Vallat, R. & Walker, M. P. An open-source, high-performance tool for automated sleep staging. *eLife* **10**, e70092 (2021).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=34648426) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8516415) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB38XotVSqsLk%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20open-source%2C%20high-performance%20tool%20for%20automated%20sleep%20staging&journal=eLife&volume=10&publication_year=2021&author=Vallat%2CR&author=Walker%2CMP)
25. Hanna, J. & Flöel, A. An accessible and versatile deep learning-based sleep stage classifier. *Front. Neuroinform.* **17**, 1086634 (2023).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=36938361) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10017438) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20accessible%20and%20versatile%20deep%20learning-based%20sleep%20stage%20classifier&journal=Front.%20Neuroinform.&volume=17&publication_year=2023&author=Hanna%2CJ&author=Fl%C3%B6el%2CA)
26. Gagliardi, G., Alfeo, L., Cimino, M. G. C. A., Valenza, G. & De Vos, M. Physioex, a new Python library for explainable sleep staging through deep learning. *Physiol Meas.* **46**, 025006 (2025).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Physioex%2C%20a%20new%20Python%20library%20for%20explainable%20sleep%20staging%20through%20deep%20learning.&journal=Physiol%20Meas.&volume=46&publication_year=2025&author=Gagliardi%2CG&author=Alfeo%2CL&author=Cimino%2CMGCA&author=Valenza%2CG&author=De%20Vos%2CM)
27. Perslev, M. et al. DCSM Sleep staging dataset (University of Copenhagen). *Electronic Research Data Archive* <https://erda.ku.dk/public/archives/db553715ecbe1f3ac66c1dc569826eef/published-archive.html> (2021).
28. Alvarez-Estevez, D. & Rijsman, R. Haaglanden Medisch Centrum sleep staging database (v.1.1). PhysioNet <https://doi.org/10.13026/t79q-fr32> (2022).
29. Wu, P. et al. Mapping ICD-10 and ICD-10-CM codes to phecodes: workflow development and initial evaluation. *JMIR Med. Inform.* **7**, e14325 (2019).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31553307) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6911227) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Mapping%20ICD-10%20and%20ICD-10-CM%20codes%20to%20phecodes%3A%20workflow%20development%20and%20initial%20evaluation&journal=JMIR%20Med.%20Inform.&volume=7&publication_year=2019&author=Wu%2CP)
30. Wennberg, A. M. V., Wu, M. N., Rosenberg, P. B. & Spira, A. P. Sleep disturbance, cognitive decline, and dementia: a review. *Semin. Neurol.* **37**, 395–406 (2017).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28837986) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5910033) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20disturbance%2C%20cognitive%20decline%2C%20and%20dementia%3A%20a%20review.&journal=Semin.%20Neurol.&volume=37&pages=395-406&publication_year=2017&author=Wennberg%2CAMV&author=Wu%2CMN&author=Rosenberg%2CPB&author=Spira%2CAP)
31. Stefani, A. & Högl, B. Sleep in Parkinson’s disease. *Neuropsychopharmacology* **45**, 121–128 (2020).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31234200) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20in%20Parkinson%E2%80%99s%20disease&journal=Neuropsychopharmacology&volume=45&pages=121-128&publication_year=2020&author=Stefani%2CA&author=H%C3%B6gl%2CB)
32. Ravichandran, R. et al. The interplay between sleep disorders and cardiovascular diseases: a systematic review. *Cureus* **15**, e45898 (2023).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37885512) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10598613) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20interplay%20between%20sleep%20disorders%20and%20cardiovascular%20diseases%3A%20a%20systematic%20review.&journal=Cureus&volume=15&publication_year=2023&author=Ravichandran%2CR)
33. Shigesato, M. et al. Association between sleep duration and breast cancer incidence: the multiethnic cohort. *Int. J. Cancer* **146**, 664–670 (2020).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=30895617) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BC1MXntVGiu74%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20between%20sleep%20duration%20and%20breast%20cancer%20incidence%3A%20the%20multiethnic%20cohort&journal=Int.%20J.%20Cancer&volume=146&pages=664-670&publication_year=2020&author=Shigesato%2CM)
34. Freeman, J. R. et al. Actigraphy-derived measures of sleep and risk of prostate cancer in the UK Biobank. *J. Natl Cancer Inst.* **116**, 434–444 (2024).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38013591) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10919343) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2MXit1ersr%2FF) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Actigraphy-derived%20measures%20of%20sleep%20and%20risk%20of%20prostate%20cancer%20in%20the%20UK%20Biobank&journal=J.%20Natl%20Cancer%20Inst.&volume=116&pages=434-444&publication_year=2024&author=Freeman%2CJR)
35. Windred, D. P. et al. Sleep regularity is a stronger predictor of mortality risk than sleep duration: a prospective cohort study. *Sleep* **47**, zsad253 (2024).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37738616) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10782501) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20regularity%20is%20a%20stronger%20predictor%20of%20mortality%20risk%20than%20sleep%20duration%3A%20a%20prospective%20cohort%20study&journal=Sleep&volume=47&publication_year=2024&author=Windred%2CDP)
36. Westwood, A. J. et al. Prolonged sleep duration as a marker of early neurodegeneration predicting incident dementia. *Neurology* **88**, 1172–1179 (2017).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28228567) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5373785) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Prolonged%20sleep%20duration%20as%20a%20marker%20of%20early%20neurodegeneration%20predicting%20incident%20dementia&journal=Neurology&volume=88&pages=1172-1179&publication_year=2017&author=Westwood%2CAJ)
37. Shi, L. et al. Sleep disturbances increase the risk of dementia: a systematic review and meta-analysis. *Sleep Med. Rev.* **40**, 4–16 (2018).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28890168) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20disturbances%20increase%20the%20risk%20of%20dementia%3A%20a%20systematic%20review%20and%20meta-analysis&journal=Sleep%20Med.%20Rev.&volume=40&pages=4-16&publication_year=2018&author=Shi%2CL)
38. Mc Carthy, C. E. et al. Sleep patterns and the risk of acute stroke: results from the interstroke international case-control study. *Neurology* **100**, e2191–e2203 (2023).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20patterns%20and%20the%20risk%20of%20acute%20stroke%3A%20results%20from%20the%20interstroke%20international%20case-control%20study&journal=Neurology&volume=100&pages=e2191-e2203&publication_year=2023&author=Carthy%2CCE)
39. Shahrbabaki, S. S., Linz, D., Hartmann, S., Redline, S. & Baumert, M. Sleep arousal burden is associated with long-term all-cause and cardiovascular mortality in 8001 community-dwelling older men and women. *Eur. Heart J.* **42**, 2088–2099 (2021).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33876221) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8197565) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20arousal%20burden%20is%20associated%20with%20long-term%20all-cause%20and%20cardiovascular%20mortality%20in%208001%20community-dwelling%20older%20men%20and%20women&journal=Eur.%20Heart%20J.&volume=42&pages=2088-2099&publication_year=2021&author=Shahrbabaki%2CSS&author=Linz%2CD&author=Hartmann%2CS&author=Redline%2CS&author=Baumert%2CM)
40. Leary, E. B. et al. Association of rapid eye movement sleep with mortality in middle-aged and older adults. *JAMA Neurol.* **77**, 1241–1251 (2020).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32628261) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7550971) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20of%20rapid%20eye%20movement%20sleep%20with%20mortality%20in%20middle-aged%20and%20older%20adults&journal=JAMA%20Neurol.&volume=77&pages=1241-1251&publication_year=2020&author=Leary%2CEB)
41. Young, T. et al. Sleep disordered breathing and mortality: eighteen-year follow-up of the Wisconsin sleep cohort. *Sleep* **31**, 1071–1078 (2008).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=18714778) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2542952) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20disordered%20breathing%20and%20mortality%3A%20eighteen-year%20follow-up%20of%20the%20Wisconsin%20sleep%20cohort&journal=Sleep&volume=31&pages=1071-1078&publication_year=2008&author=Young%2CT)
42. Wallace, M. L. et al. Physiological sleep measures predict time to 15-year mortality in community adults: application of a novel machine learning framework. *J. Sleep Res.* **30**, e13386 (2021).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33991144) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8591145) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Physiological%20sleep%20measures%20predict%20time%20to%2015-year%20mortality%20in%20community%20adults%3A%20application%20of%20a%20novel%20machine%20learning%20framework&journal=J.%20Sleep%20Res.&volume=30&publication_year=2021&author=Wallace%2CML)
43. Bubu, O. M. et al. Sleep, cognitive impairment, and Alzheimer’s disease: a systematic review and meta-analysis. *Sleep* **40**, zsw032 (2017).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%2C%20cognitive%20impairment%2C%20and%20Alzheimer%E2%80%99s%20disease%3A%20a%20systematic%20review%20and%20meta-analysis&journal=Sleep&volume=40&publication_year=2017&author=Bubu%2COM)
44. Ju, Yo-El. S. et al. Slow wave sleep disruption increases cerebrospinal fluid amyloid-*β* levels. *Brain* **140**, 2104–2111 (2017).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28899014) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5790144) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Slow%20wave%20sleep%20disruption%20increases%20cerebrospinal%20fluid%20amyloid-%CE%B2%20levels&journal=Brain&volume=140&pages=2104-2111&publication_year=2017&author=Ju%2CYo-ElS)
45. Falgàs, N. & Walsh, C. M. The importance of rapid eye movement sleep and its implications for Alzheimer’s disease. *Sleep* **47**, zsae117 (2024).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38752396) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC11236946) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20importance%20of%20rapid%20eye%20movement%20sleep%20and%20its%20implications%20for%20Alzheimer%E2%80%99s%20disease.&journal=Sleep&volume=47&publication_year=2024&author=Falg%C3%A0s%2CN&author=Walsh%2CCM)
46. Weng, Yuan-Yuan, Lei, X. & Yu, J. Sleep spindle abnormalities related to Alzheimer’s disease: a systematic mini-review. *Sleep Med.* **75**, 37–44 (2020).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32853916) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Sleep%20spindle%20abnormalities%20related%20to%20Alzheimer%E2%80%99s%20disease%3A%20a%20systematic%20mini-review&journal=Sleep%20Med.&volume=75&pages=37-44&publication_year=2020&author=Weng%2CYuan-Yuan&author=Lei%2CX&author=Yu%2CJ)
47. André, C. et al. REM sleep is associated with the volume of the cholinergic basal forebrain in aMCI individuals. *Alzheimers Res Ther* **15**, 151 (2023).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37684650) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10485959) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=REM%20sleep%20is%20associated%20with%20the%20volume%20of%20the%20cholinergic%20basal%20forebrain%20in%20aMCI%20individuals&journal=Alzheimers%20Res%20Ther&volume=15&publication_year=2023&author=Andr%C3%A9%2CC)
48. Brink-Kjaer, A. et al. End-to-end deep learning of polysomnograms for classification of rem sleep behavior disorder. In *Proc 2022 44th Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC)* 2941–2944 (IEEE, 2022).
49. Yang, Y. et al. Artificial intelligence-enabled detection and assessment of Parkinson’s disease using nocturnal breathing signals. *Nature Med.* **28**, 2207–2215 (2022).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35995955) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9556299) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB38Xit1SksLfP) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Artificial%20intelligence-enabled%20detection%20and%20assessment%20of%20Parkinson%E2%80%99s%20disease%20using%20nocturnal%20breathing%20signals&journal=Nature%20Med.&volume=28&pages=2207-2215&publication_year=2022&author=Yang%2CY)
50. Li, H. et al. A deep learning model for early prediction of Alzheimer’s disease dementia based on hippocampal magnetic resonance imaging data. *Alzheimers Dementia* **15**, 1059–1070 (2019).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20deep%20learning%20model%20for%20early%20prediction%20of%20Alzheimer%E2%80%99s%20disease%20dementia%20based%20on%20hippocampal%20magnetic%20resonance%20imaging%20data&journal=Alzheimers%20Dementia&volume=15&pages=1059-1070&publication_year=2019&author=Li%2CH)
51. Ereira, S., Waters, S., Razi, A. & Marshall, C. R. Early detection of dementia with default-mode network effective connectivity. *Nat. Mental Health* **2**, 787–800 (2024).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Early%20detection%20of%20dementia%20with%20default-mode%20network%20effective%20connectivity.&journal=Nat.%20Mental%20Health&volume=2&pages=787-800&publication_year=2024&author=Ereira%2CS&author=Waters%2CS&author=Razi%2CA&author=Marshall%2CCR)
52. Hansson, O. et al. Association between CSF biomarkers and incipient Alzheimer’s disease in patients with mild cognitive impairment: a follow-up study. *Lancet Neurol.* **5**, 228–234 (2006).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=16488378) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD28XisF2qsbg%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20between%20CSF%20biomarkers%20and%20incipient%20Alzheimer%E2%80%99s%20disease%20in%20patients%20with%20mild%20cognitive%20impairment%3A%20a%20follow-up%20study&journal=Lancet%20Neurol.&volume=5&pages=228-234&publication_year=2006&author=Hansson%2CO)
53. Klunk, W. E. et al. Imaging brain amyloid in Alzheimer’s disease with Pittsburgh Compound-B. *Ann. Neurol.* **55**, 306–319 (2004).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=14991808) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BD2cXisFKntb8%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Imaging%20brain%20amyloid%20in%20Alzheimer%E2%80%99s%20disease%20with%20Pittsburgh%20Compound-B&journal=Ann.%20Neurol.&volume=55&pages=306-319&publication_year=2004&author=Klunk%2CWE)
54. Janelidze, S. et al. Plasma p-tau181 in Alzheimer’s disease: relationship to other biomarkers, differential diagnosis, neuropathology and longitudinal progression to Alzheimer’s dementia. *Nature Med.* **26**, 379–386 (2020).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32123385) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3cXktFemt70%3D) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Plasma%20p-tau181%20in%20Alzheimer%E2%80%99s%20disease%3A%20relationship%20to%20other%20biomarkers%2C%20differential%20diagnosis%2C%20neuropathology%20and%20longitudinal%20progression%20to%20Alzheimer%E2%80%99s%20dementia&journal=Nature%20Med.&volume=26&pages=379-386&publication_year=2020&author=Janelidze%2CS)
55. Moreno-Sánchez, P. A. et al. ECG-based data-driven solutions for diagnosis and prognosis of cardiovascular diseases: a systematic review. *Comput. Biol. Med.* **172**, 108235 (2024).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38460311) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=ECG-based%20data-driven%20solutions%20for%20diagnosis%20and%20prognosis%20of%20cardiovascular%20diseases%3A%20a%20systematic%20review.&journal=Comput.%20Biol.%20Med.&volume=172&publication_year=2024&author=Moreno-S%C3%A1nchez%2CPA)
56. Mitra, A. K., Bhuiyan, A. R. & Jones, E. A. Association and risk factors for obstructive sleep apnea and cardiovascular diseases: a systematic review. *Diseases* **9**, 88 (2021).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=34940026) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8700568) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Association%20and%20risk%20factors%20for%20obstructive%20sleep%20apnea%20and%20cardiovascular%20diseases%3A%20a%20systematic%20review&journal=Diseases&volume=9&publication_year=2021&author=Mitra%2CAK&author=Bhuiyan%2CAR&author=Jones%2CEA)
57. Barone, M. T. U. & Menna-Barreto, L. Diabetes and sleep: a complex cause-and-effect relationship. *Diabetes Res. Clin. Pract.* **91**, 129–137 (2011).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=20810183) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Diabetes%20and%20sleep%3A%20a%20complex%20cause-and-effect%20relationship&journal=Diabetes%20Res.%20Clin.%20Pract.&volume=91&pages=129-137&publication_year=2011&author=Barone%2CMTU&author=Menna-Barreto%2CL)
58. Yang, C. et al. Associations of sleep with cardiometabolic risk factors and cardiovascular diseases: an umbrella review of observational and Mendelian randomization studies. *Sleep Med. Rev.* **77**, 101965 (2024).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=39137553) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB2cXhslGisbnP) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Associations%20of%20sleep%20with%20cardiometabolic%20risk%20factors%20and%20cardiovascular%20diseases%3A%20an%20umbrella%20review%20of%20observational%20and%20Mendelian%20randomization%20studies.&journal=Sleep%20Med.%20Rev.&volume=77&publication_year=2024&author=Yang%2CC)
59. Figorilli, M., Puligheddu, M., Congiu, P. & Ferri, R. The clinical importance of periodic leg movements in sleep. *Curr. Treatment Options Neurol.* **19**, 10 (2017).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20clinical%20importance%20of%20periodic%20leg%20movements%20in%20sleep&journal=Curr.%20Treatment%20Options%20Neurol.&volume=19&publication_year=2017&author=Figorilli%2CM&author=Puligheddu%2CM&author=Congiu%2CP&author=Ferri%2CR)
60. Vallat, R., Shah, V. D. & Walker, M. P. Coordinated human sleeping brainwaves map peripheral body glucose homeostasis. *Cell Rep. Med.* **4**, 101100 (2023).

    [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37421946) 
    [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10394167) 
    [CAS](/articles/cas-redirect/1:CAS:528:DC%2BB3sXhsVGjurjO) 
    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Coordinated%20human%20sleeping%20brainwaves%20map%20peripheral%20body%20glucose%20homeostasis.&journal=Cell%20Rep.%20Med.&volume=4&publication_year=2023&author=Vallat%2CR&author=Shah%2CVD&author=Walker%2CMP)

[Download references](https://citation-needed.springer.com/v2/references/10.1038/s41591-025-04133-4?format=refman&flavour=references)




## Acknowledgements

We acknowledge E. Steinberg for his valuable insights into survival analysis. The Multi-Ethnic Study of Atherosclerosis (MESA) Sleep Ancillary study was funded by NIH-NHLBI Association of Sleep Disorders with Cardiovascular Health Across Ethnic Groups (RO1 HL098433). MESA is supported by NHLBI funded contracts HHSN268201500003I, N01-HC-95159, N01-HC-95160, N01-HC-95161, N01-HC-95162, N01-HC-95163, N01-HC-95164, N01-HC-95165, N01-HC-95166, N01-HC-95167, N01-HC-95168 and N01-HC-95169 from the National Heart, Lung and Blood Institute, and by cooperative agreements UL1-TR-000040, UL1-TR-001079 and UL1-TR-001420 funded by NCATS. The National Sleep Research Resource was supported by the National Heart, Lung and Blood Institute (R24 HL114473, 75N92019R002). The National Heart, Lung and Blood Institute provided funding for the ancillary MrOS Sleep Study, ‘Outcomes of Sleep Disorders in Older Men,’ under the following grant numbers: R01 HL071194, R01 HL070848, R01 HL070847, R01 HL070842, R01 HL070841, R01 HL070837, R01 HL070838 and R01 HL070839. The National Sleep Research Resource was supported by the National Heart, Lung and Blood Institute (R24 HL114473, 75N92019R002). The Sleep Heart Health Study (SHHS) was supported by National Heart, Lung and Blood Institute cooperative agreements U01HL53916 (University of California, Davis), U01HL53931 (New York University), U01HL53934 (University of Minnesota), U01HL53937 and U01HL64360 (Johns Hopkins University), U01HL53938 (University of Arizona), U01HL53940 (University of Washington), U01HL53941 (Boston University) and U01HL63463 (Case Western Reserve University). The National Sleep Research Resource was supported by the National Heart, Lung and Blood Institute (R24 HL114473, 75N92019R002). R.T. is supported by the Knight-Hennessy Scholars funding. E.M. and M.B.W. are supported by a grant from the National Heart, Lung and Blood Institute of the NIH (R01HL161253). J.Z. is supported by funding from the Chan-Zuckerberg Biohub.




## Author information

Author notes

1. These authors contributed equally: Rahul Thapa, Magnus Ruud Kjaer.
2. These authors jointly supervised this work: Emmanuel Mignot, James Zou.

### Authors and Affiliations

1. Department of Biomedical Data Science, Stanford University, Stanford, CA, USA

   Rahul Thapa & James Zou
2. Department of Computer Science, Stanford University, Stanford, CA, USA

   Rahul Thapa, Bryan He, Ian Covert & James Zou
3. Department of Psychiatry and Behavioral Sciences, Stanford University, Stanford, CA, USA

   Magnus Ruud Kjaer, Hyatt Moore IV, Gauri Ganjoo & Emmanuel Mignot
4. Department of Health Technology, Technical University of Denmark, Kongens Lyngby, Denmark

   Magnus Ruud Kjaer & Andreas Brink-Kjaer
5. Department of Clinical Neurophysiology, Danish Center for Sleep Medicine, Rigshospitalet, Glostrup, Denmark

   Magnus Ruud Kjaer, Umaer Hanif & Poul Jennum
6. Department of Systems Engineering, Naval Postgraduate School, Monterey, CA, USA

   Hyatt Moore IV
7. Data Science, BioSerenity, Paris, France

   Umaer Hanif
8. Department of Neurology, Beth Israel Deaconess Medical Center, Harvard Medical School, Boston, MA, USA

   M. Brandon Westover
9. Department of Clinical Medicine, University of Copenhagen, Copenhagen, Denmark

   Poul Jennum

Authors

1. Rahul Thapa

   [View author publications](/search?author=Rahul%20Thapa)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Rahul%20Thapa) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Rahul%20Thapa%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
2. Magnus Ruud Kjaer

   [View author publications](/search?author=Magnus%20Ruud%20Kjaer)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Magnus%20Ruud%20Kjaer) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Magnus%20Ruud%20Kjaer%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
3. Bryan He

   [View author publications](/search?author=Bryan%20He)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Bryan%20He) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Bryan%20He%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
4. Ian Covert

   [View author publications](/search?author=Ian%20Covert)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Ian%20Covert) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Ian%20Covert%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
5. Hyatt Moore IV

   [View author publications](/search?author=Hyatt%20Moore%20IV)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Hyatt%20Moore%20IV) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Hyatt%20Moore%20IV%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
6. Umaer Hanif

   [View author publications](/search?author=Umaer%20Hanif)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Umaer%20Hanif) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Umaer%20Hanif%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
7. Gauri Ganjoo

   [View author publications](/search?author=Gauri%20Ganjoo)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Gauri%20Ganjoo) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Gauri%20Ganjoo%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
8. M. Brandon Westover

   [View author publications](/search?author=M.%20Brandon%20Westover)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=M.%20Brandon%20Westover) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22M.%20Brandon%20Westover%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
9. Poul Jennum

   [View author publications](/search?author=Poul%20Jennum)

   Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Poul%20Jennum) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Poul%20Jennum%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
10. Andreas Brink-Kjaer

    [View author publications](/search?author=Andreas%20Brink-Kjaer)

    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Andreas%20Brink-Kjaer) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Andreas%20Brink-Kjaer%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
11. Emmanuel Mignot

    [View author publications](/search?author=Emmanuel%20Mignot)

    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Emmanuel%20Mignot) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Emmanuel%20Mignot%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)
12. James Zou

    [View author publications](/search?author=James%20Zou)

    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=James%20Zou) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22James%20Zou%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

### Contributions

R.T. and M.R.K. contributed equally to brainstorming the project, running experiments and writing the manuscript. B.H., I.C., P.J., A.B.-K., and M.B.W. provided high-level brainstorming and contributed to writing and editing the paper. U.H., G.G. and H.M. IV assisted with data access. E.M. and J.Z., as senior co-authors, conceived the project and provided overall guidance. All authors reviewed and approved the final manuscript.

### Corresponding authors

Correspondence to
[Emmanuel Mignot](mailto:mignot@stanford.edu) or [James Zou](mailto:jamesz@stanford.edu).




## Ethics declarations

### Competing interests

M.B.W. is a cofounder, scientific advisor, consultant to, and has personal equity interest in, Beacon Biosignals. The other authors declare no competing interests.




## Peer review

### Peer review information

*Nature Medicine* thanks Henri Korkalainen, Thomas Penzel and the other, anonymous, reviewer(s) for their contribution to the peer review of this work. Primary Handling Editor: Michael Basson, in collaboration with the *Nature Medicine* team.




## Additional information

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.




## Extended data

### [Extended Data Fig. 1 Age estimation performance on the Stanford cohort.](/articles/s41591-025-04133-4/figures/5)

Left: Scatterplot showing predicted versus chronological age across all patients (n=5,019), with the diagonal line representing perfect prediction. The coefficient of determination (R2), mean absolute error (MAE), and Pearson correlation coefficient (Corr) are shown in the top left corner. Right: Mean Absolute Error (MAE) across chronological age groups, with vertical error bars indicating the standard error of the mean (SEM) within each age bin. The horizontal dashed line represents the overall MAE. Our model achieves an MAE comparable to state-of-the-art models and demonstrates improved age estimation performance for younger age groups compared to older ones.

### [Extended Data Fig. 2 Performance across clinically relevant diseases evaluated on Stanford data (n=5019).](/articles/s41591-025-04133-4/figures/6)

Performance is evaluated using multiple metrics: C-Index and AUROC. The selected conditions include critical health outcomes such as death, heart failure, stroke, and dementia. Each panel uses violin/point plots derived from 1000 patient-level bootstrapping: the violin encodes the distribution of bootstrap estimates, faint points are individual bootstrap draws, the filled dot is the mean, and the vertical line with end caps marks the 95% bootstrap percentile CI. Numbers above violins report the mean. Metrics are C-index (top) and AUROC at 6 years (bottom).

### [Extended Data Fig. 3 Performance of SleepFM for key clinical outcomes on the temporal test set.](/articles/s41591-025-04133-4/figures/7)

Metrics include C-Index and AUROC for critical conditions such as death, heart failure, chronic kidney disease, dementia, and stroke. Each panel uses violin/point plots derived from 1000 patient-level bootstrapping: the violin encodes the distribution of bootstrap estimates, faint points are individual bootstrap draws, the filled dot is the mean, and the vertical line with end caps marks the 95% bootstrap percentile CI. Numbers above violins report the mean. Metrics are C-index (top) and AUROC (bottom). All conditions are statistically significant with a p-value < 0.01 after Bonferroni correction.

### [Extended Data Fig. 4 Scaling behavior of fine-tuning SleepFM on the SHHS dataset.](/articles/s41591-025-04133-4/figures/8)

Scaling behavior of fine-tuning SleepFM on the SHHS dataset (test size = 2,000 participants). We progressively increased the percentage of labeled SHHS data used during fine-tuning from 10% to 100%. The plots show C-Index performance across six cardiovascular outcomes, comparing SleepFM with Demographics and End-to-End PSG baselines. Error bars indicate 95% confidence intervals derived from 1,000 participant-level bootstrap resamples with replacement. Even with as little as 10% of training data (330 samples), SleepFM demonstrates strong predictive accuracy and consistent performance improvements as more labeled data becomes available. SleepFM outperforms both baseline models in most conditions, particularly when the dataset size is smaller, and its performance scaling is more stable across all outcomes.

### [Extended Data Fig. 5 Impact of pretraining dataset size on downstream performance. Stanford cohort is used for this analysis.](/articles/s41591-025-04133-4/figures/9)

Each subplot shows C-Index performance for a specific disease as a function of the percentage of pretraining data used (0%, 25%, 50%, 100%). The downstream fine-tuning and test datasets are held constant. Error bars represent 95% confidence intervals estimated via 1,000 participant-level bootstrap resamples with replacement. The 100% mark corresponds to a full epoch of pretraining on the entire dataset (n=24,137). Intermediate checkpoints at 25% and 50% represent models saved partway through that epoch, while the 0% point denotes a model with no pretraining, resulting in near-random performance. Performance improves consistently with more pretraining data, highlighting the value of large-scale self-supervised pretraining across diverse phenotypes, including cardiovascular, metabolic, neurological, and respiratory conditions.

**Extended Data Table 1 Demographic characteristics of the Stanford Sleep Clinic (SSC) cohort**

[Full size table](/articles/s41591-025-04133-4/tables/3)

**Extended Data Table 2 Demographic characteristics of the Bioserenity cohort**

[Full size table](/articles/s41591-025-04133-4/tables/4)

**Extended Data Table 3 Per-sleep-stage F1 performance of SleepFM across four cohorts**

[Full size table](/articles/s41591-025-04133-4/tables/5)

**Extended Data Table 4 Sleep staging performance on the SSC cohort**

[Full size table](/articles/s41591-025-04133-4/tables/6)

**Extended Data Table 5 Comparison of category-averaged C-Index across SleepFM baseline**

[Full size table](/articles/s41591-025-04133-4/tables/7)




## Supplementary information

### [Supplementary Information (download PDF )](https://static-content.springer.com/esm/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_MOESM1_ESM.pdf)

Supplementary Figs. 1–12 and Tables 1–19.

### [Reporting Summary (download PDF )](https://static-content.springer.com/esm/art%3A10.1038%2Fs41591-025-04133-4/MediaObjects/41591_2025_4133_MOESM2_ESM.pdf)




## Rights and permissions

**Open Access** This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit <http://creativecommons.org/licenses/by/4.0/>.

[Reprints and permissions](https://s100.copyright.com/AppDispatchServlet?title=A%20multimodal%20sleep%20foundation%20model%20for%20disease%20prediction&author=Rahul%20Thapa%20et%20al&contentID=10.1038%2Fs41591-025-04133-4&copyright=The%20Author%28s%29&publication=1078-8956&publicationDate=2026-01-06&publisherName=SpringerNature&orderBeanReset=true&oa=CC%20BY)




## About this article

[![Check for updates. Verify currency and authenticity via CrossMark](data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjgxIiB3aWR0aD0iNTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj48cGF0aCBkPSJtMTcuMzUgMzUuNDUgMjEuMy0xNC4ydi0xNy4wM2gtMjEuMyIgZmlsbD0iIzk4OTg5OCIvPjxwYXRoIGQ9Im0zOC42NSAzNS40NS0yMS4zLTE0LjJ2LTE3LjAzaDIxLjMiIGZpbGw9IiM3NDc0NzQiLz48cGF0aCBkPSJtMjggLjVjLTEyLjk4IDAtMjMuNSAxMC41Mi0yMy41IDIzLjVzMTAuNTIgMjMuNSAyMy41IDIzLjUgMjMuNS0xMC41MiAyMy41LTIzLjVjMC02LjIzLTIuNDgtMTIuMjEtNi44OC0xNi42Mi00LjQxLTQuNC0xMC4zOS02Ljg4LTE2LjYyLTYuODh6bTAgNDEuMjVjLTkuOCAwLTE3Ljc1LTcuOTUtMTcuNzUtMTcuNzVzNy45NS0xNy43NSAxNy43NS0xNy43NSAxNy43NSA3Ljk1IDE3Ljc1IDE3Ljc1YzAgNC43MS0xLjg3IDkuMjItNS4yIDEyLjU1cy03Ljg0IDUuMi0xMi41NSA1LjJ6IiBmaWxsPSIjNTM1MzUzIi8+PHBhdGggZD0ibTQxIDM2Yy01LjgxIDYuMjMtMTUuMjMgNy40NS0yMi40MyAyLjktNy4yMS00LjU1LTEwLjE2LTEzLjU3LTcuMDMtMjEuNWwtNC45Mi0zLjExYy00Ljk1IDEwLjctMS4xOSAyMy40MiA4Ljc4IDI5LjcxIDkuOTcgNi4zIDIzLjA3IDQuMjIgMzAuNi00Ljg2eiIgZmlsbD0iIzljOWM5YyIvPjxwYXRoIGQ9Im0uMiA1OC40NWMwLS43NS4xMS0xLjQyLjMzLTIuMDFzLjUyLTEuMDkuOTEtMS41Yy4zOC0uNDEuODMtLjczIDEuMzQtLjk0LjUxLS4yMiAxLjA2LS4zMiAxLjY1LS4zMi41NiAwIDEuMDYuMTEgMS41MS4zNS40NC4yMy44MS41IDEuMS44MWwtLjkxIDEuMDFjLS4yNC0uMjQtLjQ5LS40Mi0uNzUtLjU2LS4yNy0uMTMtLjU4LS4yLS45My0uMi0uMzkgMC0uNzMuMDgtMS4wNS4yMy0uMzEuMTYtLjU4LjM3LS44MS42Ni0uMjMuMjgtLjQxLjYzLS41MyAxLjA0LS4xMy40MS0uMTkuODgtLjE5IDEuMzkgMCAxLjA0LjIzIDEuODYuNjggMi40Ni40NS41OSAxLjA2Ljg4IDEuODQuODguNDEgMCAuNzctLjA3IDEuMDctLjIzcy41OS0uMzkuODUtLjY4bC45MSAxYy0uMzguNDMtLjguNzYtMS4yOC45OS0uNDcuMjItMSAuMzQtMS41OC4zNC0uNTkgMC0xLjEzLS4xLTEuNjQtLjMxLS41LS4yLS45NC0uNTEtMS4zMS0uOTEtLjM4LS40LS42Ny0uOS0uODgtMS40OC0uMjItLjU5LS4zMy0xLjI2LS4zMy0yLjAyem04LjQtNS4zM2gxLjYxdjIuNTRsLS4wNSAxLjMzYy4yOS0uMjcuNjEtLjUxLjk2LS43MnMuNzYtLjMxIDEuMjQtLjMxYy43MyAwIDEuMjcuMjMgMS42MS43MS4zMy40Ny41IDEuMTQuNSAyLjAydjQuMzFoLTEuNjF2LTQuMWMwLS41Ny0uMDgtLjk3LS4yNS0xLjIxLS4xNy0uMjMtLjQ1LS4zNS0uODMtLjM1LS4zIDAtLjU2LjA4LS43OS4yMi0uMjMuMTUtLjQ5LjM2LS43OC42NHY0LjhoLTEuNjF6bTcuMzcgNi40NWMwLS41Ni4wOS0xLjA2LjI2LTEuNTEuMTgtLjQ1LjQyLS44My43MS0xLjE0LjI5LS4zLjYzLS41NCAxLjAxLS43MS4zOS0uMTcuNzgtLjI1IDEuMTgtLjI1LjQ3IDAgLjg4LjA4IDEuMjMuMjQuMzYuMTYuNjUuMzguODkuNjdzLjQyLjYzLjU0IDEuMDNjLjEyLjQxLjE4Ljg0LjE4IDEuMzIgMCAuMzItLjAyLjU3LS4wNy43NmgtNC4zNmMuMDcuNjIuMjkgMS4xLjY1IDEuNDQuMzYuMzMuODIuNSAxLjM4LjUuMjkgMCAuNTctLjA0LjgzLS4xM3MuNTEtLjIxLjc2LS4zN2wuNTUgMS4wMWMtLjMzLjIxLS42OS4zOS0xLjA5LjUzLS40MS4xNC0uODMuMjEtMS4yNi4yMS0uNDggMC0uOTItLjA4LTEuMzQtLjI1LS40MS0uMTYtLjc2LS40LTEuMDctLjctLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDQtLjI2LS45NS0uMjYtMS41MnptNC42LS42MmMwLS41NS0uMTEtLjk4LS4zNC0xLjI4LS4yMy0uMzEtLjU4LS40Ny0xLjA2LS40Ny0uNDEgMC0uNzcuMTUtMS4wNy40NS0uMzEuMjktLjUuNzMtLjU4IDEuM3ptMi41LjYyYzAtLjU3LjA5LTEuMDguMjgtMS41My4xOC0uNDQuNDMtLjgyLjc1LTEuMTNzLjY5LS41NCAxLjEtLjcxYy40Mi0uMTYuODUtLjI0IDEuMzEtLjI0LjQ1IDAgLjg0LjA4IDEuMTcuMjNzLjYxLjM0Ljg1LjU3bC0uNzcgMS4wMmMtLjE5LS4xNi0uMzgtLjI4LS41Ni0uMzctLjE5LS4wOS0uMzktLjE0LS42MS0uMTQtLjU2IDAtMS4wMS4yMS0xLjM1LjYzLS4zNS40MS0uNTIuOTctLjUyIDEuNjcgMCAuNjkuMTcgMS4yNC41MSAxLjY2LjM0LjQxLjc4LjYyIDEuMzIuNjIuMjggMCAuNTQtLjA2Ljc4LS4xNy4yNC0uMTIuNDUtLjI2LjY0LS40MmwuNjcgMS4wM2MtLjMzLjI5LS42OS41MS0xLjA4LjY1LS4zOS4xNS0uNzguMjMtMS4xOC4yMy0uNDYgMC0uOS0uMDgtMS4zMS0uMjQtLjQtLjE2LS43NS0uMzktMS4wNS0uN3MtLjUzLS42OS0uNy0xLjEzYy0uMTctLjQ1LS4yNS0uOTYtLjI1LTEuNTN6bTYuOTEtNi40NWgxLjU4djYuMTdoLjA1bDIuNTQtMy4xNmgxLjc3bC0yLjM1IDIuOCAyLjU5IDQuMDdoLTEuNzVsLTEuNzctMi45OC0xLjA4IDEuMjN2MS43NWgtMS41OHptMTMuNjkgMS4yN2MtLjI1LS4xMS0uNS0uMTctLjc1LS4xNy0uNTggMC0uODcuMzktLjg3IDEuMTZ2Ljc1aDEuMzR2MS4yN2gtMS4zNHY1LjZoLTEuNjF2LTUuNmgtLjkydi0xLjJsLjkyLS4wN3YtLjcyYzAtLjM1LjA0LS42OC4xMy0uOTguMDgtLjMxLjIxLS41Ny40LS43OXMuNDItLjM5LjcxLS41MWMuMjgtLjEyLjYzLS4xOCAxLjA0LS4xOC4yNCAwIC40OC4wMi42OS4wNy4yMi4wNS40MS4xLjU3LjE3em0uNDggNS4xOGMwLS41Ny4wOS0xLjA4LjI3LTEuNTMuMTctLjQ0LjQxLS44Mi43Mi0xLjEzLjMtLjMxLjY1LS41NCAxLjA0LS43MS4zOS0uMTYuOC0uMjQgMS4yMy0uMjRzLjg0LjA4IDEuMjQuMjRjLjQuMTcuNzQuNCAxLjA0Ljcxcy41NC42OS43MiAxLjEzYy4xOS40NS4yOC45Ni4yOCAxLjUzcy0uMDkgMS4wOC0uMjggMS41M2MtLjE4LjQ0LS40Mi44Mi0uNzIgMS4xM3MtLjY0LjU0LTEuMDQuNy0uODEuMjQtMS4yNC4yNC0uODQtLjA4LTEuMjMtLjI0LS43NC0uMzktMS4wNC0uN2MtLjMxLS4zMS0uNTUtLjY5LS43Mi0xLjEzLS4xOC0uNDUtLjI3LS45Ni0uMjctMS41M3ptMS42NSAwYzAgLjY5LjE0IDEuMjQuNDMgMS42Ni4yOC40MS42OC42MiAxLjE4LjYyLjUxIDAgLjktLjIxIDEuMTktLjYyLjI5LS40Mi40NC0uOTcuNDQtMS42NiAwLS43LS4xNS0xLjI2LS40NC0xLjY3LS4yOS0uNDItLjY4LS42My0xLjE5LS42My0uNSAwLS45LjIxLTEuMTguNjMtLjI5LjQxLS40My45Ny0uNDMgMS42N3ptNi40OC0zLjQ0aDEuMzNsLjEyIDEuMjFoLjA1Yy4yNC0uNDQuNTQtLjc5Ljg4LTEuMDIuMzUtLjI0LjctLjM2IDEuMDctLjM2LjMyIDAgLjU5LjA1Ljc4LjE0bC0uMjggMS40LS4zMy0uMDljLS4xMS0uMDEtLjIzLS4wMi0uMzgtLjAyLS4yNyAwLS41Ni4xLS44Ni4zMXMtLjU1LjU4LS43NyAxLjF2NC4yaC0xLjYxem0tNDcuODcgMTVoMS42MXY0LjFjMCAuNTcuMDguOTcuMjUgMS4yLjE3LjI0LjQ0LjM1LjgxLjM1LjMgMCAuNTctLjA3LjgtLjIyLjIyLS4xNS40Ny0uMzkuNzMtLjczdi00LjdoMS42MXY2Ljg3aC0xLjMybC0uMTItMS4wMWgtLjA0Yy0uMy4zNi0uNjMuNjQtLjk4Ljg2LS4zNS4yMS0uNzYuMzItMS4yNC4zMi0uNzMgMC0xLjI3LS4yNC0xLjYxLS43MS0uMzMtLjQ3LS41LTEuMTQtLjUtMi4wMnptOS40NiA3LjQzdjIuMTZoLTEuNjF2LTkuNTloMS4zM2wuMTIuNzJoLjA1Yy4yOS0uMjQuNjEtLjQ1Ljk3LS42My4zNS0uMTcuNzItLjI2IDEuMS0uMjYuNDMgMCAuODEuMDggMS4xNS4yNC4zMy4xNy42MS40Ljg0LjcxLjI0LjMxLjQxLjY4LjUzIDEuMTEuMTMuNDIuMTkuOTEuMTkgMS40NCAwIC41OS0uMDkgMS4xMS0uMjUgMS41Ny0uMTYuNDctLjM4Ljg1LS42NSAxLjE2LS4yNy4zMi0uNTguNTYtLjk0LjczLS4zNS4xNi0uNzIuMjUtMS4xLjI1LS4zIDAtLjYtLjA3LS45LS4ycy0uNTktLjMxLS44Ny0uNTZ6bTAtMi4zYy4yNi4yMi41LjM3LjczLjQ1LjI0LjA5LjQ2LjEzLjY2LjEzLjQ2IDAgLjg0LS4yIDEuMTUtLjYuMzEtLjM5LjQ2LS45OC40Ni0xLjc3IDAtLjY5LS4xMi0xLjIyLS4zNS0xLjYxLS4yMy0uMzgtLjYxLS41Ny0xLjEzLS41Ny0uNDkgMC0uOTkuMjYtMS41Mi43N3ptNS44Ny0xLjY5YzAtLjU2LjA4LTEuMDYuMjUtMS41MS4xNi0uNDUuMzctLjgzLjY1LTEuMTQuMjctLjMuNTgtLjU0LjkzLS43MXMuNzEtLjI1IDEuMDgtLjI1Yy4zOSAwIC43My4wNyAxIC4yLjI3LjE0LjU0LjMyLjgxLjU1bC0uMDYtMS4xdi0yLjQ5aDEuNjF2OS44OGgtMS4zM2wtLjExLS43NGgtLjA2Yy0uMjUuMjUtLjU0LjQ2LS44OC42NC0uMzMuMTgtLjY5LjI3LTEuMDYuMjctLjg3IDAtMS41Ni0uMzItMi4wNy0uOTVzLS43Ni0xLjUxLS43Ni0yLjY1em0xLjY3LS4wMWMwIC43NC4xMyAxLjMxLjQgMS43LjI2LjM4LjY1LjU4IDEuMTUuNTguNTEgMCAuOTktLjI2IDEuNDQtLjc3di0zLjIxYy0uMjQtLjIxLS40OC0uMzYtLjctLjQ1LS4yMy0uMDgtLjQ2LS4xMi0uNy0uMTItLjQ1IDAtLjgyLjE5LTEuMTMuNTktLjMxLjM5LS40Ni45NS0uNDYgMS42OHptNi4zNSAxLjU5YzAtLjczLjMyLTEuMy45Ny0xLjcxLjY0LS40IDEuNjctLjY4IDMuMDgtLjg0IDAtLjE3LS4wMi0uMzQtLjA3LS41MS0uMDUtLjE2LS4xMi0uMy0uMjItLjQzcy0uMjItLjIyLS4zOC0uM2MtLjE1LS4wNi0uMzQtLjEtLjU4LS4xLS4zNCAwLS42OC4wNy0xIC4ycy0uNjMuMjktLjkzLjQ3bC0uNTktMS4wOGMuMzktLjI0LjgxLS40NSAxLjI4LS42My40Ny0uMTcuOTktLjI2IDEuNTQtLjI2Ljg2IDAgMS41MS4yNSAxLjkzLjc2cy42MyAxLjI1LjYzIDIuMjF2NC4wN2gtMS4zMmwtLjEyLS43NmgtLjA1Yy0uMy4yNy0uNjMuNDgtLjk4LjY2cy0uNzMuMjctMS4xNC4yN2MtLjYxIDAtMS4xLS4xOS0xLjQ4LS41Ni0uMzgtLjM2LS41Ny0uODUtLjU3LTEuNDZ6bTEuNTctLjEyYzAgLjMuMDkuNTMuMjcuNjcuMTkuMTQuNDIuMjEuNzEuMjEuMjggMCAuNTQtLjA3Ljc3LS4ycy40OC0uMzEuNzMtLjU2di0xLjU0Yy0uNDcuMDYtLjg2LjEzLTEuMTguMjMtLjMxLjA5LS41Ny4xOS0uNzYuMzFzLS4zMy4yNS0uNDEuNGMtLjA5LjE1LS4xMy4zMS0uMTMuNDh6bTYuMjktMy42M2gtLjk4di0xLjJsMS4wNi0uMDcuMi0xLjg4aDEuMzR2MS44OGgxLjc1djEuMjdoLTEuNzV2My4yOGMwIC44LjMyIDEuMi45NyAxLjIuMTIgMCAuMjQtLjAxLjM3LS4wNC4xMi0uMDMuMjQtLjA3LjM0LS4xMWwuMjggMS4xOWMtLjE5LjA2LS40LjEyLS42NC4xNy0uMjMuMDUtLjQ5LjA4LS43Ni4wOC0uNCAwLS43NC0uMDYtMS4wMi0uMTgtLjI3LS4xMy0uNDktLjMtLjY3LS41Mi0uMTctLjIxLS4zLS40OC0uMzctLjc4LS4wOC0uMy0uMTItLjY0LS4xMi0xLjAxem00LjM2IDIuMTdjMC0uNTYuMDktMS4wNi4yNy0xLjUxcy40MS0uODMuNzEtMS4xNGMuMjktLjMuNjMtLjU0IDEuMDEtLjcxLjM5LS4xNy43OC0uMjUgMS4xOC0uMjUuNDcgMCAuODguMDggMS4yMy4yNC4zNi4xNi42NS4zOC44OS42N3MuNDIuNjMuNTQgMS4wM2MuMTIuNDEuMTguODQuMTggMS4zMiAwIC4zMi0uMDIuNTctLjA3Ljc2aC00LjM3Yy4wOC42Mi4yOSAxLjEuNjUgMS40NC4zNi4zMy44Mi41IDEuMzguNS4zIDAgLjU4LS4wNC44NC0uMTMuMjUtLjA5LjUxLS4yMS43Ni0uMzdsLjU0IDEuMDFjLS4zMi4yMS0uNjkuMzktMS4wOS41M3MtLjgyLjIxLTEuMjYuMjFjLS40NyAwLS45Mi0uMDgtMS4zMy0uMjUtLjQxLS4xNi0uNzctLjQtMS4wOC0uNy0uMy0uMzEtLjU0LS42OS0uNzItMS4xMy0uMTctLjQ0LS4yNi0uOTUtLjI2LTEuNTJ6bTQuNjEtLjYyYzAtLjU1LS4xMS0uOTgtLjM0LTEuMjgtLjIzLS4zMS0uNTgtLjQ3LTEuMDYtLjQ3LS40MSAwLS43Ny4xNS0xLjA4LjQ1LS4zMS4yOS0uNS43My0uNTcgMS4zem0zLjAxIDIuMjNjLjMxLjI0LjYxLjQzLjkyLjU3LjMuMTMuNjMuMi45OC4yLjM4IDAgLjY1LS4wOC44My0uMjNzLjI3LS4zNS4yNy0uNmMwLS4xNC0uMDUtLjI2LS4xMy0uMzctLjA4LS4xLS4yLS4yLS4zNC0uMjgtLjE0LS4wOS0uMjktLjE2LS40Ny0uMjNsLS41My0uMjJjLS4yMy0uMDktLjQ2LS4xOC0uNjktLjMtLjIzLS4xMS0uNDQtLjI0LS42Mi0uNHMtLjMzLS4zNS0uNDUtLjU1Yy0uMTItLjIxLS4xOC0uNDYtLjE4LS43NSAwLS42MS4yMy0xLjEuNjgtMS40OS40NC0uMzggMS4wNi0uNTcgMS44My0uNTcuNDggMCAuOTEuMDggMS4yOS4yNXMuNzEuMzYuOTkuNTdsLS43NC45OGMtLjI0LS4xNy0uNDktLjMyLS43My0uNDItLjI1LS4xMS0uNTEtLjE2LS43OC0uMTYtLjM1IDAtLjYuMDctLjc2LjIxLS4xNy4xNS0uMjUuMzMtLjI1LjU0IDAgLjE0LjA0LjI2LjEyLjM2cy4xOC4xOC4zMS4yNmMuMTQuMDcuMjkuMTQuNDYuMjFsLjU0LjE5Yy4yMy4wOS40Ny4xOC43LjI5cy40NC4yNC42NC40Yy4xOS4xNi4zNC4zNS40Ni41OC4xMS4yMy4xNy41LjE3LjgyIDAgLjMtLjA2LjU4LS4xNy44My0uMTIuMjYtLjI5LjQ4LS41MS42OC0uMjMuMTktLjUxLjM0LS44NC40NS0uMzQuMTEtLjcyLjE3LTEuMTUuMTctLjQ4IDAtLjk1LS4wOS0xLjQxLS4yNy0uNDYtLjE5LS44Ni0uNDEtMS4yLS42OHoiIGZpbGw9IiM1MzUzNTMiLz48L2c+PC9zdmc+)](https://crossmark.crossref.org/dialog/?doi=10.1038/s41591-025-04133-4)

### Cite this article

Thapa, R., Kjaer, M.R., He, B. *et al.* A multimodal sleep foundation model for disease prediction.
*Nat Med* **32**, 752–762 (2026). https://doi.org/10.1038/s41591-025-04133-4

[Download citation](https://citation-needed.springer.com/v2/references/10.1038/s41591-025-04133-4?format=refman&flavour=citation)

* Received: 03 February 2025
* Accepted: 18 November 2025
* Published: 06 January 2026
* Version of record: 06 January 2026
* Issue date: February 2026
* DOI: https://doi.org/10.1038/s41591-025-04133-4

### Share this article

Anyone you share the following link with will be able to read this content:

Get shareable link

Sorry, a shareable link is not currently available for this article.

Copy shareable link to clipboard

Provided by the Springer Nature SharedIt content-sharing initiative

[Download PDF](/articles/s41591-025-04133-4.pdf)
