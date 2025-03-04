# Technical Support SLA Analysis & Data Pipeline

## **Project Overview**

This project focuses on analyzing SLA (Service Level Agreement) compliance in technical support tickets. The analysis involves extracting data from PostgreSQL, processing it, and loading it into Elasticsearch for visualization in Kibana.

## **Key Features**

- **Data Extraction**: Fetching technical support ticket data from PostgreSQL.
- **Data Cleaning & Transformation**: Processing raw data to ensure quality.
- **Data Storage & Visualization**: Storing processed data in Elasticsearch and analyzing it using Kibana.
- **Technology Stack**:
  - Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)
  - PostgreSQL
  - Elasticsearch & Kibana
  - Apache Airflow
  - Great Expectations (GX)

## **Dataset**

- `technical_support_dataset.csv`
- `technical_support_dataset_clean.csv`

## **How to Run the Project**

1. Clone this repository:
   ```bash
   git clone https://github.com/username/your-repo-name.git
   cd your-repo-name
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Airflow DAG:
   ```bash
   airflow dags trigger technical_support_sla
   ```
4. Validate Data with GX:
   ```bash
   jupyter notebook P2M3_yasminenaraindassetiadi_GX.ipynb
   ```
5. Visualize Data in Kibana:
   - **Kibana**: Query and explore data.

## **Directory Structure**

```
Technical_Support_SLA_Analysis/
├── dags/
│   ├── gx/
│   │   ├── expectations/
│   │   ├── plugins/custom_data_docs/styles/
│   │   ├── uncommitted/
│   │   ├── great_expectations.yml
│   ├── P2M3_yasminenaraindassetiadi_DAG.py
│   ├── P2M3_yasminenaraindassetiadi_DAG_graph.jpg
│   ├── P2M3_yasminenaraindassetiadi_GX.ipynb
├── images/
│   ├── introduction & objective.png
│   ├── kesimpulan.png
│   ├── plot & insight 01.png
│   ├── plot & insight 02.png
│   ├── plot & insight 03.png
│   ├── plot & insight 04.png
│   ├── plot & insight 05.png
│   ├── plot & insight 06.png
├── P2M3_yasminenaraindassetiadi_conceptual.txt
├── P2M3_yasminenaraindassetiadi_ddl.txt
├── README.md
├── airflow_ES.yaml
```

## **Results and Insights**

- **SLA Compliance Trends:** Analyzed the percentage of tickets meeting SLA requirements.
- **Key Influencing Factors:** Response time, ticket priority, and support agent workload.
- **Optimization Strategies:** Automating ticket triage and prioritization to improve SLA compliance.

## **Contact**

For any inquiries, reach out via [LinkedIn](https://www.linkedin.com/in/yasminenaraindas-setiadi/) or email at [ysmnaraindas.work@gmail.com](mailto\:ysmnaraindas.work@gmail.com).

---

⭐ Don't forget to star this repository if you found it useful!

