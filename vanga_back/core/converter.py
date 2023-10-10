from django.conf import settings


def convert():
    with open(settings.BASE_DIR/'data/sales_df_train.csv', 'r') as f:
        string = f.__next__
        print(string)
