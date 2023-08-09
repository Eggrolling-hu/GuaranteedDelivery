import sys  # noqa: E501
sys.path.append("/media/shadowmotion/0CD113590CD11359/code/demo/smp/GuaranteedDelivery")  # noqa: E501

from elasticsearch import Elasticsearch


if __name__ == "__main__":
    es = Elasticsearch('http://localhost:50004')
