'''
=================================================
Milestone 3

Nama  : Yasmina Narainda Setiadi
Batch : FTDS HCK-024

Program ini dibuat untuk melakukan automatisasi transform dan load data dari PostgreSQL ke ElasticSearch.
Dataset : [https://www.kaggle.com/datasets/bhavikjikadara/retail-transactional-dataset]
=================================================
'''

# Import modul yang diperlukan
from airflow import DAG  # Untuk mendefinisikan dan menjadwalkan workflow DAG di Airflow
from airflow.providers.postgres.hooks.postgres import PostgresHook  # Untuk menghubungkan ke database PostgreSQL
from airflow.operators.python import PythonOperator  # Untuk menjalankan fungsi Python dalam DAG
from datetime import datetime  # Untuk mendefinisikan waktu dan jadwal
import pandas as pd  # Untuk manipulasi data (seperti membaca, mengolah data)
from elasticsearch import Elasticsearch  # Untuk berinteraksi dengan Elasticsearch

# Mendefinisikan default_args untuk DAG
default_args = {
    'owner': 'ysmnaraindassetiadi',  # Pemilik DAG
    'start_date': datetime(2024, 11, 1),  # Tanggal mulai eksekusi DAG
    'retries': 1,  # Jumlah upaya ulang (retries) jika task dalam DAG gagal
}

def fetch_data_from_postgres(**context):
    """
    Fetch data from PostgreSQL database and save it to a CSV file.
    """
    # Membuat koneksi ke PostgreSQL menggunakan PostgresHook dengan ID koneksi "postgres_default"
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

    # Mendapatkan engine SQL untuk melakukan query ke database PostgreSQL
    conn = postgres_hook.get_sqlalchemy_engine()

    # Mendefinisikan query SQL untuk mengambil semua data dari tabel "table_m3"
    query = "SELECT * FROM table_m3"

    # Menjalankan query SQL dan menyimpan hasilnya dalam DataFrame Pandas
    data = pd.read_sql(query, conn)

    # Menentukan path di mana file CSV akan disimpan
    path = '/opt/airflow/dags/P2M3_yasminenaraindassetiadi_data_raw.csv'

    # Menyimpan DataFrame ke dalam file CSV tanpa menyertakan indeks
    data.to_csv(path, index=False)

    # Menggunakan XCom untuk mengirim path file CSV ke task lain dalam DAG Airflow
    context['ti'].xcom_push(key='raw_data_path', value=path)


def clean_data(**context):
    """
    Clean data retrieved from Elasticsearch
    """
    # Mengambil nilai dari XCom untuk mendapatkan path file data mentah
    ti = context['ti']
    data_path = ti.xcom_pull(task_ids='fetch_data_from_postgres', key='raw_data_path')

    # Membaca data dari file CSV ke dalam DataFrame menggunakan pandas
    data = pd.read_csv(data_path)

    # Normalisasi nama kolom agar menjadi huruf kecil, menghapus spasi di awal/akhir, dan mengganti spasi dengan garis bawah
    data.columns = [col.lower().strip().replace(" ", "_") for col in data.columns]

    # Memfilter data untuk kolom 'age', hanya menyimpan baris dengan nilai 'age' antara 18 hingga 65
    data = data[(data["age"] >= 18) & (data["age"] <= 65)]

    # Mengonversi nilai kolom 'age' ke tipe data integer
    data["age"] = data["age"].astype(int)

    # Menghapus baris yang mengandung nilai kosong (missing values) pada kolom mana pun
    data.dropna(inplace=True)
    
    # Menghapus baris duplikat berdasarkan kolom 'transaction_id'
    data.drop_duplicates(subset=["transaction_id"], inplace=True)

    # Menyimpan DataFrame yang sudah dibersihkan ke file CSV dengan nama tertentu
    clean_path = '/opt/airflow/dags/P2M3_yasminenaraindassetiadi_data_clean.csv'
    data.to_csv(clean_path, index=False)

    # Menyimpan path file data yang telah dibersihkan ke XCom untuk digunakan di task berikutnya
    context['ti'].xcom_push(key='clean_data_path', value=clean_path)

    # Mencetak pesan untuk menunjukkan bahwa proses pembersihan data selesai
    print("Data cleaned and saved with range filtering and type correction.")


def load_data_to_elasticsearch(**context):
    """
    Load cleaned data to Elasticsearch
    """
    # Mengambil objek TaskInstance untuk mengambil data dari XCom
    ti = context['ti']

    # Mengambil path data yang telah dibersihkan dari task 'clean_data' melalui XCom
    data_path = ti.xcom_pull(task_ids='clean_data', key='clean_data_path')

    # Membuat koneksi ke Elasticsearch menggunakan URL instance Elasticsearch
    es = Elasticsearch(['http://elasticsearch:9200'])

    # Membaca data yang telah dibersihkan dari file CSV
    data_clean = pd.read_csv(data_path)

    # Menentukan nama indeks untuk Elasticsearch
    index_name = "milestone3_clean_data"

    # Melakukan indexing data ke Elasticsearch
    for _, row in data_clean.iterrows():  # Iterasi melalui setiap baris data
        doc = row.to_dict()  # Mengubah baris data menjadi dictionary
        es.index(index=index_name, body=doc)  # Memasukkan data ke dalam indeks Elasticsearch

    # Menampilkan pesan keberhasilan
    print(f"Data successfully loaded to Elasticsearch index '{index_name}'.")

# Membuat DAG dengan nama 'P2M3_yasminenaraindassetiadi_DAG'
with DAG(
    'P2M3_yasminenaraindassetiadi_DAG',  # Nama DAG
    default_args=default_args,  # Menggunakan default_args yang sudah diinisialisasi
    description='DAG for data extraction, cleaning, and loading into Elasticsearch',  # Deskripsi DAG
    schedule_interval='10,20,30 9 * * 6',  # Menjadwalkan DAG untuk berjalan pada pukul 09:10, 09:20, dan 09:30 setiap Sabtu
) as dag:

    # Task pertama: Mengambil data dari PostgreSQL
    fetch_data = PythonOperator(
        task_id='fetch_data_from_postgres',  # ID unik untuk task ini
        python_callable=fetch_data_from_postgres,  # Fungsi Python yang akan dijalankan
    )

    # Task kedua: Membersihkan data yang telah diambil
    clean_data_task = PythonOperator(
        task_id='clean_data',  # ID unik untuk task ini
        python_callable=clean_data,  # Fungsi Python yang akan dijalankan untuk membersihkan data
    )

    # Task ketiga: Memuat data bersih ke Elasticsearch
    load_to_es = PythonOperator(
        task_id='load_data_to_elasticsearch',  # ID unik untuk task ini
        python_callable=load_data_to_elasticsearch,  # Fungsi Python yang akan dijalankan untuk memuat data ke Elasticsearch
    )

    # Mendefinisikan urutan eksekusi task
    fetch_data >> clean_data_task >> load_to_es
