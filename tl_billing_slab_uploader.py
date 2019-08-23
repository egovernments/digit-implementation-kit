from common import superuser_login
from uploader_tl_billing_slab import create_and_update_billing_slab


def tl_billingslab_uploader():
    tenants = [
        "pb.banga"
    ]
    return tenants


def main():
    auth_token = superuser_login()["access_token"]
    tenants = tl_billingslab_uploader()
    for tenant in tenants:
        create_and_update_billing_slab(auth_token, tenant)


if __name__ == "__main__":
    main()