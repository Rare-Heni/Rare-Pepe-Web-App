# Importing packages for the python code
from ast import If
from cmath import nan
from errno import EILSEQ
from pickle import TRUE
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from requests.auth import HTTPBasicAuth
from decimal import Decimal
from datetime import datetime
from datetime import date
import time
from pathlib import Path
from PIL import Image
import json
import requests

#############################################################
# Page Layout
#############################################################

# Layout setting of the page
st.set_page_config(layout="wide")

# Importing pictures of the dashboard
pepe = Image.open("01_pictures/rare_pepe.png")
st.sidebar.image(pepe)
c1, c2 = st.columns((2, 2))

# Defining header of the page
st.markdown("<h1 style='text-align: center; color: green;'>Rare Pepe Scientific Analysis Tool</h1>", unsafe_allow_html=True)

# Defining sidebar of the page
with st.sidebar.form(key = "columns in form"):
    
    # Defining checkboxes for analysis methods
    st.subheader("Analysis Method")
    unweighted = st.checkbox("Unweighted Price Index")
    marketcap_weighted = st.checkbox("Market Cap Weighted Price Index")
    gini_coef = st.checkbox("Gini-Coefficient")
    volume_sold = st.checkbox("Volume Sold")
    dataset_analysis = st.checkbox("Dataset")
    
    # Defining checkboxes for filters
    st.subheader("Filters")
    observation_time = st.selectbox(label = "Period of Time", options = ["All",2016,2017,2018,2019,2020,2021,2022])
    all_series = ["All"]
    series_test = list(range(1,38))
    all_series.extend(series_test)
    card_series = st.selectbox(label = "Card Series", options = all_series)
    card_supply = st.radio(label = "Max Supply Card", options = [100, 500,1000])
    number_transactions = st.radio(label = "Min Number Transactions", options = [5,10])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Defining checkboxes for indices
    st.subheader("Benchmark Index")
    bitcoin_index = st.checkbox("Bitcoin")
    xcp_index = st.checkbox("XCP")
    pepecash_index = st.checkbox("PepeCash")
    nasdaq_index = st.checkbox("NASDAQ")  
    submitted = st.form_submit_button("Submit")
st.sidebar.subheader("Impressum")
st.sidebar.caption("This dashboard is a result of the master thesis of Henrik Pitz. If you like the analysis, you can support me with a donation at: 1HKuL7ecSsExU3KAU7qVtVLusUgt7DYHo6. I am working on adding more analysis.")

# Anzeigen der Startseite, wenn keiner der Checkboxen auf der linken Seite ausgewählt sind
if unweighted == False and marketcap_weighted == False and volume_sold == False and dataset_analysis == False and gini_coef == False:
    
    # Introduction
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: left; color: green;font-size:30px;'>Welcome to the first Rare Pepe Analysis Tool in the world.</h1>", unsafe_allow_html=True)
    st.write("This tool was created as part of a master thesis by Henrik Pitz to simplify collecting and investing in Rare Pepes.")
    st.write("For this purpose a Rare Pepe Index was developed, which shows the performance over the whole collection.")
    st.write("With that you can track the current performance of the collection and buy Rare Pepes based on the information.")
    st.write("In addition, further analyses such as the gini coefficient, the transaction volume in USD and a comparison with other indices are possible.")
    
    st.subheader("Have fun in the world of Rare Pepes!")
    st.markdown("<hr/>", unsafe_allow_html=True)

    # Abstract of the Paper
    st.markdown("<h1 style='text-align: left; color: green;font-size:30px;'>Abstract of the Paper:</h1>", unsafe_allow_html=True)
    st.write("Since 2021, NFTs have experienced tremendous hype in society. This paper analyzes this hype using the Rare Pepes collection to gain a better understanding of the NFT markets and its pricing. For this purpose, one of the largest NFT data sets of a collection is created and made available using an open-source web tool. Based on this, a price index is constructed using the hedonic regression methodology and the performance of the Rare Pepes collection compared to other assets is evaluated. The results of this analysis show that the Rare Pepes collection has generated above average returns since release, outperforming the compared indices, while maintaining a relatively low correlation. The above-average returns come with higher risk and volatility. Using fixed effects regression, the driving factors of the price formation of a Rare Pepe were also identified. The results show that supply, distribution, quantity, and aesthetic attributes have an influence on the price formation. Surprisingly, burns do not have a significant effect on price, which is especially important for investors. The magnitude of the effects suggests that price formation is currently still inefficient. The results of this paper thus provide insightful findings for understanding the NFT market and, together with the web tool, provide an important foundation for further research.")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Useful links in the Rare Pepe World
    st.markdown("<h1 style='text-align: left; color: green;font-size:30px;'>Useful Links to the Rare Pepe World:</h1>", unsafe_allow_html=True)
    st.write("Explorer to see all transactions and assets: [https://xchain.io](https://xchain.io)")
    st.write("Free open-source wallet for bitcoins and Counterparty to trade and store assets: [https://freewallet.io](https://freewallet.io)")
    st.write("Telegram Groupe for traders and collectors: [https://telegram.me/pepetraders](https://telegram.me/pepetraders)")
    st.write("Rare Pepe Directory: [http://rarepepedirectory.com](http://rarepepedirectory.com)")
    st.write("Pepe.WTF: [https://pepe.wtf](https://pepe.wtf)")
    st.write("RarePepes.com: [https://rarepepes.com](https://rarepepes.com)")
    

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Note Thesis Time
    st.markdown("<h1 style='text-align: center; color: grey;font-size:12px;'>Note: For the master thesis evaluation, the data of the tool will not be updated. Next update 01 October.</h1>", unsafe_allow_html=True)
     

else:
    #############################################################
    # Current prices Cryptocurrencies
    #############################################################

    # Information for the Xchain API to get bitcoin and xcp price
    url = "https://xchain.io/api/network"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', '1234')
                
    # Save the output as JSON output to work with it
    response= requests.post(url, headers=headers, auth=auth)
    response = response.json()

    # Reading bitcoin and xcp
    bitcoin_price = float(response["currency_info"][0]["price_usd"])
    xcp_price = float(response["currency_info"][1]["price_usd"])

    # Information for the Xchain API to get pepecash price
    url = "https://xchain.io/api/asset/PEPECASH"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', '1234')
                
    # Save the output as JSON output to work with it
    response= requests.post(url, headers=headers, auth=auth)
    response = response.json()

    # Reading xcp price and converting it to dollar
    pepecash_price = float(response["estimated_value"]["xcp"])*xcp_price

    #############################################################
    # Import of the relevant data
    #############################################################

    # Test if the data is already up to date
    f = open( "00_requirements/Load_Month.txt", 'r' )
    file_contents = f.read()
    load_month = file_contents
    begin_time = datetime.now()
    current_month = begin_time.strftime("%Y-%m")

    # Import of all Rare Pepes
    df_all_pepes = pd.read_csv ("02_input_data/01_all_information_pepes.csv")

    # If filters are activated less pepes are imported
    if card_supply != "All":
        
        if card_supply == 100:
            df_pepes = pd.read_csv("02_input_data/02_all_pepes_supply_max_100.csv")

        if card_supply == 500:
            df_pepes = pd.read_csv("02_input_data/03_all_pepes_supply_max_500.csv")

        if card_supply == 1000:
            df_pepes = pd.read_csv("02_input_data/04_all_pepes_supply_max_1000.csv")

        if card_supply == 10000:
            df_pepes = pd.read_csv("02_input_data/05_all_pepes_supply_max_10000.csv")

    if card_supply == "All":
        df_pepes = pd.read_csv ("02_input_data/00_official_rare_pepes.csv")

    # Creation of the list to work with
    df_pepes = df_pepes.iloc[: , 1:]
    pepes_list = df_pepes["Name"].tolist()
    official_rare_pepes = pepes_list

    #############################################################
    # Creation of the dataset
    #############################################################

    # If the month does not correspond to the month of the last data reconciliation, an updated record is created
    if current_month != load_month: 
        
    #############################################################
    # Add the original supply when minting as information for the calculation of the gini coefficient
    #############################################################

        # Creation of a dataframe to save the information
        page_counter = 100
        page = 1
        column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Source", "Destination"]
        df_gini_ts = pd.DataFrame(columns = column_names)

        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:

            # API call by issuances and 100 assets per page
            url = "https://xchain.io/api/issuances/" + names + "/" + str(page) + "/100"
            headers = {'content-type': 'application/json'}
            auth = HTTPBasicAuth('rpc', '1234')
                            
            # Saving the output as JSON
            response_xchain = requests.post(url, headers=headers, auth=auth)
            response_xchain_json = response_xchain.json()

            # Getting all issuances
            for data in response_xchain_json["data"]:
                names = data["asset"]
                supply = float(data["quantity"])
                source = "NON"
                destination = data["issuer"]
                ts = time.gmtime(data['timestamp'])
                date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                date_index = time.strftime("%Y-%m", ts)

            # Saving the information in the dataframe 
                if supply > 0:
                    df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"sends",date,date_index,0, supply,0,supply, source, destination]
                    
    #############################################################
    # Add transactions with dispensers
    #############################################################                

        # Creation of dataframes to save the information
        column_names = ["Name", "Date", "Price", "Currency", "Price in USD", "Quantity" , "TX_Hash_Dispenser", "TX_Hash_Dispenses"]
        df_dispensers = pd.DataFrame(columns = column_names)
        
        column_total = ["Name","Series", "Date", "Price in USD", "Quantity", "Type", "Date_Index"]
        df_total = pd.DataFrame(columns = column_total)

        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = card["Series"].iloc[0]
            page_counter = 100
            page = 1
            Assets = 0
            Used_Dispensers = 0

            # Page counter, this runs until no more assets are displayed on a page
            while page_counter > 0:

                # API call by dispenser and 100 assets per page
                url = "https://xchain.io/api/dispensers/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                
                # Saving the output as JSON
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page = page + 1
                page_counter = 0
                
                # Reading the dispenser to get the transaction hash
                # Since dispensers can be used more than once, it is not enough to look at the dispenser only
                # You need all the dispenses performed per dispenser
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1
                    tx_hash = data["tx_hash"]
                    Assets = Assets + 1

                    # API call for the right dispenses
                    url = "https://xchain.io/api/dispenses/" + tx_hash
                    headers = {'content-type': 'application/json'}
                    auth = HTTPBasicAuth('rpc', '1234')
                
                    # Saving the output as JSON
                    dispenses_xchain = requests.post(url, headers=headers, auth=auth)
                    response_dispenses_xchain = dispenses_xchain.json()

                    # If there is an entry in the respective transcations, it means that the dispenser was used
                    if response_dispenses_xchain["total"] > 0:
                        Used_Dispensers = Used_Dispensers + 1

                        # Loop through the transactions to get all the dispenses performed
                        for transactions in response_dispenses_xchain["data"]:
                            value_give = float(data['satoshirate'])
                            quantity = float((data['give_quantity']))
                            ts = time.gmtime(transactions['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)    
                            date_index = time.strftime("%Y-%m", ts) 
                            TX_Hash_Dispenser = data["tx_hash"]
                            TX_Hash_Dispenses = transactions["tx_hash"]
                            quantity_dispenses = float((transactions['quantity']))
                            value = (value_give / quantity)

                            # API call with the performed dispenses to get source and destination   
                            # This information is needed for the gini coefficient                            
                            url = "https://xchain.io/api/tx/" + TX_Hash_Dispenses
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')

                            # Saving the output as JSON
                            info_dispenses = requests.post(url, headers=headers, auth=auth)
                            response_info_dispenses = info_dispenses.json()
                            
                            # Saving information in dataframes
                            source = response_info_dispenses["source"]
                            destination = response_info_dispenses["destination"]

                            #for gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"dispenser",date,date_index,series,0,value*bitcoin_price,quantity, source, destination] 

                            #for dispenser only
                            df_dispensers.loc[df_dispensers.shape[0]] = [names, date, value, "BTC", value*bitcoin_price, quantity_dispenses, TX_Hash_Dispenser, TX_Hash_Dispenses]

                            #for the final dataset
                            df_total.loc[df_total.shape[0]] = [names,series, date, value*bitcoin_price,quantity_dispenses, "dispenser", date_index]

        # Saving dispenser dataframe as csv
        df_dispensers.to_csv("03_output_data/" + 'all_transactions_dispensers.csv', index = False)
        
    #############################################################
    # Add transactions with get and give order
    #############################################################    

        # Creation of dataframes to save the information of get and give orders
        column_names = ["Name", "Date", "Price", "Currency", "Price in USD"]
        df_get = pd.DataFrame(columns = column_names)
        df_give = pd.DataFrame(columns = column_names)

        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = str(card["Series"].iloc[0])

            Assets = 0
            page_counter = 100
            page = 1
            pages = 0

            # Page Counter, this runs until no more assets are displayed on a page
            while page_counter > 0:

                # API call by orders and 100 assets per page
                url = "https://xchain.io/api/order_matches/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                    
                page = page + 1
                pages = pages + 1

                # Saving the output as JSON
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page_counter = 0

                # Loop over all assets
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1

                    Assets = Assets + 1
                    
                    # Read out all Get_Assets
                    if data["forward_asset"] == names:

                            value_order = float(data['backward_quantity'])
                            quantity = float(data['forward_quantity'])
                            currency = data["backward_asset"]
                            value = (value_order / quantity)
                            
                            # Transform to USD
                            value_usd = 0
                            if currency == "BTC":
                                value_usd = value * bitcoin_price
        
                            if currency == "XCP":
                                value_usd = value * xcp_price

                            if currency == "PEPECASH":
                                value_usd = value * pepecash_price

                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                            date_index = time.strftime("%Y-%m", ts)
                            destination = data["tx1_address"]
                            source = data["tx0_address"]

                            # for gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"get",date,date_index,series,0,value_usd, quantity, source, destination] 
                            
                            # for get only
                            df_get.loc[df_get.shape[0]] = [names,date, value, currency, value_usd]

                            # for the final dataframe
                            df_total.loc[df_total.shape[0]] = [names, series, date, value_usd,quantity, "order_get", date_index]

                    # Read out all Give_Assets
                    if data["backward_asset"] == names:

                            value_order = float((data['forward_quantity']))
                            quantity = float((data['backward_quantity']))
                            currency = data["forward_asset"]
                            value = (value_order / quantity)

                            # Transform to USD
                            value_usd = 0
                            if currency == "BTC":
                                value_usd = value * bitcoin_price
        
                            if currency == "XCP":
                                value_usd = value * xcp_price

                            if currency == "PEPECASH":
                                value_usd = value * pepecash_price
                                
                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                            date_index = time.strftime("%Y-%m", ts) 
                            source = data["tx1_address"]
                            destination = data["tx0_address"]

                            # for gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"give",date,date_index,series,0,value_usd, quantity, source, destination]

                            # for get only
                            df_give.loc[df_get.shape[0]] = [names, date, value, currency, value_usd]

                            # for the final dataframe
                            df_total.loc[df_total.shape[0]] = [names, series, date, value_usd,quantity, "order_give", date_index]

        # Saving orders dataframe as csv
        df_get.to_csv("03_output_data/" +'all_transactions_get_orders.csv', index = False)
        df_give.to_csv("03_output_data/" +'all_transactions_give_orders.csv', index = False)

    #############################################################
    # Add send transactions
    #############################################################    

        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:

            Assets = 0
            page_counter = 100
            page = 1
            pages = 0

            # Page counter, this runs until no more assets are displayed on a page
            while page_counter > 0:

                # API call by sends and 100 assets per page
                url = "https://xchain.io/api/sends/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                    
                page = page + 1
                pages = pages + 1

                # Saving the output as csv
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page_counter = 0

                # Loop over all assets
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1

                    Assets = Assets + 1

                    # Readout of all sends that have been validated
                    if data["status"] == "valid":

                            quantity = float(data['quantity'])
                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                            date_index = time.strftime("%Y-%m", ts)

                            source = data["source"]
                            destination = data["destination"]

                            # for gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"sends",date,date_index,0,0,0, quantity, source, destination]              

    #############################################################
    # Add burns to calculate "real" supply
    #############################################################   

        # Creation of dataframes to save the information of get and give orders
        column_names = ["Name", "Date", "Quantity"]
        df_burns = pd.DataFrame(columns = column_names)
        column_names = ["Name","Series", "Supply", "Burns" , "Remaining_Supply", "Remaining_Percentage"]
        df_burns_total = pd.DataFrame(columns = column_names)
        
        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = card["Series"].iloc[0]

            page_counter = 100
            page = 1
            Assets = 0
            Used_Dispensers = 0
            total_quantity_burns = 0

            # Query the holders of the assets
            while page_counter > 0:
                url = "https://xchain.io/api/holders/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                
                # saving output as JSON
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page = page + 1
                page_counter = 0

                # Loop through the Holders and query if the address contains "Burn"
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1
                    address = "nopepe"

                    # If yes, the Holder address is saved
                    if "Burn" in data["address"]:
                        address = data["address"]
                    if "BURN" in data["address"]:
                        address = data["address"]
                    if address != "nopepe":

                        page_counter_1 = 100
                        page_1 = 1

                        while page_counter_1 > 0:

                            # API call to analyze the sends of the burn address
                            # All assets sent here are burned
                            url = "https://xchain.io/api/sends/"+  address + "/" + str(page_1) + "/100"
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')
                
                            # Saving output as JSON
                            response_xchain = requests.post(url, headers=headers, auth=auth)
                            response_xchain_json = response_xchain.json()

                            page_1 = page_1 + 1
                            page_counter_1 = 0
                            
                            # Take only the assets whose name corresponds to the searched Rare Pepe
                            for data in response_xchain_json["data"]:
                                page_counter_1 = page_counter_1 + 1
                                
                                if data["asset"] == names:
                                    Assets = Assets + 1
                                    quantity = float((data['quantity']))
                                    ts = time.gmtime(data['timestamp'])
                                    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                                    TX_Hash= data["tx_hash"]
                                    source = data["source"]
                                    
                                    # for burns
                                    df_burns.loc[df_burns.shape[0]] = [names, date, quantity]        

        # Saving bruns dataframe as csv
        df_burns.to_csv("03_output_data/" +'all_burns.csv', index = False)
        
    #############################################################
    # Add burns to final dataset and substract them from supply
    #############################################################   

        df_total["Supply"] = 0
        df_total = df_total.sort_values(by=["Date"], ascending = True)

        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            df_total_names = df_total.loc[df_total['Name'] == names]
            df_burns_names = df_burns.loc[df_burns['Name'] == names]
            df_burns_names = df_burns_names.sort_values(by=["Date"], ascending = True)
            name_supply = df_all_pepes["Name"] == names
            supply = df_all_pepes[name_supply]["Quantity"].iloc[0]
            
            # Change data format to float if needed
            if type(supply) == str:
                supply = supply.replace(",", "")

            amount = 0
            burns_row = 0
            burns_quantity = 0
            amount_burns = len(df_burns_names) -1
            length = len(df_burns_names)
            
            # Comparison of the burns with the data to subtract them from the original supply
            for ind in df_total_names.index:
                if amount == 0 and burns_quantity == 0:
                    amount = float(supply)
                
                # Only continue counting if the last burn has not yet been reached
                if burns_row < length:
                    if df_burns_names.iloc[burns_row]["Date"] < df_total_names["Date"][ind]:
                        burns_quantity = df_burns_names.iloc[burns_row]["Quantity"]
                        amount = amount - burns_quantity

                        if burns_row <= amount_burns:
                            burns_row = burns_row + 1
                        
                # Inserting the real supplies
                df_total_names["Supply"][ind] = amount
                df_total["Supply"][ind] = amount

                # Burns are added to the final table
                df_total_names = df_total.loc[df_total['Name'] == names]
                
    #############################################################
    # Add burns to the holders dataset
    #############################################################               

        df_gini_ts["Supply"] = 0
        
        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
            df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)
            df_burns_names = df_burns.loc[df_burns['Name'] == names]
            df_burns_names = df_burns_names.sort_values(by=["Date"], ascending = True)

            name_supply = df_all_pepes["Name"] == names
            supply = df_all_pepes[name_supply]["Quantity"].iloc[0]

            # Change data format to float if needed
            if type(supply) == str:
                supply = supply.replace(",", "")

            amount = 0
            burns_row = 0
            burns_quantity = 0
            amount_burns = len(df_burns_names) -1
            length = len(df_burns_names)
            
            # Comparison of the burns with the data to subtract them from the original supply
            for ind in df_gini_ts_names.index:
                if amount == 0 and burns_quantity == 0:
                    amount = float(supply)
                
                # Only continue counting if the last burn has not yet been reached
                if burns_row < length:
                    if df_burns_names.iloc[burns_row]["Date"] < df_gini_ts_names["Date"][ind]:
                        burns_quantity = df_burns_names.iloc[burns_row]["Quantity"]
                        
                        amount = amount - burns_quantity

                        if burns_row <= amount_burns:
                            burns_row = burns_row + 1
                        
                # Inserting the real supplies
                df_gini_ts_names["Supply"][ind] = amount
                df_gini_ts["Supply"][ind] = amount

                # Burns are added to the final table
                df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]

        # Saving all holders as csv
        df_gini_ts = df_gini_ts.sort_values(by=["Date"], ascending = True)
        df_gini_ts.to_csv("03_output_data/" +'all_holders_gini.csv',index=False)
        
    #############################################################
    # Add sweeps to the dataset
    # This was used to create the data set with sweeps. In the current tool, this is no longer included due to the high runtime
    #############################################################     

        if False:
            # Adding dataframe to save the output
            column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Source", "Destination", "TX_Hash"]
            df_sweep = pd.DataFrame(columns = column_names)

            # Loop with all Rare Pepe to call the api
            for names in official_rare_pepes: 
                
                df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
                df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)

                # Getting the source and destination of the transaction
                unique_source = df_gini_ts_names["Source"].unique()
                unique_destination = df_gini_ts_names["Destination"].unique()
                unique_adress = df_gini_ts_names["Source"].append(df_gini_ts_names["Destination"]).reset_index(drop=True)
                unique_adress = unique_adress.unique().tolist()
                unique_adress.remove('NON')
                
                # Loop over all addresses to get the sweeps
                for address in unique_adress:

                    page = 1
                    page_counter = 100
                    page = 1
                    pages = 0
                    
                    # Page Counter, this runs until no more assets are displayed on a page
                    while page_counter > 0:

                        # API Call by debits and 100 assets per page
                        url = "https://xchain.io/api/debits/" + address + "/" + str(page) + "/100"
                        headers = {'content-type': 'application/json'}
                        auth = HTTPBasicAuth('rpc', '1234')

                        page = page + 1
                        pages = pages + 1                            
                                
                        # Saving the output as csv
                        response_xchain = requests.post(url, headers=headers, auth=auth)
                        response_xchain_json = response_xchain.json()

                        page_counter = 0
                        
                        # Getting all transaction hashs of sweeps with the current Rare Pepe
                        for data in response_xchain_json["data"]:
                            if data["action"] == "sweep":
                                if data["asset"] == names:
                                    
                                    names = data["asset"]
                                    quantity = float((data['quantity']))

                                    ts = time.gmtime(data['timestamp'])
                                    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                                    date_index = time.strftime("%Y-%m", ts)
                                    tx_hash = data["event"]
                                    
                                    # Saving sweep in dataframe
                                    if quantity > 0:
                                        df_sweep.loc[df_sweep.shape[0]] = [names,"sweep",date,date_index,0,0,0, quantity, 0, 0, tx_hash]
                        
                            page_counter = page_counter + 1
                    
                    # If there are sweeps for the Rare Pepe
                    if len(df_sweep) > 0:
                        sweep_list = df_sweep["TX_Hash"].tolist()

                        page = 1
                        page_counter = 100
                        page = 1
                        pages = 0

                        # Page counter, this runs until no more assets are displayed on a page
                        while page_counter > 0:

                            # API call by sweep with address and 100 assets per page
                            url = "https://xchain.io/api/sweeps/" + address + "/" + str(page) + "/100"
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')

                            page = page + 1
                            pages = pages + 1                            
                                    
                            # Saving the output as csv
                            response_xchain = requests.post(url, headers=headers, auth=auth)
                            response_xchain_json = response_xchain.json()

                            page_counter = 0
                            
                            # Saving in sweep dataframe
                            for data in response_xchain_json["data"]:
                                if data["tx_hash"] in sweep_list:
                                    df_sweep.loc[df_sweep.TX_Hash == data["tx_hash"], 'Source'] = data["source"]
                                    df_sweep.loc[df_sweep.TX_Hash == data["tx_hash"], 'Destination'] = data["destination"]

                                page_counter = page_counter + 1

                    # Adding sweeps to gini dataframe
                    column_names = list(df_sweep.columns.values)
                    if "TX_Hash" in column_names:
                        df_sweep.drop("TX_Hash", axis=1, inplace=True)
                    df_gini_ts = pd.concat([df_gini_ts, df_sweep], ignore_index=True, sort=False)
                    df_gini_ts = df_gini_ts.sort_values(by=["Date"], ascending = True)

    #############################################################
    # Calculation of the Gini coefficient
    #############################################################     

        # Creation of dataframes to save the information of gini coefficient and errors
        column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Gini", "Top_3", "Top_5", "Top_10"]
        df_gini_final = pd.DataFrame(columns = column_names)
        column_names = ["Name"]
        errors = pd.DataFrame(columns = column_names)
        
        # Loop with all Rare Pepe to call the api
        for names in official_rare_pepes:
            non_test = 0
            supply_1 = 0
            holders = {}
            df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
            df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)
            
            # Saving information of the dataframe
            for ind in df_gini_ts_names.index:
                supply = df_gini_ts_names["Supply"][ind]
                date = df_gini_ts_names["Date"][ind]   
                source = df_gini_ts_names["Source"][ind]
                destination = df_gini_ts_names["Destination"][ind]
                quantity = df_gini_ts_names["Quantity"][ind]
                Type = df_gini_ts_names["Type"][ind]
                price_usd = df_gini_ts_names["Price in USD"][ind]
                date_index = df_gini_ts_names["Date_Index"][ind]
                series = df_gini_ts_names["Series"][ind]

                # Getting the first transaction with minting
                if source == "NON":
                    if destination in holders.keys():
                        holders[destination] += quantity

                    else:
                        holders[destination] = quantity
                    
                    if non_test ==0:
                        supply = quantity
                        non_test = non_test + 1
                        supply_1 = supply
                    else:
                        supply = supply_1 + quantity
                        supply_1 = supply
                
                # Here still special case Burns add. Then namely only subtract and not add the burn address
                else:
                    send_burn = 0

                    if "Burn" in destination:
                        send_burn = 1

                    if "BURN" in destination:
                        send_burn = 1

                    if send_burn == 1:
                        holders[source] -= quantity
                    
                    if send_burn == 0:
                        if destination in holders.keys():
                            holders[destination] += quantity
                        else:
                            holders[destination] = quantity

                        if source in holders.keys():
                            holders[source]  -= quantity
                        else:
                            holders[source]  = quantity

                        if (source  , 0) in holders.items():
                            holders.pop(source)
                    send_burn = 0
                
                # Creation of the holders list to calculate gini coefficient
                holders_list = pd.DataFrame(list(holders.items()),columns = ['Holder','Quantity'])
                holders_list= holders_list["Quantity"]
                holders_list_sorted = holders_list.sort_values(ascending = False)

                # Calculating top_3, top_5 and top_10 holders
                top_3 = holders_list_sorted.iloc[0:3].sum() / supply
                top_5 = holders_list_sorted.iloc[0:5].sum() / supply
                top_10 = holders_list_sorted.iloc[0:10].sum() / supply

                holders_list_sorted = holders_list.sort_values()
                
                # Formula to calculate gini coefficient
                def gini(list_of_values):
                    sorted_list = sorted(list_of_values)
                    height, area = 0, 0
                    for value in sorted_list:
                        height += value
                        area += height - value / 2.
                    fair_area = height * len(list_of_values) / 2.

                    # Error because sweeps are not included
                    try: 
                        return (fair_area - area) / fair_area
                    except ZeroDivisionError:
                        errors.loc[errors.shape[0]] = [names]
                        return nan
            
                # Rounding of the output                 
                gini_holders = round(gini(holders_list_sorted),3)

                # saving all to dataframe
                df_gini_final.loc[df_gini_final.shape[0]] = [names,Type,date,date_index,series, supply,price_usd,quantity, gini_holders, top_3, top_5, top_10]

        # saving dataframe with gini coefficient as csv
        df_gini_final.to_csv("03_output_data/" +'all_holders_gini_final.csv',index=False)
        
        # saving new dataframe to work on with
        df_total = pd.read_csv("03_output_data/" +'all_holders_gini_final.csv')
        
        # saving erros as csv
        errors.to_csv("03_output_data/" +'all_errors.csv',index=False)

        # Import the data of my new table with time series gini, top holders and supply into big table.
        # Export the data to go through the data only once a day/month
        name_dataframe = "all_transactions_max_" + str(card_supply) + ".csv"
        df_total.to_csv("03_output_data/" + name_dataframe,index=False)
        
    #############################################################
    # Cleanup of the data set
    #############################################################     

        # It is possible to created a dataframe without cleaning
        divisible_transactions = True
        filter_outliers = True

        # Here it is filtered whether transactions were carried out with divisible asssets, if so they are deleted.
        if divisible_transactions == True:
            df_total_non_divisible = df_total.loc[df_total['Quantity'] >= 1]
            
            #delete of sends in dataframe, only important for the ginig calculation
            df_total_non_divisible = df_total_non_divisible.loc[df_total_non_divisible['Type']!= "sends"]
            
            #delete of transactions prices < 0, errors in the transaction protocol
            df_total_non_divisible = df_total_non_divisible.loc[df_total_non_divisible['Price in USD']> 0]

            # Saving of all transactions non divisible as csv
            name_dataframe = "all_transactions_nd_max_" + str(card_supply) + ".csv"
            df_total_non_divisible.to_csv("03_output_data/" + name_dataframe, index = False)
        
        column_total = ["Name","Type","Date","Date_Index","Supply","Price in USD","Quantity", "Gini", "Top_3", "Top_5", "Top_10"]
        df_total_nd_no = pd.DataFrame(columns = column_total)

        # Here the data set is cleaned from outliers
        if filter_outliers == True:
            for names in official_rare_pepes:

                # Dropping the Outliers Non Divisible
                name_transactions_1 = df_total_non_divisible.loc[df_total_non_divisible["Name"] == names]
                df_total_non_disible_non_outliers = name_transactions_1[name_transactions_1["Price in USD"] > name_transactions_1["Price in USD"].quantile(0.02)]
                df_total_non_disible_non_outliers = name_transactions_1[name_transactions_1["Price in USD"] < name_transactions_1["Price in USD"].quantile(0.98)]

                # Remove Gini greater than 1 (Not possible by definition, error due to sweeps)
                df_total_non_disible_non_outliers = df_total_non_disible_non_outliers.loc[df_total_non_disible_non_outliers['Gini']<= 1]     

                # Save transactions as csv non dvisible (nd) and non outliers (no)
                df_total_nd_no = df_total_nd_no.append(df_total_non_disible_non_outliers, ignore_index=True)
                name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + ".csv"
                df_total_nd_no.to_csv("03_output_data/" + name_dataframe,index=False)

    #############################################################
    # Calculation of the price level
    ############################################################# 

        df_total = df_total_nd_no

        # Creation of dataframes to save the price level
        column_names = [ "Price_Level", "Date_Index"]
        df_price_level = pd.DataFrame(columns = column_names)

        # Loop over all months and years
        month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
        year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

        today = datetime.now()
        current_month = today.strftime("%Y-%m")

        # Loop with all Rare Pepe to call the api   
        for names in official_rare_pepes:
            preisniveau = 0
            test = df_total.loc[df_total['Name'] == names]
            for y in year:

                for m in month:
                    date = y + "-" + m
                    if date == current_month:
                        break
                    else:
                        preisniveau_davor = preisniveau
                        test_names = test.loc[test['Date_Index'] == date]
                        anzahl = len(test_names)

                        if anzahl == 0 and preisniveau_davor == 0:
                            preisniveau = 0
                        if anzahl == 0 and preisniveau_davor !=0:
                            preisniveau = preisniveau_davor
                        if anzahl != 0:
                            preisniveau = test_names["Price in USD"].mean()

                        df_price_level.loc[df_price_level.shape[0]] = [preisniveau, date]
        
        # Saving of the price level as csv
        name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + ".csv"
        df_price_level.to_csv("03_output_data/" + name_dataframe, index = False)
        df_price_level_series = df_price_level.groupby(["Date_Index"]).sum()

        # last load date
        end_time = datetime.now()
        load_month = end_time.strftime("%Y-%m")

        # Save last load date
        f = open( "00_requirements/Load_Month.txt", 'w' )
        f.write(load_month)
        f.close()

    #############################################################
    # This section of the code is used if in the month the record has already been updated.
    # This reduces the runtime of the code
    ############################################################# 

    else:
        # Read Rare Pepes depending on filter
        if card_supply != "All":
            
            if card_supply == 100:
                df_pepes = pd.read_csv("02_input_data/02_all_pepes_supply_max_100.csv")

            if card_supply == 500:
                df_pepes = pd.read_csv("02_input_data/03_all_pepes_supply_max_500.csv")

            if card_supply == 1000:
                df_pepes = pd.read_csv("02_input_data/04_all_pepes_supply_max_1000.csv")

            if card_supply == 10000:
                df_pepes = pd.read_csv("02_input_data/05_all_pepes_supply_max_10000.csv")

        if card_supply == "All":
            df_pepes = pd.read_csv ("02_input_data/00_official_rare_pepes.csv")

        # Creation of the Rare Pepe list
        df_pepes = df_pepes.iloc[: , 1:]
        pepes_list = df_pepes["Name"].tolist()
        official_rare_pepes = pepes_list

        # Saving dataframe as csv
        name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + ".csv"
        df_total = pd.read_csv("03_output_data/" + name_dataframe)

        # Sort the dataframe
        df_total = df_total.sort_values(by=["Date"], ascending = False)

        # Filtering by the number of transactions of a rare pepe
        if number_transactions != "All":
            for names in official_rare_pepes:
                name_transaction = df_total.loc[df_total["Name"] == names]

                if len(name_transaction) < number_transactions:
                    df_total = df_total.loc[df_total["Name"] != names]
        
        # Restrict loop to existing rare pepes in the used dataset
        column_values = df_total["Name"].values
        unique_values = np.unique(column_values)
        pepes_list = unique_values.tolist()
        official_rare_pepes = pepes_list

        # Filter by series
        if card_series != "All":
            for names in official_rare_pepes:
                name_transaction = df_total.loc[df_total["Name"] == names]

                if name_transaction["Series"].iloc[0] != card_series:
                    df_total = df_total.loc[df_total["Name"] != names]

        # Saving dataframe as csv
        name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        df_total.to_csv("03_output_data/" + name_dataframe, index = False)

        # Restrict loop to existing rare pepes in the used dataset
        column_values = df_total["Name"].values
        unique_values = np.unique(column_values)
        pepes_list = unique_values.tolist()
        official_rare_pepes = pepes_list

        # Showing used Rare Pepes in the analysis
        
        d1, d2 = st.columns((2, 2))
        d1.write("Used Rare Pepes: " + str(len(unique_values)))
        st.markdown("<hr/>", unsafe_allow_html=True)

        # Saving dataframe as csv
        name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path("03_output_data/" + path_to_file)

    #############################################################
    # Calculation of the price level
    # Explanation see above
    ############################################################# 

        # Checking if file already exists
        if path.is_file() == True:
            df_price_level = pd.read_csv ("03_output_data/" + name_dataframe)

        else:
            if number_transactions != "All" or card_series != "All" or observation_time !="All":
                column_names = [ "Price_Level", "Date_Index"]
                df_price_level = pd.DataFrame(columns = column_names)

                month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
                year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

                today = datetime.now()
                current_month = today.strftime("%Y-%m")

                for names in official_rare_pepes:
                    preisniveau = 0
                    test = df_total.loc[df_total['Name'] == names]
                    for y in year:

                        for m in month:
                            date = y + "-" + m
                            if date == current_month:
                                break
                            else:
                                preisniveau_davor = preisniveau
                                test_names = test.loc[test['Date_Index'] == date]
                                anzahl = len(test_names)

                                if anzahl == 0 and preisniveau_davor == 0:
                                    preisniveau = 0
                                if anzahl == 0 and preisniveau_davor !=0:
                                    preisniveau = preisniveau_davor
                                if anzahl != 0:
                                    preisniveau = test_names["Price in USD"].mean()

                                df_price_level.loc[df_price_level.shape[0]] = [preisniveau, date]

                name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
                df_price_level.to_csv("03_output_data/" + name_dataframe, index = False)
                df_price_level = df_price_level.sort_values(by=["Date_Index"], ascending = False)

        df_price_level = df_price_level.sort_values(by=["Date_Index"], ascending = False)

        month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
        year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]
        
        # Subset of dataframe when filter ist on
        if observation_time !="All":
            year = [str(observation_time)]

        # Update of the current month
        today = datetime.now()
        current_month = today.strftime("%Y-%m")

    #############################################################
    # Calculation of the unweighted price index
    ############################################################# 

    if unweighted==True:

        name_dataframe = "df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path("03_output_data/" + path_to_file)

        un1, un2 = st.columns((2, 3)) 
        un1.subheader("Unweighted Price Index")
        e1, e2 = st.columns((2, 3))
        
        # Checking if file already exists
        # if yes show results
        if path.is_file() == True:
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df = df[['Date_Index','Price_Level']]
            e1.markdown("Data:")
            e1.dataframe(df, height=500)

            name_dataframe = "png_df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open("04_graphs/" + name_dataframe)
            e2.markdown("Graph:")
            e2.image(price)

        # Creation of the unweighted price index dataset and graph    
        else:
            
            # Filter by observation
            if observation_time !="All":
                test = df_price_level
                test["Year"] = df_price_level["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_price_level = test
            
            # Calculation of the price index
            df_unweighted_price_level = df_price_level.groupby(["Date_Index"]).sum()
            df_unweighted_price_level = df_unweighted_price_level.loc[df_unweighted_price_level['Price_Level'] != 0]

            # Save as csv
            name_dataframe = "df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_unweighted_price_level.to_csv("03_output_data/" + name_dataframe)
            
            # Show dataframe
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df = df[['Date_Index','Price_Level']]
            e1.markdown("Data:")
            e1.dataframe(df, height=500)
            
            # show graph
            e2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date_Index"])
            df_test.plot(x ='time', y='Price_Level', kind = 'line')

            # save graph
            name_dataframe = "png_df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig("04_graphs/" + name_dataframe)
            plt.close()
            price = Image.open("04_graphs/" + name_dataframe)
            e2.image(price)
               
            # cumulative price index
            df_cum = df_test
            df_cum['Price_Level'] = df_cum['Price_Level'].div(df_cum['Price_Level'].iat[0])
            
            df_cum["time"] = pd.to_datetime(df_cum["Date_Index"])
            df_cum.plot(x ='time', y='Price_Level', kind = 'line')
            
            name_dataframe = "png_df_cum_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig("04_graphs/" + name_dataframe)
            
        st.markdown("<hr/>", unsafe_allow_html=True)   

    #############################################################
    # Calculation of the market weighted price index
    ############################################################# 

    if marketcap_weighted == True:
        
        mcap1, mcap2 = st.columns((2, 3)) 
        mcap1.subheader("Market-Cap Weighted Price Index")
        f1, f2 = st.columns((2, 3))
        
        name_dataframe = "df_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path("03_output_data/" + path_to_file)

        # Checking if file already exists
        # if yes show results
        if path.is_file() == True:
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df = df[['Date_Index','Price_Level']]
            f1.markdown("Data:")
            f1.dataframe(df, height=500)

            name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open("04_graphs/" + name_dataframe)
            f2.markdown("Graph:")
            f2.image(price)
            
        # Creation of the market weighted price index dataset and graph    
        else:

            # Creation of dataframes to save the price level
            column_names = [ "Price_Level", "Date_Index"]
            df_price_level_market_cap = pd.DataFrame(columns = column_names)

            month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
            year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

            today = datetime.now()
            current_month = today.strftime("%Y-%m")

            # Loop over all Rare Pepes
            for names in official_rare_pepes:
                preisniveau_market_cap = 0
                test = df_total.loc[df_total['Name'] == names]
                for y in year:

                    for m in month:
                        date = y + "-" + m
                        if date == current_month:
                            break
                        else:
                            preisniveau_davor = preisniveau_market_cap
                            test_names = test.loc[test['Date_Index'] == date]
                            anzahl = len(test_names)

                            if anzahl == 0 and preisniveau_davor == 0:
                                preisniveau_market_cap = 0
                            if anzahl == 0 and preisniveau_davor !=0:
                                preisniveau_market_cap = preisniveau_davor
                            if anzahl != 0:
                                preisniveau = test_names["Price in USD"].mean()
                                supply = test_names["Supply"].mean()

                                # Calculation of the marke capitalization
                                preisniveau_market_cap = preisniveau * supply

                            # Saving output in dataframe
                            df_price_level_market_cap.loc[df_price_level_market_cap.shape[0]] = [preisniveau_market_cap, date]
                            
            # Filter by observation time
            if observation_time !="All":
                test = df_price_level_market_cap
                test["Year"] = df_price_level_market_cap["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_price_level_market_cap = test
            
            # Calculation of the market weighted price index
            df_market_cap = df_price_level_market_cap.groupby(["Date_Index"]).sum()
            df_market_cap = df_market_cap.loc[df_market_cap['Price_Level'] != 0]
            
            name_dataframe = "df_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_market_cap.to_csv("03_output_data/" + name_dataframe)

            # show dataframe
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df = df[['Date_Index','Price_Level']]
            f1.markdown("Data:")
            f1.dataframe(df, height=500)
        
            # show graph
            f2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date_Index"])
            df_test.plot(x ='time', y='Price_Level', kind = 'line')

            # save graph
            name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig("04_graphs/" + name_dataframe)
            price = Image.open("04_graphs/" + name_dataframe)
            f2.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    #############################################################
    # Visualization of the Gini coefficient
    ############################################################# 

    if gini_coef == True:
        
        name_dataframe = "df_gini_list_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path("03_output_data/" + path_to_file)

        gini1, gini2 = st.columns((2, 3)) 
        gini1.subheader("Gini Coefficient")
        g1, g2 = st.columns((2, 3))

        # check if dataframe already exists
        if path.is_file() == True:
            df_gini_list = pd.read_csv("03_output_data/" + name_dataframe)

            # show dataframe
            g1.markdown("Individual Gini-Coefficient:")
            df_gini_list = df_gini_list[['Name','gini']]
            g1.dataframe(df_gini_list)
            total_gini = df_gini_list["gini"].mean()
            total_gini = round(total_gini, 3)      

            # show graph
            graph = "png_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            gini_graph = Image.open("04_graphs/" + graph)
            g2.markdown("Graph:")
            g2.image(gini_graph)
            g1.write("The Gini-Coefficient is the most well-known measure of inequality. A Gini-Coefficient of zero means all holders have the same amount of cards. A Gini-Coefficient of one means one holder has all cards. The lower the Gini coefficient, the more equal the holders are. The current total Gini-Coefficient equals: " + str(total_gini)+ ".")
        
        # Calculation of the Gini coefficient
        # Explanation see above
        
        else:
            column_names = ["Name", "address", "quantity", "percentage"]
            df_holders = pd.DataFrame(columns = column_names)

            column_names = ["Name", "x", "points"]
            df_gini = pd.DataFrame(columns = column_names)

            column_names = ["Name", "gini"]
            df_gini_list = pd.DataFrame(columns = column_names)

            for names in official_rare_pepes:
                page_counter = 100
                page = 1
                
                while page_counter > 0:

                    url = "https://xchain.io/api/holders/" + names + "/" + str(page) + "/100"
                    headers = {'content-type': 'application/json'}
                    auth = HTTPBasicAuth('rpc', '1234')

                    response= requests.post(url, headers=headers, auth=auth)
                    response = response.json()

                    page = page + 1
                    page_counter = 0

                    for data in response["data"]:
                        page_counter = page_counter + 1

                        if "BURN" in data["address"]:
                            continue

                        elif "Burn" in data["address"]:
                            continue

                        else:
                            address = data["address"]
                            quantity = float(data["quantity"])
                            percentage = data["percentage"]     

                            df_holders.loc[df_holders.shape[0]] = [names, address, quantity, percentage]

                holders_name = df_holders.loc[df_holders['Name'] == names]
                df_holders_sorted = holders_name["quantity"]
                df_holders_sorted = df_holders_sorted.sort_values()
                quantity = len(df_holders_sorted)
                quartiles = round(quantity / 5)

                def gini(list_of_values):
                    sorted_list = sorted(list_of_values)
                    height, area = 0, 0
                    for value in sorted_list:
                        height += value
                        area += height - value / 2.
                    fair_area = height * len(list_of_values) / 2.
                    try: 
                        return (fair_area - area) / fair_area
                    except ZeroDivisionError:
                        errors.loc[errors.shape[0]] = [names]
                        return nan

                gini_card = round(gini(df_holders_sorted),3)

                df_gini_list.loc[df_gini_list.shape[0]] = [names, gini_card]
                
                # Method to see all gini coefficients
                first_q = df_holders_sorted[:(quartiles)].sum() / df_holders_sorted.sum()
                second_q = df_holders_sorted[:(quartiles*2)].sum() / df_holders_sorted.sum()
                third_q = df_holders_sorted[:(quartiles*3)].sum() / df_holders_sorted.sum()
                fourth_q = df_holders_sorted[:(quartiles*4)].sum() / df_holders_sorted.sum()
                fifth_q = df_holders_sorted.sum() / df_holders_sorted.sum()

                points = [0,first_q,second_q,third_q,fourth_q,fifth_q]
                x = [0,0.2,0.4,0.6,0.8,1.0]
                df = pd.DataFrame()
                df["Name"] = str(names)
                df["x"] = x
                df["points"] = points

                df_gini = df_gini.append(df, ignore_index=True)

            # Save output as csv
            df_gini_list_name = "df_gini_list_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_gini_list.to_csv("03_output_data/" + df_gini_list_name, index = False)

            # Show dataframe of Gini Coefficients
            g1.markdown("Individual Gini-Coefficient:")
            df_gini_list = df_gini_list[['Name','gini']]
            g1.dataframe(df_gini_list)
            total_gini = df_gini_list["gini"].mean()
            total_gini = round(total_gini, 3)        

            # All values per quantile
            df_gini_name = "df_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_gini.to_csv("03_output_data/" + df_gini_name, index = False)

            graph = "png_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            
            # Creation of the gini coefficient dataframe
            df_gini_total = df_gini.groupby(["x"]).mean()
            plt.close()
            plt.plot(x,df_gini_total["points"],"--o" )
            plt.plot(x,x,"--o" )
            plt.title("Card Distribution of Holders:")
            plt.savefig("04_graphs/" + graph)

            # Showing the graph
            gini_graph = Image.open("04_graphs/" + graph)
            g2.markdown("Graph:")
            g2.image(gini_graph)
            g1.write("The Gini-Coefficient is the most well-known measure of inequality. A Gini-Coefficient of zero means all holders have the same amount of cards. A Gini-Coefficient of one means one holder has all cards. The lower the Gini coefficient, the more equal the holders are. The current total Gini-Coefficient equals: " + str(total_gini)+ ".")
        st.markdown("<hr/>", unsafe_allow_html=True)

    #############################################################
    # Calculation of the volume sold
    ############################################################# 

    if volume_sold == True:

        vo1, vo2 = st.columns((2, 3)) 
        vo1.subheader("Volume sold")
        h1, h2 = st.columns((2, 3))

        name_dataframe = "df_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path("03_output_data/" + path_to_file)

        # Checking if file already exists 
        # If yes show results
        if path.is_file() == True:
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df = df[['Date','Volume sold']]
            h1.markdown("Data:")
            h1.dataframe(df, height=500)

            name_dataframe = "png_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open("04_graphs/" + name_dataframe)
            h2.markdown("Graph:")
            h2.image(price)
        
        # Calculation of the volume sold
        else:

            # Filter by observation time
            if observation_time !="All":
                test = df_total
                test["Year"] = df_total["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_total = test
            
            # Creation of a dictionary to add volume
            dict_total = {}

            # Calculation of the volume sold by month
            for ind in df_total.index:
                price = df_total["Price in USD"][ind]
                date = df_total["Date_Index"][ind]

                if date in dict_total.keys():
                    dict_total[date] += price
                else:
                    dict_total[date] = price

            data_items = dict_total.items()
            data_list = list(data_items)

            df_new_total = pd.DataFrame(data_list)
            df_new_total = df_new_total.rename(columns={0: 'Date', 1: 'Volume sold'})
            df_new_total = df_new_total.sort_values(by=["Date"], ascending = False)
            
            # Save dataframe as csv
            name_dataframe = "df_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_new_total.to_csv("03_output_data/" + name_dataframe, index = False)

            # Show dataframe
            df = pd.read_csv("03_output_data/" + name_dataframe)
            df_test = df[['Date','Volume sold']]
            h1.markdown("Data:")
            h1.dataframe(df_test, height=500)

            # Show graph
            h2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date"])
            df_test.plot(x ='time', y='Volume sold', kind = 'line')

            # Save graph
            name_dataframe = "png_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig("04_graphs/" + name_dataframe)
            price = Image.open("04_graphs/" + name_dataframe)
            h2.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    #############################################################
    # Comparison with indices
    ############################################################# 

    if bitcoin_index == True:

        bi1, bi2 = st.columns((2, 3)) 
        bi1.subheader("Benchmark Rare Pepe - Bitcoin (Cumulative Returns)")
        i1, i2 = st.columns((2, 2))

        # Import Bitcoin data
        df = pd.read_csv("02_input_data/" + "_bitcoin-usd.csv")
        df_test = df[['timestamp','close']]
        df_test['close'] = df_test['close'].div(df_test['close'].iat[0])
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        # Create graph
        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig("04_graphs/" + '_bitcoin_time_series.png')

        # Show graph Bitcoin
        price = Image.open("04_graphs/" + '_bitcoin_time_series.png')
        i2.markdown("Bitcoin Time Series:")
        i2.image(price, width=670)

        # Show graph Rare Pepe
        name_dataframe = "png_df_cum_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open("04_graphs/" + name_dataframe)
        i1.markdown("Rare Pepe Time Series:")
        i1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)
            

    if xcp_index == True:

        xcp1, xc2 = st.columns((2, 3)) 
        xcp1.subheader("Benchmark Rare Pepe - XCP (Cumulative Returns)")
        j1, j2 = st.columns((2, 2))
        
        # Import XCP data
        df = pd.read_csv("02_input_data/" + "_xcp-usd.csv")
        df_test = df[['timestamp','close']]
        df_test['close'] = df_test['close'].div(df_test['close'].iat[0])
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        # Create graph
        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig("04_graphs/" + '_xcp_time_series.png')

        # Show graph XCP
        price = Image.open("04_graphs/" + '_xcp_time_series.png')
        j2.markdown("XCP Time Series:")
        j2.image(price, width=670)

        # Show graph Rare Pepe
        name_dataframe = "png_df_cum_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open("04_graphs/" + name_dataframe)
        j1.markdown("Rare Pepe Time Series:")
        j1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if pepecash_index == True:

        pepe1, pepe2 = st.columns((2, 3)) 
        pepe1.subheader("Benchmark Rare Pepe - Pepe Cash (Cumulative Returns)")
        k1, k2 = st.columns((2, 2))
        
        # Import Pepe Cash data
        df = pd.read_csv("02_input_data/" + "_pepecash-usd.csv")
        df_test = df[['timestamp','close']]
        df_test['close'] = df_test['close'].div(df_test['close'].iat[0])
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        # Create graph
        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig("04_graphs/" + '_pepecash_time_series.png')

        # Show graph Pepe Cash
        price = Image.open("04_graphs/" + '_pepecash_time_series.png')
        k2.markdown("Pepecash Time Series:")
        k2.image(price, width=670)

        # Show graph Rare Pepe
        name_dataframe = "png_df_cum_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open("04_graphs/" + name_dataframe)
        k1.markdown("Rare Pepe Time Series:")
        k1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if nasdaq_index == True:

        nas1, nas2 = st.columns((2, 3)) 
        nas1.subheader("Benchmark Rare Pepe - NASDAQ (Cumulative Returns)")
        l1, l2 = st.columns((2, 2))

        # Import NASDAQ data
        df = pd.read_csv("02_input_data/" + "_nasdaq.csv")
        df_test = df[['timestamp','close']]
        df_test['close'] = df_test['close'].div(df_test['close'].iat[0])
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        # Create graph
        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig("04_graphs/" +'_nasdaq_time_series.png')

        # Show graph NASDDAQ
        price = Image.open("04_graphs/" + '_nasdaq_time_series.png')
        l2.markdown("NASDAQ Time Series:")
        l2.image(price, width=670)

        # Show graph Rare Pepe
        name_dataframe = "png_df_cum_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open("04_graphs/" + name_dataframe)
        l1.markdown("Rare Pepe Time Series:")
        l1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    # Show final dataset
    if dataset_analysis == True:
        
        # Filter by observation time
        if observation_time !="All":
            test = df_total
            test["Year"] = df_total["Date_Index"].str.split("-").str[0]
            test = test.loc[test['Year'] == str(observation_time)]
            df_total_time = test
        else:
            df_total_time = df_total

        # Show total transactions
        st.subheader("Dataset: ")
        st.write("Transaction: " + str(len(df_total_time)))
        st.dataframe(df_total_time)
        st.markdown("<hr/>", unsafe_allow_html=True)

    # Execution Time
    st.subheader("Metadata:")
    end_time = datetime.now()
    execution_time = end_time - begin_time
    st.caption("Runtime: " + str(execution_time))
    st.caption("Current Date: " + current_month)
    st.caption("Load Date: " + load_month)
