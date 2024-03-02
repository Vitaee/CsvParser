import pandas as pd, concurrent.futures
from collections import deque
from core.models import User
from celery import shared_task


def process_csv_batch(batch):
    users = []

    for index, row in batch.iterrows():
        first_name = row['First Name']
        last_name = row['Last Name']
        address = row['Address']
        dob = pd.to_datetime(row['DoB'], format='%d-%m-%Y')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=first_name+last_name,
            address=address,
            date_of_birth=dob
        )

        users.append(user)

    created_users = User.objects.bulk_create(users)

    return len(created_users)


#@shared_task
def create_users_from_csv_parallel(csv_file):
    results = deque()

    chunk_size = 1000
    max_workers = 10

    with pd.read_csv(csv_file, chunksize=chunk_size) as reader:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            tasks = [executor.submit(process_csv_batch, chunk) for chunk in reader]

            concurrent.futures.wait(tasks)

    return results