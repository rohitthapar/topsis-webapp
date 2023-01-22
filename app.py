# Rohit Thapar 
# 102003482
# 3CO19


import streamlit as st
# from topsis_rohitThapar_102003482 import topsis
# base="light"
st.title("Topsis method for multiple-criteria decision making (MCDM)")

st.write("* Number of entries for weights and impacts should be equal")

csvInput = st.file_uploader("Please Upload Input CSV")
Weights = st.text_input("Weights", value="1,1,1,1,1")
Impacts = st.text_input("Impacts", value="+,+,+,+,+")
Email_id = st.text_input("Email ID", value="test@test.com")

submit = st.button("Submit")

if submit:
    import pandas as pd
    import numpy as np
    import sys
    import uuid
    import base64
    import os

    def checkNumeric(_df):
        if _df.shape[1] == _df.select_dtypes(include=np.number).shape[1]:
            return True
        else:
            return False
    def normalize(result_df):
        for i in range(result_df.shape[1]):
            rootofsums = 0
            for j in range(result_df.shape[0]):
                rootofsums = rootofsums + result_df.iloc[j, i] ** 2
            rootofsums = rootofsums ** 0.5
            for j in range(result_df.shape[0]):
                result_df.iloc[j, i] = (result_df.iloc[j, i] / rootofsums)
        return result_df
    def addingWeight(result_df, _weights):
        weights = _weights.split(",")
        if len(weights) != result_df.shape[1]:
            print("Size of weights is not equal to number of columns")
            sys.exit()

        for i in range(len(weights)):
            try:
                weights[i] = float(weights[i])
            except:
                print("Value of weight is not in float. Please enter only float value.")
                sys.exit()

        for i in range(result_df.shape[1]):
            for j in range(result_df.shape[0]):
                result_df.iloc[j, i] = (result_df.iloc[j, i]) * (weights[i])
        return result_df

    def idealbestworst(result_df, _impacts):
        impacts = _impacts.split(",")
        if len(impacts) != result_df.shape[1]:
            print("Size of Impacts is not equal to number of columns")
            sys.exit()
        for i in range(len(impacts)):
            if impacts[i] == '+' or impacts[i] == '-':
                continue
            else:
                print("Impacts are not '+' or '-'")
                sys.exit()
        idealbest = []
        idealworst = []
        for i in range(result_df.shape[1]):
            if impacts[i] == "+":
                idealbest.append(max(result_df.iloc[:, i]))
                idealworst.append(min(result_df.iloc[:, i]))
            if impacts[i] == "-":
                idealbest.append(min(result_df.iloc[:, i]))
                idealworst.append(max(result_df.iloc[:, i]))

        result_df.loc[len(result_df.index)] = idealbest
        result_df.loc[len(result_df.index)] = idealworst
        return result_df


    def euclideandistance(result_df):
        idealbest = list(result_df.iloc[-2, :])
        idealworst = list(result_df.iloc[-1, :])
        result_df = result_df.iloc[:-2, :].copy()

        edp = []
        edn = []

        for i in range(result_df.shape[0]):
            tempedp = 0
            tempedn = 0
            for j in range(result_df.shape[1]):
                tempedp = tempedp + (result_df.iloc[i, j] - idealbest[j]) ** 2
                tempedn = tempedn + (result_df.iloc[i, j] - idealworst[j]) ** 2
            edp.append(tempedp ** 0.5)
            edn.append(tempedn ** 0.5)

        result_df["edp"] = edp
        result_df["edn"] = edn
        result_df["edp+edn"] = result_df["edp"] + result_df["edn"]

        pscore = []

        for i in range(result_df.shape[0]):
            pscore.append(((result_df["edn"][i]) / (result_df["edp+edn"][i])) * 100)

        result_df["Topsis Score"] = pscore

        return result_df
    def givingranks(result_df):
        mapping = {}
        temp_psscore = list(result_df.iloc[:, -1])
        temp_psscore.sort(reverse=True)

        for i in range(len(temp_psscore)):
            mapping[temp_psscore[i]] = i + 1

        ranks = []

        for i in range(result_df.shape[0]):
            ranks.append(mapping[result_df.iloc[i, -1]])

        result_df = result_df.copy()
        result_df["Rank"] = ranks

        return result_df


    def topsis(_inputcsv, _weights, _impacts, _resultfilename):
        try:
            df = pd.read_csv(_inputcsv)
        except:
            print("Input file could not be found")
            sys.exit()

        if len(df.columns) < 3:
            print("There needs to be atleast 3 columns")
            sys.exit()
        if checkNumeric(df.iloc[:, 1:]) == False:
            print("Need only numerical values")
            sys.exit()

        evaldf = df.iloc[:, 1:]
        weights = _weights
        impacts = _impacts
        evaldf1 = normalize(evaldf)
        evaldf2 = addingWeight(evaldf1, weights)
        evaldf3 = idealbestworst(evaldf2, impacts)
        evaldf4 = euclideandistance(evaldf3)
        evaldf5 = givingranks(evaldf4)
        df["Topsis Score"] = evaldf5["Topsis Score"]
        df["Rank"] = evaldf5["Rank"]
        df.to_csv(_resultfilename, index=False)


    filenameout = "result-" + str(uuid.uuid4().hex)[0:5] + ".csv"
    topsis(csvInput, Weights, Impacts, filenameout)
    def send_with_mailjet(sender, to, filename, base64encoded=""):
        from mailjet_rest import Client
        import os
        api_key = "9ae8ee62a4169678790a7a9b276e1fd8"
        api_secret = '613e4ccb98c4e31d42ae7320d89ba7ca'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender,
                        "Name": "Topsis method for multiple-criteria decision making (MCDM)"
                    },
                    "To": [
                        {
                            "Email": to,
                            "Name": "Sir"
                        }
                    ],
                    "Subject": "Your TOPSIS Result",
                    "TextPart": "Topsis result analysis",
                    "HTMLPart": "<h3>Topsis result anaysis of the given input</h3>",
                    "Attachments": [
                        {
                            "ContentType": "text/csv",
                            "Filename": filename,
                            "Base64Content": encoded
                        }
                    ]
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    import base64
    data = open(filenameout, "r").read()
    data = data.encode("utf-8")
    encoded = base64.b64encode(data)
    encoded = encoded.decode("utf-8")
    send_with_mailjet("thaprt206@gmail.com", Email_id, "result.csv", encoded)
    st.write("Email sent successfully")
    st.write("Check Spam if not recieved in Primary Folder")
    os.remove(filenameout)