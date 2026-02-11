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
2. Define a reference mission (e.g., 150 passengers, 3000 km range).
3. Select:
   - Energy source: **Kerosene**
   - Propulsion: **Turbofan**
4. Record the resulting:
   - Payload–range diagram
   - Operating cost
   - Fuel consumption

Then:

5. Modify the configuration by selecting:
   - Energy source: **Liquid Hydrogen**
   - Propulsion: **Turbofan**

6. Compare:
   - Payload–range capability
   - Aircraft mass breakdown
   - Flight cash operating cost

This comparison enables users to directly observe the impact of alternative energy carriers on aircraft performance and economics under identical mission assumptions.

### Scenario II: Sensitivity Study
Users can also modify:
- Structural technology factors
- Engine efficiency
- Specific energy of storage media

and immediately observe changes in:
- Maximum takeoff weight
- Required thrust
- Operating cost trends

This makes GAM suitable for:
- Classroom demonstrations
- Student design projects
- Preliminary technology trade studies

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


