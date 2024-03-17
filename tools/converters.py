from models.database.database_models import ConvertedUrl


class Url:
    @classmethod
    def convert(cls, url: str):
        splitted_url = url.split("/")
        return ConvertedUrl(hostname=splitted_url[2].split(":")[0],
                            port=int(splitted_url[2].split(":")[1]),
                            user=splitted_url[3].split(":")[0],
                            password=splitted_url[3].split(":")[1],
                            db=splitted_url[4])
