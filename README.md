### Predictive Maintenance for NASA Aircraft Engines

This project focuses on predictive maintenance for aircraft turbo engines, utilizing machine learning models like XGBoost and Random Forest. The objective is to predict the Remaining Useful Life (RUL) of engines based on historical sensor data, achieving an accuracy of approximately 80%.  All the codes are written and executed within Jupyter notebooks.

Once the models were trained and evaluated, the deployment was handled using FastAPI for serving the model, Docker for containerization, and Streamlit for interactive visualization. The project is deployed using Render, enabling efficient scaling and access. The focus of this MLOps approach is on seamless model deployment and interaction.

#### Project Organization

```
├── LICENSE  
├── Makefile              <- Makefile with commands like `make data` or `make train`  
├── README.md             <- The top-level README for developers using this project.  
├── data  
│   ├── external          <- Data from third-party sources.  
│   ├── interim           <- Intermediate data that has been transformed.  
│   ├── processed         <- The final, canonical datasets for modeling.  
│   └── raw               <- The original, immutable data dump.  
├── models                <- Trained and serialized models, model predictions, or model summaries.  
├── notebooks             <- Jupyter notebooks for analysis and model development.  
├── references            <- Data dictionaries, manuals, and other explanatory materials.    
├── requirements.txt      <- Requirements for reproducing the analysis environment. 
```

---

### Data Sets and Experimental Scenario

- **Data Set: FD001**  
  - Train trajectories: 100  
  - Test trajectories: 100  
  - Conditions: One (Sea Level)  
  - Fault Modes: One (HPC Degradation)  

- **Data Set: FD002**  
  - Train trajectories: 260  
  - Test trajectories: 259  
  - Conditions: Six  
  - Fault Modes: One (HPC Degradation)  

- **Data Set: FD003**  
  - Train trajectories: 100  
  - Test trajectories: 100  
  - Conditions: One (Sea Level)  
  - Fault Modes: Two (HPC Degradation, Fan Degradation)  

- **Data Set: FD004**  
  - Train trajectories: 248  
  - Test trajectories: 249  
  - Conditions: Six  
  - Fault Modes: Two (HPC Degradation, Fan Degradation)  

The datasets consist of multiple multivariate time series, with each time series corresponding to a different engine from a fleet of similar engines. The data is contaminated with sensor noise and includes three operational settings that significantly affect engine performance. The goal is to predict the remaining operational cycles before failure, based on the data provided. Faults develop during the series, growing in magnitude until system failure.

Each dataset contains 26 columns, with data for unit number, time (in cycles), operational settings, and sensor measurements, as follows:
1) Unit number  
2) Time (in cycles)  
3) Operational setting 1  
4) Operational setting 2  
5) Operational setting 3  
6) Sensor measurement 1  
...  
26) Sensor measurement 26  

**Reference**: A. Saxena, K. Goebel, D. Simon, and N. Eklund, "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation," in *Proceedings of the 1st International Conference on Prognostics and Health Management (PHM08)*, Denver CO, Oct 2008.

---

### Deployment

- **Docker Image**: `aswaths/predictive_maintenance:v1`
- **Streamlit App**: [Predictive Maintenance Streamlit App](https://predictivemaintenancet.streamlit.app)

