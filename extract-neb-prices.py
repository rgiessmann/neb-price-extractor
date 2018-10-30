
from bs4 import BeautifulSoup
import pandas
import glob

dataframes = []
for node in glob.glob("neb/*.html"):
    soup = BeautifulSoup(open(node), "html.parser")

    list = []

    for i, item in enumerate(soup.find_all("div", "row item")):
        all_divs = item.find_all("div")
        name            = all_divs[1].h2.text
        articlenumber   = all_divs[0].text.strip()
        units           = int(all_divs[1].span.text.replace("Menge: ","").replace(" units", "").replace(".",""))
        price_in_euro   = float(item.find_all("span")[2].text.replace(",", "."))
        price_per_unit  = price_in_euro / units
        foobar = dict()
        for j in ["name", "articlenumber", "units", "price_in_euro", "price_per_unit"]:
            foobar.update( { j : locals()[j] } )
        list.append(foobar)
    print(list)

    dataframes.append(pandas.DataFrame.from_dict(list))

merged_df = pandas.concat(dataframes, ignore_index=True)
merged_df["relative_price"] = merged_df.price_per_unit / merged_df.price_per_unit.min()
merged_df["relative_price"] = merged_df["relative_price"].round(1)
print(merged_df)
merged_df.sort_values(by="name").to_excel("neb-prices.xlsx")
