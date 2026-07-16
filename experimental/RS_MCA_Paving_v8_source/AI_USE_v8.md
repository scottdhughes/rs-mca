# AI-use disclosure for `RS_MCA_Paving_v8`

Date: 16 July 2026

## System and scope

OpenAI ChatGPT in Work Mode, using a GPT-5-based Codex system, provided
substantive assistance in preparing this manuscript. The interface did not
expose a more specific stable model-build identifier. Assistance included
drafting and restructuring mathematical prose, proposing proof formulations,
checking algebra and finite arithmetic, comparing successive manuscripts,
editing LaTeX, compiling and visually inspecting the PDF, and surveying cited
primary sources.

All sections received some prose or LaTeX assistance. Substantive machine
assistance affected the formulation or presentation of results in the
introduction, the MDS paving argument, syndrome and mean-overlap sections,
locator-prefix and pole-line constructions, smooth/circle transfers,
partial-occupancy discussion, the primitive Sidon/BSG/Boolean-cube reduction,
the asymptotic synthesis, and the appendices. The verification scripts were
also prepared and revised with machine assistance.

The human author supplied the research objective, source manuscripts,
repository materials, proposed proof architecture, counterexamples,
normalization corrections, requested theorem scope, and repeated mathematical
and editorial feedback. The human author selected the claims retained in v8
and is solely responsible for correctness, originality, attribution, and the
decision to disseminate the work. AI software is not an author.

## Material prompt excerpts

The following excerpts identify the principal instructions that shaped the
manuscript. They are representative of the substantive prompts; routine
requests to compile, rename, compare, or correct formatting are omitted.

> “build the best version out of these three papers and make sure we prove
> asymptotic RS MSA for smooth/circle domains unconditionally.”

> “we're proving new results, not trying to recall what's in literature.”

> “Write the completed proof as a publishable math research paper using
> amsart using a4paper, margin=1in. … Be rigorous and self-contained.”

> “The theorem statements should be tightened … Unconditional finite-row
> theorem package … Countertheorem … Conditional profile-envelope compiler.”

> “merge the image-normalization patch carefully … one must not silently
> replace image-normalized moments by ambient moments.”

> “integrate everything into a one clean paper for Proximity Prize committee.”

> “make sure also to settle positive density smooth/circle RS MCA following
> the notes … Sidon-heavy must be killed before BSG is invoked.”

> “now let's cut fluff, unnecessary results and also results that are not
> original to the literature.”

> “in the end there's no proof through Gowers theorem and cube? where and
> when that went away?”

> “write this version v7-3.”

> “do all that … give me v8 — but do not overblow it in size.”

## Post-generation review and limitations

Successive outputs were revised in response to user-supplied counterexamples,
normalization warnings, literature comparisons, theorem-scope corrections,
and requests to separate unconditional, imported, conditional, and open
claims. For v8, additional audits checked the central paving proof, the
ambient/image identity, the fixed-\(\sigma\) Sidon argument, the BSG/cube
specialization, BCHKS parameter normalization, citation provenance, and PDF
layout.

The two Python scripts accompanying v8 certify only their stated integer and
symbolic calculations. They do not formally verify the mathematical proofs,
the imported BCHKS theorem, novelty, or the missing smooth/circle Sidon and ray
inputs. No claim of human verification should be inferred from successful
compilation or script output. Before public submission, the named author must
independently read, understand, check, and affirm every statement, proof,
calculation, citation, and novelty claim.
