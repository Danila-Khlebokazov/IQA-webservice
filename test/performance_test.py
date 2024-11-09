from iqadataset import load_dataset
from locust import HttpUser, task

# NOTE! If you got error that csv/LIVE.txt file is not found, you need to move data/LIVE/LIVE.txt to csv/LIVE.txt
dataset = load_dataset("LIVE", dataset_root="data", download=True)


def get_image_data():
    for image_data in dataset:
        yield image_data


class PerformanceTest(HttpUser):
    @task
    def test_brisque(self):
        image_data = next(get_image_data())

        with open("data/" + image_data["dis_img_path"], "rb") as f:
            self.client.post("/api/v1/iqa/nr/brisque/", files={"image": f})
        with open("data/" + image_data["ref_img_path"], "rb") as f:
            self.client.post("/api/v1/iqa/nr/brisque/", files={"image": f})

    @task
    def test_ms_ssim(self):
        image_data = next(get_image_data())

        o_f = open("data/" + image_data["ref_img_path"], "rb")
        d_f = open("data/" + image_data["dis_img_path"], "rb")

        self.client.post(
            "/api/v1/iqa/fr/ms-ssim/", files={"distorted_image": d_f, "original_image": o_f}
        )

        o_f.close()
        d_f.close()
