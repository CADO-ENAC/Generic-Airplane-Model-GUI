[![DOI](https://zenodo.org/badge/927149892.svg)](https://doi.org/10.5281/zenodo.18613415)
# Web Application of Generic Airplane Model (GAM) V2.0

This repository contains a web application for the Generic Airplane Model (GAM) available at <https://generic-airplane-model.streamlit.app/>. GAM is a Python toolbox for **preliminary airplane design based on statistical regressions** published at <https://gitlab.com/m6029/genericairplanemodel.git>. GAM and its web application cover various airplane propulsion systems, including conventional thermal engines, electric engines, and fuel cells, as well as various energy sources such as kerosene, hydrogen, batteries, methane, and ammonia.

The tool was developed by ENAC and ISAE-SUPAERO in Toulouse, France.


## Dependencies
This project relies on the following Python packages:
- Numpy
- Scipy
- Copy
- Pandas
- Openpyxl
- Matplotlib
- Plotly
- Streamlit
- Tabulate


***
## Quickstart
You can use GAM either through the online web application or by running it locally.

### 🌐 Option 1 – Use the live web application
The simplest way to use GAM is through the web interface:
👉 https://generic-airplane-model.streamlit.app/

No installation is required.


### 💻 Option 2 – Run locally

1. Clone the repository:

```bash
git clone https://github.com/CADO-ENAC/Generic-Airplane-Model-GUI.git
cd Generic-Airplane-Model-GUI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the application:
```bash
streamlit run Conceptual_Airplane_Design.py
```


## Example Scenario
The following example illustrates a typical use case in conceptual aircraft design:

### Scenario I: Comparing Conventional and Hydrogen Aircraft
1. Open the **Conceptual Aircraft Design** module.
2. Define the power system:
   - Energy Type: **Liquid H2**
   - Number of Engines: **2**
   - Propulsion: **Turbofan**
   - Engine Bypass Ratio: **5.9**
3. Define the design mission:
   - Airplane Category: **Short/Medium Range**
   - Airplane Design Range (km): **6000**
   - Number of Passengers: **156**
   - Cruise Mach Number: **0.78**
   - Cruise Altitude (ft): **35000**
4. Review the results:
   - Propulsion system characteristics
   - Design definition summary
   - Mass breakdown
   - Design mission performance results
   - Performance factors & efficiencies
   - Payload–range diagram
5. Save the aircraft configuration by specifying airplane name and clicking the `Save Airplane` button.
 
Next, benchmark against a conventional aircraft:
1. Open the **Tune Existing Airplane** module.
2. Select `By Airplane Manufacturer and ICAO Code`
3. Choose:
   - Airplane Manufacturer: **Airbus**
   - ICAO code:A319
   - Airplane Name:A319-100
4. Save the aircraft configuration by specifying airplane name and clicking the `Save Airplane` button.
2. Open the **Payload-Range Comparison** module to visualize differences.

This workflow allows users to directly compare a hydrogen-powered aircraft concept with a conventional kerosene aircraft under comparable mission assumptions, highlighting differences in mass distribution, payload–range capability, and overall performance characteristics.

### Scenario II: Sensitivity Study
1. Open the **Flight COC Analysis** module.
2. Select the **Long Range** category.

Users can vary technology and cost assumptions such as:
- Battery Energy Desity
- Fuel Cell Power Density
- LH2 Tank Gravimetric Index
- eMotor Price
- Fuel Cell Price
- LH2 Tank Price
- Battery Capacity Price
- LH2 Energy Price
- LCH4 Energy Price
- eFuel Energy Price

The platform immediately updates performance and cost metrics, allowing users to identify the propulsion system and energy carrier combination that minimizes operating cost for a given seat capacity and mission range.
 
These scenarios demonstrate how GAM supports:

- Classroom demonstrations of aircraft design trade-offs  
- Student-led conceptual design projects  
- Preliminary evaluation of emerging propulsion technologies  
- Comparative assessment of decarbonization pathways  

***
## Funding

This research was funded by the Fédération ENAC ISAE-SUPAERO ONERA, Université de Toulouse, France.


## License

> This **second version** of GAM is available under the [GNU Lesser General Public License](LICENSE.txt).
> If you publish your work, please cite the following contribution in your work:
[Kambiri et al., *Energy consumption of Aircraft with new propulsion systems
and storage media*, Scitech Forum, Orlando, January 2024](https://doi.org/10.2514/6.2024-1707)
> 
> The *CADO airplane database* is available at [entrepot.recherche.data.gouv.fr](https://doi.org/10.57745/LLRJO0) under the [Open Database License](database/DATABASE_LICENSE.txt). Any rights in individual contents of the database are licensed under the [Database Contents License](http://opendatacommons.org/licenses/dbcl/1.0/).
> 
> In summary, you have the following freedoms:
> * **Freedom to Share**: You can copy, distribute, and use the database.
> * **Freedom to Create**: You can produce works based on the database.
> * **Freedom to Adapt**: You can modify, transform, and build upon the database.
> 
> However, you must adhere to these conditions:
> 
> * **Attribute**: You must attribute any public use of the database, or works produced from the database, in the manner specified in the Open Database License (ODbL). For any use or redistribution of the database, or works produced from it, you must make clear to others the license of the database and keep intact any notices on the original database. 
> * **Share-Alike**: If you publicly use any adapted version of this database, or works produced from an adapted database, you must also offer that adapted database under the ODbL. 
> * **Keep open**: If you redistribute the database, or an adapted version of it, then you may use technological measures that restrict the work (such as DRM) as long as you also redistribute a version without such measures.
> 
> This database was developed by the Conceptual Air transport Design and Operations (CADO) team at the French National School of Civil Aviation (ENAC) in Toulouse, France.


## Contact

For any request, please contact <cado@lists.enac.fr>.


