---
title: "Technology tradespace exploration in Aircraft Conceptual Design and Analysis"

tags:
  - aerospace engineering
  - aircraft design
  - conceptual design
  - education
  - open-source software
authors:
  - name: Dajung Kim
    orcid: 0000-0002-2550-3099 
    affiliation: 1
  - name: Thierry Druot
    affiliation: 1
  - name: Nicolas Monrolin
    affiliation: 1
  - name: Nicolas Peteilh
    affiliation: 1
affiliations:
  - name: F\'ed\'eration ENAC ISAE-SUPAERO ONERA, Universit\'e de Toulouse, 31000, Toulouse, France.
    index: 1
date: 2026-02-12
bibliography: references.bib
---


## Summary
GAM (Generic Airplane Model) is an open-source computational framework for conceptual aircraft design and technology trade-space exploration. The software integrates empirical preliminary design methods with propulsion–energy system modeling and operating cost evaluation to support systematic comparison of alternative aircraft configurations.

The framework enables users to define aircraft propulsion architectures, energy carriers, and mission requirements, and then evaluate resulting performance metrics, mass breakdown, payload–range capability, and flight cash operating cost. In addition to conventional kerosene-powered turbofan configurations, GAM supports alternative energy carriers including liquid hydrogen, liquid methane, ammonia, batteries, and hybrid-electric architectures.

A central contribution of this implementation is the integration of propulsion–energy system selection and technology sensitivity analysis within a unified computational workflow. Users can vary technological assumptions—such as specific energy, tank gravimetric index, component power density, and cost parameters—and systematically evaluate their influence on aircraft sizing and operating economics. The framework includes benchmarking capabilities against a curated database of approximately 300 existing aircraft.

Although GAM can be accessed through a web-based interface, this repository contains the complete computational implementation, including propulsion–energy integration, cost modeling, and trade-off analysis modules.




## Statement of Need
Aircraft conceptual design relies heavily on empirical methods and iterative trade studies to evaluate the impact of design choices on performance and cost [@raymer2024; @torenbeek2013advanced]. However, existing industrial tools are often proprietary, computationally intensive, and not well suited for rapid exploration of alternative propulsion systems and emerging energy carriers [@David2021; @lukaczyk2015suave; @drela2010tasopt].

In parallel, aviation decarbonization efforts require systematic evaluation of hydrogen, electric, and hybrid-electric propulsion concepts under consistent mission assumptions [@lee2023climate]. While numerous studies examine specific propulsion technologies, fewer open-source computational frameworks integrate aircraft sizing, propulsion–energy coupling, and operating cost evaluation within a unified and reproducible environment.

GAM addresses this gap by providing:

- Aircraft sizing based on empirical preliminary design relations
- Coupled propulsion–energy system modeling across multiple architectures
- Sensitivity analysis for energy efficiency related parameters that varies with the technological advancement
- Operating cost estimation enabling identification of propulsion–energy combinations that minimize cost under specified mission constraints
- Benchmarking against existing operational aircraft

Unlike visualization-only web tools or simple front-end wrappers, this repository implements the full computational workflow required for propulsion–energy trade-space exploration in conceptual aircraft design. The software is intended for aerospace engineering education, early-stage research studies, and preliminary evaluation of emerging propulsion technologies.

By lowering barriers to reproducible trade studies and enabling transparent comparison of alternative configurations, GAM supports systematic exploration of decarbonization pathways in civil aviation.




## Availability

- **Repository**: https://github.com/CADO-ENAC/Generic-Airplane-Model-GUI
- **Live demonstration**: https://generic-airplane-model.streamlit.app/
- **Archive**: https://doi.org/10.5281/zenodo.18613416
- **License**: GNU Lesser General Public License (LGPL-3.0)
- **Programming language**: Python
- **Operating system**: Platform independent


## AI Usage Disclosure

Large language models were used solely for language editing and stylistic refinement of portions of the manuscript. All technical content, software design, methodology, and scientific conclusions were developed by the authors. The authors take full responsibility for the accuracy and integrity of the work.


## References

