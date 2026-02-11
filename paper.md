---
title: "An Interactive Web-Based Tool for Conceptual Aircraft Design and Analysis"
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
date: 2026-02-11
bibliography: references.bib
---


## Summary

GAM (Generic Airplane Model) is an open-source, web-based software platform for conceptual aircraft design and analysis, developed to support education and early-stage design exploration. It provides an interactive environment in which users can investigate how key design decisions—such as energy sources, propulsion system configurations, and mission requirements—affect aircraft performance and operating cost.

The platform is organized into six integrated modules covering conceptual aircraft design, tuning and modification of existing or user-defined configurations, database trend visualization and comparison, payload–range comparison, and flight cash operating cost analysis. These modules enable users to design new aircraft concepts, benchmark them against approximately 300 reference aircraft, and perform systematic performance and cost comparisons under varying technological assumptions.

Through immediate visual and numerical feedback, GAM supports parametric study and technology impact assessment within a browser-based environment that requires no local installation. This accessibility makes the tool suitable for aerospace engineering education, demonstration activities, and preliminary research studies.


## Statement of Need

Aircraft conceptual design education faces inherent challenges due to limited access to large-scale experimental facilities and real-world aerospace systems[@raymer2024;@torenbeek2013advanced]. Although industrial design tools provide advanced capabilities, they are typically proprietary, computationally intensive, and not well suited for teaching fundamental design trade-offs at an early stage[@David2021;@lukaczyk2015suave;@wells2017flight;@drela2010tasopt]. Consequently, students and early-career researchers often struggle to develop intuition about how design decisions influence aircraft performance, operational characteristics, and cost drivers.

GAM addresses this need by offering an open-source, web-based platform for rapid conceptual aircraft design exploration. Built upon empirical methods commonly used in preliminary design [@kambiri2025energy;@kambiri2024energy], the tool reduces the number of primary decision variables that users must explicitly define while transparently exposing the dependent parameters influenced by those choices. Dynamic adjustment of parameter ranges and default values guides users toward physically consistent configurations, lowering cognitive complexity and reducing the risk of unrealistic designs.

The relevance of such a platform is amplified in the context of aviation decarbonization [@lee2023climate]. As the industry evaluates alternative propulsion systems and energy carriers, accessible tools for comparing technology pathways are increasingly important. Unlike conventional design tools that primarily focus on kerosene-based aircraft, GAM supports conceptual analysis across multiple energy sources—including liquid hydrogen, liquid methane, and liquid ammonia—and propulsion architectures such as turbofan, turboprop, piston engines, and electric motors. The inclusion of performance data from approximately 300 existing aircraft enables direct benchmarking between emerging concepts and operational fleets.

By lowering technical and licensing barriers, GAM facilitates reproducible design studies and transparent comparison of alternative aircraft configurations across educational and research environments.


## Availability

- **Repository**: https://github.com/CADO-ENAC/Generic-Airplane-Model-GUI
- **Live demonstration**: https://generic-airplane-model.streamlit.app/
- **License**: GNU Lesser General Public License (LGPL-3.0)
- **Programming language**: Python
- **Operating system**: Platform independent
- **User interface**: Web-based (Streamlit)
- **Archive**: https://doi.org/10.5281/zenodo.18613416


## References

