# Quiver Quantitative
### Receiving API Token
You can sign up for a Quiver API token [here](https://api.quiverquant.com). 

The cost is $10/month, please [e-mail me](mailto:chris@quiverquant.com) if that is an issue and I may be able to help cover.

### Connecting to Client
After running the pip install shown above in your terminal, you can connect to the client in Python as shown below:
```python
import quiverquant
quiverClient = quiverquant.quiver("<API TOKEN>")
```
with \<API TOKEN\> replaced with your unique token.

### Fetching data
Using this client, you can access data on:
- Trading by US congressmen *quiverClient.congress_trading()*
- Corporate Lobbying *quiverClient.lobbying()*
- Government Contracts *quiverClient.gov_contracts()*

if you sign up for the Trader API plan, you can also access data on:
- Companies' Wikipedia page views *quiverClient.wikipedia()*
- Discussions on Reddit's /r/WallStreetBets *quiverClient.wallstreetbets()*

Here is an example of how to get a Pandas dataframe of trades by US congressmen:
```python
df = quiverClient.congress_trading()
```
You can also fetch this data by ticker, as shown below:
```python
dfAAPL = quiverClient.congress_trading("TSLA")
```

