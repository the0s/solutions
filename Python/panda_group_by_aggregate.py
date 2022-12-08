# Using panda dataframes, create a dataframe of sales
# then use lookup prices table to add prices to sales
# then aggregate sales by product category
import pandas as pd

def sum_and_categorise(sales_list, prices):
    ds = []
    for sale in sales_list:
        temp = {'lookup':sale}
        temp['price'] = prices.get(sale)
        temp['name'] = sale.split(' ')[0]
        ds.append(temp)
    df = pd.DataFrame(ds)
    result = df.groupby(['name']).agg(sales=("price", 'sum'))
    result[['sales']] = result[['sales']].apply(lambda x : round(x,2))
    result = result.T.to_dict('r')[0]
    return result


if __name__ == "__main__":
    example_sales = [
        "orange (valencia)",
        "plum (victoria)",
        "plum (victoria)",
        "apple (braeburn)",
        "plum (victoria)",
        "apple (cox)",
    ]
    example_prices = {
        "apple (braeburn)": 0.5,
        "apple (cox)": 0.4,
        "orange (valencia)": 0.75,
        "plum (victoria)": 0.3,
    }

    print(sum_and_categorise(example_sales, example_prices))

